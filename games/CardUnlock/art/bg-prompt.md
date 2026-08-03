# 배경 UI 프롬프트 — 8비트 레트로퓨처 / 네온 / 웜그레이 베이스

> **용도**: 해금게임(룰렛→퍼즐→해금) 시퀀스의 **배경 플레이트** 생성용 AI 이미지 프롬프트.
> **전제(중요)**: 콘티 미확정 + "그리드가 자유로웠으면" → 배경에 **UI를 굽지 않는다.**
> 배경은 *레이아웃*이 아니라 **판(plate)**. 패널·슬롯·프레임을 그려 넣으면 그 순간 그리드가 고정된다.
> PIMMotion 매핑: 이 이미지는 `frameType: "fullframe"` (1920×1080 전체, 좌표는 이미지에 구워지지 않음).

---

## 0. 설계 결론 (왜 이렇게 뽑는가)

| 원칙 | 이유 |
|---|---|
| **중앙 세이프존 비우기** (1400×780) | 룰렛·카드·가이드·컬렉션이 전부 화면 중앙을 쓴다. 여기에 무늬가 있으면 나중에 뭘 올려도 지저분해짐 |
| **디테일은 가장자리·모서리로** | 위/아래/좌우 밴드에만 정보를 몰면, 중앙 구성이 바뀌어도 배경은 그대로 재사용 |
| **UI 요소 금지** (패널/버튼/창/글자/HUD) | 배경에 창을 그리면 박스 위치가 그 창에 묶임 = 그리드 고정 |
| **밝기 낮게 · 대비 낮게** | 그 위에 올라갈 네온 UI 박스가 주인공. 배경이 세면 UI가 죽음 |
| **1장으로 여러 씬 커버** | 색상 무드만 바꿔 변주(§4) → 에셋 수 절감 + 연속성(persist) 유지 쉬움 |

---

## 1. 메인 프롬프트 (복붙용 · 영문)

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

STYLE: 8-bit pixel art, rendered on a coarse pixel grid (roughly 480x270 logical
pixels upscaled 4x with hard nearest-neighbour edges, no anti-aliasing, no blur).
Limited palette, ordered dithering for all gradients. Retro-future / synthwave
terminal mood: CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey. Deep warm charcoal (#2A2724) in the center, rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) toward the edges.
The whole plate reads as warm neutral grey, NOT blue-grey, NOT black.

NEON: sparse neon accents only, used as light sources and rim-light, never as
solid shapes. Neon mint (#00FF99) as the primary accent, with small secondary
touches of neon magenta (#FF3D8B) and neon cyan (#38E8FF). Neon appears as thin
glowing tubes, edge-lit seams, and soft bloom halos bleeding onto the warm grey.

COMPOSITION (critical):
- The central area (about 70% width, 70% height) must stay almost EMPTY:
  flat low-contrast warm grey with only faint dithering and a soft vignette.
- All visual interest is pushed to the outer border: the top band, the bottom
  band, and the left/right margins.
- Along those edges: chunky pixel-art machinery — heat-sink fins, cable runs,
  rivet rows, ventilation slots, thin neon piping, tiny idle indicator lights.
  Read as the inner casing of a large retro machine, seen head-on.
- Perfectly flat, straight-on view. No perspective, no vanishing point, no
  horizon line, no floor grid.
- Lighting is even and dim; a gentle vignette darkens the four corners.

MUST NOT CONTAIN: any UI element, window, panel, frame, card, slot, button,
dialog box, HUD, meter, icon, logo, watermark, text, letters, numbers, characters,
people, creatures, or a dominant regular grid pattern across the center.
```

### 왜 마지막 줄이 제일 중요한가
"패널/슬롯/프레임"을 안 막으면 AI는 **거의 항상** 화면에 창틀을 그려 넣습니다. 그 순간 그리드가 그 창에 고정돼서, 룰렛을 왼쪽으로 옮기고 싶어도 못 옮깁니다.

---

## 2. 네거티브 프롬프트 (별도 입력란이 있는 모델용)

```
ui, hud, window, panel, frame, border box, card, slot, button, dialog,
text, letters, numbers, logo, watermark, signature,
character, person, face, creature, mascot,
perspective grid, floor grid, horizon, vanishing point, tron grid,
busy center, high contrast, blown highlights, photorealistic, 3d render,
smooth gradient, anti-aliased, blurry, depth of field, jpeg artifacts,
checkerboard transparency pattern, blue-grey, cool grey, pure black
```

---

## 3. 팔레트 정본 (이 값으로 고정)

| 역할 | HEX | 용도 |
|---|---|---|
| 웜그레이 딥 | `#2A2724` | 중앙 세이프존 바닥 |
| 웜그레이 미드 | `#3E3A35` | 가장자리 구조물 면 |
| 웜그레이 라이트 | `#6B645C` | 하이라이트 면·리벳 |
| 웜 하이라이트 | `#A89E92` | 최상단 에지 |
| **네온 민트** | `#00FF99` | **주 액센트** (핌 시그니처) |
| 네온 마젠타 | `#FF3D8B` | 보조 (경고·하드 난이도) |
| 네온 시안 | `#38E8FF` | 보조 (정보·이지 난이도) |
| 네온 앰버 | `#FFB020` | 보조 (해금·보상 연출) |

> 네온은 **면적 5% 이하**. 넓게 칠하면 8비트가 아니라 그냥 형광 그림이 됩니다.

---

## 4. 씬별 변주 (메인 프롬프트에 한 줄만 갈아끼움)

배경을 씬마다 새로 뽑지 말고, **위 프롬프트 + 아래 한 줄**로 변주하세요. 구조가 같아야 씬 전환 시 `continuity: persist`로 배경을 유지(디졸브·깜빡임 없음)할 수 있습니다.

| 씬 | 추가할 한 줄 | 무드 |
|---|---|---|
| 룰렛 (S02–S04) | `The edge machinery glows with neon mint (#00FF99); indicator lights are lively.` | 기대·활기 |
| 퍼즐 가이드 (S05) | `Dimmer overall; edge neon reduced to a thin cyan (#38E8FF) outline. Very calm.` | 집중 |
| 자물쇠 대기 (S06) | `Slow-pulse magenta (#FF3D8B) rim light along the bottom band only.` | 긴장 |
| 해금 연출 (S07) | `Warm amber (#FFB020) bloom washing in from all four edges toward the center.` | 보상 |
| 컬렉션·커스터마이즈 (S08–S09) | `Neutral and evenly lit, minimal neon, slightly lighter warm grey overall.` | 진열 |
| 결과 (S11) | `All edge neon at full brightness, mint and amber together.` | 마무리 |

---

## 5. 규격 체크리스트 (받은 뒤 확인)

- [ ] **1920×1080 정확히** (16:9). 모자라면 에셋에디터에서 캔버스 리사이즈
- [ ] **중앙 1400×780 세이프존**이 실제로 비어 있는가 — 여기에 무늬가 있으면 재생성
- [ ] 그레이가 **웜**인가 (푸른기 돌면 재생성 — AI가 자주 쿨그레이로 감)
- [ ] 글자·숫자·로고 **0개** (AI가 몰래 그려 넣는 1순위)
- [ ] 픽셀이 **뭉툭한가** — 매끈하면 8비트가 아님. 안 되면 480×270으로 뽑아 4배 니어리스트 업스케일
- [ ] 격자무늬 가짜 투명 배경이 아닌가 (제미나이 흔한 이슈 → 에셋에디터 §2 배경제거로 처리)

## 6. PIMMotion 반영값

```
frameType   : fullframe      # 1920×1080 전체. 박스 좌표는 "콘텐츠 영역 표시"용
role        : background
continuity  : persist        # 씬이 바뀌어도 유지 (crossSceneId 공유 → 파괴/재생성 금지)
z           : 0              # 최하단
파일명       : bg_plate_base.png  /  변주는 bg_plate_<scene>.png
저장위치     : assets/assetsIngame/
```

> 변주를 **상태(배리에이션)**로 넣으면 박스 1개로 씬마다 스프라이트만 스왑됩니다 (C# 0줄).
> `states: [상태1=base, 상태2=roulette, 상태3=guide, ...]` + `setState`.
