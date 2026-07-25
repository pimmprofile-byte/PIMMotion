# 포피스 대시보드 — poffice_board.json 스키마 (확정본 v1)

> 핸드오프 회신: 코드 세션 → 코워크. `tool/PIMM_Poffice.ver0.1.html` 이 이 스키마를 로드한다.
> 원칙: **코어(엔진) + 데이터(JSON) 분리. 읽기 전용.** 유일한 로컬 인터랙션은 투두 '체크'뿐이며,
> 그 결과는 `poffice_check_export.json` 으로만 내보내 코워크가 세션로그에 반영한다(역방향 쓰기 없음).

## 데이터 흐름 (단방향 + 체크 예외)
```
코워크: 세션로그 집계 → poffice_board.json 생성/갱신(동일 파일명, modifiedTime 최신본=정본)
   → 대시보드가 파일선택/드래그앤드롭으로 로드 (서버 불필요)
대시보드: 투두 '체크'만 로컬 변경 → [체크상태 내보내기] → poffice_check_export.json
   → 코워크가 읽어 세션로그에 반영 (데이터 꼬임 방지: 포피스는 '체크'만 다룸)
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
      "yellow_policy": "auto",          // auto(자율진행) | report(필수보고) — 게이트 🟡 표시 구분
      "master": true,                   // [조정1] 회사 마스터보드 → 항상 최상단 고정. 심상윤만 true
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
    }
    // × 5인 (심상윤·이정민·유지호·오세원·신승희)
  ],
  "docs": [ { "no": "MTG-20260725_포피스자동화", "type": "회의록",
              "source": "260725_1530_..._log.md" } ]
}
```

### 조정 3건 (확정 요청)
1. **`member.master: true`** — 심상윤 보드를 미션보드 최상단에 고정하기 위한 플래그.
2. **`todo.importance` (high|mid|low) + `todo.date` (YYMMDD)** — 요구된 *중요도별/일자별 정렬*의 근거 필드. WO(`wo:true`)는 정렬과 무관하게 항상 최상단.
3. **게이미피케이션은 데이터에서 파생(derive)** — 별도 스키마 불필요. 대시보드가 `todos` 중 `state==="done"` 수를 세어 **처리량·칭호(신입→숙련→베테랑→게이트마스터)·진행률·뱃지**를 자동 계산한다. 추후 수동 지정이 필요하면 `member.title` 오버라이드 필드를 옵션으로 추가 가능(현재는 미사용).

## 체크상태 내보내기 포맷 (`poffice_check_export.json`)
```jsonc
{
  "generated_from": "2026-07-25T16:00:00+09:00",   // 원본 board.json의 generated_at
  "check_overrides": {
    "심상윤": { "0": "done", "2": "doing" },        // todos 인덱스 → 변경된 상태
    "이정민": { "1": "done" }
  }
}
```
코워크는 이 오버라이드를 읽어 해당 팀원 세션로그의 투두 상태에 반영한다. (인덱스는 board.json의 `members[].todos` 배열 순서 기준)

## 대시보드 3판 (구현 완료 — v0.1)
1. **미션보드** — 인별 마일스톤 카드(상태 pill·D-day·진행률·역산 로드맵). 심상윤 마스터보드 최상단.
2. **게이트보드** — 🔴 보고처리 / 🟡 자체결재(yellow_policy로 자율·필수보고 표시) / 🟢 기록만. 항목별 상태·타임스탬프·근거로그.
3. **투두리스트** — 인별 체크박스(3상태 순환 todo→doing→done), WO 태그·상단고정, 미션 id·중요도·일자 태그, 중요도/일자 정렬.

＋ **WO 배너**(대표 지시 필수확인, 최상단 고정) · **게이미피케이션 스트립**(처리량·칭호·진행률·뱃지).
