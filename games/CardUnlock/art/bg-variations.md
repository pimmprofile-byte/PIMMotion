# 배경 배리에이션 10종 — 검수 + 프롬프트

> 기준 원본: `art/ref/sub_bg.jpeg` (Drive: 콤보제작/서브게임에셋/sub_bg.jpeg, 1024×572)
> 마스터 프롬프트: `art/bg-prompt.md`

---

## 1. sub_bg 검수 결과 — **채택 권장**

| 항목 | 결과 | 비고 |
|---|---|---|
| 중앙 세이프존 | ✅ **기준 초과 달성** | 실측 안전 사각형 ≈ 1920 환산 **1620×790** (요구치 1400×780보다 넓음) |
| 웜그레이 베이스 | ✅ | 탠/카키 기운. 쿨그레이로 안 샘 |
| 글자·숫자·로고 | ✅ 0개 | |
| 네온 절제 | ✅ | 민트 주 + 시안/마젠타 보조, 면적 5% 이하. 앰버는 미사용(해금 연출용으로 남겨둠) |
| 비네팅 방향 | ✅ | 중앙 딥 → 가장자리 밝음. 의도대로 |
| **해상도** | ⚠️ **수정 필요** | **1024×572**. 1920×1080 아니고, 비율도 1.790 (16:9=1.778) — 미세하게 어긋남 |
| 8비트 거칠기 | ⚠️ 약함 | 그라데이션이 매끈하고 픽셀 청크가 작음. "픽셀아트 느낌"까지는 오는데 8비트는 아님 |
| 사방 닫힌 베젤 | ◐ **결과적으로 OK** | 프롬프트에선 프레임을 막았는데 모델이 사방 베젤로 해석. 다만 화면 최외곽에 붙어 있어 **내부 배치를 제약하지 않음** — 오히려 게임 화면 프레임으로 기능. 단 **라운드 코너 반경이 커서 네 모서리는 배치 불가 구역** |

### 조치 2가지

1. **해상도**: 1024×572 → 1920×1080은 배율 1.875x/1.888x로 **정수배가 아님** → 픽셀이 뭉갬.
   재생성한다면 **1920×1080 네이티브** 또는 **960×540**(정확히 1/2 → 2x 니어리스트)로.
   지금 것을 그냥 쓸 거면 1920×1080 리사이즈로 충분합니다(0.6% 종횡비 왜곡, 육안 식별 불가).
2. **8비트 거칠기**: 더 뭉툭하게 원하면 아래 프롬프트의 `PIXEL SCALE` 줄을 강화해서 재생성.
   지금 톤이 마음에 들면 **그대로 두는 걸 권합니다** — 거칠기를 올리면 중앙의 부드러운 디더가 지저분해져서
   그 위에 올라갈 UI가 오히려 안 읽힙니다.

---

## 2. 10종 구성 — A/B 두 그룹으로 나눈 이유 (★ 먼저 읽기)

두 그룹은 **생성 방식이 다릅니다.** 같은 방식으로 뽑으면 하나는 반드시 깨집니다.

| | A그룹 (5종) | B그룹 (5종) |
|---|---|---|
| 무엇 | **게임 카테고리별** 배경 (20종을 5카테고리로) | **진행 단계별** 배경 (룰렛→가이드→대기→해금→결과) |
| 언제 바뀌나 | 라운드가 넘어갈 때 (큰 전환) | **한 라운드 안에서 연속 전환** |
| 구조 | **달라도 됨** — 오히려 달라야 톤전환이 체감됨 | **반드시 동일해야 함** |
| 생성 방식 | 신규 생성 (아래 전체 프롬프트) | **sub_bg를 img2img 베이스로 색/조명만** |

**왜 B는 구조가 같아야 하나**: 진행 중엔 배경 박스를 `continuity: persist`로 유지하고 스프라이트만 스왑(`setState`)합니다. 구조가 다르면 스왑 순간 화면이 튑니다. 반대로 구조가 같으면 조명만 바뀌는 것처럼 보여서 **C# 0줄**로 연출이 끝납니다.

> img2img가 없는 툴이면: B그룹도 전체 프롬프트로 뽑되 전환에 크로스페이드(0.3s)를 넣어야 합니다. 차선책입니다.

---

## 3. A그룹 — 게임 카테고리 배경 5종 (신규 생성)

### 공통 헤더 (A1~A5 모든 프롬프트 앞에 붙임)

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels
upscaled 4x, hard nearest-neighbour edges, no anti-aliasing, no blur).
Limited palette, ordered dithering for all gradients. CRT phosphor glow,
faint scanlines, subtle chromatic fringing.

BASE: warm grey throughout — deep warm charcoal (#2A2724) in the center rising
to mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges.
Warm neutral grey, NOT blue-grey, NOT black.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat low-contrast warm
grey with faint dithering and a soft vignette. All detail is pushed to the top
band, bottom band and left/right margins, forming a thin bezel of chunky
pixel-art machinery hugging the screen edge. Keep the inner corner radius SMALL
so the corners stay usable. Perfectly flat straight-on view, no perspective,
no horizon, no floor grid, even dim lighting, corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter,
icon, logo, watermark, text, letters, numbers, character, person, creature,
or a dominant regular grid across the center.
```

### A1 — 관찰·탐색 (Observation) · 시안
> 대상 게임: 틀린그림찾기 · 개수세기 · 그림자매칭 · 미로경로

```
CONCEPT: optical inspection bay. The edge machinery reads as lens housings,
iris rings, calibration ticks and thin fiber-optic runs. Neon cyan (#38E8FF)
is the dominant accent as cool clean examination light; a few tiny mint
(#00FF99) status pips. Center is very slightly brighter than usual, as if lit
for close inspection.
```

### A2 — 논리·수리 (Logic) · 민트 *(= sub_bg 계열, 기본값)*
> 대상 게임: 아이콘연산 · 도형규칙 · 논리추론 · 진법변환

```
CONCEPT: computation rack. The edge machinery reads as heat-sink fins,
ventilation slots, cable looms and rivet rows. Neon mint (#00FF99) dominant as
steady operating light, with small magenta (#FF3D8B) and cyan (#38E8FF) pips.
Calm, neutral, everyday-operation mood.
```

### A3 — 암호·해독 (Cipher) · 마젠타
> 대상 게임: 시저암호 · 모스부호 · 심볼사전 · 아나그램

```
CONCEPT: cryptography desk. The edge machinery reads as rotor drums, punched
tape reels, thin slotted apertures and coiled wiring. Neon magenta (#FF3D8B)
dominant with deep violet bloom; mint (#00FF99) reduced to rare tiny pips.
Overall darker and more secretive than the other plates; the warm grey pushed
toward a dusky plum-tinted grey while staying warm.
```

### A4 — 공간·좌표 (Spatial) · 앰버
> 대상 게임: 방향추적 · 좌표격자 · 오버레이 · 시계각도

```
CONCEPT: navigation console. The edge machinery reads as brass-toned bezels,
gimbal rings, engraved bearing ticks and dial housings. Neon amber (#FFB020)
dominant as warm instrument light, with small cyan (#38E8FF) pips. The warm
grey leans toward aged brass-grey. Slightly older, more analogue than the rest.
```

### A5 — 복합·조합 (Composite) · 프리즘
> 대상 게임: 순서배열 · 다단복합 · 음계리듬 · 색배열 — 최고 난이도 그룹

```
CONCEPT: prism core. The edge machinery reads as faceted crystal mounts, split
light guides and layered plating. All four neons appear at once as a thin
spectral gradient running along the bezel: mint (#00FF99) -> cyan (#38E8FF) ->
magenta (#FF3D8B) -> amber (#FFB020). Brighter and more ornate than the other
plates, but the center stays just as empty and low-contrast.
```

---

## 4. B그룹 — 진행 단계 배경 5종 (sub_bg img2img)

**공통 설정**: 입력 = `sub_bg` (또는 확정된 A그룹 배경) · **denoise / strength 0.25 ~ 0.35** · 구조 보존.
> strength를 0.4 이상 올리면 구조가 무너져서 스프라이트 스왑이 튑니다. 0.3 근처를 유지하세요.

**공통 지시문** (B1~B5 앞에 붙임)
```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the
reference image. Change ONLY the lighting, neon color and overall brightness.
Do not add or remove any object. Do not add text.
```

### B1 — 룰렛 / 기대
```
Bring all edge neon up to full brightness in mint (#00FF99). Indicator pips lit
and lively. Slightly warmer overall. Energetic, anticipatory.
```

### B2 — 퍼즐 가이드 / 집중
```
Dim the whole plate by about 30%. Reduce edge neon to a thin cyan (#38E8FF)
outline only; switch off most indicator pips. Very calm and quiet, so foreground
content reads clearly.
```

### B3 — 자물쇠 대기 / 긴장
```
Darken the plate. Neon magenta (#FF3D8B) rim light concentrated along the BOTTOM
band only; the top and sides fall to near-unlit warm grey. Tense, waiting.
```

### B4 — 해금 연출 / 보상
```
Warm amber (#FFB020) bloom washing inward from all four edges toward the center,
lifting the center from charcoal to a warm lit grey. Neon at maximum. Celebratory,
radiant.
```

### B5 — 컬렉션·결과 / 진열
```
Raise overall brightness; the base warm grey becomes noticeably lighter and more
even. Flat museum-style lighting, minimal neon, no vignette falloff. Neutral and
display-like.
```

---

## 5. 파일명 · PIMMotion 반영값

```
assets/assetsIngame/
  bg_plate_A1_observe.png     bg_plate_B1_roulette.png
  bg_plate_A2_logic.png       bg_plate_B2_guide.png
  bg_plate_A3_cipher.png      bg_plate_B3_wait.png
  bg_plate_A4_spatial.png     bg_plate_B4_unlock.png
  bg_plate_A5_composite.png   bg_plate_B5_collection.png
```

**박스는 1개만 만듭니다.** 10장은 그 박스의 **상태(배리에이션)**로 들어갑니다.

```jsonc
{
  "id": "bg_plate", "role": "background", "type": "image",
  "frameType": "fullframe",          // 1920×1080 전체
  "x": 0, "y": 0, "w": 1920, "h": 1080, "z": 0,
  "continuity": "persist",           // 씬 넘어가도 파괴/재생성 금지
  "crossSceneId": "BG_MAIN",
  "states": [
    {"id":"s1","name":"A1_관찰","assetId":"bg_plate_A1_observe"},
    {"id":"s2","name":"A2_논리","assetId":"bg_plate_A2_logic"},
    {"id":"s3","name":"A3_암호","assetId":"bg_plate_A3_cipher"},
    {"id":"s4","name":"A4_공간","assetId":"bg_plate_A4_spatial"},
    {"id":"s5","name":"A5_복합","assetId":"bg_plate_A5_composite"},
    {"id":"s6","name":"B1_룰렛","assetId":"bg_plate_B1_roulette"},
    {"id":"s7","name":"B2_가이드","assetId":"bg_plate_B2_guide"},
    {"id":"s8","name":"B3_대기","assetId":"bg_plate_B3_wait"},
    {"id":"s9","name":"B4_해금","assetId":"bg_plate_B4_unlock"},
    {"id":"s10","name":"B5_컬렉션","assetId":"bg_plate_B5_collection"}
  ],
  "defaultStateId": "s2"
}
```

- 배경 전환 = `setState` 한 줄. **C# 0줄**(리스킨 경계 유지).
- A그룹 전환(라운드 넘어감)에만 디졸브 0.4s, B그룹 전환은 컷 또는 0.15s 크로스페이드.

## 6. 배치 금지 구역 (sub_bg 실측 기준 · 1920×1080 환산)

| 구역 | 범위 | 사유 |
|---|---|---|
| 상단 밴드 | y < 110 | 베젤 기계 구조물 |
| 하단 밴드 | y > 940 | 베젤 기계 구조물 |
| 좌우 밴드 | x < 150 / x > 1770 | 베젤 기계 구조물 |
| **네 모서리** | 각 모서리 190×190 | **라운드 코너** — 여기 박스를 놓으면 잘려 보임 |

→ **실질 안전 배치 영역: x 150~1770, y 110~940 (1620×830).** HUD를 밴드 위에 얹고 싶으면 밴드 안쪽 경계에 맞춰 반투명 없이 올리는 게 낫습니다(베젤 위에 겹치면 픽셀 구조와 싸움).

---

## 7. C그룹 — 아날로그 / 레트로 / VHS 3종

### 7.1 먼저 — 8비트와의 충돌 (★)

VHS·아날로그는 **소프트·번짐·흔들림**이고 8비트는 **하드 엣지**입니다. 한 프롬프트에 그냥 같이 넣으면 서로 상쇄돼서 "흐릿한 픽셀 그림"이라는 최악이 나옵니다. 해결은 **층 분리**:

> **밑그림은 하드 픽셀아트 그대로 두고, VHS 손상은 그 위에 별도 레이어로 얹는다.**
> → "픽셀아트를 VCR로 재생한 화면"으로 읽힘. 아래 프롬프트의 `CONCEPT` 줄이 이 역할을 합니다.

**섞어 쓰기 규칙**: C그룹은 A/B와 계열이 달라서 **한 라운드 안에서 8비트↔VHS를 오가면 안 됩니다.** 갈아탈 거면 **라운드 단위**로(= 카테고리 배경을 통째로 C로 교체), 또는 C를 **특정 시퀀스 전용**으로 두세요.

**정지 이미지의 함정**: 진짜 VHS는 노이즈가 매 프레임 움직입니다. PNG 한 장에 노이즈를 구워두면 "얼어붙은 노이즈"로 보여서 오히려 싸구려가 됩니다.
→ 움직임이 필요하면 **노이즈 오버레이만 2~3장 따로** 뽑아 100ms 루프로 상태 스왑(에셋 기반 애니메이션, C# 0줄).

### 7.2 공통 헤더 (C1~C3 앞에 붙임 · A그룹 헤더와 다름)

```
A 16:9 empty background plate for a retro arcade game UI, 1920x1080.

BASE: warm grey throughout — deep warm charcoal (#2A2724) in the center rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges. Warm neutral
grey, NOT blue-grey, NOT black.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat, low-contrast, quiet.
All detail is pushed to the top band, bottom band and left/right margins, forming a
thin bezel hugging the screen edge. Small inner corner radius. Flat straight-on
view, no perspective, no horizon, no floor grid.

ANALOG DISCIPLINE (critical): every analog artifact — noise, tracking lines, chroma
bleed, warble, dropout — must stay LOW AMPLITUDE across the central area and may only
be strong inside the outer bands. The center must stay clean enough to read UI on top.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon,
logo, watermark, text, letters, numbers, character, person, creature, timecode,
date stamp, "PLAY" / "REC" / "SP" indicator, or a dominant grid across the center.
```

> 마지막 줄의 `timecode / date stamp / PLAY·REC 표시` 금지가 핵심입니다. VHS 프롬프트는 **거의 항상** 우상단에 타임코드나 "▶ PLAY"를 그려 넣습니다.

### C1 — VHS 플레이백 *(기본 · A그룹 대체 프리셋)*

```
CONCEPT: an 8-bit pixel-art machine bezel being played back on a worn VHS tape.
The underlying artwork keeps hard nearest-neighbour pixel edges; the VHS damage sits
ON TOP as a separate layer, so it reads as "pixel art through a VCR", not as a
blurry painting.

ARTIFACTS: horizontal tracking noise bands drifting near the top and bottom edges,
RGB chroma bleed smearing to the right of every neon element, soft luminance halo,
fine analog grain, faint interlace comb on high-contrast edges, and a band of
head-switching tear along the very bottom 3% of the frame.

COLOR: warm grey base slightly desaturated with lifted, milky blacks (never pure
black). Neon mint (#00FF99) and magenta (#FF3D8B) bleed and halate the most.
```

### C2 — CRT 브라운관 *(B2 가이드 자리 · 텍스트 많은 화면용)*

```
CONCEPT: the same machine bezel seen on a warm, softly curved CRT monitor.
The pixel structure stays hard-edged underneath; the CRT behaviour is the layer on top.

ARTIFACTS: visible phosphor scanlines, subtle RGB triad texture, gentle barrel
curvature implied only by corner falloff (the plate itself stays flat and rectangular),
soft blooming around every lit element, and a slight vertical roll bar sitting in the
upper third at very low contrast.

COLOR: warm grey base with a faint amber phosphor cast. Neon cyan (#38E8FF) and mint
(#00FF99) glow with a soft round bloom rather than a hard edge.
Calm, steady, comfortable to look at for a long time — this plate sits under
text-heavy content.
```

### C3 — 열화 테이프 *(A3 암호 자리 · 미스터리 계열)*

```
CONCEPT: the same machine bezel recovered from a badly degraded, sun-faded tape.
Hard pixel edges survive underneath; the decay is layered over them.

ARTIFACTS: intermittent dropout — short white and black dashes scattered along the top
and side bands; a wobbling, unstable left edge (time-base error); heavy grain; smeared
chroma drifted off-register; a soft crease of tape damage crossing one corner.
The center stays comparatively intact.

COLOR: heavily faded and warm — the grey has yellowed toward ochre, blacks are lifted
and murky, saturation is low overall. Neon magenta (#FF3D8B) survives best and reads
as sickly pink; mint is dulled toward grey-green.
Unsettling, forgotten, archival.
```

### 7.3 파일명 · 배치

```
assets/assetsIngame/
  bg_plate_C1_vhs.png
  bg_plate_C2_crt.png
  bg_plate_C3_decay.png
  bg_noise_ovl_01.png ~ 03.png    # (선택) 노이즈 오버레이 루프용
```

- 동일한 `bg_plate` 박스의 **상태 s11~s13**으로 추가(§5 구조 그대로).
- 노이즈 오버레이를 쓸 경우: **별도 박스** `bg_noise` (`frameType: fullframe`, `z: 1`, 알파 PNG,
  `continuity: persist`) + 상태 3개 100ms 루프. 배경 판과 독립이라 어떤 배경 위에도 얹힘.
