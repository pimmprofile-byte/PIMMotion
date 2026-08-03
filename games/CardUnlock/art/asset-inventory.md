# 서브게임에셋 분류표 — 36개 파일 검수 · 계열 · 쓰임새 · 리네임

> 원본 위치: Drive `콤보제작/서브게임에셋/` (36개)
> 검수일 기준 전량 확인 완료. 아래는 **구조 계열 → 쓰임새 배정 → 리네임** 순.

---

## 0. 한눈에

| 계열 | 개수 | 정체 | 배정 |
|---|---|---|---|
| **BAY** 정비창 베젤 | 8 | `sub_bg` 원본 + 색 배리에이션 | **진행 단계 배경(B그룹)** |
| **HAND** 게임기 셸 | 6 | 핸드헬드 + 좌측 5-LED 컬럼 | **룰렛 스핀 애니메이션** ★ |
| **CON** 성장 콘솔 | 5 | 같은 기계 위에 장식이 누적 | **진행도 성장 연출** ★ |
| **GRV** 자연 침식 | 3 | 기계를 나무·마을이 뒤덮음 | **진행도 후반 tier** |
| **POD** 캡슐 | 2 | 둥근 포드 + 시안 | 카테고리 배경 |
| **RACK** 서버랙 | 2 | 카세트·서버 + 마젠타/시안 | 카테고리 배경 |
| **GLS / SUB / HATCH / CBL** | 4 | 글래스 · 잠수함 · 에어록 · 케이블 | 카테고리 배경 · 타이틀 |
| **POP** 팝업 | 6 | 해금 안내 팝업 (텍스트 0) | **해금 팝업** |

**★ 표시 2개는 제가 제안하지 않았던 것인데, 오히려 더 좋습니다.** §3·§4 참조.

---

## 1. 계열 판정 원칙 (왜 계열이 중요한가)

배경 전환은 박스 1개 + `setState` 스프라이트 스왑으로 처리합니다. 그런데 **구조가 다른 두 장을 스왑하면 화면이 튑니다.**

> **같은 계열 안에서만 스왑한다. 계열이 바뀔 때는 디졸브 0.4s를 넣는다.**

36장을 눈으로 확인한 결과 **11개 계열**로 갈립니다. 이름(`var`, `phase`)만으로는 계열이 안 갈려서 — 예를 들어 `sub_bg_phase1`과 `sub_bg_phase2`는 완전히 다른 기계입니다 — 아래 분류를 기준으로 쓰세요.

---

## 2. 계열 BAY — 정비창 베젤 (8종) → 진행 단계 배경

`sub_bg` 원본과 **픽셀 구조가 완전히 동일**한 8장. 좌상단 라디에이터, 우측 벤트 슬롯, 하단 케이블 런이 모두 같은 자리입니다. **스왑에 가장 안전한 계열**이고, 제가 프롬프트로 요청했던 B그룹 5종이 여기 다 들어 있습니다.

| 원본 파일 | 상태 | 배정 | 새 이름 |
|---|---|---|---|
| `sub_bg.jpeg` | 민트, 분절 네온바 | 기준 원본 | `bg_BAY_base_mint` |
| `sub_bg_var7_green.jpeg` | 민트 풀 플러드 | **B1 룰렛 · 기대** | `bg_BAY_step_roulette` |
| `sub_bg_var3_dark.jpeg` | 디밍 + 얇은 시안 아웃라인 | **B2 가이드 · 집중** | `bg_BAY_step_guide` |
| `sub_bg_var8_red.jpeg` | 레드 플러드 | **B3 대기 · 긴장** | `bg_BAY_step_wait` |
| `sub_bg_var4_orange.jpeg` | 앰버 플러드 | **B4 해금 · 보상** | `bg_BAY_step_unlock` |
| `sub_bg_var5_white.jpeg` | 화이트, 전체 밝음 | **B5 컬렉션 · 진열** | `bg_BAY_step_collection` |
| `sub_bg_var6_blue.jpeg` | 블루 플러드 | 예비 (실패/타임아웃?) | `bg_BAY_tint_blue` |
| `sub_bg_var2.jpeg` | 그린 틴트, 분절 네온바 | 예비 | `bg_BAY_tint_green` |

> **B2·B4·B5는 의도한 것보다 정확히 나왔습니다.** `var3_dark`의 "얇은 시안 아웃라인만 남기고 다 끔"은 가이드 화면에 그대로 쓰면 됩니다.
>
> 세부 차이: `sub_bg`·`var2`는 네온이 **짧은 막대 여러 개**, `var3~8`은 **개구부를 두르는 연속 아웃라인**입니다. 엄밀히는 두 하위 그룹이라 `var3~8`끼리 스왑하는 게 가장 매끄럽습니다.

---

## 3. 계열 HAND — 게임기 셸 (6종) → **룰렛 스핀 애니메이션** ★

이름은 `sub_bg_roll*`이지만 배경이 아닙니다. 6장 모두 동일한 핸드헬드 셸이고, **좌측 5칸 LED 컬럼의 색 순서만 다릅니다.** 즉 이건 정지 배경이 아니라 **룰렛이 돌아가는 프레임 시퀀스**입니다.

| 원본 | LED 상태 | 새 이름 |
|---|---|---|
| `sub_bg_roll0.jpeg` | 전부 소등 | `bg_HAND_roulette_f0_idle` |
| `sub_bg_roll1.jpeg` | 전부 백색 점등 | `bg_HAND_roulette_f1_charge` |
| `sub_bg_roll2.jpeg` | 적·황·녹·시안·청 | `bg_HAND_roulette_f2` |
| `sub_bg_roll3.jpeg` | 적·청·녹·황·시안 | `bg_HAND_roulette_f3` |
| `sub_bg_roll4.jpeg` | 청·황·적·시안·녹 | `bg_HAND_roulette_f4` |
| `sub_bg_roll5.jpeg` | 적·녹·청·황·시안 | `bg_HAND_roulette_f5` |

**제가 제안했던 원형 룰렛 휠보다 이쪽이 낫습니다.** 이유:
- 20슬롯 원형 휠은 1024폭에서 슬롯 하나가 너무 작아 카드 그림이 안 읽힙니다
- LED 컬럼은 **물리 장치(게이밍보드 버튼·LED)와 직결**됩니다 — 화면 LED와 실물 LED를 싱크시키면 몰입이 확 올라갑니다
- 프레임 스왑만으로 스핀이 되므로 **C# 0줄**

### 구현 (에셋 기반 애니메이션)
```
f0(대기) → [스핀 버튼 IN] → f2~f5 를 80ms 간격 루프 (감속: 80→120→200→400ms)
        → f1(전체 백색 = 확정 플래시) → 카드 결과 팝업
```
- 감속 곡선만 config 값. 프레임은 4장 순환이라 **추가 에셋 0**.
- 결과 카드가 무엇인지는 LED가 아니라 팝업이 알려주므로, LED 순서와 당첨 카드는 **무관해도 됩니다**(연출 전용).

> 주의: HAND 계열은 셸 자체가 화면을 차지해 **BAY 계열과 구조가 완전히 다릅니다.** 룰렛 구간 전용으로 쓰고, 진입/이탈에 디졸브 0.4s를 넣으세요.

---

## 4. 계열 CON + GRV — 성장하는 배경 (8종) → **진행도 연출** ★

`sub_phase3 ~ phase7`은 **같은 기계 배치 위에 장식이 누적되는 시리즈**입니다. 좌측 X자 밸브, 우측 러기드 랙, 하단 팬·다이얼, 회로기판 조각이 전부 같은 자리에 있고 데코만 늘어납니다. GRV(6~7)는 거기에 나무·마을이 덮입니다.

**이건 20종 해금 진행도(n/20)에 그대로 매핑됩니다.** 카드를 모을수록 배경이 화려해지는 = 진행 자체가 보상이 되는 구조입니다.

| 원본 | 인상 | 제안 tier | 해금 수 | 새 이름 |
|---|---|---|---|---|
| `sub_phase3_og.jpeg` | 마젠타, 깨끗 | 1 | 0–2 | `bg_CON_tier1_clean` |
| `sub_phase3.jpeg` | 녹·파손·적색 경고등 | 2 | 3–5 | `bg_CON_tier2_decay` |
| `sub_phase4.jpeg` | 앰버 랜턴·놋쇠 계기 | 3 | 6–8 | `bg_CON_tier3_amber` |
| `sub_phase5_minimal.jpeg` | 4색 크리스탈 (간소) | 4 | 9–11 | `bg_CON_tier4_crystal` |
| `sub_phase5.jpeg` | 4색 크리스탈 만개 | 5 | 12–14 | `bg_CON_tier5_prism` |
| `sub_phase6.jpeg` | 나무 침식 시작 + 마을 | 6 | 15–17 | `bg_GRV_tier6_overgrown` |
| `sub_phase7_village.jpeg` | 자연·마을 완전 지배 | 7 | 18–20 | `bg_GRV_tier7_village` |
| `sub_phase6_var1.jpeg` | tier6 + 하단 정보패널 | 6-alt | — | `bg_GRV_tier6_panel` ⚠ |

- 전환은 **해금 팝업이 떠 있는 동안** 몰래 바꾸면 자연스럽습니다(플레이어가 배경을 안 보는 순간).
- CON→GRV는 재질이 크게 바뀌므로 tier5→6 전환에만 디졸브 0.6s를 주세요.
- `phase6_var1`은 하단에 정보 패널이 그려져 있어 **레이아웃을 고정합니다.** 그 패널을 실제 HUD 자리로 쓸 게 아니면 `phase6`를 쓰세요.

---

## 5. 단독 컨셉 (8종) → 카테고리 배경 · 타이틀

| 원본 | 정체 | 배정 | 새 이름 |
|---|---|---|---|
| `sub_bg_solid.jpeg` | 유리·아크릴 패널 + 시안 튜브 | **D1 글래스** = 관찰·탐색 | `bg_GLS_base` |
| `sub_bg_lust.jpeg` | 녹슨 강판·파이프·밸브휠·앰버 | **D3 잠수함** = 공간·좌표 | `bg_SUB_base` |
| `sub_bg_title.jpeg` | 두꺼운 에어록 해치 프레임 | **타이틀 / 시퀀스 진입** | `bg_HATCH_title` |
| `sub_bg_var.jpeg` | 케이블 밀집 + 민트·마젠타 이중선 | 복합·조합 | `bg_CBL_base` |
| `sub_bg_phase1.jpeg` | 둥근 캡슐·포드 + 시안 | 논리·수리 | `bg_POD_base` |
| `sub_bg_phase1_var.jpeg` | POD + 민트 사각 아웃라인 | POD 점등 상태 | `bg_POD_lit_mint` |
| `sub_bg_phase2.jpeg` | 카세트·서버랙 + 마젠타(어두움) | **암호·해독** | `bg_RACK_dark_magenta` |
| `sub_bg_phase2_var.jpeg` | 동일 구조 + 화이트·시안(밝음) | RACK 밝은 변형 | `bg_RACK_light_cyan` |

- `phase1`↔`phase1_var`, `phase2`↔`phase2_var`는 **각각 같은 구조 페어**라 서로 스왑 가능합니다.
- `sub_bg_solid`는 D1 글래스 프롬프트를 안 쓰고도 글래스가 나왔습니다. 다만 §7 참조.

---

## 6. 계열 POP — 해금 팝업 (6종)

6장 전부 **구조 동일**, 헤더/푸터 네온색만 다릅니다. P1 프롬프트가 의도대로 재현됐습니다 — 헤더 명판, 좌측 3:4 웰(코너 브래킷), 우측 4단 플레이트(첫 칸 좌측에 배지 소켓), 푸터 명판이 전부 비어 있습니다.

| 원본 | 헤더 / 푸터 | 배정 | 새 이름 |
|---|---|---|---|
| `popup1.png` | 민트 / 앰버 | **기본 · 이지 해금** | `ui_popup_unlock_mint` |
| `popup3.png` | 시안 / 크림슨 | 이지 대체 | `ui_popup_unlock_cyan` |
| `popup2.png` | 마젠타 / 앰버 | **하드 해금** | `ui_popup_unlock_magenta` |
| `popup6.png` | 핑크 / 블루 | 하드 대체 | `ui_popup_unlock_pink` |
| `popup4.png` | 오렌지 / 바이올렛 | **최종 완주(20/20)** | `ui_popup_unlock_orange` |
| `popup5.png` | 블루 / 앰버 | 정보·안내용 | `ui_popup_info_blue` |

**분류 4종(장신구·무기·상의·하의)을 팝업 색으로 쓰지 마세요.** 색은 난이도(이지/하드)에 쓰고, 분류는 **P3 배지 아이콘**으로 구분해야 합니다. 색에 두 가지 의미를 겹치면 둘 다 안 읽힙니다.

---

## 7. 조치가 필요한 것

| # | 대상 | 문제 | 조치 |
|---|---|---|---|
| 1 | **배경 전 30장** | **1024×572** — 1920×1080 아니고 비율도 1.790 (16:9=1.778) | 1920×1080 리사이즈. 0.6% 왜곡은 육안 식별 불가 |
| 2 | **팝업 6장** | **629×396** — 1200×760 배치 시 1.9배 업스케일 | 소프트해집니다. 중요 화면이니 1200×760 네이티브 재생성 권장 |
| 3 | `sub_phase6_var1` | 우상단 **♥ 하트 아이콘**, 우하단 **"8-BIT ART" 워터마크** | 에셋에디터에서 제거. 안 지우면 화면에 그대로 나옵니다 |
| 4 | `sub_phase4`, `sub_phase5` | 개구부 상·하단에 **희미한 문자열 흔적** | 확대 확인 → 글자면 지우거나 그 영역을 피해 배치 |
| 5 | `sub_bg_solid` | 8비트 거칠기 없음(매끈·고해상), 다른 계열과 텍스처 불일치 | 단독 씬 전용으로. BAY·CON과 인접 배치 금지 |
| 6 | `sub_phase7_village`, `sub_bg_phase2_var`, `sub_bg_var5_white` | 개구부가 **밝음** | 그 위 텍스트는 **어두운 색**이어야 합니다. 밝은 텍스트 프리셋을 그대로 쓰면 안 보입니다 |
| 7 | 전 파일 | JPEG (팝업만 PNG) | 배경은 JPEG로 충분. **팝업·아이콘은 반드시 알파 PNG 유지** |

> 1·2번은 규격이라 지금 정해야 하고, 3~6번은 개별 파일 보정이라 나중에 해도 됩니다.

---

## 8. 리네임 스크립트

Drive 동기 폴더에서 **로컬로 실행**하세요. 원본을 `_original/`로 옮기지 않고 이름만 바꿉니다(되돌리기 쉽게 복사본 생성 방식).

```bash
#!/usr/bin/env bash
# 콤보제작/서브게임에셋/ 에서 실행
set -e
mkdir -p renamed

cp sub_bg.jpeg                renamed/bg_BAY_base_mint.jpeg
cp sub_bg_var7_green.jpeg     renamed/bg_BAY_step_roulette.jpeg
cp sub_bg_var3_dark.jpeg      renamed/bg_BAY_step_guide.jpeg
cp sub_bg_var8_red.jpeg       renamed/bg_BAY_step_wait.jpeg
cp sub_bg_var4_orange.jpeg    renamed/bg_BAY_step_unlock.jpeg
cp sub_bg_var5_white.jpeg     renamed/bg_BAY_step_collection.jpeg
cp sub_bg_var6_blue.jpeg      renamed/bg_BAY_tint_blue.jpeg
cp sub_bg_var2.jpeg           renamed/bg_BAY_tint_green.jpeg

cp sub_bg_roll0.jpeg          renamed/bg_HAND_roulette_f0_idle.jpeg
cp sub_bg_roll1.jpeg          renamed/bg_HAND_roulette_f1_charge.jpeg
cp sub_bg_roll2.jpeg          renamed/bg_HAND_roulette_f2.jpeg
cp sub_bg_roll3.jpeg          renamed/bg_HAND_roulette_f3.jpeg
cp sub_bg_roll4.jpeg          renamed/bg_HAND_roulette_f4.jpeg
cp sub_bg_roll5.jpeg          renamed/bg_HAND_roulette_f5.jpeg

cp sub_phase3_og.jpeg         renamed/bg_CON_tier1_clean.jpeg
cp sub_phase3.jpeg            renamed/bg_CON_tier2_decay.jpeg
cp sub_phase4.jpeg            renamed/bg_CON_tier3_amber.jpeg
cp sub_phase5_minimal.jpeg    renamed/bg_CON_tier4_crystal.jpeg
cp sub_phase5.jpeg            renamed/bg_CON_tier5_prism.jpeg
cp sub_phase6.jpeg            renamed/bg_GRV_tier6_overgrown.jpeg
cp sub_phase6_var1.jpeg       renamed/bg_GRV_tier6_panel.jpeg
cp sub_phase7_village.jpeg    renamed/bg_GRV_tier7_village.jpeg

cp sub_bg_solid.jpeg          renamed/bg_GLS_base.jpeg
cp sub_bg_lust.jpeg           renamed/bg_SUB_base.jpeg
cp sub_bg_title.jpeg          renamed/bg_HATCH_title.jpeg
cp sub_bg_var.jpeg            renamed/bg_CBL_base.jpeg
cp sub_bg_phase1.jpeg         renamed/bg_POD_base.jpeg
cp sub_bg_phase1_var.jpeg     renamed/bg_POD_lit_mint.jpeg
cp sub_bg_phase2.jpeg         renamed/bg_RACK_dark_magenta.jpeg
cp sub_bg_phase2_var.jpeg     renamed/bg_RACK_light_cyan.jpeg

cp popup1.png                 renamed/ui_popup_unlock_mint.png
cp popup3.png                 renamed/ui_popup_unlock_cyan.png
cp popup2.png                 renamed/ui_popup_unlock_magenta.png
cp popup6.png                 renamed/ui_popup_unlock_pink.png
cp popup4.png                 renamed/ui_popup_unlock_orange.png
cp popup5.png                 renamed/ui_popup_info_blue.png

echo "완료: $(ls renamed | wc -l) / 36"
```

**명명 규칙**: `bg_<계열>_<역할>[_<변형>]` · `ui_<종류>_<용도>_<변형>`
계열 코드 — BAY 정비창 / HAND 게임기 / CON 성장콘솔 / GRV 자연침식 / POD 캡슐 / RACK 서버랙 / GLS 글래스 / SUB 잠수함 / HATCH 에어록 / CBL 케이블

---

## 9. 아직 없는 것 (Phase 1 잔여)

이번 36장으로 **배경·룰렛·해금팝업이 다 채워졌습니다.** 남은 껍데기는:

- [ ] 카드 프레임 (P2, 400×533) — 팝업 좌측 웰·컬렉션·룰렛 결과 공용
- [ ] 분류 배지 4종 (P3, 128×128) — 장신구·무기·상의·하의
- [ ] 가이드 프레임 4타입 (G-A/B/C/D)
- [ ] HUD — 진행 n/20, 점수
- [ ] 컬렉션 20칸 그리드
- [ ] 커스터마이즈 착장 스테이지
- [ ] 버튼 3종 × 3상태
- [ ] 자물쇠 대기 비주얼

> 배경이 계열별로 확정됐으니, 남은 껍데기는 **어느 계열 위에 올라갈지**를 먼저 정하고 그 계열의 금속 톤에 맞춰 뽑아야 합니다. 예를 들어 카드 프레임을 BAY 톤으로 만들면 GRV(나무) 배경 위에서 겉돕니다. **가장 무난한 건 팝업과 같은 톤**(중립 웜그레이 기계)입니다.
