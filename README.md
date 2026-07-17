# PIMMotion

> **워크툴** — 핌코프 3층 위계(Plogic=마스터로직 / Partwork=워크로직 / **PIMMotion=워크툴**)의 손발.
> Partwork의 워크로직을 코드로 실체화해, 프로젝트보드를 실제로 굴리는 도구.

Bible: `[4.퍼플필드].PIMM_log/[3.세션로그].Session/PIMMotion R&D_Log/PIMMotion-bible.md`

---

## 아키텍처 (Bible §2)

```
┌─────────────┐    HTTP/JSON     ┌──────────────────┐   files/json   ┌──────────────┐
│  web/  (HTML │ ───────────────▶ │  server/ (FastAPI)│ ─────────────▶ │ Google Drive │
│  프로젝트보드) │ ◀─────────────── │  얇은 로컬 서버    │ ◀───────────── │  (실파일 저장) │
└─────────────┘                  └────────┬─────────┘                └──────────────┘
                                          │ relay (JSON-only + 백오프)
                                          ▼
                                   ┌──────────────┐
                                   │  Claude API  │  (claude-opus-4-8)
                                   └──────────────┘
```

**순수 브라우저❌ / 유니티❌ → HTML 프런트 + 얇은 로컬 서버.** 두 변수가 서버를 강제:

- **에셋(결정타):** 브라우저 단독은 실파일 read/write 불가 → 업로드물을 드라이브에 못 남김 →
  **Claude가 Read 검수 불가** (= v1 트래커 반려 원인). 서버가 드라이브 폴더에 실파일로 저장해 해결.
- **API:** 브라우저 직접호출은 CORS·키노출·재시도불가 → 로컬 릴레이(FastAPI)가
  **JSON-only 강제 + 지수 백오프 3회 + 키 서버측 보관**.

유니티는 툴 UI가 아니라 머더미스터리 게임 **런타임**(PIMMplayer)으로만 분리 유지.

---

## forge 구조 (Bible §1)

**코어 1개 + 카테고리별 보드 스키마(데이터)**. 카테고리를 추가해도 코어 코드는 0줄 수정.

| 카테고리 | 성격 | 스키마 |
|---|---|---|
| 머더미스터리 | 생성형 forge (Forge Loop) | `schemas/murdermystery.json` |
| 핌업 (PIMM-UP) | 절차형 forge (17단계 6페이즈) | `schemas/pimmup.json` |
| 피머시브 | 절차형 forge (현장시공형) | `schemas/pimmersive.json` |

## 코어 (Bible §3)

- **상태모델 5단계:** 미착수 / 진행 / 검수대기 / 완료 / 보류
- **완료 게이트 = 3-Gate:** 체크리스트 전항목 + 산출물 링크 + PD 승인
- **업로드→검수 파이프라인:** 업로드 → 서버가 드라이브에 실파일 저장 → Claude가 Read 검수 → 승인
- **프로젝트보드** = 각 프로젝트의 단일 정본(JSON, git 버전관리 가능)

---

## 실행

```bash
# 1) 의존성
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) 환경변수
cp .env.example .env
# .env 에 ANTHROPIC_API_KEY, STORAGE_ROOT (드라이브 동기폴더 경로) 설정

# 3) 서버 기동
uvicorn server.main:app --reload --port 8787

# 4) 브라우저에서 http://localhost:8787 접속
```

`STORAGE_ROOT`를 **Google Drive 데스크톱 동기 폴더**로 지정하면, 서버가 쓰는 실파일이
곧바로 드라이브에 올라가고 Claude(코워크)가 Read로 검수할 수 있다. `STORAGE_BACKEND=gdrive`로
바꾸면 Drive API를 직접 호출한다(서비스계정 필요, `server/storage.py` 참조).

---

## 상태

R&D 스캐폴드 (Partwork STEP 4 착수분). 빌드 플랜 Bible §8:
①보드 스키마 v1 → ②로컬 서버 → ③코어 → ④카테고리 스키마 → ⑤최소 프로토타입.
현재 ①~③ 골격 + ④ 스키마 3종 + 최소 프런트 구현. 미확정: 배포 모델(로컬앱 vs 호스팅).
