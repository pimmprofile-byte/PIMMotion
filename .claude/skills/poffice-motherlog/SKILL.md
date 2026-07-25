---
name: poffice-motherlog
description: 포피스 마더로그 생성 스킬. 각 개인세션로그를 읽어 요약·분석하여 '포피스 대시보드가 그대로 읽는 config(마더 세션로그)'를 만들어 드라이브 그린필드 내 포피스영역에 뿌린다. 구형의 리포트/브리프/워크오더 텍스트 형식이 아니라, 현재 포피스 대시보드(tool/PIMM_Poffice.ver0.2.html)에 노출되는 데이터 형식(poffice_board.json)으로 출력한다. 빌드된 HTML이 이 config를 로드한다. 트리거: 마더세션로그, 마더로그, 포피스 config 생성, 포피스 대시보드 갱신, 세션로그 집계, poffice_board.json 생성. 데이터 생성 담당(개인 기록은 Poffice-Skill, 브리핑은 Poffice-Report-Bot).
---

# Poffice-MotherLog — 개인세션로그 → 대시보드 config(마더 세션로그)

> 역할: 각 인물의 **개인세션로그를 읽어 요약·분석** → **포피스 대시보드가 읽는 config**(마더 세션로그)를 생성.
> 저장: 드라이브 **그린필드 내 포피스영역**. 빌드된 대시보드 HTML이 이 config를 로드한다.
> 개인 기록은 `Poffice-Skill`, 브리핑은 `Poffice-Report-Bot`. 스키마 정본: `docs/poffice-board-spec.md`(A~H).

## ★ 최상위 원칙 2개 (무엇보다 우선)
1. **텍스트가 절대 깨지면 안 된다.**
   - UTF-8 보존 · 한글/특수문자 mojibake 금지 · 줄바꿈/따옴표 등 **JSON 이스케이프 정확**.
   - 누락·잘림(truncation) 금지. 생성 후 **JSON 파싱 검증**(깨지면 폐기·재생성, 손상본을 덮어쓰지 않음).
2. **원문을 참조·아카이빙하여 왜곡이 없게 한다.**
   - 모든 요약·분석 항목은 **출처 개인세션로그**(파일명/경로/ts)를 근거로 단다(게이트의 `log`, 세션의 `ts` 등).
   - **원문 아카이빙**: 개인세션로그 원본은 불변 보존(요약이 원본을 대체하지 않음).
   - 요약 시 **사실 왜곡·과장·축소·창작 금지.** 불확실하면 추정하지 말고 원문 참조로 넘긴다.

## 1. 저장 위치 & 폴더 구조 (그린필드 / 포피스영역)
- 그린필드: `[1.그린필드:프레임워크].PIMM_framework` (id `1HB1X19PN6DQDXpEFpheE-BFLC2eBc3CG`)
- 포피스영역: `[2.포피스_섹터].Poffice` (id `1dbUhEa2ByRtLhKryM4YpYHC4bNLzBdFm`)
- **라이브**: `poffice_board.json`(대시보드 로드 정본). 동일 파일명 덮어쓰기 → 최신본이 정본.
- **카테고리 폴더(넘버링+영문, 대시보드 카테고리와 동일)** — 구버전·이전 자료 확인용 아카이브 축:
  `01_Mission_미션보드/` · `02_Gate_게이트보드/` · `03_Checklist_체크리스트/` · `04_LogArchive_로그집계/`(구 '세션로그') · `05_WorkOrder_워크오더/` · `06_Notice_사내공지/`
- **아카이빙**: `poffice_board.json` 갱신 시 **직전 버전/변경분을 해당 카테고리 폴더에** `{YYMMDD_HHMM}_{요약}` 로 남긴다(원문 무왜곡·불변, 원칙 2). 세션로그 원본은 블루필드/개인DB에 있고 여기 `04_LogArchive_로그집계/`는 집계 스냅샷·참조용.
- 구조 정본: 포피스영역 `README_포피스섹터구조.md`.

## 2. 입력
- 각 인물 `개인DB/{이름}/Session_세션로그/`(**평면 구조** · 경로/ID 정본 = `pimm-artisan-session` 테이블)의
  `{YYMMDD_HHMM}_{요약}_log.md`(세션로그 원본), 롤업(`GATE_현황.md`·`TODO_현황.md`·`MISSION_보드.md`), `workorder/`(WO), 역방향 입력 `poffice_export_{이름}.json`.
- 대표 주간보고 판단(있으면) — 게이트(🔴/🟡/🟢)·WO 반영에 사용.
> 개인세션로그 폴더 경로·Drive ID는 **artisan-session 정본을 따른다**(중첩 구조·평행 폴더 신설 금지). 이 스킬의 하드코딩 ID는 **출력처(그린필드 Poffice)** 에 한정.

## 3. 처리 (요약·분석 → 결정론 변환)
- 세션로그를 읽어 **현재 상태**로 요약: 미션(마일스톤 progress·roadmap), 게이트(권한 신호등), 투두(체크·중요도·일자·WO), 최근 세션 `sessions[]`.
- **최근 윈도우 + 롤업만** 담는다(전체 히스토리 X — 오래된 건 원본 파일로).
- 심상윤 `master:true`(마스터보드 최상단).
- 게이트 권한: 🔴 대표검수 / 🟡 팀장판단·보고(`yellow_policy`) / 🟢 자율.

## 4. 출력 = 대시보드 config (구형 폐기)
- 형식은 **포피스 대시보드에 노출되는 데이터**(spec 스키마 + G의 `sessions[]`) = `poffice_board.json`.
- ~~구형: 리포트/브리프/워크오더 텍스트 문서~~ → **더 이상 정본 아님.** 대시보드 config로 일원화.
- 빌드된 `tool/PIMM_Poffice.ver0.2.html`이 이 config를 로드(같은 폴더 fetch 또는 드래그앤드롭).

## 5. 자동예약 / 흐름
- CronCreate 등으로 **주기적 생성·갱신**(예: 주 1회·세션로그 갱신 시).
- `Poffice-Skill`(개인 기록) → **`Poffice-MotherLog`(집계→config)** → 대시보드(시각화) → export(체크·메모) → Poffice-Skill 반영 → `Poffice-Report-Bot`(직전 config와 diff 브리핑).

## 6. 경계
- **원본 세션로그 수정 금지**(불변·아카이빙). config만 생성.
- 개인 데이터 격리(타인 혼입 금지). 손상 JSON 덮어쓰기 금지(원칙 1).
