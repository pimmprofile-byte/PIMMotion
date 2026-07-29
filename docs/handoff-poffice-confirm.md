# 코워크 핸드오프 — 포피스 결재 반영(`Poffice_confirm` → 보드 게이트)

_발신: coworking-review 세션(대시보드 담당) → 수신: 코워크(마더로그·Drive 담당) · 2026-07-29_

## 목적
결재자(레드=대표 심상윤 / 옐로=오세원·유지호)가 대시보드에서 내린 결재(승인·반려·보류 + 메모)를,
**대상 인물의 세션로그 하위 `Poffice_confirm/` 폴더**로 전달 → 코워크가 **보드 게이트에 반영**한다.
반영되면 대시보드가 그 게이트를 "결재됨(decision 배지 + 메모)"으로 표시하고, 완료 건은 인박스에서 빠진다(루프 종료).

## 전체 흐름 (사용자 확정)
```
[대시보드]  결재자가 인박스에서 승인/반려/보류 + 메모 → '인물별 내보내기'
   → poffice_confirm_<대상>.json  (아래 스키마)
        ↓  결재자가 각 대상 인물의  <세션로그>/Poffice_confirm/  폴더에 직접 드롭
[코워크]  Poffice_confirm/ 인입 → confirm_id로 보드 게이트 매칭 → decision·reply 병합 + 상태 반영
        ↓
[대시보드]  다음 보드 로드 시 게이트가 decision 배지+메모로 표시, 완료 건은 인박스에서 제외
```
- **전달 방식**: 결재자가 Drive 데스크톱 마운트로 **각 인물 `Poffice_confirm/` 에 직접 드롭**(사용자 확정).
- **반영 시점(둘 다)**: ① 전용 트리거 **"결재 반영해줘"** 즉시 처리, ② **일일 마더로그 run**에도 항상 스캔.

## 대시보드가 내보내는 파일 (입력 스키마)
파일명 `poffice_confirm_<대상>.json`, 대상 인물의 `Poffice_confirm/` 에 드롭됨.
```json
{
  "type": "poffice_confirm",
  "approver": "오세원",
  "target": "신승희",
  "gate_kind": "yellow",                // red | yellow
  "generated_from": "2026-07-25T15:40:00+09:00",
  "record_to": "[2.포피스_섹터].Poffice/신승희/세션로그/Poffice_confirm/",
  "confirms": [
    {
      "confirm_id": "yellow|신승희|260725_0930",   // = gate_kind|대상|gate_ts (게이트 유일키)
      "gate_kind": "yellow",
      "gate_ts": "260725_0930",
      "item": "시나리오 방향 보고",
      "prev_state": "대기",
      "log": "260725_0930_log.md",
      "decision": "승인",                 // 승인 | 반려 | 보류
      "reply": "방향 A 승인, 예산 내",     // 메모(선택)
      "decided_by": "오세원"
    }
  ]
}
```

## 코워크가 할 일 (반영 규칙)
매 처리(트리거 or 일일 run)마다, 각 인물 `Poffice_confirm/*.json` 을 스캔해 다음을 수행한다.

1. **게이트 매칭** — `confirm_id`(=`gate_kind|대상|gate_ts`)로 보드의 해당 인물 `gates[gate_kind]` 항목을 특정.
   매칭 실패(해당 게이트 없음)면 그 confirm은 건너뛰고 로그에 남긴다(오작동 방지).
2. **필드 병합** — 매칭된 게이트 항목에 기록:
   - `decision`(승인/반려/보류), `reply`(메모), `decided_by`, `decided_at`(=반영 시각, KST 분단위 코워크가 부여).
3. **상태 반영(state)**:
   - `승인` → `state = "완료"`
   - `반려` → `state = "완료"` + `outcome:"반려"`(대시보드는 반려도 완료로 간주해 인박스에서 제외; 배지로 반려 표시)
   - `보류` → `state` 유지(대기/진행), `decision:"보류"`만 기록(인박스에 계속 노출)
4. **세션로그 반영** — 대상 인물의 세션로그(또는 롤업)에 "결재됨: <decision> — <decided_by> (<reply>)" 한 줄 추가.
   (각 개인이 자신의 세션로그에서 확인·기록하는 사용자 의도 충족.)
5. **미러 갱신** — 보드 정본 갱신 후 런처 폴더 `poffice_board.json` + `poffice_board.js` 도 함께 제자리 덮어쓰기(기존 §미러 규칙 그대로).

## 절대 규칙
1. **제자리·중복금지·하드삭제금지** — confirm 처리/보드 갱신 모두 `open(path,"w")` 제자리 덮어쓰기(inode 보존). 처리 완료된 confirm 파일은 **제로필드로 이동**(재처리 방지), 하드삭제 금지.
2. **멱등(idempotent)** — 같은 `confirm_id`가 이미 그 decision으로 반영돼 있으면 **재적용 없이 스킵**. 트리거+일일 중복 실행에도 안전해야 함.
3. **최신 우선** — 같은 confirm_id로 결재가 바뀌면(예: 보류→승인) **가장 최근 파일의 decision이 우선**. (파일에 generated_from/드롭시각 활용.)
4. **텍스트 무손상** — UTF-8·한글·이모지·JSON 이스케이프 정확. 생성 후 파싱 검증.
5. **권한 경계** — 레드 confirm은 `approver=="심상윤"(master)` 만, 옐로 confirm은 `approver`가 `yellow_approver`(오세원·유지호)인 경우만 반영. 그 외 approver의 confirm은 무시+로그.

## 대시보드 쪽(이미 반영 · v0.14)
- 인박스 각 건: **승인/반려/보류 셀렉터 + 메모** → `poffice_confirm_<대상>.json` 내보내기(위 스키마).
- 보드 게이트 항목에 `decision`(+`reply`/`decided_by`)이 있으면 **decision 배지 + 결재 메모** 표시. (반영 결과 읽기.)
- 스키마 정본: `docs/poffice-board-spec.md` (gate 항목에 `decision`·`reply`·`decided_by`·`decided_at`·`outcome` 추가).

## 참고
- 대시보드: `tool/PIMM_Poffice.ver0.14.html`
- 미러/저장 규칙: `docs/handoff-poffice-js-mirror.md`
- 스키마: `docs/poffice-board-spec.md`
