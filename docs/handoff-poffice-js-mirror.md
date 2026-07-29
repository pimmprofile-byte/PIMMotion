# 코워크 핸드오프 — 포피스 마더로그: `poffice_board.js` 미러 추가 + 원문 축약 금지

_발신: coworking-review 세션(대시보드/스킬 담당) → 수신: 코워크(마더로그 실행 담당) · 2026-07-26_

## 왜 (배경)
- 팀원은 대시보드 HTML을 **더블클릭(`file://`)** 으로 여는 경우가 많다. 이때 브라우저는 `fetch("poffice_board.json")`를 **보안상 차단** → 같은 폴더에 파일이 있어도 자동 로드가 안 되고 "갱신 실패"가 뜬다.
- 단, 브라우저는 **`<script src>` 태그 로딩은 막지 않는다.** 그래서 데이터를 `.js`(전역 대입)로도 주면 **더블클릭만으로 자동 로드**된다.
- 대시보드는 **v0.7**에서 로드 순서를 `poffice_board.js`(script) → `poffice_board.json`(fetch) → 내장 SAMPLE 로 바꿨다. 검증 완료(파일:// 더블클릭에서 `.js` 자동 로드 확인).

## 코워크가 바뀌어야 할 것 (마더로그 미러 단계)
매 run, 정본 생성 직후 **런처 폴더에 `.json`과 `.js` 두 파일을 함께** 덮어쓴다.

- **런처 폴더**: `PIMM_Launcher` (id `1pC9V2ZKO5rWrIDXc0mRAsHRgDEL9iqkX`) — 대시보드/허브 HTML이 있는 곳.
- **포피스영역(정본)**: `[2.포피스_섹터].Poffice` (id `1dbUhEa2ByRtLhKryM4YpYHC4bNLzBdFm`) — 여기엔 `.json` 정본만 유지.

### 파일 3개 (매 run 덮어쓰기)
| 위치 | 파일 | 내용 | 규칙 |
|---|---|---|---|
| 포피스영역 | `poffice_board.json` | 정본 JSON | 제자리 덮어쓰기(in-place), 단일 |
| 런처 폴더 | `poffice_board.json` | 정본과 동일 JSON (미러) | 제자리 덮어쓰기(in-place), 단일 |
| 런처 폴더 | `poffice_board.js` | `window.POFFICE_BOARD = <그 JSON 그대로>;` | 제자리 덮어쓰기(in-place), 단일 |

### `poffice_board.js` 생성 방법
- 내용은 **딱 한 줄 전역 대입**:
  ```js
  window.POFFICE_BOARD = { ...poffice_board.json 의 내용 100% 동일... };
  ```
- `create_file` 시: `contentMimeType` = `application/javascript`(또는 `text/javascript`), `disableConversionToGoogleType` = `true` (구글독 변환 금지, `.js` 확장자 유지).
- `.js` 안의 JSON은 `.json`과 **글자 하나까지 동일**해야 한다(같은 소스에서 문자열로 만들어 앞에 `window.POFFICE_BOARD = `, 뒤에 `;`만 붙임).

## 절대 규칙 (반드시 준수)
1. **중복 금지 · 제자리 수정(in-place overwrite).** 커넥터에 update 도구가 없으므로 `.json`/`.js` 모두 **같은 경로를 `open(path,"w")`로 덮어써 inode/fileId 보존**(Drive 데스크톱 마운트가 새 리비전으로 처리). create 반복 금지 → 안 그러면 `poffice_board (1).json`·`(2)`… 처럼 복제되고, 접미사 없는 정본은 옛 파일이 되어 대시보드가 **옛 데이터를 읽는 버그**가 난다. 하드삭제 금지(폐기물=제로필드 이동).
2. **★ 원문 축약 금지 (이번 핸드오프 핵심).** `sessions[].raw`는 **개인 세션로그 원본 전문을 그대로** 담는다. 요약·축약·재작성·의역 금지. `summary`는 1줄 헤드라인만 별도. `.js`/`.json` 미러도 **내용 변형 없이** 같은 JSON을 옮긴다. (요약된 board는 실제 업무 파악이 안 된다는 실사용 피드백 반영.)
3. **텍스트 무손상.** UTF-8·한글·이모지(🔴🟡🟢) 안 깨지게, JSON 이스케이프 정확. 생성 후 JSON 파싱 검증. (LLM이 긴 원문을 base64로 나르면 손상되므로, 커넥터의 안정적 읽기/쓰기 경로를 쓸 것.)
4. **윈도우 = 실행 주기와 무관.** 최근 14일 + 인물별 최소 5건(14일 넘겨도 포함) + raw 예산 200KB/인. 주기 기반 슬라이딩(13h 등) 안 씀 — 봇이 하루 죽어도 다음 회차가 덮음. 롤업(게이트·투두·미션)은 상시 유지. (정본 = poffice-motherlog SKILL §3.)

## 실행 후 검증
- 런처 폴더에 `poffice_board.json`(1개) + `poffice_board.js`(1개)만 있고 `(1)(2)(3)` 없음.
- `.js`를 `window.POFFICE_BOARD =` 떼고 파싱했을 때 `.json`과 완전히 동일.
- 대시보드를 **더블클릭**해서 실데이터가 뜨는지(샘플 아님) 확인.

## 참고 (정본 문서)
- 스킬: `.claude/skills/poffice-motherlog/SKILL.md` (§1 저장·미러·`.js`, §3 14일 윈도우)
- 스키마: `docs/poffice-board-spec.md`
- 대시보드: `tool/PIMM_Poffice.ver0.15.html` (로드 순서 `.js`→`.json`→SAMPLE)
