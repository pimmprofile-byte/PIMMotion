# 코워크 핸드오프 — 포피스 워크오더(WO) 발신 + 인물별 통합 export(`poffice_person`)

_발신: coworking-review 세션(대시보드 담당) → 수신: 코워크(마더로그·Drive 담당) · 2026-07-30_

## 목적
대표(또는 지시권자)가 대시보드에서 **워크오더(WO)를 발신**하고, 기존 **게이트 결재**와 **한 파일로 통합**해 대상 인물별로 내보낸다. 코워크는 그 파일을 받아 각 인물의 보드에 반영한다.
추가로, **대표 본인이 스스로 처리해야 하는 레드게이트**는 마더로그가 **WO로도 편입**한다(아래 §3).

## 대시보드가 내보내는 파일 (입력 스키마) — `poffice_person_<대상>.json`
v0.16부터 결재(confirms)와 워크오더(work_orders)를 **한 파일**로 통합(구 `poffice_confirm_*` 대체).
대상 인물의 세션로그 하위 **`Poffice_confirm/`** 폴더에 드롭됨.
```json
{
  "type": "poffice_person",
  "target": "오세원",
  "from": "심상윤",
  "generated_from": "2026-07-25T15:40:00+09:00",
  "record_to": "[2.포피스_섹터].Poffice/오세원/세션로그/Poffice_confirm/",
  "confirms": [
    { "confirm_id": "red|오세원|260725_1530", "gate_kind": "red", "gate_ts": "260725_1530",
      "item": "...", "decision": "승인", "reply": "...", "decided_by": "심상윤" }
  ],
  "work_orders": [
    { "text": "마지막 실험실 포스터 서브컷", "importance": "high", "mission": "A1",
      "issued_by": "심상윤", "wo": true, "state": "todo" }
  ]
}
```
- `confirms`: **기존 결재 반영** 규칙 그대로(§handoff-poffice-confirm.md) — confirm_id로 게이트에 decision·reply 병합 + 상태 반영.
- `work_orders`: **신규** — 대상 인물 `todos`에 **wo:true 항목으로 추가**.

## 코워크가 할 일 — work_orders 반영
각 `work_orders[]` 항목을 **`target` 인물의 `todos[]`에 추가**한다.
```json
{ "text": "...", "state": "todo", "wo": true,
  "issued_by": "심상윤", "importance": "high", "mission": "A1",
  "date": "<반영시각 YYMMDD>" }         // date/타임스탬프는 반영 시각을 코워크가 부여
```
- **중복 방지(멱등):** 같은 `(target, text, issued_by)` WO가 이미 미완료로 있으면 **재추가하지 않음**. (트리거+일일 중복 실행 안전)
- `wo:true` 라 대시보드에서 대상 인물 상단 **WO 배너**에 뜨고, 발신자 화면 **발신 WO 현황**에도 집계된다.
- 완료 처리(state=done)는 기존 세션로그/체크 반영 흐름을 따른다.

## §3. 대표 레드게이트 → WO 편입 (마더로그 신규 작업)
대표(`master:true`, 심상윤)가 **스스로 결정해야 하는 레드게이트**(자기 자신에게 온 red gate)는,
보드 생성 시 마더로그가 **동일 내용을 대표의 `todos`에 wo:true(자기지시)로도 넣는다.**
- 목적: 대표의 '해야 할 결정'이 게이트보드뿐 아니라 **할 일/발신 WO 목록에도** 보이게(누락 방지).
- 예: red gate `{item:"M3 텀블벅 포함 여부 결정"}` → 심상윤 todos에 `{text:"M3 텀블벅 포함 여부 결정", wo:true, issued_by:"심상윤", target=심상윤(=본인)}` 추가.
- **멱등·중복 방지**: 같은 게이트에서 파생된 WO는 1개만. 게이트가 완료(결재됨)되면 파생 WO도 done 처리.
- (대시보드의 발신 WO 현황은 `대상≠나`만 보여주므로, 본인 자기지시 WO는 발신 현황엔 안 뜨고 본인 '할 일'에만 뜬다.)

## 신규 스키마 필드 (board / poffice-board-spec)
- `member.wo_issuer: true` — 이 인물이 WO를 발신할 수 있음(대시보드 발신 WO 영역 노출). `master`는 자동 발신권자.
- `todo.issued_by: "심상윤"` — 이 WO(wo:true)를 지시한 사람. 없으면 대표(master) 발신으로 간주.

## 절대 규칙
1. **제자리·중복금지·하드삭제금지** — 보드/미러 갱신은 `open(path,"w")` 제자리 덮어쓰기. 처리된 파일은 제로필드 이동.
2. **멱등** — confirms(confirm_id)·work_orders(target+text+issued_by)·파생WO(게이트 출처) 모두 재적용 방지.
3. **텍스트 무손상** — UTF-8·한글·이모지·JSON 이스케이프 정확. 생성 후 파싱 검증.
4. **권한 경계** — red confirms는 `from==master`만, yellow confirms는 `from`이 `yellow_approver`인 경우만. work_orders는 `issued_by`가 발신권자(master/wo_issuer)인 경우만 반영.
5. **미러** — 갱신 후 런처 폴더 `poffice_board.json`+`poffice_board.js` 제자리 덮어쓰기(§handoff-poffice-js-mirror).

## 반영 시점 (기존과 동일)
- 전용 트리거 **"결재 반영해줘"/"워크오더 반영해줘"** 즉시 + 일일 마더로그 배치. 둘 다 멱등.

## 참고
- 대시보드: `tool/PIMM_Poffice.ver0.16.html` (발신 WO 영역 + exportPerson 통합 export)
- 결재 반영 규칙: `docs/handoff-poffice-confirm.md` (confirms 처리 — 이 문서가 파일명만 `poffice_person`으로 통합)
- 스키마: `docs/poffice-board-spec.md`
