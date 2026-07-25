---
name: poffice-skill
description: 포피스 업무보고 코어 스킬. 기존 개인세션로그 스킬 + 포피스 스킬을 통합한 것. 코워크/코드 대화를 개인세션로그로 자동기록(게이트·체크·미션 분류)하고, 개인세션로그·개인DB를 취합해 포피스 대시보드가 읽는 _board.json(= 포피스 업데이트 '마더 세션로그')을 자동생성·자동예약 갱신한다. 대시보드에서 나온 역방향 export(체크·메모)를 세션로그에 반영한다. 데이터 생성/기록 담당(브리핑은 Poffice-Report-Bot). 트리거: 세션로그, 세션, 스케줄, 작업보고, 업무지시, 업무보고, 미션보드, 포피스, 포피스 업로드, 포피스 수정, _board.json 생성.
---

# Poffice-Skill — 세션로그 기록 + 포피스 데이터 생성 (코어)

> "서류를 쓰는 게 아니라 대화가 서류가 된다." 대화 → 세션로그 → 분류 → `_board.json`.
> **데이터 생성·기록만.** 시각화는 포피스 대시보드(`tool/PIMM_Poffice.ver0.2.html`),
> 알림·브리핑은 `Poffice-Report-Bot`. 정본 스키마·계층: `docs/poffice-board-spec.md`(A~H).

## 1. 데이터 계층 (개인세션로그 폴더 · spec §2/C)
```
개인DB/{이름}/Session_세션로그/
├─ MISSION_보드.md · GATE_현황.md · TODO_현황.md   (롤업, 현재 상태)
├─ workorder/{YYMMDD_HHMM}_{요약}_wo.md            (대표 지시 WO)
├─ logs/YYYY/MM/{YYMMDD_HHMM}_{요약}_log.md         (세션로그 원본, append-only·불변)
├─ memo/session/{로그ID}.md · memo/mission/{미션ID}.md  (사람이 다는 유일한 mutable)
├─ _board.json                                     (마더 세션로그 = 대시보드 정본)
└─ _export/poffice_export_{이름}.json              (허브→코워크 역방향)
```

## 2. 세션로그 기록 규칙 (대화 → 로그)
- 파일명 **`{YYMMDD_HHMM}_{요약}_log.md`** — **시간(HHMM)까지** 반드시 포함(날짜만 금지).
- 게이트 표기: `- [대기|진행|완료] {YYMMDD_HHMM} | 내용 | 근거로그`
- 투두 표기: `[ ]`(todo) / `[~]`(doing) / `[x]`(done), 대표 지시는 **`[WO]`** 태그.
- 세션로그 원본은 **불변(append-only)**. 분류(게이트/투두/미션)는 롤업 문서로 파생.

## 3. 게이트 = 권한 신호등 (위험 아님 · spec A)
- 🔴 **레드**: 대표(심상윤) 검수·승인 후 진행.
- 🟡 **옐로**: 팀장 판단 진행. `yellow_policy:"report"`(이정민·신승희)는 **팀원 보고 필수**, `"auto"`(오세원·유지호)는 자율.
- 🟢 **그린**: 자율 진행(기록만).

## 4. _board.json 생성 (마더 세션로그 · spec 스키마 + G)
개인세션로그·개인DB를 취합해 대시보드 스키마로 **결정론 변환**. **최근 윈도우 + 롤업만**(전체 히스토리 X):
- `members[]`: `name/role/yellow_policy/master`, `missions[]`(status·due·progress·roadmap = 마일스톤), `gates{red,yellow,green}`, `todos[]`(state·wo·mission·importance·date), **`sessions[]`**(최근 세션로그 `{ts,summary,detail}` — 오래된 건 파일로), `last_session`.
- 심상윤 = `master:true`(마스터보드 최상단).
- 대표 주간보고 판단을 반영해 게이트(🔴/🟡/🟢)·WO 세팅.
- 갱신 시마다 **동일 파일명 `_board.json`** 덮어쓰기(modifiedTime 최신본 = 정본).

## 5. 역방향 반영 (export → 세션로그) · spec §C
- 대시보드가 내보낸 `poffice_export_{이름}.json`(`check_overrides` + `memo_overrides`)을 읽어
  해당 투두 체크상태·메모(mission|·session| 키)를 세션로그/롤업에 반영.
- **데이터 꼬임 방지: 포피스에서 온 것은 '체크·메모'만** 반영(그 외 역방향 쓰기 없음).

## 6. 자동예약
- CronCreate 등으로 **주기적 `_board.json` 갱신**(예: 주 1회 또는 세션로그 갱신 시).
- 활성화·주기는 대표/개인 지시로 설정.

## 7. 다른 구성요소와의 관계
- **Poffice-Report-Bot**: 이 스킬이 만든 마더 세션로그(`_board.json`/업데이트 로그)를 직전 버전과 diff해 페르소나 브리핑. (합치지 않음 — 토큰 절약)
- **대시보드**: `_board.json` 로드·시각화(읽기전용 + 체크·메모).

## 8. 경계
- 세션로그 **원본 수정 금지**(불변). 롤업·`_board.json`만 갱신.
- 개인별 데이터 격리(타인 것 혼입 금지).
