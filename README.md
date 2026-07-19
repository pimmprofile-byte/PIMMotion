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

## PIMM UnityGameCreator (핌플레이어 게임크리에이터 툴)

핌플레이어(Unity 런타임)용 **콘티/레이아웃/핸드오프 툴**. 단일 HTML(외부 의존성 0, localStorage 자동저장)로,
개발지식 없이 그래픽 에셋만 준비하면 유니티로 핌플레이어를 빌드·수정할 수 있게 하는 것이 목표.

- 산출물: `scratchpad/PIMM_UnityGameCreator.ver1.0.html`
- 유니티 에디터형 3분할 UI(하이어라키 / 씬 1920×1080 / 인스펙터) + 다크그레이·`#00FF99`
- 8단계 파이프라인(BEATSHEET→ASSET→MANAGE→LAYOUT→INTEGRATE→SIMULATE→BUILD&TEST→COMPLETE)
- 프리미어식 시퀀스 탭(코드명 SEQ# 자동·불변, 라벨만 수정) · 하이어라키 락/가시성
- 텍스트(static/dynamic) · 에셋(button/image) · 배경 · SFX/BGM · 인스펙터 논코딩 메모
- 내보내기: **핸드오프 JSON** + **SVG 아트보드**(박스별 인덱스) + config 9종(repo 스키마 정합)

### 연동 (선택 — 서버 켰을 때)

- **툴 내 Claude 챗**: `POST /api/chat` (키는 서버 보관). 툴 안에서 기획/프롬프트/맵핑 상담.
- **Drive 로컬폴더 저장**: `POST /api/export/save` → `.env`의 `PIMM_DRIVE_EXPORT_DIR`(구글드라이브 앱 동기폴더
  `옐로필드/아웃풋섹터/PIMMplayer_JSON`)에 핸드오프를 바로 저장. Drive API 불필요, **로컬 경로면 충분**.
- 서버가 없어도 툴은 오프라인으로 동작(내보내기는 브라우저 저장/다운로드 폴백).

### 문서

- `docs/guide-nodev-build.md` — 무개발 사용자용 빌드/수정 가이드
- `docs/guide-cowork-unity.md` — Cowork+Unity 실전 워크플로우(이미지 프롬프트→입력맵핑→런타임 검수)
- `docs/backend-architecture.md` — 에셋·Unity·Cowork·Drive 연동 백엔드/DB 설계

---

## 상태

R&D 스캐폴드 (Partwork STEP 4 착수분). 빌드 플랜 Bible §8:
①보드 스키마 v1 → ②로컬 서버 → ③코어 → ④카테고리 스키마 → ⑤최소 프로토타입.
현재 ①~③ 골격 + ④ 스키마 3종 + 최소 프런트 구현 + **게임크리에이터 툴 ver1.0** + 연동/가이드.
미확정: 배포 모델(로컬앱 vs 호스팅).
