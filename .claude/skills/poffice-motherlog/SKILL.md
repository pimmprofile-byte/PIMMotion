---
name: poffice-motherlog
description: 포피스 마더로그 생성 스킬. 각 개인세션로그를 읽어 분석하여 '포피스 대시보드가 그대로 읽는 config(마더 세션로그)'를 만들어 드라이브 그린필드 내 포피스영역에 뿌린다. ★원문 보존 우선(요약 금지) — sessions[]에 원문 전문 raw + 1줄 summary, 분단위 타임스탬프. 구형의 리포트/브리프/워크오더 텍스트 형식이 아니라, 현재 포피스 대시보드(tool/PIMM_Poffice.ver0.9.html)에 노출되는 데이터 형식(poffice_board.json)으로 출력한다. 빌드된 HTML이 이 config를 로드한다. 트리거: 마더세션로그, 마더로그, 포피스 config 생성, 포피스 대시보드 갱신, 세션로그 집계, poffice_board.json 생성. 데이터 생성 담당(개인 기록은 Poffice-Skill, 브리핑은 Poffice-Report-Bot).
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
- **라이브**: `poffice_board.json`(대시보드 로드 정본) — 포피스영역에 **딱 1개**만.
  > ⚠️ **동일 파일명 중복 금지.** 커넥터에 **update 도구가 없다**(create 계열뿐, 2026-07-27 실측). 같은 이름으로 create를 반복하면 Drive가 fileId로 구분해 `poffice_board (1).json`·`(2)`… 로 복제되고, 접미사 없는 정본이 옛 파일이 되어 대시보드가 **옛 데이터를 읽는 버그**가 난다.
  > ✅ **쓰기 규칙 = 제자리 수정(in-place overwrite)** — *구 "update-by-fileId"는 커넥터에 update가 없어 구현 불가, 폐기.* 라이브·미러는 **같은 경로를 `open(path,"w")`로 덮어써 inode를 유지**한다. Drive 데스크톱 마운트가 이를 새 파일이 아니라 **같은 파일의 새 리비전**으로 처리 → fileId 보존, `(1)(2)` 복제 없음. (실측: 마운트에서 `rm`은 "Operation not permitted"로 막히고, in-place 덮어쓰기·`rename`은 정상. truncate가 `Errno 35 Resource deadlock`로 거부되면 **rename-swap 폴백**.)
  > **하드삭제 금지**: 폐기물은 지우지 말고 제로필드로 이동.
  > **파이프라인 3단**: **scan**(변경 감지·수집) → **assemble**(아카이브 `04_LogArchive_로그집계/`에 `{YYMMDD_HHMM}_poffice_board.json` **타임스탬프 신규 생성**) → **promote**(라이브 + 런처 미러에 **제자리 덮어쓰기**). 아카이브만 파일이 쌓임(의도됨·별도 정리). 예약(`pimm-motherlog-daily`, 1일 1회 11:00)이 scan+assemble+promote까지 수행. 정본은 언제나 **접미사 없는 단일 `poffice_board.json`**.
- **★ 배포 미러 (런처 폴더 · 매 run promote 단계)**: 런처 폴더 `PIMM_Launcher`(id `1pC9V2ZKO5rWrIDXc0mRAsHRgDEL9iqkX`)의 `poffice_board.json`을 **제자리 덮어쓰기**(+ 개인DB 동일본 미러도 함께 유지). 대시보드/허브가 같은 폴더 상대 fetch로 로드 — 별도 링크·ID 불필요.
  > **★ `.js` 미러도 함께 (더블클릭 자동 로드용):** 런처 폴더에 `poffice_board.js`(=**`window.POFFICE_BOARD = <그 JSON 그대로>;`**, 한 줄 전역 대입, 내용 100% 동일)도 **제자리 덮어쓰기**로 둔다. `file://`에서 `fetch(.json)`는 막히지만 `<script src>`는 허용 → 팀원이 대시보드를 **더블클릭만 해도** 실데이터 로드(대시보드 v0.7+가 `.js` 우선 로드). `contentMimeType=application/javascript` + **UTF-8 BOM(`utf-8-sig`)** (file://서 charset보다 우선해 이모지 보존). **promote가 라이브·미러·`.js` 3종을 항상 함께 동기화**(v0.9.10에서 조기리턴 제거·`--mirror append` 수정 완료).
  > ※ 정본은 포피스영역(.json), 런처의 .json/.js는 대시보드 로드용 미러. 세 파일 모두 제자리 덮어쓰기, 내용 동일.
  > ※★ **원문 축약 금지**: `.js`/`.json` 어느 쪽이든 `sessions[].raw`는 스크립트가 **원본 바이트를 그대로 주입**(요약·재작성 금지). 예산(멤버당 최근 14일/최소 5건/200KB) 초과 시만 **통째 생략** + `raw:null`·`raw_omitted:true`·`raw_source`(경로) — 절대 절단하지 않음.
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
- **세션 원문 보존(§원칙 3)**: `sessions[]` 각 항목 = `ts`(분단위) + `file` + `summary`(1줄) + **`raw`(세션로그 원문 전문)**. raw는 **스크립트가 원본 바이트를 그대로 주입**(모델이 타이핑하지 않음 — 손상·경량화). 자르거나 재요약하지 않는다.
  - **예산 초과 시 통째 생략**(절단 금지): `raw:null` + `raw_omitted:true` + `raw_source`(원본 경로). 예산 = 멤버당 최근 14일 / 최소 5건 / 200KB.
  - MotherLog 내부용 필드: 멤버별 `_fingerprint`(sha1, 증분 갱신)·`_carried_forward`(직전 board에서 그대로 가져온 인물). **HTML·타 소비자는 무시.**
- 파생 상태(요약 아님, 롤업/원문에서 도출): 미션(progress·roadmap), 게이트(권한 신호등), 투두(체크·중요도·일자·WO).
- **★ 윈도우 = 실행 주기와 무관 (2026-07-27 확정).** **최근 14일 + 인물별 최소 5건(14일을 넘겨도 포함) + raw 예산 200KB/인** 을 그대로 쓴다.
  - **주기 기반 슬라이딩 윈도우(13h 등)를 두지 않는다** — 그렇게 하면 봇이 하루 죽었을 때 그 하루가 영구 실종된다. **고정 14일 윈도우**면 다음 회차가 빈 구간을 자동으로 덮는다(안전장치). **예약 주기를 바꿔도 윈도우는 손대지 않는다.**
  - *구 "13h(2회/일 기준)"은 ver0.2 시절 잔재라 폐기.* 원문은 안 자르고 **담는 범위만** 위 기준으로 제한(초과분은 raw_omitted, §3 상단).
  - 창 밖으로 밀린 원문은 **삭제 아님** — 개인 세션폴더(불변) + `04_LogArchive_로그집계/`에 보존. 롤업(게이트·투두·미션)은 윈도우와 무관하게 **상시 유지**.
  - **작업물**: 각 인물 `Output_산출물/`의 산출물 참조(파일명·경로)를 세션 raw에 남긴다. ※ 대시보드 전용 렌더 칸은 후속.
- **신선도 파생**: 인별 `freshness{last_log_ts, status}` — `green`(24h 이내)/`yellow`(24~72h)/`red`(72h+ stale). **숨기지 않는다**(기록 공백 가시화).
- **메타**: `meta{generated_at(ISO 분단위), generator, source_files[{member,file,drive_id,modified}], warnings[]}`. 롤업 동일파일명 다중 존재 시 **modifiedTime 최신본만 채택** + 채택 근거를 `source_files`에.
- **사용 지침**: `guide{title, items[]}`(대시보드 상단 렌더 — 하드코딩 금지, config가 정본).
- **사내공지**: 그린필드 `06_Notice_사내공지/`의 **active 공지**를 `notices[]`(최신순, `active=true`만)로 집계. 대표 발화 **"사내공지로 해줘: {내용}"** → 소스 파일 생성 → 다음 run 반영, **"공지 내려줘"** → `active:false`. body **원문 보존**(요약 금지). 스키마·트리거 정본 = spec §I-4.
- 심상윤 `master:true`. 게이트 권한: 🔴 대표검수 / 🟡 팀장판단·보고(`yellow_policy`) / 🟢 자율.

## 4. 출력 = 대시보드 config (구형 폐기)
- 형식 = **포피스 대시보드가 읽는 데이터** = `poffice_board.json`. 스키마 정본 `docs/poffice-board-spec.md`(A~H + 확장: meta·guide·freshness·sessions[].raw). 스키마 변경 시 **확정본을 코워크에 회신**.
- ~~구형: 리포트/브리프/워크오더 텍스트 문서~~ → **더 이상 정본 아님.** 대시보드 config로 일원화.
- 빌드된 `tool/PIMM_Poffice.ver0.9.html`이 이 config를 로드(같은 폴더 fetch 또는 드래그앤드롭).

## 5. 자동예약 / 흐름
- **예약 = 1일 1회 11:00 KST**(태스크 `pimm-motherlog-daily`, 디스패치 지터로 실착수 11:0x). 구 `pimm-log-bot`(2회/일)은 `enabled:false` 퇴역 보존.
- `Poffice-Skill`(개인 기록) → **`Poffice-MotherLog`(scan→assemble(아카이브)→promote(라이브+런처/개인DB 미러 + `.js` 제자리 덮어쓰기))** → 대시보드(같은 폴더 로드) → export(체크·메모) → Poffice-Skill 반영 → `Poffice-Report-Bot`(직전 config와 diff 브리핑 + 인물별 디스코드 푸시, 웹훅 URL 정본은 `pimm-notice` 스킬 한 곳).
- **Report-Bot §4.5 예외(2026-07-27)**: `sessions`가 **비어 있으면**(로그 0건) `_carried_forward` 무관하게 **매일 1줄 발송**. 로그는 있는데 이번 회차 변경만 없는 인물은 기존대로 건너뜀. (0건이어도 매일 보낸다 = 대표 지시.)

## 5-1. 중복본 수거 (매 회차 ①scan 직전)
팀원 세션은 드라이브 커넥터에 **파일 수정 도구가 없어** 롤업을 갱신할 때 동명 새 파일을 만들 수밖에 없다(`pimm-artisan-session` 규정). 드라이브 데스크톱이 그걸 로컬로 내리면서 `GATE_현황 (1).md`가 생긴다. **중복은 팀원 실수가 아니라 구조적 산물**이고, 정리를 대표에게 맡기면 브리핑을 안 돌린 날마다 쌓인다. 그래서 마더로그가 스캔하는 김에 함께 치운다(`collect-dupes` 서브커맨드, `build_poffice_board.py`).
- **`--apply` 없으면 드라이런.** 처음 보는 패턴은 드라이런으로 먼저 확인.
- 대상 = **롤업 3종(`GATE_현황.md`·`TODO_현황.md`·`MISSION_보드.md`) 화이트리스트뿐.** 세션로그 원본(`_log.md`)은 이름이 매번 달라 충돌하지 않으므로 대상 아님(§6 불변 유지).
- 승격 판정 = **mtime + 파일 내부 「갱신 이력」 마지막 ts 교차검증.** 동기화 중 mtime이 뒤집힐 수 있어 단독으로 안 믿음. **두 근거가 다른 파일을 가리키면 병합 포기·「보류」 보고**(추측으로 남의 기록 덮지 않음).
- 승격 = **원본 파일 제자리 쓰기(inode 보존)** → 드라이브가 리비전으로 받아 중복 재생산 없음. **원본 이름 파일은 어떤 경우에도 휴지통행 금지**(내용이 승격된 정본).
- 구본은 `{YYMMDD_HHMM}_{이름}_세션로그중복본/` 으로 **이동만**(하드삭제 없음). 보류 건은 runlog `--note`+대표 보고.

## 6. 경계
- **원본 세션로그 수정 금지**(불변·아카이빙). config만 생성.
  - **유일한 예외: §5-1 중복본 수거** — 롤업 3종에 한해 제자리 승격·구본 이동 허용. `_log.md`에는 예외 미적용.
  - 타인 세션로그 영역 쓰기 루트는 이제 **둘**: `gate-briefing`(workorder 기록) + `Poffice-MotherLog` §5-1(수거). 그 외 금지. (gate-briefing 스킬 문구도 갱신 완료.)
- 개인 데이터 격리(타인 혼입 금지). 손상 JSON 덮어쓰기 금지(원칙 1).
- **`poffice_board.json` 은 단 1개 · 제자리 수정(in-place overwrite, create 반복 금지).** 중복본(`(1)(2)(3)…`)을 만들지 않는다. 라이브·미러는 같은 경로 덮어쓰기(inode 유지)로만 갱신, 아카이브(`04_LogArchive_로그집계/`)에만 `{ts}_poffice_board.json` 타임스탬프로 쌓는다. **하드삭제 금지**(폐기물=제로필드 이동).
