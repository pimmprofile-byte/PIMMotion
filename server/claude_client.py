"""Claude API 릴레이 (Bible §7 API 안정화 4원칙).

① JSON-only 응답 강제 + 스트립 파싱
② 지수 백오프 3회 재시도
③ 브라우저 직접호출 금지 → 이 로컬 서버만 Claude를 호출 (키 서버측 보관)
④ 수정은 diff/부분수정 지향 (Forge Loop의 Reviser 단계에서 활용)

모델 기본값 claude-opus-4-8 + 어댑티브 씽킹.
"""
from __future__ import annotations

import json
import random
import time
from typing import Any

from .config import settings

try:
    import anthropic
except Exception:  # SDK 미설치 환경에서도 import는 통과
    anthropic = None  # type: ignore


class ClaudeError(RuntimeError):
    pass


def _client() -> "anthropic.Anthropic":
    if anthropic is None:
        raise ClaudeError("anthropic SDK 미설치 — pip install anthropic")
    if not settings.has_claude:
        raise ClaudeError("ANTHROPIC_API_KEY 미설정 (.env 확인)")
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


def _extract_text(message: Any) -> str:
    for block in message.content:
        if getattr(block, "type", None) == "text":
            return block.text
    return ""


def _strip_to_json(text: str) -> str:
    """```json 펜스나 앞뒤 잡텍스트를 걷어내고 JSON 본문만 남긴다 (원칙 ①)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```", 2)[1] if "```" in t[3:] else t
        t = t.split("\n", 1)[1] if "\n" in t else t
        t = t.rsplit("```", 1)[0]
    start, end = t.find("{"), t.rfind("}")
    if start != -1 and end != -1 and end > start:
        return t[start : end + 1]
    return t.strip()


def generate_json(
    system: str,
    user: str,
    schema: dict[str, Any] | None = None,
    max_tokens: int = 8000,
    max_retries: int = 3,
) -> dict[str, Any]:
    """JSON 객체를 강제로 받아 dict로 반환. 지수 백오프 3회 (원칙 ①②③)."""
    client = _client()
    kwargs: dict[str, Any] = {
        "model": settings.model,
        "max_tokens": max_tokens,
        "thinking": {"type": "adaptive"},
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    # 구조화 출력이 가능하면 스키마로 강제
    if schema is not None:
        kwargs["output_config"] = {
            "format": {"type": "json_schema", "schema": schema}
        }

    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(**kwargs)
            text = _extract_text(msg)
            return json.loads(_strip_to_json(text))
        except Exception as e:  # noqa: BLE001 — 재시도 판단은 아래
            last_err = e
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(delay)
            continue
    raise ClaudeError(f"Claude 호출 실패 ({max_retries}회): {last_err}")


def review_asset(text_content: str, criteria: str) -> dict[str, Any]:
    """업로드 산출물(텍스트)을 검수 루브릭으로 채점 (업로드→검수 파이프라인).

    실파일은 서버가 Read해서 이 함수에 넘긴다 (Bible §3).
    """
    schema = {
        "type": "object",
        "properties": {
            "pass": {"type": "boolean"},
            "score": {"type": "integer"},
            "issues": {"type": "array", "items": {"type": "string"}},
            "note": {"type": "string"},
        },
        "required": ["pass", "score", "issues", "note"],
        "additionalProperties": False,
    }
    system = (
        "너는 핌코프 PIMMotion의 검수자다. 산출물을 검수 루브릭에 따라 "
        "냉정하게 채점한다. 통계/방법론 근거를 대고, 과잉제안 금지."
    )
    user = f"[검수 루브릭]\n{criteria}\n\n[산출물]\n{text_content}"
    return generate_json(system, user, schema=schema, max_tokens=4000)
