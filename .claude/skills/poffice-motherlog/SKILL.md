---
name: poffice-motherlog
description: 포피스 마더로그 생성 스킬. 각 개인세션로그를 읽어 분석하여 '포피스 대시보드가 그대로 읽는 config(마더 세션로그)'를 만들어 드라이브 그린필드 내 포피스영역에 뿌린다. ★원문 보존 우선(요약 금지) — sessions[]에 원문 전문 raw + 1줄 summary, 분단위 타임스탬프. 구형의 리포트/브리프/워크오더 텍스트 형식이 아니라, 현재 포피스 대시보드(tool/PIMM_Poffice.ver0.2.html)에 노출되는 데이터 형식(poffice_board.json)으로 출력한다. 빌드된 HTML이 이 config를 로드한다. 트리거: 마더세션로그, 마더로그, 포피스 config 생성, 포피스 대시보드 갱신, 세션로그 집계, poffice_board.json 생성. 데이터 생성 담당(개인 기록은 Poffice-Skill, 브리핑은 Poffice-Report-Bot).
---

# Poffice-MotherLog — 개인세션로그 → 대시보드 config(마더 세션로그)

> 역할: 각 인물의 **개인세션로그를 읽어 요약·분석** → **포피스 대시보드가 읽는 config**(마더 세션로그)를 생성.
> 저장: 드라이브 **그린필드 내 포피스영역**. 빌드된 대시보드 HTML이 이 config를 로드한다.
> 개인 기록은 `Poffice-Skill`, 브리핑은 `Poffice-Report-Bot`. 스키마 정본: `docs/poffice-board-spec.md`(A~H).

## ★ 최상위 원칙 3개 (무엇보다 우선)
1. **텍스트가 절대 깨지면 안 된다.**
   - UTF-8 보존 · 한글/특수문자 mojibake 금지 · 줄바꿈/따옴표 등 **JSON 이스케이프 정확**.
   - 누락·잘림(truncation) 금지. 생성 후 **JSON 파싱 검증**(깨지면 폐기·재생성, 손상본을 덮어쓰지 않음).
2. **원문을 참조·아카이빙하여 왜곡이 없게 한다.**
   - 모든 분석 항목은 **출처 개인세션로그**(파일명/경로/ts)를 근거로 단다(게이트의 `log`, 세션의 `ts`, `meta.source_files`).
   - **원문 아카이빙**: 개인세션로그 원본은 불변 보존.
   - **사실 왜곡·과장·축소·창작 금지.** 불확실하면 추정하지 말고 원문 참조로 넘긴다.
3. **★원문 보존 우선 (2026-07-26 확정 — 요약 중심 폐기).**
   - **세션로그 본문을 요약하지 않는다.** `sessions[]` 각 항목에 **원문 전문을 `raw`로 그대로** 담고, `summary`는 **1줄 헤드라인**만.
   - 파일이 커지면 **윈도우 폭(담는 세션 수)을 줄이지, 원문을 자르지 않는다.** (과잉 요약 = 실제 업무 파악 불가 → 실사용 피드백 반영.)
   - **분단위 타임스탬프 필수**: `sessions[].ts`·게이트 `ts` = `YYMMDD_HHMM`, `meta.generated_at` = ISO 분단위. **날짜만 찍는 것 금지.**

## 1. 저장 위치 & 폴더 구조 (그린필드 / 포피스영역)
- 그린필드: `[1.그린필드:프레임워크].PIMM_framework` (id `1HB1X19PN6DQDXpEFpheE-BFLC2eBc3CG`)
- 포피스영역: `[2.포피스_섹터].Poffice` (id `1dbUhEa2ByRtLhKryM4YpYHC4bNLzBdFm`)
- **라이브**: `poffice_board.json`(대시보드 로드 정본) — 포피스영역에 **딱 1개**만 존재해야 한다.
  > ⚠️ **동일 파일명 중복 금지 (반드시 준수).** 드라이브는 파일을 **이름이 아니라 fileId**로 구분해서, 매 run **새로 생성(create)** 하면 같은 이름 파일이 계속 쌓이고 동기화 시 `poffice_board (1).json`·`(2)`·`(3)`… 로 복제된다. 이때 **정작 `poffice_board.json`(접미사 없는 정본 이름)은 대개 맨 처음(가장 오래된) 파일**이라, 대시보드의 고정 fetch가 **최신본이 아니라 옛 데이터를 읽는 심각한 오류**가 난다.
  > ✅ **쓰기 규칙 = "찾아서 덮어쓰기(update-by-fileId)".** ① 포피스영역에서 이름 `poffice_board.json`을 **검색** → ② 있으면 **그 fileId의 내용을 update(미디어 덮어쓰기)** — 새 파일 생성 금지. ③ 없을 때만 **최초 1회 create**. ④ 이후 실행은 **그 canonical fileId를 기억해 항상 그 ID를 update**(검색이 중복본을 집지 않도록). ⑤ `(1)(2)(3)` 중복본이 이미 있으면 **최신 내용만 정본 파일에 반영 후 나머지는 휴지통 처리**(불가 시 사용자에게 수동 정리 안내).
  > ※ create만 지원하고 update가 없는 커넥터라면, **중복을 만드는 create를 반복하지 말고** 정본 파일을 update할 수 있는 경로(Drive `files.update` media)를 쓴다. 정본은 언제나 **접미사 없는 단일 `poffice_board.json`**.
- **카테고리 폴더(넘버링+영문, 대시보드 카테고리와 동일)** — 구버전·이전 자료 확인용 아카이브 축:
  `01_Mission_미션보드/` · `02_Gate_게이트보드/` · `03_Checklist_체크리스트/` · `04_LogArchive_로그집계/`(구 '세션로그') · `05_WorkOrder_워크오더/` · `06_Notice_사내공지/`
- **아카이빙**: `poffice_board.json` 갱신 시 **직전 버전/변경분을 해당 카테고리 폴더에** `{YYMMDD_HHMM}_{요약}` 로 남긴다(원문 무왜곡·불변, 원칙 2). 세션로그 원본은 블루필드/개인DB에 있고 여기 `04_LogArchive_로그집계/`는 집계 스냅샷·참조용.
- 구조 정본: 포피스영역 `README_포피스섹터구조.md`.

## 2. 입력
- 각 인물 `개인DB/{이름}/Session_세션로그/`(**평면 구조** · 경로/ID 정본 = `pimm-artisan-session` 테이블)의
  `{YYMMDD_HHMM}_{요약}_log.md`(세션로그 원본), 롤업(`GATE_현황.md`·`TODO_현황.md`·`MISSION_보드.md`), `workorder/`(WO), 역방향 입력 `poffice_export_{이름}.json`.
- 대표 주간보고 판단(있으면) — 게이트(🔴/🟡/🟢)·WO 반영에 사용.
> 개인세션로그 폴더 경로·Drive ID는 **artisan-session 정본을 따른다**(중첩 구조·평행 폴더 신설 금지). 이 스킬의 하드코딩 ID는 **출력처(그린필드 Poffice)** 에 한정.

## 3. 처리 (원문 보존 + 상태 파생 → 결정론 변환)
- **세션 원문 보존(§원칙 3)**: `sessions[]` 각 항목 = `ts`(분단위) + `file` + `summary`(1줄) + **`raw`(세션로그 원문 전문, 요약·축약 없음)**. raw를 자르거나 재요약하지 않는다.
- 파생 상태(요약 아님, 롤업/원문에서 도출): 미션(progress·roadmap), 게이트(권한 신호등), 투두(체크·중요도·일자·WO).
- **윈도우**: 최근 세션 N개(원문 포함)만 담고, 커지면 **N을 줄인다**(원문은 안 자름). 더 오래된 건 원본 파일·아카이브로.
- **신선도 파생**: 인별 `freshness{last_log_ts, status}` — `green`(24h 이내)/`yellow`(24~72h)/`red`(72h+ stale). **숨기지 않는다**(기록 공백 가시화).
- **메타**: `meta{generated_at(ISO 분단위), generator, source_files[{member,file,drive_id,modified}], warnings[]}`. 롤업 동일파일명 다중 존재 시 **modifiedTime 최신본만 채택** + 채택 근거를 `source_files`에.
- **사용 지침**: `guide{title, items[]}`(대시보드 상단 렌더 — 하드코딩 금지, config가 정본).
- **사내공지**: 그린필드 `06_Notice_사내공지/`의 **active 공지**를 `notices[]`(최신순, `active=true`만)로 집계. 대표 발화 **"사내공지로 해줘: {내용}"** → 소스 파일 생성 → 다음 run 반영, **"공지 내려줘"** → `active:false`. body **원문 보존**(요약 금지). 스키마·트리거 정본 = spec §I-4.
- 심상윤 `master:true`. 게이트 권한: 🔴 대표검수 / 🟡 팀장판단·보고(`yellow_policy`) / 🟢 자율.

## 4. 출력 = 대시보드 config (구형 폐기)
- 형식 = **포피스 대시보드가 읽는 데이터** = `poffice_board.json`. 스키마 정본 `docs/poffice-board-spec.md`(A~H + 확장: meta·guide·freshness·sessions[].raw). 스키마 변경 시 **확정본을 코워크에 회신**.
- ~~구형: 리포트/브리프/워크오더 텍스트 문서~~ → **더 이상 정본 아님.** 대시보드 config로 일원화.
- 빌드된 `tool/PIMM_Poffice.ver0.2.html`이 이 config를 로드(같은 폴더 fetch 또는 드래그앤드롭).

## 5. 자동예약 / 흐름
- CronCreate 등으로 **주기적 생성·갱신**(예: 주 1회·세션로그 갱신 시).
- `Poffice-Skill`(개인 기록) → **`Poffice-MotherLog`(집계→config)** → 대시보드(시각화) → export(체크·메모) → Poffice-Skill 반영 → `Poffice-Report-Bot`(직전 config와 diff 브리핑).

## 6. 경계
- **원본 세션로그 수정 금지**(불변·아카이빙). config만 생성.
- 개인 데이터 격리(타인 혼입 금지). 손상 JSON 덮어쓰기 금지(원칙 1).
- **`poffice_board.json` 은 포피스영역에 단 1개 · update-by-fileId (create 반복 금지).** 중복본(`(1)(2)(3)…`)을 만들지 않는다. 매 run 새 파일 생성은 대시보드가 옛 데이터를 읽게 만드는 버그다(§1 쓰기 규칙 준수). 아카이빙(스냅샷)은 `04_LogArchive_로그집계/`에 **다른 이름(ts 접두)** 으로만 남기고, 라이브 정본 이름은 건드리지 않는다.
