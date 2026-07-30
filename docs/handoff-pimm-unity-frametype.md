# 코워크 핸드오프 — 피모션 게임 빌드: 좌표·frameType(프레임그래픽/크롭/풀프레임) 정본

_발신: coworking-review 세션 → 수신: 코워크(핌플레이어 빌드 + 플러그인 유니티 스킬 담당) · 2026-07-30_
_배경: 이정민 현장 보고(좌표 어긋남) + 대표 지시. **가장 시급 = README·스킬에 프레임그래픽 설명이 없음** → 먼저 채운다._
_기준 = **현재 툴 `tool/PIMM_UnityGameCreator.ver1.14.html`** (툴은 이번에 안 고침). 정본 스킬: `.claude/skills/pimm-handoff/SKILL.md`(이번에 §3·§6 갱신)._

---

## 0. 무엇이 문제였나 (근본원인 2겹)
1. **구버전 export 사용** — 이정민의 `ROULETTE_NEW_layout.json`은 박스에 `x/y/w/h/assetFile/role/continuity`만 있고 `frameType/crop/clip/unity`가 없다. **현재 툴(v1.14)은 `assetFile`을 안 쓰고 `assetId`를 쓴다** → 그 파일은 프레임 파이프라인(v1.12+) **이전의 옛 내보내기**. 유니티가 fit을 알 수 없어 추측 → 어긋남.
2. **좌표/프레임 개념 미이해** — 박스는 1920×1080 좌표. 박스와 다른 비율의 에셋을 만들고 프레임모드를 안 골랐다. 이걸 위해 **cropframe/framegraphic/fullframe**가 있는 것.

그리고 **문서 gap**: README·(배포)스킬에 **framegraphic 설명이 없고**, cropframe이 **cover**라는 사실이 어디에도 명시돼 있지 않았다 → 유니티가 `preserveAspect`(stretch/contain)로 떨어져 cover가 안 나옴. (이정민이 낸 진단·해법이 정확함.)

---

## 1. 현재 툴이 실제 내보내는 것 (v1.14 · 신뢰 가능한 스키마)
> 코워크가 받는 레이아웃 JSON. **fit 정보는 이미 다 들어있다** — 옛 파일이 아니라 v1.14로 재export하면 됨.

최상위: `sequenceId, phaseId, seqLabel, resolution:[1920,1080], background, bgm, prefabs[], activeSceneId, scenes[](각 boxes[]), interactions[], boxes[](활성씬·하위호환)`

박스 1개(`encodeHandoffBox`):
- `index, id, type, x, y, w, h`(정수·1920×1080 픽셀), `opacity, locked, hidden`, **`unity`**(anchorMin/Max — **Y-flip 반영 완료**, 그대로 사용), `role`
- 이미지/프리팹/텍스트별: `subtype, assetId, states[], defaultStateId, activeStateId, fps, hasImage` / 텍스트 `text,fontSize,fontColor,align,variants` / 프리팹 `prefabId,instanceIndex,stateId`
- `span{fromInteraction,toInteraction}`, **`continuity`**(persist/change/enter/exit), `crossSceneId`
- **`clip`**(+`unityMask`: RectMask2D/SpriteMask), **`crop`{x,y,w,h}**(0..1 정규화, +`cropUnity`{mode:"spriteRect"})
- **`frameType`**(cropframe/fullframe/framegraphic) + **`frameTypeUnity`**(fit 힌트) + framegraphic이면 `ratioLock, frameSrcW, frameSrcH`
- `prompts[]`, `events[]{trigger,commands[]}`

씬/흐름: `scenes[]{sceneId,name,order,sceneNote,boxes[]}`, `interactions[]{id,label,note,action}`.

---

## 2. ★ frameType 3모드 — 이게 핵심 (README·스킬에 반드시 이 표를 넣을 것)
기준 좌표 = **1920×1080**. 각 모드의 **에디터 실제 렌더(object-fit)가 곧 재현 목표**다.

| frameType | 에디터 실제 렌더 = 재현 목표 | Unity 매핑 |
|---|---|---|
| **cropframe** (크롭프레임·기본) | **`object-fit: cover`** — 박스 W×H를 꽉 채우고 넘침 **중앙 크롭**. (button subtype만 `contain`.) `crop` 있으면 그 영역만. | 박스 W×H RectTransform + **cover(중앙크롭)** 스프라이트. **`preserveAspect` 금지** → §3 헬퍼. |
| **fullframe** (풀프레임) | 이미지 = **1920×1080 전체**, 위치가 이미지에 구워짐. 박스=콘텐츠영역(주석). | 풀스크린 RectTransform(anchorMin 0,0 / anchorMax 1,1). 박스좌표 배치에 안 씀. |
| **framegraphic** (프레임그래픽) | `object-fit: fill` — **박스가 이미지 원본비율로 생성돼(ratioLock) fill이어도 왜곡 0**. `frameSrcW/H`=원본. | 박스 rect(=이미지 원본크기)에 스프라이트 그대로. **좌표·크기 픽셀 그대로 신뢰.** |

**사용자에게 설명하는 법(코워크가 할 수 있어야 함)**: 박스는 1920×1080 위의 '틀'.
- 틀에 맞춰 채운다(에셋 비율 달라도 OK) → **cropframe** (cover로 채우고 넘침 크롭).
- 에셋 원본 크기/비율을 그대로 살려 특정 위치에 놓는다 → **framegraphic** (박스가 이미지 크기로 생성되니 좌표만 맞추면 끝, 왜곡 없음).
- 화면 전체 배경 → **fullframe**.
> "박스로 만들었으면 에셋도 같은 비율로 제작" = cropframe에서 왜곡 피하려는 것. "반대면 프레임그래픽으로 이미지 크기에 맞춰 좌표에 배치" = framegraphic. **이 셋이 없으면 피모션을 쓰는 의미가 없다.**

---

## 3. cover 매핑 = Sprite.Create 중앙 크롭 (공용 헬퍼 · 마스크 불필요)
cropframe(cover)는 **원본 텍스처에서 박스 비율에 맞춘 중앙 사각형**을 `Sprite.Create` rect로 주면 cover와 수학적으로 동일(마스크 오브젝트 불필요, 렌더비용 그대로).
```csharp
static Sprite CoverSprite(Texture2D tex, float boxW, float boxH){
  float tr = (float)tex.width/tex.height, br = boxW/boxH;
  float cw = tex.width, ch = tex.height;
  if (tr > br) cw = tex.height * br;   // 원본이 더 넓음 → 좌우 크롭
  else         ch = tex.width  / br;   // 원본이 더 높음 → 상하 크롭
  float px = (tex.width-cw)*0.5f, py = (tex.height-ch)*0.5f;
  return Sprite.Create(tex, new Rect(px,py,cw,ch), new Vector2(0.5f,0.5f));
}
```
- **GameRoulette / GameBoxSort / GamePIMMotion이 이 하나를 공유** → 클래스별 `preserveAspect`(stretch/contain) 불일치 제거·재발 방지. (GameBoxSort.cs:486 "// GamePIMMotion과 동일" 주석도 실제와 맞게 정리.)
- `crop{x,y,w,h}`(0..1) 있으면 **그걸 우선**(정규화→픽셀 rect). button만 contain. framegraphic/fullframe은 cover 아님(§2 표).

---

## 4. 클립 / 크롭 / 좌표
- **clip**: rect·roundrect(radius)·ellipse·maskBox → 사각/둥근=**RectMask2D**, 타원/커스텀=**SpriteMask**(알파). `unityMask` 힌트 그대로.
- **crop**: 비파괴 `{x,y,w,h}`(0..1) → 스프라이트 rect/uv로 그 영역만.
- **좌표**: `unity.anchorMin/Max`는 Y-flip 완료 → 그대로. 픽셀 좌표는 1920×1080 기준.

---

## 5. 적용 전 스터디 게이트 (필수 · 바로 만들지 말 것)
복잡한 지시를 받자마자 씬/코드를 건드리지 않는다.
1. **스키마 완독**: `resolution`, 박스별 `frameType/crop/clip/unity/continuity`.
2. **모든 메모 완독**: `sceneNote`, 박스 메모, `prompts`, 인터랙션 성공/실패 메모.
3. **적용순서를 말로 먼저 제시하고 확인받은 뒤** 빌드. (실사용 피드백: 한 번에 안 읽고 바로 적용해 누락 발생.)

---

## 6. 이정민 현장 즉시조치 (별도 안내)
1. **v1.14로 재export** — 지금 쓰는 `..._layout.json`에 `assetFile`이 있으면 **옛 파일**이다. 폐기하고 현재 툴에서 다시 내보낼 것(그래야 frameType/crop/unity 포함).
2. **프레임모드 선택**: 틀에 채움=cropframe / 이미지 원본크기 유지=framegraphic / 배경=fullframe.
3. cropframe인데 에셋 비율이 박스와 다르면 → cover로 중앙크롭됨(정상). 특정 부분만 보이게 하려면 툴에서 **crop(자르기)** 지정.
4. 에셋을 박스와 다른 크기로 만들었어도 framegraphic이면 문제없음(박스가 이미지 크기로 생성). cropframe로 정확히 맞추려면 에셋을 박스 비율로 제작.

---

## 7. 코워크 적용 체크리스트 (플러그인 패치)
- [ ] 플러그인 유니티 빌드 스킬 + **README에 §2 frameType 3모드 표(특히 framegraphic) 추가** — 현재 없음(최우선).
- [ ] cropframe = **object-fit: cover** 명시 + §3 `CoverSprite` 공용 헬퍼 채택, `preserveAspect` 사용 금지 명문화.
- [ ] 세 게임 클래스(GameRoulette/GameBoxSort/GamePIMMotion) fit을 헬퍼로 통일.
- [ ] §5 스터디 게이트(완독→적용순서 제시→확인) 절차 추가.
- [ ] 배포 스킬을 repo `.claude/skills/pimm-handoff/SKILL.md`(이번 갱신본)와 동기화.
- [ ] 툴 export는 이번에 **안 고침**(B 보류) — 현재 v1.14가 이미 frameType/frameTypeUnity/crop/unity를 내보냄. 필요 시 후속.

> 참고 원문: `docs/encoding-and-build.md`, `docs/asset-pipeline-spec.md`, `docs/timeline-view-spec.md`, 스킬 `.claude/skills/pimm-handoff/SKILL.md`(§3·§6 갱신). 진단 로그: `sessionlogs/심상윤/Session_세션로그/260730_0851_피모션게임툴_좌표프레임_진단_log.md`.
