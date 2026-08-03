# 해금 안내 팝업 · 카드 프레임 · 분류 배지 — 프롬프트 (텍스트 0)

> 전부 **텍스트 없이** 생성하고, 유니티에서 TextMeshPro를 빈 구역 위에 얹습니다.
> 배경 프롬프트: `prompts-ready.md` · 설계 근거: `bg-variations.md`

---

## 0. 핵심 기법 — "빈 구역"을 사물로 묘사한다

`leave this area empty`, `blank space for text` 같은 지시는 **거의 항상 실패**합니다. AI는 여백을 채우려 하고, "text"라는 단어를 보면 글자를 그려 넣습니다.

> **해결: 빈 구역을 "움푹 파인 빈 명판(recessed blank nameplate)"이라는 물리적 사물로 묘사한다.**
> 사물이 되면 비어 있는 게 자연스러워지고, `text`라는 단어를 쓰지 않아도 됩니다.

### 좌표는 "생성 후 실측"으로 잡는다 (중요)
AI에게 픽셀 좌표를 지시해도 정확히 안 맞습니다. 순서를 뒤집으세요.

```
① 프롬프트로 프레임 생성 (비율·배치만 지시)
② 나온 결과물에서 빈 명판의 실제 픽셀 좌표를 잰다
③ 그 실측값을 유니티 TextMesh 박스 좌표로 넣는다
```
아래 §4의 좌표표는 **설계 목표값**입니다. 실제 생성물이 다르면 **생성물 기준으로 고칩니다.**

---

## P1 · 해금 안내 팝업 프레임

- **생성 크기: 1200 × 760** · 알파 PNG(모서리 투명) · `frameType: framegraphic`
- 배치: 1920×1080 화면 중앙 → x 360, y 160 (세이프존 안쪽)

```
A 1200x760 UI popup frame for a retro-futuristic 8-bit game, on a transparent background.

WHAT IT IS: a heavy machined bezel enclosing an award plaque. It is an empty fixture —
every place where information would go is a physically recessed blank plate, milled flat,
with a thin inner shadow and a faint bevel. The fixture has been photographed before
anything was engraved or mounted on it.

LAYOUT (a single fixture, divided by raised metal ribs):
- A narrow header rail spans the full width across the top: one long recessed blank
  nameplate set into it.
- The lower area is split by a vertical rib into a narrow left column and a wider
  right column.
- LEFT COLUMN: one large empty recessed well in a tall 3:4 portrait proportion,
  bordered by a raised lip with corner brackets. The well is a flat dark surface with
  an inner shadow — nothing is mounted in it.
- RIGHT COLUMN, stacked top to bottom with even gaps, four recessed blank plates:
  1. a short wide plate with a small empty square socket at its left end
  2. a wide plate, slightly taller than the first
  3. a large tall plate occupying most of the column
  4. a short wide plate at the bottom
- A narrow footer rail spans the full width across the bottom: one long recessed blank
  nameplate set into it.
- All recessed plates are flat, evenly lit, and slightly darker than the bezel around them.

STYLE: 8-bit pixel art, coarse pixel grid, hard nearest-neighbour edges, no anti-aliasing,
no blur. Limited palette, ordered dithering. Machined metal with visible seams, rivets and
bevels.

COLOR: warm grey — bezel in mid warm grey (#3E3A35) and dusty warm grey (#6B645C),
recessed plates in deep warm charcoal (#2A2724). Warm neutral grey, NOT blue-grey.

NEON: neon mint (#00FF99) as a thin light strip along the top header rail and short
accent segments at the two upper corners. Neon amber (#FFB020) as a thin underline on the
footer rail. Sparse — under 5% of the image. Soft bloom onto the surrounding metal.

BACKGROUND: fully transparent outside the fixture. The fixture has slightly rounded outer
corners and a soft drop shadow.

MUST NOT CONTAIN: text, letters, numbers, glyphs, runes, symbols, engraving, labels,
icons, logo, watermark, character, person, creature, portrait, item, artwork or any
content inside the recessed plates or the large well, progress bar, star rating,
checkerboard transparency pattern.
```

### 변형 — 등급별 팝업 (선택)
`NEON:` 문단만 교체합니다. 구조는 동일.

| 등급 | 교체 문장 |
|---|---|
| 이지 | `NEON: neon cyan (#38E8FF) as a thin light strip along the top header rail and short accent segments at the two upper corners. Sparse — under 5% of the image.` |
| 하드 | `NEON: neon magenta (#FF3D8B) as a thin light strip along the top header rail, with amber (#FFB020) accent segments at all four corners. Sparse — under 5% of the image.` |

---

## P2 · 카드 프레임 (팝업 · 컬렉션 · 룰렛 공용)

- **생성 크기: 400 × 533** (3:4) · 알파 PNG · `frameType: framegraphic`
- 팝업 좌측 웰, 컬렉션 그리드, 룰렛 슬롯에서 **같은 파일 재사용**

```
A 400x533 empty trading-card frame for a retro-futuristic 8-bit game, on a transparent
background.

WHAT IT IS: a machined metal card holder in 3:4 portrait proportion. The middle is a large
empty recessed window — a flat dark milled surface with an inner shadow, with nothing
mounted in it. A narrow recessed blank nameplate runs across the bottom of the holder.
Small corner brackets clamp the four corners of the window.

STYLE: 8-bit pixel art, coarse pixel grid, hard nearest-neighbour edges, no anti-aliasing,
no blur. Limited palette, ordered dithering. Machined metal with rivets and bevels.

COLOR: warm grey — holder in mid warm grey (#3E3A35) and dusty warm grey (#6B645C),
recessed window in deep warm charcoal (#2A2724). Warm neutral grey, NOT blue-grey.

NEON: neon mint (#00FF99) as a thin edge-light along the inner lip of the window only.
Sparse. Soft bloom onto the metal.

BACKGROUND: fully transparent outside the holder. Slightly rounded outer corners,
soft drop shadow.

MUST NOT CONTAIN: text, letters, numbers, glyphs, symbols, engraving, labels, icons, logo,
watermark, character, person, creature, portrait, artwork or any content inside the window,
star rating, checkerboard transparency pattern.
```

**등급 변형** — `NEON:` 한 줄만 교체 → `bg`가 아니라 카드 테두리 색으로 난이도 구분:
- 이지: `neon cyan (#38E8FF)` · 하드: `neon magenta (#FF3D8B)` · 미해금: `no neon at all; the whole holder is unlit, desaturated and dimmed by 50%`

> **미해금 상태**는 별도 생성하지 말고 **같은 파일에 유니티에서 그레이스케일 + 밝기 50%** 처리해도 됩니다(에셋 1장 절약).

---

## P3 · 분류 배지 아이콘 4종

- **생성 크기: 128 × 128** 각 1장 · 알파 PNG · `frameType: framegraphic`
- 팝업 우측 첫 번째 플레이트의 **왼쪽 빈 사각 소켓**에 들어감
- 텍스트가 없으므로 **분류는 아이콘 + 색으로 읽혀야 합니다.** 유니티 TextMesh는 그 옆에 라벨을 붙이는 보조 역할

**공통 프롬프트** (`SUBJECT` 한 줄만 교체)

```
A 128x128 pixel-art category icon on a fully transparent background.

SUBJECT: <여기에 아래 표의 문장 하나>

STYLE: 8-bit pixel art on a 32x32 logical pixel grid upscaled 4x. Hard nearest-neighbour
edges, no anti-aliasing, no blur. Bold, chunky, highly readable at small size. A simple
filled silhouette with one internal highlight — not a detailed illustration.

COLOR: the silhouette is dusty warm grey (#6B645C) with a warm highlight (#A89E92) on the
upper-left edge, and a 2-pixel neon rim light in <여기에 아래 표의 색상>.

BACKGROUND: fully transparent. The icon is centered with even padding on all four sides.

MUST NOT CONTAIN: text, letters, numbers, background fill, frame, border, badge shape,
circle backing, shadow, checkerboard transparency pattern.
```

| 분류 | `SUBJECT` | 네온 색 |
|---|---|---|
| **장신구** | `a simple ring with a single faceted gem set into it, seen straight on` | `neon cyan (#38E8FF)` |
| **무기** | `a short sword seen straight on, blade pointing up, with a simple crossguard` | `neon magenta (#FF3D8B)` |
| **상의** | `a simple short-sleeved tunic seen straight on from the front, flat and symmetrical` | `neon mint (#00FF99)` |
| **하의** | `a simple pair of trousers seen straight on from the front, flat and symmetrical` | `neon amber (#FFB020)` |

> 4개를 **한 번에 한 장으로 뽑지 마세요.** 4장 따로 뽑아야 크기·여백이 균일해지고 개별 교체가 됩니다.

---

## 4. 팝업 내부 좌표 (설계 목표값 · 1920×1080 전역 기준)

팝업 위치: **x 360, y 160, 1200×760**

| # | 용도 | 유니티 요소 | x | y | w | h |
|---|---|---|---|---|---|---|
| 1 | 헤더 (예: "NEW UNLOCK") | TextMesh | 384 | 180 | 1152 | 92 |
| 2 | 카드 아트 | Image (P2 프레임 + 보상 아트) | 416 | 300 | 400 | 533 |
| 3 | 분류 배지 | Image (P3 아이콘) | 856 | 310 | 88 | 88 |
| 4 | 분류 라벨 (장신구/무기/상의/하의) | TextMesh | 960 | 310 | 544 | 88 |
| 5 | 보상 이름 | TextMesh | 856 | 418 | 648 | 80 |
| 6 | 설명문 | TextMesh (멀티라인) | 856 | 514 | 648 | 240 |
| 7 | 착용 슬롯 정보 | TextMesh | 856 | 610 | 648 | 64 |
| 8 | 하단 안내 (예: 버튼을 누르세요) | TextMesh | 384 | 850 | 1152 | 48 |

- 전부 세이프존(x 150~1770, y 110~940) 안입니다.
- **텍스트 박스는 배경 프레임과 z를 분리**: 프레임 `z:10`, 아트 `z:11`, 텍스트 전부 `z:12`.
- 팝업 등장 = `continuity: enter`, 퇴장 = `exit`. 배경(`BG_MAIN`)은 `persist`로 그대로 둡니다.
- 텍스트 위치·크기는 config대로 정확히 재현되지만 **폰트 렌더링(자간/힌팅)만 브라우저↔Unity 미세차**가 있습니다.
  최종은 Play에서 확인하세요 (`guide-cowork-unity.md` §5).

## 5. 산출 파일명

```
assets/assetsIngame/
  ui_popup_unlock.png            # P1 (1200x760)
  ui_popup_unlock_easy.png       # P1 변형 (선택)
  ui_popup_unlock_hard.png       # P1 변형 (선택)
  ui_card_frame_easy.png         # P2 (400x533)
  ui_card_frame_hard.png         # P2
  ui_card_frame_locked.png       # P2 (또는 유니티에서 그레이스케일 처리)
  ui_badge_accessory.png         # P3 (128x128)
  ui_badge_weapon.png
  ui_badge_top.png
  ui_badge_bottom.png
```
