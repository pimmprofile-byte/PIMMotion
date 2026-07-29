# 포피스 대시보드 — poffice_board.json 스키마 (확정본 v1)

> 핸드오프 회신: 코드 세션 → 코워크. 포피스 대시보드(현행 `tool/PIMM_Poffice.ver0.2.html`)가 이 스키마를 로드한다.
> 원칙: **코어(엔진) + 데이터(JSON) 분리. 읽기 전용.** 로컬 인터랙션은 투두 '체크' + '메모'뿐이며,
> 그 결과는 `poffice_export_{이름}.json` 으로만 내보내 코워크가 세션로그에 반영한다(그 외 역방향 쓰기 없음).

## 데이터 흐름 (단방향 + 체크·메모 예외)
```
코워크: 세션로그 집계 → poffice_board.json 생성/갱신(**단일 파일 · 제자리 수정(in-place overwrite)**, create 반복 금지)
  ⚠️ 커넥터에 update 도구가 없어 매 run 새로 create하면 드라이브가 `poffice_board (1)(2)(3).json` 로 복제되고, 접미사 없는 정본이 옛 파일이 되어 대시보드가 옛 데이터를 읽는다. → **같은 경로 `open(path,"w")` 제자리 덮어쓰기**(inode/fileId 보존, Drive 데스크톱 마운트가 새 리비전으로 처리). 하드삭제 금지(제로필드 이동). 파이프라인 scan→assemble(아카이브 타임스탬프)→promote(라이브·미러 제자리 덮어쓰기). (상세: poffice-motherlog SKILL §1)
   → 대시보드가 파일선택/드래그앤드롭으로 로드 (서버 불필요)
대시보드: 투두 '체크' + '메모'만 로컬 변경 → [내보내기] → poffice_export_{이름}.json
   → 코워크가 읽어 세션로그에 반영 (데이터 꼬임 방지: 포피스는 '체크·메모'만 다룸)
```

## 스키마 v1 (핸드오프안 확정 + 조정 3건)

```jsonc
{
  "version": 1,
  "generated_at": "2026-07-25T16:00:00+09:00",
  "members": [
    {
      "name": "심상윤",
      "role": "Master PD",
      "yellow_policy": "auto",          // auto(자체진행) | report(보고대상) — 옐로게이트 정책. 대시보드가 인물별 배지(자체 진행/보고 대상)로 표시
      "master": true,                   // 마스터 플래그(심상윤만 true). ver0.12: 모든 인물의 레드게이트를
                                        //          '나에게 온 레드게이트' 인박스로 자동 취합·인물별 색인
      "yellow_approver": true,          // [ver0.12] 옐로게이트 결재자 플래그(오세원·유지호=true). true인 인물 화면에
                                        //          yellow_policy=="report" 인물(이정민·신승희)의 옐로게이트가 인박스로 취합
                                        //          (결재 답신 방식(취합→푸시→답변)은 시스템 미확정 — 현재는 자동 확인·색인까지)
      "missions": [
        { "id": "M0", "title": "홈페이지 리뉴얼 런칭",
          "status": "진행",             // 예정 | 진행 | 달성 | 보류
          "due": "2026-08-15",          // D-day 자동 계산
          "progress": 0.35,             // 0~1
          "roadmap": [ { "step": "파워링크 소재", "done": true },
                       { "step": "핌 사이트 리뉴얼", "done": false } ] }
      ],
      "gates": {
        "red":    [ { "ts": "260725_1530", "item": "M3 텀블벅 포함 여부 결정",
                      "state": "대기",     // 대기 | 진행 | 완료
                      "log": "260725_1530_..._log.md" } ],
        "yellow": [], "green": []
      },
      "todos": [
        { "text": "홈페이지 작업 시작",
          "state": "doing",             // todo | doing | done
          "wo": false,                  // true면 대표 지시 → WO 배너 상단 강제 고정 + 강조
          "mission": "M0",              // 연결 미션 id (표시용)
          "importance": "high",         // [조정2] high | mid | low — '중요도별' 정렬용
          "date": "260725" }            // [조정2] YYMMDD — '일자별' 정렬용
      ],
      "last_session": { "file": "260725_1600_..._log.md", "summary": "..." }
                                        // [옵션·현재 대시보드 미사용] 로그 뷰는 sessions[]를 사용
    }
    // × 5인 (심상윤·이정민·유지호·오세원·신승희)
  ],
  "docs": [ { "no": "MTG-20260725_포피스자동화", "type": "회의록",   // [옵션·현재 대시보드 미사용]
              "source": "260725_1530_..._log.md" } ]
}
```

### 조정 3건 (확정 요청)
1. **`member.master: true`** — 심상윤 보드를 미션보드 최상단에 고정하기 위한 플래그. **데이터에는 존재하나 최상단 고정은 현재 대시보드(ver0.2) 미구현(ver0.3 예정)** — ver0.2는 인물선택 개인 워크스페이스라 `m.master`를 읽지 않는다.
2. **`todo.importance` (high|mid|low) + `todo.date` (YYMMDD)** — 요구된 *중요도별/일자별 정렬*의 근거 필드. WO(`wo:true`)는 정렬과 무관하게 항상 최상단.
3. **게이미피케이션은 데이터에서 파생(derive)** — 별도 스키마 불필요. 대시보드가 `todos` 중 `state==="done"` 수를 세어 **처리량·칭호(신입→숙련→베테랑→게이트마스터)·진행률·뱃지**를 자동 계산한다. 추후 수동 지정이 필요하면 `member.title` 오버라이드 필드를 옵션으로 추가 가능(현재는 미사용).

## 역방향 내보내기 포맷 (`poffice_export_{이름}.json`) — 인물별 단일 파일
```jsonc
{
  "member": "심상윤",                                // 내보낸 본인 이름(인물선택 워크스페이스)
  "generated_from": "2026-07-25T16:00:00+09:00",   // 원본 board.json의 generated_at
  "check_overrides": {                              // todos 인덱스 → 변경된 상태 (본인 것만)
    "0": "done", "2": "doing"
  },
  "memo_overrides": {                               // "mission|{미션ID}" 또는 "session|{ts}" → 메모 텍스트
    "mission|M0": "런칭 일정 재확인 필요",
    "session|260725_1600": "이 세션 관련 후속 메모"
  },
  "note": "Poffice-Skill 이 세션로그·미션 메모/체크에 반영 (타임스탬프는 반영 시 부여)"
}
```
코워크(`Poffice-Skill`)는 이 오버라이드를 읽어 **본인** 세션로그의 투두 체크상태·메모에 반영한다. (인덱스는 board.json의 해당 인물 `todos` 배열 순서 기준 — 이름-키가 아니라 인덱스-키.)

## 대시보드 3판 (구현 완료 — v0.2)
1. **미션보드** — 인별 마일스톤 카드(상태 pill·D-day·진행률·역산 로드맵). (심상윤 마스터보드 최상단 고정은 ver0.3 예정, ver0.2 미구현.)
2. **게이트보드** — 🔴 보고처리 / 🟡 자체결재(yellow_policy로 자율·필수보고 표시) / 🟢 기록만. 항목별 상태·타임스탬프·근거로그.
3. **투두리스트** — 인별 체크박스(3상태 순환 todo→doing→done), WO 태그·상단고정, 미션 id·중요도·일자 태그, 중요도/일자 정렬.

＋ **WO 배너**(대표 지시 필수확인, 최상단 고정) · **게이미피케이션 스트립**(처리량·칭호·진행률·뱃지).

---

# v0.2 확정 사항 (2026-07-25 로직 점검 반영)

## A. 게이트 = 신호등, 단 '위험'이 아니라 '권한/중요도'
| | 의미 | 진행 규칙 |
|---|---|---|
| 🔴 레드 | 대표 검수 필요 | **대표(심상윤) 검수·승인 후** 진행 |
| 🟡 옐로 | 팀장 판단 | 팀장 판단으로 진행 · **팀원은 팀장 또는 대표에게 보고 필수** (`yellow_policy: report`가 이 대상) |
| 🟢 그린 | 자율 | 알아서 진행 (기록만) |

## B. 미션보드 = 마일스톤 + Day char 스프라이트
- 골인지점(goal)과 현재 위치를 **경로 위 캐릭터 전진**으로 도식화(게임식). progress(0~1) → 캐릭터 위치.
- 스프라이트 정본: Drive `RuleTheDay/day.png` (Day Mario 캐릭터). `poffice_board.json`엔 이미지 미포함, 대시보드가 참조.
- 미션에는 **메모 필수 슬롯**.

## C. 데이터 계층 (개인세션로그 폴더) — §2 규칙 확정, 추가:
- **폴더 구조·Drive 경로/ID 정본 = `pimm-artisan-session`** (개인세션로그는 `Session_세션로그` **바로 아래 평면 구조**; 중첩 폴더·평행 구조 신설 금지). Poffice 3종은 이 구조·ID 테이블을 **그대로 소비**한다.
- 메모(사람이 다는 mutable)는 역방향 export의 `memo_overrides`(`"mission|{미션ID}"`/`"session|{ts}"` 키)로 반영 — 별도 `memo/` 폴더 트리 없음(평면 유지).
- 세션로그 UX: **최근=선명 → 오래될수록 opacity 흐림 → 드롭다운/스크롤로 더 로드** (이메일 아닌 게임식). `poffice_board.json`은 최근 윈도우(**14일 + 인물별 최소 5건**)+롤업만.
- 역방향 export = **체크 + 메모** 둘 다 (`poffice_export_{이름}.json`에 `memo_overrides` 포함).

### C-1. 구형 주간보고 폐기 (v2.0 정합 · 사용자 확정)
- 구형 **텍스트 주간보고**(리포트/브리프/워크오더 문서, `pimm-weekly-review → WK-` 조립기 개편안 포함)는 **폐기**.
- 주간보고는 **`Poffice-Report-Bot` 페르소나 브리핑 + `poffice_board.json` config로 일원화**(대화가 서류가 된다). 별도 텍스트 리포트 산출물 없음.

## D. 개인화
- 실행 시 **인물 선택**(자기 이름) → 개인 워크스페이스. 타인 내용 기본 비노출. 선택 이름 = 로컬 config.
- 디자인: 기존 피모션(네온 터미널)과 다르게 **차분한 다크 워크스페이스** — 명확·직관·도식화 우선.

## E. 스킬 아키텍처 → **§H(스킬 3종) 참조**
현행 정본은 아래 **§H의 3-스킬 모델**이다: `Poffice-Skill`(기록) → `Poffice-MotherLog`(집계→config 생성) → `Poffice-Report-Bot`(페르소나 브리핑).
```
① Poffice-Skill (기록): 대화 → 개인세션로그 자동저장 + 게이트/체크/미션 분류 → 개인DB 기록
② Poffice-MotherLog (집계→config): [자동예약·주기적] 각 개인세션로그 스캔·요약·분석
     → poffice_board.json 생성/갱신 (최근 윈도우+롤업), 그린필드/포피스영역 저장
대시보드: 열 때 최신 poffice_board.json 자동 로드 → 반영
         (자동 로드 = 허브와 poffice_board.json이 같은 Drive 동기 폴더에 있을 때 fetch,
          아니면 드래그앤드롭 폴백)
```
- **집계 담당(`Poffice-MotherLog`) 책무**: `Poffice-Skill`의 산출물(개인세션로그) 형식을 정확히 알고, 그것을 이 문서의 `poffice_board.json` 스키마로 결정론적으로 변환. 대표 주간보고 판단을 반영해 게이트(레드/옐로/그린)·WO를 세팅.
- 트리거: 1일 1회 11:00 KST 자동예약(`pimm-motherlog-daily`).

## F. 스킬 통합명 = `Poffice-Skill` (확정)
- 기존 **개인세션로그 스킬 + 포피스 스킬**을 하나로 통합해 신설하는 스킬의 이름은 **`Poffice-Skill`** (간소화 확정).
- 읽기/분석 트리거: 세션로그·세션·스케줄·작업보고·업무지시·업무보고·미션보드·포피스 등.
- 동작 트리거: 포피스 업로드·포피스 수정 등.
- 세션로그 타임스탬프는 `YYMMDD_HHMM`(시간 포함) 규칙 준수.

> ※ A~F 대표 확정 완료(2026-07-25). 이 문서가 `Poffice-Skill`·대시보드 공용 정본.

## G. v0.2 스키마 추가분 (`tool/PIMM_Poffice.ver0.2.html` 반영)
- **`member.sessions`**: 세션로그 배열 — 대시보드의 시간순 opacity-fade 드롭다운 소스.
  `[{ "ts":"YYMMDD_HHMM", "summary":"...", "detail":"..." }]` (최근순 정렬, 오래될수록 흐림).
  `poffice_board.json`은 최근 윈도우만 담고, 더 오래된 건 개인세션로그 파일로.
- **export 확장**: `poffice_export_{이름}.json` = `{ member, generated_from, check_overrides, memo_overrides, note }` (인물별 단일 파일).
  - `check_overrides` 키: **todos 인덱스 → 상태**(본인 것만, 이름-키 아님).
  - `memo_overrides` 키: `"mission|{미션ID}"` 또는 `"session|{ts}"` → 메모 텍스트.
  - Poffice-Skill 이 이 export를 읽어 세션로그·미션 메모/체크에 반영(타임스탬프는 반영 시 부여).
- **진입**: 인물 선택 → `localStorage.poffice_me` 저장, 본인 데이터만 표시.
- **옵션/미사용 필드**: `member.last_session`(로그 뷰는 `sessions[]` 사용), 최상위 `docs[]`, 샘플 스키마의 `generator` 는 **현재 대시보드가 사용하지 않는 옵션 필드**다(삭제하지 않고 보존 — 스키마·대시보드가 상충하는 것이 아니라 옵션임).
- **스킬 표기 관례**: 스킬 frontmatter `name:`은 소문자(`poffice-skill`·`poffice-motherlog`·`poffice-report-bot`)이고 본문 산문은 `Poffice-Skill` 식 대문자 표기를 쓴다 — **의도된 관례이며 불일치가 아니다.**

## H. 스킬 3종 분리 (관심사·토큰 분리)
| 스킬 | 역할 | 트리거 |
|---|---|---|
| **`Poffice-Skill`** | **기록** — 대화 → 개인세션로그 자동기록(게이트·체크·미션 분류) + 역방향 export(체크·메모) 반영 | 세션로그·세션·스케줄·작업보고·업무지시·업무보고·미션보드·포피스 / 포피스 업로드·수정 |
| **`Poffice-MotherLog`** | **집계→config** — 각 개인세션로그를 요약·분석 → 대시보드가 읽는 `poffice_board.json`(마더 세션로그) 생성, **그린필드/포피스영역**에 저장, 자동예약 | 마더세션로그·마더로그·포피스 config 생성·포피스 대시보드 갱신·세션로그 집계·poffice_board.json 생성 |
| **`Poffice-Report-Bot`** | **알림·브리핑** — 마더 config를 직전 버전과 diff → 갱신·특이사항·사내공지를 **개인별 페르소나 말투**로 전달. 강제 아님, "{이름} 포피스알림켜줘"로 예약 활성화 | 포피스 알림·포피스알림켜줘·주간보고·일일보고·브리핑 |

흐름: `Poffice-Skill`(기록) → `Poffice-MotherLog`(집계→config) → 대시보드(로드·시각화) → export(체크·메모) → `Poffice-Skill` 반영 → `Poffice-Report-Bot`(diff 브리핑).

**저장 위치(마더 config)**: 그린필드 `[1.그린필드:프레임워크].PIMM_framework` / `[2.포피스_섹터].Poffice`. 대시보드 HTML은 같은 폴더 `poffice_board.json`을 fetch(없으면 드래그앤드롭·샘플).
**구형 폐기**: 리포트/브리프/워크오더 텍스트 문서 형식 → 대시보드 config로 일원화.

### ★ 마더로그 최상위 원칙 2개 (`Poffice-MotherLog` §최상위)
1. **텍스트가 절대 깨지면 안 된다** — UTF-8·한글 보존, JSON 이스케이프 정확, 잘림·mojibake 금지, 생성 후 파싱 검증(손상본 덮어쓰기 금지).
2. **원문 참조·아카이빙·무왜곡** — 항목마다 출처 개인세션로그 근거, 원본 불변 보존, 요약 시 과장·축소·창작 금지(불확실하면 원문 참조).

- 페르소나 정본: `.claude/skills/poffice-report-bot/SKILL.md` §4. 정보 정확성 > 캐릭터성(🔴·마감·리스크 항상 명확).
- 세 스킬 미통합(토큰 절약). 세션로그 원본 불변, 역방향은 체크·메모만.

---

# I. 원문 보존 · 정밀 추적 확장 (v1.1 · 2026-07-26 대표 확정 · 플러그인 v0.9.2 정합)

> 정책 변경: 마더로그 **"요약 중심 → 원문 보존"**. 요약본만으론 실제 업무 파악 불가(실사용 피드백). 대시보드는 **raw를 1급 콘텐츠**로 취급. 스킬 정본: `.claude/skills/poffice-motherlog/SKILL.md` §원칙3·§3.

## I-1. 스키마 확장 (기존 A~H에 추가, 하위호환)
```jsonc
{
  "meta": {
    "generated_at": "2026-07-26T17:30+09:00",   // ★ISO 분단위 (날짜만 금지)
    "generator": "poffice-motherlog",
    "source_files": [ { "member":"심상윤","file":"260726_1530_..._log.md","drive_id":"...","modified":"..." } ],
    "warnings": [ "신승희: 72h+ 무기록" ]
  },
  "guide": { "title":"포피스 사용 수칙", "items":[ "…", "…", "…" ] },   // 대시보드가 이 필드로 렌더(하드코딩 금지)
  "members": [ {
    // …기존 필드(name·role·yellow_policy·master·missions·gates·todos·last_session)…
    "freshness": { "last_log_ts":"260726_1530", "status":"green" },   // green(24h)/yellow(24~72h)/red(72h+ stale)
    "sessions": [ {
      "ts":"260726_1530",                              // ★YYMMDD_HHMM 분단위 필수
      "file":"260726_1530_포피스정합_log.md",
      "summary":"1줄 헤드라인",
      "raw":"(세션로그 원문 전문 — 요약·축약 없음, 개행 이스케이프)"   // ★신설 = 원문 보존
    } ]
  } ]
}
```
- **원문 보존 규칙**: `raw`는 원문 전문 그대로. 자르거나 재요약 금지. 파일이 커지면 **윈도우(담는 범위)를 줄이지, raw를 자르지 않는다.**
- **윈도우 = 실행 주기와 무관**: 최근 **14일 + 인물별 최소 5건**(14일 넘겨도 포함) + raw 예산 200KB/인. 주기 기반 슬라이딩(13h 등) 안 씀 — 봇이 하루 죽어도 다음 회차가 빈 구간을 덮음. 밀린 원문은 개인폴더+`04_LogArchive` 보존, 롤업 상시 유지. 예약 = 1일 1회 11:00(`pimm-motherlog-daily`). 정본 = poffice-motherlog SKILL §3.
- **modifiedTime 최신본 채택**: 롤업 동일파일명 다중 존재 시 최신본만 채택 + `meta.source_files`에 근거 기록.

## I-2. 대시보드 요구사항 (`tool/PIMM_Poffice` — 반영 대상, 신규 build)
- **A. 사용 지침 패널** — `guide` 필드에서 렌더(하드코딩 금지).
- **B. 신선도 배지** — 인별 카드에 `freshness` 경과시간 + 🟢/🟡/🔴 stale. 숨기지 않음.
- **C. 연동/집계 상태 표시 (상단 상시 · 피모션 코워크 연동상태 방식)** — 헤더에 **최신 로그 타임스탬프**(전 인물 `sessions[].ts` 최댓값 = 가장 최근 기록)와 `generated_at` 분단위를 상시 표시("최근 기록 07/26 15:30 · 집계 07/26 17:30"). **오래되면**(예: 최신 로그 24h+ 또는 집계 48h+) 톤을 경고로 바꾸고 **[새로고침] 버튼** 노출 → board.json 재로드(같은 폴더 fetch 재시도, 실패 시 드래그앤드롭 안내).
- **D. 🔴 레드게이트 상단 고정** — 마스터 뷰에서 전원 🔴 대기 건 최상단 집계.
- **E. 세션 원문 뷰** — 세션 타임라인 항목: 접힘 = `ts`+`summary` 1줄 / 펼침 = `raw` 원문 전문 마크다운(또는 pre 스크롤). 검색/필터는 raw 본문 포함. **raw 자르거나 재요약 금지.**
- **F.** 기존 기능 유지(미션보드·게이트 3분류·체크리스트). ※ 대시보드 build는 spec 확정 후 별도 진행(스키마 확정본 코워크 회신).

## I-3. 정밀도 리스크 처방
- **기록 공백**(세션요약 누락) → 신선도 배지 stale로 가시화(숨김 금지).
- **구본 혼선**(롤업 동일파일명 다중) → 최신본만 채택 + `source_files` 근거.
- **과잉 요약** → 원문 보존(raw 1급 콘텐츠).

## I-4. 사내공지 (`notices[]` · 대표 발화 트리거 · durable)
> 목적: 대표가 사내공지를 올리면 포피스 대시보드(+핌런처 공지 배너)에 **강조 노출**. **마더로그 재생성마다 사라지면 안 되므로** durable 소스 파일에서 매 run 집계.
- **durable 소스**: 그린필드 `[2.포피스_섹터].Poffice/06_Notice_사내공지/{YYMMDD_HHMM}_{제목}.md` (게시글 원본, 불변).
- **트리거(대표 전용)**:
  - 추가: **"사내공지로 해줘: {내용}"** (유사: "공지 띄워줘"·"사내공지 추가") → `06_Notice_사내공지/`에 파일 생성(active) → **다음 `poffice-motherlog` run이 `notices[]`에 반영**.
  - 내림: **"공지 내려줘"** / "{제목} 공지 내려줘" → 해당 공지 `active:false`(아카이브 이동) → 다음 run에서 제외.
- **스키마** (poffice_board.json 최상위):
```jsonc
"notices": [ {
  "ts": "260726_1430",                 // 분단위 게시 시각
  "title": "사내공지 제목",
  "body": "본문 — 원문 보존(요약 금지, 개행 이스케이프)",
  "level": "normal|important|urgent",  // 강조 강도
  "active": true                        // false = 내려간 공지
} ]
```
  - `notices[]`는 **active=true만, 최신순**. 없으면 빈 배열(대시보드는 "공지 없음").
- **소비**: 포피스 대시보드 = `notices[]` 상단 **강조 렌더**(level별 톤). 핌런처 HUB 공지 배너 = 현재 수동 `NOTICE`(또는 http 서빙 시 fetch), **마더로그 자동연동은 후속**.
