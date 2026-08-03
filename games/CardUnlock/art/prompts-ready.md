# 배경 프롬프트 완성본 — 조립 없이 바로 붙여넣기

> 각 블록이 **자체완결**입니다. 공통 헤더를 따로 합칠 필요 없이 코드블록 하나를 통째로 복사해서 넣으세요.
> 설계 근거·검수 결과는 `bg-variations.md`, 원칙은 `bg-prompt.md`.
>
> - **A1~A5** = 게임 카테고리별 (신규 생성)
> - **B1~B5** = 진행 단계별 (**img2img** — `sub_bg` 필요, strength 0.25~0.35)
> - **C1~C3** = 아날로그/VHS (신규 생성)
> - **N1** = 노이즈 오버레이 (알파 PNG, 선택)
>
> 전부 **1920×1080**. 툴에 해상도 입력란이 따로 있으면 거기에도 1920×1080을 넣으세요.

---

# A그룹 — 게임 카테고리 배경 5종 (신규 생성)

## A1 · 관찰·탐색 (Observation) — 시안
> 틀린그림찾기 · 개수세기 · 그림자매칭 · 미로경로

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

CONCEPT: an optical inspection bay. The machinery along the screen edge reads as lens
housings, iris rings, calibration ticks and thin fiber-optic runs.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels upscaled 4x,
hard nearest-neighbour edges, no anti-aliasing, no blur). Limited palette, ordered
dithering for all gradients. CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey throughout — deep warm charcoal (#2A2724) in the center rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges. Warm neutral grey,
NOT blue-grey, NOT black.

NEON: neon cyan (#38E8FF) dominant, used as cool clean examination light — thin glowing
tubes and edge-lit seams only, never solid shapes. A few tiny mint (#00FF99) status pips.
Total neon coverage under 5% of the frame. The center is very slightly brighter than
usual, as if lit for close inspection.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat low-contrast warm grey with
faint dithering and a soft vignette. All detail is pushed to the top band, bottom band and
left/right margins, forming a thin bezel of chunky pixel-art machinery hugging the screen
edge. Keep the inner corner radius SMALL so the corners stay usable. Perfectly flat
straight-on view, no perspective, no vanishing point, no horizon, no floor grid. Even dim
lighting, corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, or a dominant regular grid
across the center.
```

## A2 · 논리·수리 (Logic) — 민트 *(sub_bg 계열 · 기본값)*
> 아이콘연산 · 도형규칙 · 논리추론 · 진법변환

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

CONCEPT: a computation rack. The machinery along the screen edge reads as heat-sink fins,
ventilation slots, cable looms and rivet rows.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels upscaled 4x,
hard nearest-neighbour edges, no anti-aliasing, no blur). Limited palette, ordered
dithering for all gradients. CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey throughout — deep warm charcoal (#2A2724) in the center rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges. Warm neutral grey,
NOT blue-grey, NOT black.

NEON: neon mint (#00FF99) dominant as steady operating light — thin glowing tubes and
edge-lit seams only, never solid shapes. Small magenta (#FF3D8B) and cyan (#38E8FF)
indicator pips. Total neon coverage under 5% of the frame. Calm, neutral,
everyday-operation mood.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat low-contrast warm grey with
faint dithering and a soft vignette. All detail is pushed to the top band, bottom band and
left/right margins, forming a thin bezel of chunky pixel-art machinery hugging the screen
edge. Keep the inner corner radius SMALL so the corners stay usable. Perfectly flat
straight-on view, no perspective, no vanishing point, no horizon, no floor grid. Even dim
lighting, corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, or a dominant regular grid
across the center.
```

## A3 · 암호·해독 (Cipher) — 마젠타
> 시저암호 · 모스부호 · 심볼사전 · 아나그램

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

CONCEPT: a cryptography desk. The machinery along the screen edge reads as rotor drums,
punched tape reels, thin slotted apertures and coiled wiring.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels upscaled 4x,
hard nearest-neighbour edges, no anti-aliasing, no blur). Limited palette, ordered
dithering for all gradients. CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey pushed toward a dusky plum-tinted grey while staying warm — deep
warm charcoal (#2A2724) in the center rising to mid warm grey (#3E3A35) and dusty warm
grey (#6B645C) at the edges. NOT blue-grey, NOT black. Overall darker than the other plates.

NEON: neon magenta (#FF3D8B) dominant with a deep violet bloom — thin glowing tubes and
edge-lit seams only, never solid shapes. Mint (#00FF99) reduced to rare tiny pips. Total
neon coverage under 5% of the frame. Secretive, low-lit mood.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat low-contrast warm grey with
faint dithering and a soft vignette. All detail is pushed to the top band, bottom band and
left/right margins, forming a thin bezel of chunky pixel-art machinery hugging the screen
edge. Keep the inner corner radius SMALL so the corners stay usable. Perfectly flat
straight-on view, no perspective, no vanishing point, no horizon, no floor grid. Even dim
lighting, corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, or a dominant regular grid
across the center.
```

## A4 · 공간·좌표 (Spatial) — 앰버
> 방향추적 · 좌표격자 · 오버레이 · 시계각도

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

CONCEPT: a navigation console. The machinery along the screen edge reads as brass-toned
bezels, gimbal rings, engraved bearing ticks and dial housings. Slightly older and more
analogue than the other plates.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels upscaled 4x,
hard nearest-neighbour edges, no anti-aliasing, no blur). Limited palette, ordered
dithering for all gradients. CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey leaning toward aged brass-grey — deep warm charcoal (#2A2724) in the
center rising to mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges. Warm
neutral grey, NOT blue-grey, NOT black.

NEON: neon amber (#FFB020) dominant as warm instrument light — thin glowing tubes and
edge-lit seams only, never solid shapes. Small cyan (#38E8FF) indicator pips. Total neon
coverage under 5% of the frame.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat low-contrast warm grey with
faint dithering and a soft vignette. All detail is pushed to the top band, bottom band and
left/right margins, forming a thin bezel of chunky pixel-art machinery hugging the screen
edge. Keep the inner corner radius SMALL so the corners stay usable. Perfectly flat
straight-on view, no perspective, no vanishing point, no horizon, no floor grid. Even dim
lighting, corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, or a dominant regular grid
across the center.
```

## A5 · 복합·조합 (Composite) — 프리즘
> 순서배열 · 다단복합 · 음계리듬 · 색배열 — 최고 난이도 그룹

```
A 16:9 empty background plate for a retro-futuristic arcade game UI, 1920x1080.

CONCEPT: a prism core. The machinery along the screen edge reads as faceted crystal
mounts, split light guides and layered plating. More ornate than the other plates.

PIXEL SCALE: 8-bit pixel art on a coarse pixel grid (480x270 logical pixels upscaled 4x,
hard nearest-neighbour edges, no anti-aliasing, no blur). Limited palette, ordered
dithering for all gradients. CRT phosphor glow, faint scanlines, subtle chromatic fringing.

BASE COLOR: warm grey throughout — deep warm charcoal (#2A2724) in the center rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges. Warm neutral grey,
NOT blue-grey, NOT black.

NEON: all four neons appear at once as a thin spectral gradient running along the bezel —
mint (#00FF99) into cyan (#38E8FF) into magenta (#FF3D8B) into amber (#FFB020). Thin
glowing tubes and edge-lit seams only, never solid shapes. Brighter than the other plates,
but total neon coverage still under 5% of the frame.

COMPOSITION: the central 70% x 70% stays just as EMPTY as the other plates despite the
brighter bezel — flat low-contrast warm grey with faint dithering and a soft vignette. All
detail is pushed to the top band, bottom band and left/right margins, forming a thin bezel
of chunky pixel-art machinery hugging the screen edge. Keep the inner corner radius SMALL
so the corners stay usable. Perfectly flat straight-on view, no perspective, no vanishing
point, no horizon, no floor grid. Corners vignetted.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, or a dominant regular grid
across the center.
```

---

# B그룹 — 진행 단계 배경 5종 (img2img)

> **입력 이미지**: `sub_bg` (또는 확정된 A그룹 배경 중 하나)
> **strength / denoise: 0.25 ~ 0.35** — 0.4 이상은 구조가 무너져 스프라이트 스왑이 튑니다.
> 같은 라운드 안에서 연속 전환되므로 **구조가 반드시 동일**해야 합니다.

## B1 · 룰렛 — 기대

```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the reference
image. Change ONLY the lighting, neon color and overall brightness. Do not add or remove
any object. Do not move anything. Do not add text, numbers or logos.

Bring all edge neon up to full brightness in neon mint (#00FF99). Indicator pips lit and
lively. Slightly warmer overall. Energetic, anticipatory. The center stays empty and
low-contrast.
```

## B2 · 퍼즐 가이드 — 집중

```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the reference
image. Change ONLY the lighting, neon color and overall brightness. Do not add or remove
any object. Do not move anything. Do not add text, numbers or logos.

Dim the whole plate by about 30%. Reduce edge neon to a thin neon cyan (#38E8FF) outline
only; switch off most indicator pips. Very calm and quiet so foreground content reads
clearly. The center stays empty and low-contrast.
```

## B3 · 자물쇠 대기 — 긴장

```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the reference
image. Change ONLY the lighting, neon color and overall brightness. Do not add or remove
any object. Do not move anything. Do not add text, numbers or logos.

Darken the plate. Concentrate a neon magenta (#FF3D8B) rim light along the BOTTOM band
only; the top and side bands fall to near-unlit warm grey. Tense, waiting. The center stays
empty and low-contrast.
```

## B4 · 해금 연출 — 보상

```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the reference
image. Change ONLY the lighting, neon color and overall brightness. Do not add or remove
any object. Do not move anything. Do not add text, numbers or logos.

A warm amber (#FFB020) bloom washes inward from all four edges toward the center, lifting
the center from charcoal to a warm lit grey. Neon at maximum brightness. Celebratory and
radiant, but the center stays free of objects.
```

## B5 · 컬렉션·결과 — 진열

```
Keep the exact same layout, geometry, bezel machinery and pixel structure as the reference
image. Change ONLY the lighting, neon color and overall brightness. Do not add or remove
any object. Do not move anything. Do not add text, numbers or logos.

Raise the overall brightness; the base warm grey becomes noticeably lighter and more even.
Flat museum-style lighting, minimal neon, no vignette falloff. Neutral and display-like.
The center stays empty.
```

---

# C그룹 — 아날로그 / 레트로 / VHS 3종 (신규 생성)

> 밑그림은 하드 픽셀 유지, 아날로그 손상은 그 위 별도 레이어 — "픽셀아트를 VCR로 재생한 화면".
> **A/B와 한 라운드 안에서 섞지 마세요.** 갈아탈 거면 라운드 단위로.

## C1 · VHS 플레이백 *(기본 · A그룹 대체 프리셋)*

```
A 16:9 empty background plate for a retro arcade game UI, 1920x1080.

CONCEPT: an 8-bit pixel-art machine bezel being played back on a worn VHS tape. The
underlying artwork keeps hard nearest-neighbour pixel edges; the VHS damage sits ON TOP as
a separate layer, so it reads as "pixel art through a VCR", not as a blurry painting.

BASE COLOR: warm grey throughout — deep warm charcoal (#2A2724) in the center rising to
mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges, slightly desaturated
with lifted milky blacks (never pure black). Warm neutral grey, NOT blue-grey.

ARTIFACTS: horizontal tracking noise bands drifting near the top and bottom edges, RGB
chroma bleed smearing to the right of every neon element, soft luminance halo, fine analog
grain, faint interlace comb on high-contrast edges, and a band of head-switching tear along
the very bottom 3% of the frame. Neon mint (#00FF99) and magenta (#FF3D8B) bleed and
halate the most.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat, low-contrast, quiet. All
detail is pushed to the top band, bottom band and left/right margins, forming a thin bezel
hugging the screen edge. Small inner corner radius. Flat straight-on view, no perspective,
no horizon, no floor grid.

ANALOG DISCIPLINE (critical): every analog artifact — noise, tracking lines, chroma bleed,
warble — must stay LOW AMPLITUDE across the central area and may only be strong inside the
outer bands. The center must stay clean enough to read UI on top.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, timecode, date stamp,
"PLAY" / "REC" / "SP" indicator, or a dominant grid across the center.
```

## C2 · CRT 브라운관 *(B2 가이드 자리 · 텍스트 많은 화면용)*

```
A 16:9 empty background plate for a retro arcade game UI, 1920x1080.

CONCEPT: an 8-bit pixel-art machine bezel seen on a warm, softly curved CRT monitor. The
pixel structure stays hard-edged underneath; the CRT behaviour is a layer on top.

BASE COLOR: warm grey with a faint amber phosphor cast — deep warm charcoal (#2A2724) in
the center rising to mid warm grey (#3E3A35) and dusty warm grey (#6B645C) at the edges.
Warm neutral grey, NOT blue-grey, NOT black.

ARTIFACTS: visible phosphor scanlines, subtle RGB triad texture, gentle barrel curvature
implied only by corner falloff (the plate itself stays flat and rectangular), soft blooming
around every lit element, and a slight vertical roll bar sitting in the upper third at very
low contrast. Neon cyan (#38E8FF) and mint (#00FF99) glow with a soft round bloom rather
than a hard edge.

COMPOSITION: the central 70% x 70% stays almost EMPTY — flat, low-contrast, quiet. All
detail is pushed to the top band, bottom band and left/right margins, forming a thin bezel
hugging the screen edge. Small inner corner radius. Flat straight-on view, no perspective,
no horizon, no floor grid.

ANALOG DISCIPLINE (critical): scanlines, bloom and roll bar must stay LOW AMPLITUDE across
the central area. The center must stay clean enough to read text on top. Calm, steady,
comfortable to look at for a long time.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, timecode, date stamp,
"PLAY" / "REC" / "SP" indicator, or a dominant grid across the center.
```

## C3 · 열화 테이프 *(A3 암호 자리 · 미스터리 계열)*

```
A 16:9 empty background plate for a retro arcade game UI, 1920x1080.

CONCEPT: an 8-bit pixel-art machine bezel recovered from a badly degraded, sun-faded tape.
Hard pixel edges survive underneath; the decay is layered over them.

BASE COLOR: heavily faded and warm — the grey has yellowed toward ochre, blacks are lifted
and murky, saturation is low overall. Still warm neutral grey at heart, NOT blue-grey.

ARTIFACTS: intermittent dropout — short white and black dashes scattered along the top and
side bands; a wobbling, unstable left edge (time-base error); heavy grain; smeared chroma
drifted off-register; a soft crease of tape damage crossing one corner. Neon magenta
(#FF3D8B) survives best and reads as sickly pink; mint is dulled toward grey-green.
Unsettling, forgotten, archival.

COMPOSITION: the central 70% x 70% stays almost EMPTY and comparatively intact — flat,
low-contrast, quiet. All detail and damage is pushed to the top band, bottom band and
left/right margins, forming a thin bezel hugging the screen edge. Small inner corner radius.
Flat straight-on view, no perspective, no horizon, no floor grid.

ANALOG DISCIPLINE (critical): dropout, warble and grain must stay LOW AMPLITUDE across the
central area and may only be strong inside the outer bands. The center must stay clean
enough to read UI on top.

MUST NOT CONTAIN: any window, panel, card, slot, button, dialog, HUD, meter, icon, logo,
watermark, text, letters, numbers, character, person, creature, timecode, date stamp,
"PLAY" / "REC" / "SP" indicator, or a dominant grid across the center.
```

---

# N1 · 노이즈 오버레이 (선택 · 알파 PNG 3장)

> 정지 배경에 노이즈를 구우면 "얼어붙은 노이즈"로 보입니다. 움직임이 필요하면 이것만 따로 3장 뽑아
> 100ms 루프로 스왑하세요. 배경 판과 독립이라 A·B·C 어떤 배경 위에도 얹힙니다.
> **3장을 뽑을 때 프롬프트는 그대로 두고 시드만 바꾸세요.**

```
A 1920x1080 transparent PNG overlay layer of analog video noise, nothing else.

Fully transparent background. On it: sparse horizontal VHS tracking noise streaks, fine
white and black dropout dashes, a faint band of RGB chroma smear, and light analog grain.
Elements are thin, scattered and irregular.

Keep the whole overlay very light — around 12% coverage. Concentrate the streaks near the
top and bottom edges; the central area carries only faint grain so that UI underneath stays
readable.

Hard-edged pixels, no anti-aliasing, no blur. Monochrome white and black except for the
chroma smear band.

MUST NOT CONTAIN: any solid background fill, any opaque area, checkerboard transparency
pattern, text, numbers, timecode, logo, icon, character, or any recognisable object.
```

> 받은 뒤 확인: **배경이 진짜 투명한가.** 제미나이류는 투명 대신 **격자무늬를 실제 픽셀로** 그려 넣습니다.
> 그 경우 에셋에디터의 자동 배경제거(격자 패턴 감지)로 진짜 알파로 변환하세요 — `asset-pipeline-spec.md` §2.

---

# 산출 파일명 (그대로 저장)

```
assets/assetsIngame/
  bg_plate_A1_observe.png     bg_plate_B1_roulette.png     bg_plate_C1_vhs.png
  bg_plate_A2_logic.png       bg_plate_B2_guide.png        bg_plate_C2_crt.png
  bg_plate_A3_cipher.png      bg_plate_B3_wait.png         bg_plate_C3_decay.png
  bg_plate_A4_spatial.png     bg_plate_B4_unlock.png
  bg_plate_A5_composite.png   bg_plate_B5_collection.png   bg_noise_ovl_01~03.png
```

- 13장 전부 **같은 `bg_plate` 박스 1개의 상태(states)**로 들어갑니다 → 전환은 `setState` 한 줄, C# 0줄.
- `bg_noise_ovl_*`만 **별도 박스** (`frameType: fullframe`, `z: 1`, `continuity: persist`).
- 매핑 JSON은 `bg-variations.md` §5.
