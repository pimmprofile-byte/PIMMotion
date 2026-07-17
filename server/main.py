"""PIMMotion 얇은 로컬 서버 — 프런트 정적서빙 + 보드/에셋/포지 API."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import claude_client
from .config import settings
from .models import (
    Board,
    CreateBoardReq,
    ForgeReq,
    Gate,
    Status,
    Step,
    UpdateStepReq,
)
from .storage import get_store

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
WEB_DIR = ROOT / "web"

app = FastAPI(title="PIMMotion", version="0.1.0")
store = get_store()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_category_schema(category: str) -> dict:
    p = SCHEMA_DIR / f"{category}.json"
    if not p.exists():
        raise HTTPException(404, f"카테고리 스키마 없음: {category}")
    return json.loads(p.read_text(encoding="utf-8"))


def _seed_steps(category: str) -> list[Step]:
    """카테고리 스키마(데이터)로 코어에 스텝을 얹는다 (forge: 코어+테마)."""
    schema = _load_category_schema(category)
    return [
        Step(key=s["key"], title=s["title"], guide=s.get("guide", ""))
        for s in schema.get("steps", [])
    ]


# --- 메타 ---
@app.get("/api/health")
def health() -> dict:
    return {
        "ok": True,
        "model": settings.model,
        "claude": settings.has_claude,
        "storage": settings.storage_backend,
    }


@app.get("/api/categories")
def categories() -> list[dict]:
    out = []
    for p in sorted(SCHEMA_DIR.glob("*.json")):
        if p.name == "core.schema.json":  # 메타 스키마는 카테고리 아님
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        out.append({
            "key": p.stem,
            "label": d.get("label", p.stem),
            "kind": d.get("kind", ""),
            "steps": len(d.get("steps", [])),
        })
    return out


# --- 보드 ---
@app.get("/api/boards")
def list_boards() -> list[dict]:
    return store.list_boards()


@app.post("/api/boards")
def create_board(req: CreateBoardReq) -> Board:
    board = Board(
        id=uuid.uuid4().hex[:12],
        category=req.category,
        title=req.title,
        brief=req.brief,
        steps=_seed_steps(req.category),
        created_at=_now(),
        updated_at=_now(),
    )
    store.save_board(board.id, board.model_dump())
    return board


@app.get("/api/boards/{board_id}")
def get_board(board_id: str) -> Board:
    data = store.load_board(board_id)
    if not data:
        raise HTTPException(404, "보드 없음")
    return Board(**data)


@app.patch("/api/boards/{board_id}/steps/{step_key}")
def update_step(board_id: str, step_key: str, req: UpdateStepReq) -> Board:
    data = store.load_board(board_id)
    if not data:
        raise HTTPException(404, "보드 없음")
    board = Board(**data)
    step = next((s for s in board.steps if s.key == step_key), None)
    if step is None:
        raise HTTPException(404, "스텝 없음")

    if req.checklist is not None:
        step.gate.checklist = req.checklist
    if req.pd_approved is not None:
        step.gate.pd_approved = req.pd_approved
    if req.status is not None:
        # 완료로 이동은 3-Gate 충족 시에만 (Bible §3)
        if req.status == Status.DONE and not step.gate.is_open():
            raise HTTPException(
                400,
                "3-Gate 미충족: 체크리스트 전항목 + 산출물링크 + PD승인 필요",
            )
        step.status = req.status

    board.updated_at = _now()
    store.save_board(board.id, board.model_dump())
    return board


# --- 에셋 (업로드→검수 파이프라인) ---
@app.post("/api/boards/{board_id}/steps/{step_key}/assets")
async def upload_asset(board_id: str, step_key: str, file: UploadFile) -> Board:
    data = store.load_board(board_id)
    if not data:
        raise HTTPException(404, "보드 없음")
    board = Board(**data)
    step = next((s for s in board.steps if s.key == step_key), None)
    if step is None:
        raise HTTPException(404, "스텝 없음")

    payload = await file.read()
    rel = store.save_asset(board_id, file.filename or "asset.bin", payload)
    from .models import Asset

    asset = Asset(
        id=uuid.uuid4().hex[:10],
        filename=file.filename or "asset.bin",
        rel_path=rel,
        uploaded_at=_now(),
    )
    board.assets.append(asset)
    step.gate.asset_ids.append(asset.id)
    board.updated_at = _now()
    store.save_board(board.id, board.model_dump())
    return board


@app.post("/api/boards/{board_id}/assets/{asset_id}/review")
def review_asset(board_id: str, asset_id: str, criteria: str = "") -> dict:
    """서버가 실파일을 Read → Claude로 검수 (Bible §3)."""
    data = store.load_board(board_id)
    if not data:
        raise HTTPException(404, "보드 없음")
    board = Board(**data)
    asset = next((a for a in board.assets if a.id == asset_id), None)
    if asset is None:
        raise HTTPException(404, "에셋 없음")

    raw = store.read_asset(asset.rel_path)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "텍스트 산출물만 자동검수 가능 (이미지/바이너리 제외)")

    try:
        result = claude_client.review_asset(text, criteria or "일반 품질 검수")
    except claude_client.ClaudeError as e:
        raise HTTPException(503, str(e))

    asset.reviewed = True
    asset.review_note = result.get("note", "")
    board.updated_at = _now()
    store.save_board(board.id, board.model_dump())
    return result


# --- 생성형 forge (머더미스터리 Forge Loop 진입점) ---
@app.post("/api/forge")
def forge(req: ForgeReq) -> dict:
    data = store.load_board(req.board_id)
    if not data:
        raise HTTPException(404, "보드 없음")
    board = Board(**data)
    system = (
        "너는 핌코프 PIMMotion의 생성형 forge다. 브리프와 카테고리 스키마에 맞춰 "
        "초안을 JSON으로 생성한다. 발명하지 말고 브리프에서 추출하라."
    )
    user = (
        f"[카테고리] {board.category}\n"
        f"[브리프] {json.dumps(board.brief, ensure_ascii=False)}\n"
        f"[지시] {req.instruction or '초안 생성'}\n"
        "결과는 draft 필드를 가진 JSON 하나로 반환."
    )
    schema = {
        "type": "object",
        "properties": {"draft": {"type": "string"}, "notes": {"type": "string"}},
        "required": ["draft"],
        "additionalProperties": False,
    }
    try:
        return claude_client.generate_json(system, user, schema=schema)
    except claude_client.ClaudeError as e:
        raise HTTPException(503, str(e))


# --- 프런트 정적 서빙 ---
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/", response_model=None)
def index():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        return FileResponse(idx)
    return JSONResponse({"msg": "PIMMotion server up. web/ 미구현."})
