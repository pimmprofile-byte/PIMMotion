# PIMMotion 백엔드 / DB 연동 아키텍처 (v0.1 설계)

> 목적: **PIMM_UnityGameCreator**(핸드오프 JSON + SVG 산출) 를 중심으로
> **에셋 · Unity(PIMMplayer) · Cowork(Claude) · Google Drive** 를 매끄럽게 잇는
> 백엔드/데이터 구조를 정의한다. Notion 연동은 이 버전에서 **제외**한다.

---

## 0. 설계 원칙 — 앱/블롭 분리 (App ↔ Blob Separation)

PIMMotion 데이터는 성격이 둘로 갈린다. 하나로 섞으면 느리고 깨지기 쉽다.

| 구분 | 무엇 | 저장소 | 이유 |
|---|---|---|---|
| **App data** | 프로젝트·시퀀스·박스·좌표·메모·상태·버전 인덱스 (구조화·관계형) | **DB** (SQLite→Postgres) | 빠른 질의/관계/버전/상태전이. 프론트·Cowork·Unity가 함께 읽음 |
| **Blob (원본)** | 핸드오프 JSON, SVG, 원본 에셋 파일(이미지/영상) | **Google Drive** | Cowork가 Read로 검수·작업하는 **원본 진실(source of truth)** |
| **Blob (서빙)** | 무거운 미디어의 CDN 전달본 | **R2 + CDN** | 프론트/Unity 런타임 고속 로드. Drive는 마스터, R2는 캐시 |

DB 는 **인덱스이자 오케스트레이터**, Drive/R2 는 **블롭 스토어**.
저장은 항상 write-through: `블롭을 Drive/R2 에 기록 → 그 참조(fileId/key)를 DB 에 남긴다`.

> 현재 `server/storage.py` 의 `LocalStore`(Drive 동기폴더에 실파일 기록)/`DriveStore` 골격이
> 이미 이 원칙의 씨앗이다. 여기에 **DB 인덱스 레이어**를 얹는 것이 이 설계의 핵심.

---

## 1. 데이터 모델 (DB 스키마)

관계형 코어. SQLite 로 시작(로컬 단독 동작), 서버화 시 Postgres 로 승격.
JSON 컬럼(`props`, `variants` 등)으로 유연성 확보 — 스키마 마이그레이션 없이 툴이 진화.

```sql
-- 게임 콘티 프로젝트 (하나의 PIMMplayer 테마/쇼)
CREATE TABLE project (
  id            TEXT PRIMARY KEY,          -- p_xxxxxxxx
  title         TEXT NOT NULL,
  theme_id      TEXT,                      -- PIMMplayer themeId 매핑 (예: COM60)
  group_label   TEXT,                      -- G1 순발력 / G2 추리 ...
  status        TEXT DEFAULT 'draft',      -- draft|building|review|done
  drive_folder_id TEXT,                    -- 옐로필드/아웃풋섹터/PIMMplayer_JSON 하위
  created_at    TEXT, updated_at TEXT
);

-- 시퀀스 (프리미어 시퀀스탭 = PIMMplayer SeqData/gamePhase 1개)
CREATE TABLE sequence (
  id            TEXT PRIMARY KEY,          -- s_xxxxxxxx
  project_id    TEXT NOT NULL REFERENCES project(id),
  seq_code      TEXT NOT NULL,             -- SEQ1, SEQ2 ... 자동맵핑(불변). 시리얼/아두이노 파싱 키
  label         TEXT,                      -- 사용자 편집 가능한 표시이름
  order_index   INTEGER NOT NULL,          -- 탭 순서 = seq_code 부여 순서
  phase         TEXT,                      -- 8단계: beatsheet|asset|manage|layout|integrate|simulate|build|complete
  canvas_bg     TEXT,                      -- 배경색/이미지 assetId
  bgm_asset_id  TEXT REFERENCES asset(id), -- 시퀀스 진입 시 재생할 BGM (시퀀스 단위)
  status        TEXT DEFAULT 'draft',
  UNIQUE(project_id, seq_code)
);

-- 박스 (레이아웃 요소 = 텍스트/에셋)
CREATE TABLE box (
  id            TEXT PRIMARY KEY,          -- b_xxxxxxxx
  sequence_id   TEXT NOT NULL REFERENCES sequence(id),
  kind          TEXT NOT NULL,             -- text | asset
  subtype       TEXT,                      -- (asset) button|image  /  (text) static|dynamic
  x REAL, y REAL, w REAL, h REAL,          -- 1920x1080 기준 절대좌표
  z_index       INTEGER,                   -- 레이어(하이어라키) 순서
  locked        INTEGER DEFAULT 0,         -- 하이어라키 락 (일러스트/포토샵 레이어 lock)
  visible       INTEGER DEFAULT 1,         -- 가시성 토글
  asset_id      TEXT REFERENCES asset(id), -- 현재 바인딩된 에셋 (교체 대상)
  anchor_min_x REAL, anchor_min_y REAL,    -- Unity RectTransform (Y-flip 반영)
  anchor_max_x REAL, anchor_max_y REAL,
  role          TEXT,                       -- background|button|image|text (background=풀캔버스 배경)
  opacity       REAL DEFAULT 1,
  props         TEXT                        -- JSON: {text,fontSize,fontColor,align,bgColor,
                                            --        textMode, variants:[{condition,text}],
                                            --        interactions:[{id,label,memo,trigger,sfxAssetId}]}
);

-- 에셋 (AI생성/업로드 이미지·영상·svg). NFC 정규화 파일명.
CREATE TABLE asset (
  id            TEXT PRIMARY KEY,          -- a_xxxxxxxx
  project_id    TEXT NOT NULL REFERENCES project(id),
  name          TEXT NOT NULL,             -- NFC 정규화된 표시명 (한글 안전)
  media_kind    TEXT,                      -- image|video|svg|audio (audio=SFX/BGM)
  audio_role    TEXT,                      -- (audio일 때) sfx|bgm
  source        TEXT,                      -- ai(nano-banana/gpt) | upload
  no_text       INTEGER DEFAULT 1,         -- NO-TEXT 규칙 준수 플래그
  width INTEGER, height INTEGER,
  current_version INTEGER DEFAULT 1,
  created_at    TEXT
);

-- 에셋 버전 (에셋 갈아끼우기 이력 — SVG 인덱스와 1:1 매칭되는 지점)
CREATE TABLE asset_version (
  asset_id      TEXT NOT NULL REFERENCES asset(id),
  version       INTEGER NOT NULL,
  storage       TEXT,                      -- drive|r2
  blob_ref      TEXT,                      -- drive fileId 또는 r2 key
  cdn_url       TEXT,                      -- R2 서빙 URL (있으면)
  checksum      TEXT,                      -- 중복/무결성
  created_at    TEXT,
  PRIMARY KEY (asset_id, version)
);

-- 핸드오프 산출물 (export 이력 — Cowork/Unity 소비 대상)
CREATE TABLE handoff (
  id            TEXT PRIMARY KEY,
  project_id    TEXT REFERENCES project(id),
  sequence_id   TEXT REFERENCES sequence(id),   -- null = 프로젝트 전체
  kind          TEXT,                      -- handoff_json | svg | unity_manifest
  schema_version TEXT,
  storage       TEXT, blob_ref TEXT, cdn_url TEXT,
  consumed_by_unity INTEGER DEFAULT 0,
  created_at    TEXT
);
```

**설계 포인트**
- `box.props` 는 JSON — 툴 UI(인스펙터 메모, textMode/variants, interactions)가 스키마 변경 없이 확장.
- `seq_code` 는 **불변·자동**. 시리얼/아두이노 파싱 코드가 이 값을 신뢰. 사용자는 `label` 만 수정.
- `asset` 과 `box` 는 **N:1 로 분리** → 한 에셋을 여러 박스가 참조, 에셋만 교체하면 전 박스 반영.
- `asset_version` = 에셋 갈아끼우기의 핵심. **SVG 의 박스별 인덱스**가 여기에 대응(교체 슬롯).

---

## 2. 스토리지 3-레이어와 동기 규칙

```
                    ┌────────────────────────────┐
   프론트/Cowork ── │  DB (SQLite→Postgres)      │  구조/좌표/상태/버전 인덱스
                    └──────────┬─────────────────┘
                               │ blob_ref (fileId / r2 key)
              ┌────────────────┴───────────────────┐
              ▼                                     ▼
   ┌────────────────────┐              ┌────────────────────────┐
   │ Google Drive       │  마스터원본  │ R2 + CDN               │  고속 서빙본
   │ 핸드오프JSON/SVG/   │◀───sync────▶│ 이미지/영상 캐시        │
   │ 원본 에셋           │              │ (Unity런타임/프론트)    │
   └────────────────────┘              └────────────────────────┘
```

- **쓰기(write-through)**: 저장 시 ① Drive 에 원본 기록 → ② (미디어면) R2 업로드+CDN URL 발급 → ③ DB 에 `blob_ref/cdn_url` 기록. 세 단계 중 실패 시 DB 상태를 `pending_sync` 로 남겨 재시도(지수백오프).
- **읽기**: 구조 질의는 DB, 미디어는 `cdn_url` 우선(없으면 Drive 다운로드 폴백).
- **한글 파일명**: Drive 는 NFD, macOS 도 NFD, 웹/서버는 NFC 혼재 → **DB 저장·비교는 항상 NFC 정규화**(`unicodedata.normalize('NFC', name)`), Drive 조회 시에만 필요하면 NFD 변환.
- **Drive 폴더 매핑**: `project.drive_folder_id` = `옐로필드/아웃풋섹터/PIMMplayer_JSON/<project>` 하위. 핸드오프 export 는 이 폴더로.

---

## 3. API 표면 (FastAPI — 현행 `server/main.py` 확장)

기존 board/asset/forge API 위에 게임크리에이터용 리소스를 얹는다.

```
# 프로젝트/시퀀스/박스 (게임크리에이터 데이터)
GET    /api/projects
POST   /api/projects                        {title, themeId?, group?}
GET    /api/projects/{pid}
POST   /api/projects/{pid}/sequences        → seq_code 자동부여(SEQ{n})
PATCH  /api/sequences/{sid}                  {label, phase, order_index}   # seq_code는 불변
GET    /api/sequences/{sid}/boxes
POST   /api/sequences/{sid}/boxes           {kind, subtype, x,y,w,h, props}
PATCH  /api/boxes/{bid}                      {x,y,w,h,z,locked,visible,asset_id,props}
DELETE /api/boxes/{bid}

# 에셋 파이프라인
POST   /api/projects/{pid}/assets           (upload; NFC정규화 + Drive+R2 기록)
POST   /api/projects/{pid}/assets/generate  (AI생성 릴레이: nano-banana/gpt, NO-TEXT 강제)
POST   /api/assets/{aid}/versions           (에셋 갈아끼우기 → 새 version)
GET    /api/assets/{aid}                     (버전 목록 + cdn_url)

# 핸드오프 (export & 연동)
POST   /api/sequences/{sid}/handoff/json    → 핸드오프 JSON 생성·Drive저장·DB기록
POST   /api/sequences/{sid}/handoff/svg     → 1920x1080 인덱스드 SVG 생성
POST   /api/projects/{pid}/handoff/unity    → PIMMplayer config + asset manifest 변환
GET    /api/handoff/{hid}                    (Cowork/Unity가 최신 산출물 조회)

# 동기/상태
POST   /api/sync/drive                       (pending_sync 재처리)
GET    /api/health                           (기존)
```

- **AI 생성 릴레이**는 반드시 서버측(키 노출/CORS 때문). JSON-only + 지수백오프 3회 — 현행 `claude_client` 패턴 재사용.
- 프론트(HTML 툴)는 **오프라인 우선**: 서버 없으면 localStorage + 파일 다운로드/`showSaveFilePicker` 로 동작하고, 서버가 붙으면 위 API 로 승격(점진적 향상).

---

## 4. Unity(PIMMplayer) 연동 브릿지 — 가장 중요한 접합부

이전 학습에서 확인된 **현실**: PIMMplayer 런타임은 `StreamingAssets` 의
`theme_config.json` / `config.json`(SeqData/ActEntry) / `combo_input_registry.json` 을 읽고,
**게임 프리팹은 RectTransform 앵커를 하드코딩**한다. 즉 레이아웃 JSON 을 Unity 가 직접 소비하지 않는다.

→ 그래서 브릿지는 **두 갈래**로 설계한다.

### (a) 지금 당장 되는 길 — 좌표 핸드오프 + 에셋 매니페스트
PIMMotion 이 `unity_manifest` 를 생성 → **Cowork(또는 Unity Editor 임포터 스크립트)** 가 소비:

```json
{
  "themeId": "COM60",
  "sequence": { "seqCode": "SEQ1", "label": "룰렛", "prefabPath": "COMBO/Games/Reflex" },
  "boxes": [
    { "id": "b_01", "role": "image", "assetId": "a_bg",
      "rect": { "x": 0, "y": 0, "w": 1920, "h": 1080 },
      "unityAnchor": { "min": {"x":0,"y":0}, "max": {"x":1,"y":1} },
      "cdnUrl": "https://cdn.../a_bg_v3.png", "version": 3 },
    { "id": "b_02", "role": "button", "assetId": "a_start",
      "rect": { "x": 820, "y": 900, "w": 280, "h": 120 },
      "unityAnchor": { "min": {"x":0.427,"y":0.0}, "max": {"x":0.573,"y":0.111} } }
  ]
}
```
- `unityAnchor` 는 툴이 이미 계산하는 Y-flip 앵커(`anchorMin.y=(H-y-h)/H`, `anchorMax.y=(H-y)/H`).
- Cowork 가 이 매니페스트를 읽어 프리팹 RectTransform/에셋을 교체 → 런타임 검수. **v1 의 실제 워크플로우**.

### (b) 향후 자동화 길 — Unity 측 LayoutImporter
`GameConfigLoader` 계열에 **layout 소비 로더**를 추가하면, 매니페스트를 런타임에 읽어
RectTransform 을 자동 배치 가능. 이 경우 PIMMotion 핸드오프가 곧 config 가 됨(하드코딩 제거).
→ 별도 과제로 분리(Unity repo 작업 필요). 지금 설계는 (b) 를 막지 않도록 매니페스트 스키마를
**앵커·CDN·버전** 을 모두 담게 만들어 둔다.

---

## 5. Cowork(Claude) 연동 — "핸드오프 계약"

Cowork 가 이 파이프라인의 최종 해석자일 확률이 높다(사용자 명시). 그래서 산출물은
**기계 파싱 우선 + 안정 주소 + 버전**을 만족해야 한다.

- **주소성**: 모든 산출물은 Drive 고정 폴더(`PIMMplayer_JSON/<project>/<seqCode>/`)에 버전 접미사로 저장. Cowork 는 이미 Drive MCP 로 접근 가능.
- **파싱성**: 핸드오프 JSON 과 SVG 양쪽에 `id / index / x,y,w,h / seqCode / assetId / version` 을 명시(둘의 id 를 동일 키로). SVG 는 `<g id="Artboard1">` 통합뷰 + `<g id="Artboard_b_02" data-index="2">` 박스별 아트보드.
- **계약 문서**: `docs/handoff-schema.md`(별도)에 핸드오프 JSON·SVG·unity_manifest 스키마를 고정 버전으로 명세 → Cowork/Unity/툴 삼자가 같은 계약을 참조.
- **선택적 MCP 노출**: 서버화되면 PIMMotion 을 **로컬 MCP** 로 감싸 Cowork 가 `list_projects / read_handoff / apply_asset_version` 을 직접 호출 → "대화형 기획 → 데모 → 배치 → 교체" 루프를 한 세션에서.

---

## 6. 단계적 도입 로드맵

| 단계 | 범위 | 저장 | 비고 |
|---|---|---|---|
| **P0 (현재)** | HTML 툴 단독, localStorage + 파일 저장(showSaveFilePicker) | 브라우저/로컬 | 서버 불필요, 즉시 동작 |
| **P1** | FastAPI + **SQLite** 인덱스, Drive 동기폴더(LocalStore) | DB + Drive | 프로젝트/시퀀스/박스/에셋 API, 핸드오프 생성 |
| **P2** | AI생성 릴레이 + R2/CDN 미디어 서빙 | + R2 | NO-TEXT 강제, cdn_url 발급 |
| **P3** | unity_manifest 브릿지 + (선택) Unity LayoutImporter | — | 좌표 자동적용, 런타임 검수 자동화 |
| **P4** | Postgres 승격 + PIMMotion MCP 노출 | Postgres | 팀/실무 배포, Cowork 직결 |

> Notion 은 P4 이후 별도 검토(이번 설계 범위 밖).

---

## 7. 요약 — 왜 이 구조가 연동에 유리한가

- **에셋 연동**: `asset ↔ asset_version ↔ box` 분리로 "에셋만 갈아끼우면 전 박스 반영" + SVG 인덱스가 교체 슬롯과 1:1.
- **Unity 연동**: unity_manifest 가 앵커·CDN·버전을 담아 Cowork/Editor 임포터가 바로 적용, 향후 완전자동화(b)도 개방.
- **Cowork 연동**: 안정 주소 + 기계파싱 산출물 + 고정 계약 → Claude 가 신뢰성 있게 읽고 씀.
- **Drive 연동**: 원본 진실은 Drive, 인덱스는 DB, 서빙은 CDN — 느린 Drive 질의를 DB 가 대신.
