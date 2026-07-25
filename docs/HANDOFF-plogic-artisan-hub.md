# 핸드오프 — 플로직 교육툴 · 아티잔 인재체계 · 포피스 업무체계 · 핌허브 연결 (세션 이동용)

> 작성 2026-07-25 · 브랜치 `claude/pimmartworks-homepage-renewal-9mhvqe` · 레포 `pimmprofile-byte/PIMMotion`
> 대상: 핌아트웍스(PIMM Artworks) 이머시브 콘텐츠(방탈출·팝업·전시·공포체험). 대표=심상윤(Master PD).
> 원칙: **원문 무왜곡**(플로직 정본 대조), 단일 자체완결형 HTML(외부 의존 0), 데이터 주도 렌더.

---

## 0. 이번 세션 결과물 한눈에

| 산출물 | 경로 | 상태 |
|---|---|---|
| **플로직 교육툴** | `tool/PIMM_Plogic.ver0.1.html` (~91KB) | 완성·커밋·푸시. Artifact 발행됨 |
| **핌허브** | `tool/PIMMotion_Hub.ver0.6.html` (~338KB) | ver0.5→0.6, Plogic·Poffice LIVE 연결 |
| **포피스 대시보드** | `tool/PIMM_Poffice.ver0.2.html` (~30KB) | (앞 세션 산출) 허브에 연결됨 · 상세 §2-B |
| 핸드오프(본 문서) | `docs/HANDOFF-plogic-artisan-hub.md` | — |

- **Artifact(웹 미리보기, 플로직)**: https://claude.ai/code/artifact/45a50729-1a63-4734-9477-a486a5b35b89
- **GitHub tool/ 폴더**: https://github.com/pimmprofile-byte/PIMMotion/tree/claude/pimmartworks-homepage-renewal-9mhvqe/tool
- 최신 커밋: 플로직·허브 관련 다수 (본 문서 커밋이 최신).

---

## 1. 플로직 교육툴 (`tool/PIMM_Plogic.ver0.1.html`) — 핵심 산출물

핌허브 Plogic 탭용 **신입→마스터 교육 도구.** Day 마스코트 가이드 · 퍼즐/퀴즈 · 진도 localStorage 저장 · 라이트/다크 자동 · 반응형(375/320 검증). 콘텐츠 추출 에이전트가 플로직 그린필드 정본을 읽어온 다이제스트를 기준으로 **원문 무왜곡**으로 작성.

### 1-1. 상단 탭(모드) 5개
`이해하기(learn) · 풀어보기(solve) · 심화과정(deep) · 아티잔(artisan) · 작업체계(system)` + `home`. 데이터 주도(`MODULES/CHALLENGES/DEEP_CRAFT/DOMAINS/LEVELS/FORGES` 배열 수정으로 콘텐츠 갱신).

### 1-2. 「이해하기」 — 6개 모듈 (개괄, 볼륨 유지 요청)
각 레슨에 `p/list/pipeline` + `plain`(쉽게 말하면·주황) + `ex`(실제 사례·파랑) 콜아웃. 모듈 끝 인라인 퀴즈(mc/order).
- **M0 오리엔테이션**: 이머시브 / PIMM이 만드는 것 / **PPP → IMM = Plot·Place·Persona → Immersive** / 재미 = "의도된 인과관계의 보상" / 플로직 정의(PIMM+Logic, '왜/무엇을' 정의, '어떻게/얼마로'는 파트웍·포피스)
- **M1 지도**: Tier(**프로젝트 티어** T1/T2/T3 vs **서류 티어** 테마비트 등 접미사) · Track(아래) · 티어판정 5축 · **용어사전**(아다리/스라/와리/데나오시/가쇼/뚝/장치/수율/PlaceNarrative)
- **M2 파이프라인**: **Beat(영감)→Note(논리골조·기술헌법필터)→Render(소프트워크·SW설계)→Work(하드워크·현장시공)→Max(사후공정·자산화: 스케치필름·마케팅·재계약·아카이브)**
- **M3 크래프트 이론**: 8-Cell 감정역학 / 환경적 스토리텔링 4계층 / **Flow=Density×(1/Friction)** / **어포던스=Mechanical Instinct=Physical Volume×Auditory Feedback** / P-Logline / 피크-엔드 / 엔딩 3단계 / MDA·장면연출
- **M4 실전**: 기술적 헌법(안정성>창의성, 센서 화이트리스트=마그네틱·RFID·물리버튼 / 블랙리스트=적외선·무게·진동·조도, 유선이 진리 Arduino Mega 2560, **500-500-200** 점검구) · 트랙별 적용 · 제안서 4타입(A비주얼/B인터랙션/C비즈니스/D공간, CI #262626+#00FF99)
- **M5 마스터 판단로직**: 채산성(**총견적≈콘크리트×2**, 콘크리트 최소화·진행비가 마진, 절대 마진액) / 운영(실패 뿌리=설계·기획 시스템 부재) / 법무(**잔금=체험완료**, 외부공사 배제) / 파트너십(외주 ~10배, 자체기술 우위) / 아티잔 마인드셋

### 1-3. 트랙 분류 (중요 정정 — 대표 확정)
기본 **2트랙**:
- **PIMMersive 트랙(상설·몰입)** = **PIMMscape**(방탈출, 인터랙션 위주) + **PIMMex**(체험형 콘텐츠 **상설매장**, 인터랙션 아닌 **연출체험 위주** — 공포체험관은 한 예시)
- **PIMMup 트랙(팝업·단기)** = **PIMMercial**(B2C) + **PIMMvention**(B2G)
- 스케이프·엑스·머셜·벤션은 세부 이름. 서류 표기 `PIMMup`(구 PIMM-UP).

### 1-4. 「풀어보기」
recall(기존내용) + create(심화·창작) 문항 → `exportAnswers()`가 `{tool:"PIMM-Plogic",mode:"풀어보기",learner,answers[]}` JSON 내보냄 → **코워크(Claude)가 채점.**

### 1-5. 「심화과정」 (딥다이브)
크래프트 이론을 이론별로 깊게. **서사구조 완성**(8-Cell 표·환경적 스토리텔링 4계층·피크엔드·엔딩3단계·자가점검 체크리스트). **공간구성·게임퍼즐·장면연출·장르컨셉·운영설계 = 잠금(🔒 "원문 정독 후 공개")** — 아직 원문 미정독(무왜곡).

### 1-6. 「핌 아티잔」 — 회사 인재가치 체계 (가장 많이 반복 수정됨)
개요는 **설명체(문서 목소리)**, Day 말풍선은 친근체(역할 분리 — 이질감 수정 완료).

**영역 분리(색상 밴드 헤더):**
- **영역 A · 도메인(실무)** — "무엇을 얼마나 잘하나(밸류)"
- **영역 B · 리더십** — "어떻게 사람과 팀을 이끄나"

**6개 핵심 도메인** (대표 확정, 한줄요약+상세설명, 유형 색분류):
1. **현장제작과 시공** (하드워크·purple) — 공구·공정 이해, 오프라인 공간에 테마 시공
2. **장치디바이스** (하드워크·purple) — 센서·아두이노·회로·코딩, 인터랙티브 장치
3. **설계와 디자인** (소프트워크·blue) — CAD·스케치업·그래픽·미디어, 도면·비주얼 확정
4. **미학적 감각** (미학·예술·green) — 취향을 상업 완성도로. **심미안은 평가불가 → 미술작업·특수제작물(인터랙션 장치·조형 제작물)로 미감 확인·발현**
5. **서사창작** (미학·예술·green) — 세계관·이야기 → 공간서사(PlaceNarrative)·콘텐츠
6. **사업적 감각** (시장·사업성·amber) — 시장·트렌드 판단, 팀을 흐름에. **판단기준: 시스템 설계나 사업적 판단이 실제 유의미한 지표 상승으로 증명될 때 역량 인정**

**두 갈래 축**: 기술·작업물(1·2·3, 배우면 늘·익히기 쉬움) / 감각(4·5·6, 깨닫고 타고남).

**도메인 성숙도 — 5계층 (per-domain, 사다리 UI, 역할 강조):**
1. 주니어(입문자) 2. 플로어(초급자) 3. **리더(중급자, ★전문가 시작, 역할=교육+수행/코칭 아님, 프로젝트 '안' 실무 리딩)** 4. **시니어(상급자, 역할=코칭+핸들링/교육·수행 아님, 프로젝트 '위' 리스크·표준·자원)** 5. **마스터(정점, 역할=체계 진화·밸류체크·실무X 오로지 시스템+밸류)**. 전문가=리더(중급)부터.

**도달 지점 — 4단계 (PD 직함 체계 · 실무 영역, aggregate):** 내부명은 PD 없이, 괄호=대외 직함.
1. **아티잔** (대외직함 **PD**) — 2개 이상 도메인 전문가(리더+)
2. **제너럴리스트** (대외직함 **General PD**) — 전 도메인 리더 (6각형 완성 → 밸류 정점·월급 도약·다음 자격 개방)
3. **디렉터** (대외직함 **Director**) — 전 도메인 리더 + 1개 이상 마스터 도메인 + 결과물 입증
4. **마스터** (대외직함 **EP=이그제큐티브 프로듀서**) — **전 영역 마스터 '졸업'.** 사업 총괄 역량, **반복 실무·현장 제작엔 직접 안 들어감**(마스터만 가능한 신기술·신도메인 개척은 예외), 관리감독·사업총괄 집중
> ⚠️ 이력: 한때 EP를 별도 5번째 등급으로, 마스터를 치프로 바꾼 6계층안이 있었으나 **대표가 롤백** → "5계층 유지, 최상위=마스터, EP는 마스터PD/마스터의 대외직함" → 최종적으로 위 4단계 도달지점.

**PD와 PM 두 역할**: PD=프로듀서(작업물 산출, 자기 프로젝트 내 실무판단 최고권한) / PM=프로젝트 매니저(운영·관리, 제작 압박 적어 원칙상 **사업적 감각(도메인6) 리더급**이 맡음. 사업감각 리더=팀원 매니지먼트·일정·시스템 디벨롭해 실제로 돌아가게). **실무 통례: 사업감각 리더 증빙 까다로워 2개+ 도메인 리더인 멀티도메인 PD가 PM 겸함.**

**평가·훈련·보상**: 평가 3요소=**STP테스트+작업물+시장반응** → 성과 → **월급 등 유형가치 직결**. STP=6도메인을 얽고 의도 숨긴 질문(코워크가 매번 새로 생성). MPA=**M-T-B**(Middle→Top→Bottom Point) 새 도메인 내재화 훈련.

**리더십 영역(영역 B, 팀스피릿 원문 무왜곡):**
- 근본 감각 **본질을 보는 눈**(말하지 못한 것 포착. 사례: 공포테마 "더 무섭게"의 진짜 뜻=재미)
- **인재·리더 5자질**(표): 본질 감각 / 멀티도메인 잠재력 / Dirty Prototype 체질 / 가치 중심 사고 / 논리적 솔직함
- **팀 6원칙**: ①논리>위계 ②감정 브레이크는 논리적으로 ③'천재' 단어 금지 ④가치 증명 못하면 무효 ⑤수직·수평 사이 유기체 ⑥최소 2개 전문 도메인

### 1-7. 「작업체계」
핌허브 4개 Forge 설명: **플로직**(이론·학습) / **포피스**(업무보고·운영) / **피모션**(소프트워크 실전툴) / **파트웍**(하드워크 트래커). 두 축(이론↔실무 / 소프트워크↔하드워크) + "코워크가 상급자·동료" 목표.

### 1-8. 수정한 버그(전부 검증 완료)
- **랜딩 글자 검정**: `<button>`이 색 미상속 → 다크모드에서 `.choose h3` 등 검정. **`button{color:inherit}`** 로 수정.
- 모바일 가로 넘침: `.mnav/.mod min-width:0`, body `overflow-wrap:break-word`.
- 심화 8-Cell 표 잘림: `@media(max-width:560px) .dtable{min-width:0…}`.
- 검증: `node --check` + Playwright 렌더(라이트/다크·375·320) 반복.

---

## 2. 핌허브 연결 (`tool/PIMMotion_Hub.ver0.6.html`)

- ver0.5 → **ver0.6** 복사 후 수정(브랜딩 PIMMotion 유지 — 리브랜딩은 미룸).
- 데이터 주도: `SECTORS` 배열에서 각 섹터 `status:'live' + launch:'./파일.html'` 주면 카드 클릭 시 `window.open` 런치.
- **Plogic** 섹터: `status:'live', launch:'./PIMM_Plogic.ver0.1.html'`
- **Poffice** 섹터: `status:'live', launch:'./PIMM_Poffice.ver0.2.html'`
- **Partwork**: 도구 없어 `wip` 유지. **PIMMotion**: 기존 LIVE(에디터 허브).
- ⚠️ 런치는 **상대경로**라 허브+툴 HTML을 **같은 폴더에 함께** 둬야 작동.

---

## 2-B. 포피스 업무 대시보드 체계 (`tool/PIMM_Poffice.ver0.2.html` + 스킬 3종) — 별도 핸드오프

핌코프 **업무보고·운영 포지**(핌허브 Poffice 탭). "서류를 쓰는 게 아니라 **대화가 서류가 된다**" — 코워크/코드 대화가 자동으로 개인세션로그가 되고, 집계돼 대시보드로 시각화된다. **읽기 전용 + 체크·메모만 로컬 인터랙션**(역방향 쓰기 최소화, 데이터 꼬임 방지). 정본 스펙: `docs/poffice-board-spec.md`(A~H), 사용 시나리오: `docs/poffice-usage-by-member.md`.

### 2B-1. 전체 데이터 흐름 (단방향 + 체크/메모 예외)
```
① Poffice-Skill(기록)  : 대화 → 개인세션로그 자동기록(게이트·체크·미션 분류, 불변 append-only)
② Poffice-MotherLog(집계): 개인세션로그 요약·분석 → poffice_board.json(마더 config) 생성/갱신
③ 대시보드(시각화)      : 인물 선택 → 본인 워크스페이스 로드(fetch 또는 드래그앤드롭)
④ export(역방향)        : 투두 체크 + 메모 → poffice_export_{이름}.json → ①이 세션로그에 반영
⑤ Poffice-Report-Bot(알림): 마더 config를 직전 버전과 diff → 개인 페르소나 말투 브리핑(예약)
```
세션로그 원본은 **불변**, 역방향으로 쓰는 건 **체크·메모뿐.**

### 2B-2. 대시보드 3판 + 부가 (v0.2 구현 완료)
1. **미션보드** — 인별 마일스톤 카드. `progress`(0~1)로 **Day char 스프라이트가 경로 위 전진**(게임식), 상태 pill(예정/진행/달성/보류)·D-day·역산 로드맵. (심상윤 `master:true` 최상단 고정은 데이터 플래그만 존재, 대시보드 ver0.2 미구현·ver0.3 예정.) 미션마다 메모 슬롯.
2. **게이트보드 = 권한 신호등(위험 아님)** — 🔴 레드(대표 검수·승인 후 진행) / 🟡 옐로(팀장 판단 진행, `yellow_policy:"report"`면 팀원 보고 필수·`"auto"`면 자율) / 🟢 그린(자율·기록만). 항목별 상태·타임스탬프·근거로그.
3. **투두리스트** — 체크박스 3상태 순환(todo→doing→done), **WO(대표 지시) 태그·상단 강제 고정**, 미션 id·중요도(high/mid/low)·일자(YYMMDD) 태그, 중요도/일자 정렬.
＋ **WO 배너**(대표 지시 필수확인 최상단) · **게이미피케이션 스트립**(처리량·칭호 신입→숙련→베테랑→게이트마스터·진행률·뱃지, `todos` done 수에서 파생) · **세션로그 드롭다운**(최근=선명 → 오래될수록 opacity 흐림, "더 보기").
- **진입**: 실행 시 **인물 선택 → `localStorage.poffice_me` 저장 → 본인 데이터만** 표시(타인 격리). 디자인은 피모션 네온과 다른 **차분한 다크 워크스페이스**.

### 2B-3. `poffice_board.json` 스키마(마더 config) 핵심 필드
- 최상위: `version` · `generated_at` · `members[]` · `docs[]`.
- `member`: `name` · `role` · `yellow_policy(auto|report)` · `master(심상윤만 true)` · `missions[]` · `gates{red,yellow,green}` · `todos[]` · `sessions[]`(v0.2 추가, 시간순 opacity-fade 소스) · `last_session`.
- `mission`: `id` · `title` · `status(예정|진행|달성|보류)` · `due` · `progress(0~1)` · `roadmap[{step,done}]`.
- `gate item`: `ts(YYMMDD_HHMM)` · `item` · `state(대기|진행|완료)` · `log`(근거 세션로그).
- `todo`: `text` · `state(todo|doing|done)` · `wo(bool)` · `mission` · `importance(high|mid|low)` · `date(YYMMDD)`.
- **역방향 export** `poffice_export_{이름}.json` = `{ member, check_overrides, memo_overrides }`. `check_overrides`={인덱스→상태}, `memo_overrides` 키=`"mission|{id}"` 또는 `"session|{ts}"`→텍스트.
- 샘플: `schemas/poffice_board.sample.json`. **스프라이트 정본**: Drive `RuleTheDay/day.png`(Day 마리오), board엔 미포함·대시보드가 참조.

### 2B-4. 스킬 3종 (관심사·토큰 분리, 미통합 — `.claude/skills/`)
| 스킬 | 역할 | 저장/트리거 |
|---|---|---|
| **`poffice-skill`** | **기록** — 대화→개인세션로그(게이트·체크·미션 분류, 불변) + 역방향 export(체크·메모) 반영 | 저장: **블루필드 `[2.블루필드:아카이브].PIMM_archive` > 개인DB > {이름} > Session_세션로그**. 트리거: 세션로그·세션·스케줄·작업보고·업무지시·업무보고·미션보드·포피스·포피스 업로드·수정 |
| **`poffice-motherlog`** | **집계→config** — 개인세션로그 요약·분석 → `poffice_board.json` 생성 | 저장: **그린필드 `[1.그린필드:프레임워크].PIMM_framework`(id `1HB1X19PN6DQDXpEFpheE-BFLC2eBc3CG`) > `[2.포피스_섹터].Poffice`(id `1dbUhEa2ByRtLhKryM4YpYHC4bNLzBdFm`)**. 카테고리 폴더 6종(01_Mission~06_Notice)에 직전 버전 아카이빙. 트리거: 마더세션로그·마더로그·config 생성·대시보드 갱신·세션로그 집계·_board.json 생성 |
| **`poffice-report-bot`** | **알림·브리핑** — 마더 config를 직전과 diff → 페르소나 말투 브리핑(읽기 전용) | **기본 꺼짐**, `"{이름} 포피스알림켜줘"`→주기 질문→예약(CronCreate). 트리거: 포피스 알림·주간/일일보고·브리핑 |

**★ MotherLog 최상위 원칙 2개**: ① **텍스트 절대 안 깨짐**(UTF-8·한글·JSON 이스케이프, 생성 후 파싱 검증, 손상본 덮어쓰기 금지) ② **원문 참조·아카이빙·무왜곡**(항목마다 출처 세션로그 근거, 원본 불변, 과장·축소·창작 금지).

### 2B-5. 팀원 5인 · yellow_policy · 브리핑 페르소나
| 인물 | 도메인 | yellow_policy | 페르소나 말투 |
|---|---|---|---|
| **심상윤** | Master PD | auto (`master:true`) | 논리·정리형(요점→근거→다음 액션) |
| **이정민** | Device | **report**(보고 필수) | 유아용 캐릭터(쉽게·다정) |
| **유지호** | Build | auto | 밝은 애니메이션풍 여성 캐릭터 |
| **오세원** | Art | auto | 먼저 **"큰일났다/별일없다"** 결론 선언 후 설명 |
| **신승희** | Content | **report**(보고 필수) | 《스파이 패밀리》 아냐 말투 |
> 정보 정확성 > 캐릭터성 — 🔴·마감·리스크는 항상 명확히.

### 2B-6. 포피스 남은 일
- [ ] **자동예약(CronCreate)**: MotherLog 주기 집계 + Report-Bot 개인 예약 — "내일" 예정(미설정).
- [ ] Day 스프라이트 실제 이미지 연결(`RuleTheDay/day.png` → SPRITE_URL).
- [ ] 스킬 3종 `.plugin` 재패키징(플러그인 빌드 공정).
- [ ] 실 `poffice_board.json`(그린필드/포피스영역) 최신화 — 현재 대시보드는 샘플/드롭 폴백으로 동작.
- [ ] 파트웍(하드워크 트래커) 생기면 유지호 Build 미션과 연계.

---

## 3. 구글 드라이브 상태 (중요)

### 3-1. 폴더 구조
- **PIMMhub제작** (id `1jKgutU-WAP2IjT1UhVzXkANiGaPT04uR`) — 현재 **장치개발섹터** `[2.장치개발_섹터].Dev`(id `16TOjiMOxynYLtTLsAHwD0CAL8l163Rmi`) 안으로 이동됨.
  - 하위 `01_Plogic_플로직 / 02_Poffice_포피스 / 03_PIMMotion_피모션 / 04_Partwork_파트웍 / 05_Extra_별개에리어` = **청사진·문서용(포피스 섹터 구조)** — 툴 빌드용 아님.
  - **핌런처_Dev** (id `1jWgYoSVJSQJHN9HC_QNyuBpzsQRO2HeA`) — 이번에 생성, **툴 HTML 빌드용** 폴더. 안에 `_다운로드안내_….md` 넣어둠.
- 심상윤 개인세션로그(블루필드): `260725_플로직교육HTML_세션로그.md` 기록됨.
- 정리 필요: `01_Plogic`에 잘못 넣은 `플로직_교육도구_바로가기.md` (id `1Kocd7pChoORexweK-Zdg_9syxnZe9dVi`) — **드라이브 삭제 도구 없어 수동 정리 필요.**

### 3-2. ⚠️ 드라이브 업로드 한계 (해결 못 함)
- `create_file`은 파일 내용을 **인라인**으로 받아야 하는데, 셸 출력이 ~40KB, Read가 ~25K토큰(=base64 22K자)에서 **잘림.** 따라서 **30KB 넘는 HTML은 드라이브로 직접 업로드 불가.** (작은 md/json은 됨. 예전 ~24KB 툴은 됐던 이유.)
- **결론**: 플로직·포피스·허브 HTML은 **깃(레포)에만** 있음. 드라이브에 넣으려면 **GitHub "Download raw file"로 받아 `핌런처_Dev`에 드롭**(자체완결형이라 그대로 실행). 또는 다른 업로드 경로 필요.

---

## 4. 콘텐츠 조사(에이전트) 결과 요약 — 아티잔 진위

두 번째 조사 에이전트가 플로직 그린필드에서 확인:
- **멀티도메인 원칙 존재**(팀스피릿 `03_팀스피릿_Plogic.md` 원칙 6, id `1PWgCZBwxiHF7mjTOc2NqanUKH4usvhRh`).
- **MPA 존재**(`03.1_Artisan-MPA-Training.md`) = MiddlePointAmphibious / M-T-B Trajectory.
- **STP=AST(Artisan Simulation Test) 존재** — 7개 상황 시나리오, **10개 도메인** S/A/B/C 측정.
- **"6개 도메인" 목록은 정본에 없음** — "6D 밸류포지션(문서 예정)" 스텁 + "현장 도입 난항" 미결. → **대표가 이번에 6개 도메인을 직접 확정**(위 1-6).
- 커리큘럼 갭: 중급~마스터(특화 계층·완결 예시·실패 라이브러리)는 대부분 "대표 인터뷰 필요" 스텁.

핵심 원문 id: 하이어라키 Protocol `19IMgaUlG6z1nA4-9lU8GlTKRnyKqwpZj`, 테마비트 정본 `1ehTWQNgLHDthXvsWu_IeZCpYSGc3qDeK`, 플로직 섹터 `1nN5V64ppPaLbM3XtUTkPQiF2Xb6msKGV`, 프레임워크 `1exPL3H9eBrE7qEC7cKuD92XSyo03V0qL`.

---

## 5. 앞선 세션 산출물(맥락, 이미 커밋됨)
- **포피스 체계** → **상세는 §2-B 참조.** 파일: `tool/PIMM_Poffice.ver0.2.html`(현행 대시보드; ver0.1은 구버전), `docs/poffice-board-spec.md`(A~H), `docs/poffice-usage-by-member.md`(팀원별 시나리오), `schemas/poffice_board.sample.json`, 스킬 3종 `.claude/skills/poffice-skill|poffice-motherlog|poffice-report-bot/SKILL.md`.
- **사이트**: `site/pimmartworks.html`(B2B, Random Studio식 히어로), `site/panorama.html`(B&W 라인 미니멀).
- 문서: `docs/plogic-curriculum-design.md`, `docs/pimm-skill-plugin-integration.md`, `docs/poffice-usage-by-member.md`.

---

## 6. 남은 일 / 이어서 할 것 (TODO)

**플로직 교육툴**
- [ ] 심화 나머지 5개 이론(공간구성·게임퍼즐·장면연출·장르컨셉·운영설계) — **드라이브 원문 정독 후** 서사구조와 같은 틀로 채우기(무왜곡).
- [ ] 중급~마스터 심화 콘텐츠(특화 계층·완결 예시·실패 라이브러리) — **대표 인터뷰 필요.**
- [ ] (선택) 리더십 영역에도 계층/직함 체계(팀리드 승급 단계) 설계.
- [ ] (선택) 풀어보기에 STP 진단 흐름(코워크 문항 생성→응답→JSON→도메인 레벨 채점) / 개인 6각형 레이더.

**핌허브**
- [ ] **리브랜딩 PIMMotion → PIMM hub**(명칭·로고·워터마크·타이틀) — 미룸.
- [ ] 파트웍 도구 생기면 같은 방식(한 줄) LIVE 연결.

**드라이브**
- [ ] 플로직·포피스·허브 HTML을 `핌런처_Dev`에 넣기(수동 다운로드, 또는 업로드 경로 확보).
- [ ] `01_Plogic`의 잘못 둔 바로가기 파일 정리.

**앞선 세션 이월**
- [ ] 자동예약(CronCreate) 설정, 로고 적용(SPRITE_URL 교체) — "내일" 예정.
- [ ] 스킬 3종 `.plugin` 재패키징 → 플러그인 빌드 공정.
- [ ] 플로직 드라이브 중복 정리(가이드 6벌, `_trash/260716_플로직중복`) — 이동/삭제 도구 부재로 핸드오프.

---

## 7. 작업 규칙(다음 세션이 지킬 것)
- 개발 브랜치 **`claude/pimmartworks-homepage-renewal-9mhvqe`** 유지, 작업 후 커밋·푸시(`git push -u origin …`).
- 플로직 콘텐츠는 **원문 무왜곡** — 없는 내용은 지어내지 말고 대표 확정/원문 정독 후 채움.
- 단일 HTML은 `node --check`(스크립트 추출) + Playwright 렌더로 검증. 아티팩트는 harness가 `<head>/<body>` 감싸므로 `<style>+본문+<script>`만, `:root[data-theme]` 다크 오버라이드 주입.
- 아티팩트 갱신은 **같은 파일 경로 재발행**으로 동일 URL 유지(45a50729-…).
