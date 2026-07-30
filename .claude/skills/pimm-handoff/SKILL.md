---
name: pimm-handoff
description: PIMMotion 게임에디터가 내보낸 핸드오프 패키지(인게임에셋 정제본 + 에셋활용방식 + 게임진행방식)를 코워크가 유니티(핌플레이어)로 빌드할 때 로드하는 해석 스킬. 레이아웃뷰·타임라인뷰·프레임그래픽·크롭/풀프레임·클립·크롭·연속성·이벤트·씬/시퀀스/블록 등 PIMMotion 용어와 각 필드의 Unity 매핑, 결정론적 빌드 절차를 담는다. 트리거: PIMMotion 핸드오프 폴더/패키지, project.pimm.json, .pimmgame.json, assetsIngame, frameType/프레임그래픽, "핌모션 게임 빌드" 관련 작업.
---

# PIMMotion 핸드오프 해석 스킬 (코워크용)

> PIMMotion 게임에디터가 내보낸 **핸드오프 패키지**를 읽어 **유니티(핌플레이어)** 게임으로 빌드한다.
> 이 스킬은 그 패키지의 용어·필드를 어떻게 해석·매핑하는지 정의한다. (에디터 툴 사용법·단축키는 무관 — 다루지 않음.)
> 상세 스키마·절차 원문: repo `docs/encoding-and-build.md`, `docs/asset-pipeline-spec.md`, `docs/timeline-view-spec.md`, `docs/tool-concept.md`.

## 1. 패키지에 오는 것 (3가지 + 선택)
1. **인게임 에셋 정제본** = `assets/assetsIngame/` — 최종 씬에 실제 올라간 이미지/오디오만(dedup). 이걸 유니티 에셋으로 사용.
2. **에셋 활용방식**(슬림 config) = 각 에셋을 **어디에·얼마 크기로·어떻게** 두는지: 좌표(unity 앵커)·크기·frameType·클립·크롭·z순서·연속성.
3. **게임 진행방식**(config) = 흐름/로직: 타임라인 **블록**(씬/인터랙션/영상) 순서, 박스 **이벤트**, 성공/실패 메모, 전환.
- (선택) `encode/<SEQ#>.pimmgame.json` = 위를 임베드한 **자체완결 번들**(에셋 data URI 포함). 단독으로도 빌드 가능.
- (없음) 에디터 HTML·단축키 등 툴-사용 콘텐츠는 패키지에 없음(빌드에 불필요).

## 2. 용어 사전 (반드시 이 의미로 해석)
- **레이아웃뷰**: 1920×1080 공간에 박스(에셋)를 배치한 화면 구성. = 좌표/크기/정렬 정보의 출처.
- **타임라인뷰**: 게임 **진행 순서**(시간 아님 = 인터랙션/블록 순서). 씬→인터랙션→씬… 흐름.
- **시퀀스 / 씬 / 박스**: 시퀀스(SEQ#, 게임 한 편) ▸ 씬(화면 단위) ▸ 박스(요소). 코드(SEQ#)는 불변 키.
- **블록(타임라인)**: `scene`(씬 통째) / `interaction`(진행 지점, 성공·실패 메모) / `video`(영상 구간). 순서대로 진행.
- **이벤트**: 박스별 실행조건(trigger) + 명령(commands). 논코딩 지시문 → 유니티 동작으로 구현.
- **상태(배리에이션)**: 한 이미지박스가 가질 수 있는 여러 이미지(상태1~n). `setState`로 교체(스프라이트 스왑, 코드 아님).
- **연속성(continuity)**: `persist`(여러 씬에 걸쳐 **유지** — 오브젝트 재사용, 파괴/재생성·디졸브 없음, 공유 `crossSceneId`) / `change` / `enter` / `exit`.

## 3. frameType — 에셋 배치 3모드 (★핵심 · 좌표 어긋남의 원인은 대부분 여기)

기준 좌표계 = **1920×1080**. 박스 `x,y,w,h`는 이 좌표의 픽셀. `unity.anchorMin/Max`는 **Y-flip까지 끝난 값** → 그대로 사용. 최상위 `resolution:[1920,1080]` 확인.

각 모드는 **에디터의 실제 렌더(object-fit)가 곧 재현 목표**다. 이 fit을 안 맞추면 위치·크기가 전부 틀어진다.

| frameType | 에디터 실제 렌더 = 재현 목표 | Unity 매핑 |
|---|---|---|
| **cropframe** (크롭프레임·기본) | **`object-fit: cover`** — 이미지가 박스 W×H를 **꽉 채우고 넘치는 부분은 중앙 크롭**. (subtype=button만 `contain`.) `crop` 있으면 그 영역만. | 박스 W×H RectTransform + 스프라이트를 **cover(중앙크롭)**. **`preserveAspect` 쓰지 말 것**(§3-1 헬퍼). |
| **fullframe** (풀프레임) | 이미지 = **1920×1080 전체**(위치가 이미지에 구워짐). 박스 = 콘텐츠영역 표시용(주석). | 풀스크린 RectTransform(anchorMin 0,0 / anchorMax 1,1). 박스좌표는 배치에 안 씀. |
| **framegraphic** (프레임그래픽) | `object-fit: fill` — **단, 박스가 이미지 원본비율로 생성돼(ratioLock) fill이어도 왜곡 0.** `frameSrcW/H`=원본크기. | 박스 rect(=이미지 원본크기)에 스프라이트 그대로. **좌표·크기 픽셀 그대로 신뢰.** |

> **왜 어긋나나(실사례)**: cropframe인데 Unity가 `preserveAspect=false`(stretch)/`true`(contain)로 넣으면 cover가 안 나와 다 틀어진다. 클래스마다 제각각(stretch/contain)이면 재현 불가 → **반드시 공용 cover 헬퍼로 통일.**
>
> **개념(사용자 설명용)**: 박스는 1920×1080 위의 '틀'이다. ⑴ 틀에 맞춰 채우려면 **cropframe**(에셋 비율이 달라도 cover로 채움) ⑵ 에셋 원본 비율/크기를 그대로 살려 특정 위치에 놓으려면 **framegraphic**(박스가 이미지 크기로 생성됨) ⑶ 화면 전체 배경이면 **fullframe**. "박스로 만들었으면 에셋도 같은 비율로" 또는 "framegraphic으로 이미지 크기에 맞춰라"가 이 뜻.

### 3-1. cover 매핑 = Sprite.Create 중앙 크롭 (공용 헬퍼 · 마스크 불필요)
cropframe(=cover)는 **원본 텍스처에서 박스 비율에 맞춘 중앙 사각형을 잘라 `Sprite.Create`의 rect로** 주면 cover와 수학적으로 동일(렌더비용 그대로, 마스크 오브젝트 불필요).
```csharp
// 박스 비율(boxW:boxH)에 맞춰 원본 tex 중앙을 cover 크롭한 Sprite
static Sprite CoverSprite(Texture2D tex, float boxW, float boxH){
  float tr = (float)tex.width/tex.height, br = boxW/boxH;
  float cw = tex.width, ch = tex.height;
  if (tr > br) cw = tex.height * br;     // 원본이 더 넓음 → 좌우 크롭
  else         ch = tex.width  / br;     // 원본이 더 높음 → 상하 크롭
  float px = (tex.width - cw) * 0.5f, py = (tex.height - ch) * 0.5f;
  return Sprite.Create(tex, new Rect(px, py, cw, ch), new Vector2(0.5f, 0.5f));
}
```
- **GameRoulette / GameBoxSort / GamePIMMotion이 이 하나를 공유** → `preserveAspect` 불일치 재발 방지. (기존 클래스별 stretch/contain은 이 헬퍼로 교체.)
- `crop{x,y,w,h}`(0..1 정규화)가 있으면 **그걸 우선**(정규화→픽셀 rect로 Sprite.Create). 버튼(subtype=button)만 contain.
- framegraphic/fullframe은 cover 아님 — 위 표대로.

## 4. 클립 / 크롭 → Unity
- **clip**: `rect`·`roundrect`(radius)·`ellipse`·`maskBox` → 사각/둥근 = **RectMask2D**, 타원/커스텀 = **SpriteMask**(알파). geometry/shape로 결정론 재현.
- **crop**: 비파괴 `{x,y,w,h}`(원본 0..1 정규화) → 스프라이트 **rect/uv**로 해당 영역만.
- 좌표 Y-flip은 이미 계산됨(`unity.anchorMin/Max`). 그대로 사용.

## 5. WYSIWYG 보장 / 한계
- **픽셀 동일**: 좌표·z·클립·크롭·frameType·투명도 → config 그대로 재현.
- **유일 차이**: 텍스트박스 **폰트 렌더링**(자간/힌팅)은 브라우저↔Unity TextMesh 미세차 → **위치·크기는 맞음, 최종은 Play로 확인**.

## 6. 빌드 절차 (결정론)
0. **★ 스터디 게이트 (적용 전 필수 · 바로 만들지 말 것).** 복잡한 지시를 받자마자 코드/씬을 건드리지 않는다.
   먼저 **스키마와 모든 메모를 완독**한다: `resolution`, 각 박스 `frameType/crop/clip/unity/continuity`, **모든 `sceneNote`·박스 메모·`prompts`·인터랙션 성공/실패 메모**.
   그다음 **① 무엇을(에셋·배치) ② 어떤 순서로 적용할지**를 사용자에게 **말로 먼저 제시하고 확인받은 뒤** 빌드에 들어간다.
   (실사용 피드백: 메모를 한 번에 안 읽고 바로 적용해 누락 발생. "먼저 json 스터디 → 적용순서 제시"가 AI 활용 기본.)
1. 패키지 읽기: 활용방식(배치)·진행방식(흐름)·assetsIngame(에셋). (또는 `.pimmgame.json` 단독.)
2. **리스킨 판별**: 진행방식이 **기존 핌플레이어 메커니즘**으로 표현되면 → **config + 에셋 교체만, C# 0줄.**
3. 에셋 배치: 각 박스 frameType/clip/crop/z/연속성대로 RectTransform·스프라이트·마스크 구성.
4. 흐름 구성: 블록 순서 = 진행, 인터랙션 성공/실패 메모 = onSuccess/onFail 지시(사람이 읽는 지시문 → 구현), 연속성 persist = 오브젝트 재사용(디졸브 없음).
5. 오디오·이벤트 배선. **Play로 QC**(특히 텍스트).
6. **새 메커니즘**이면: 그 부분만 **명시적으로 플래그**하고 C# 추가. 조용히 코드 생성 금지(리스킨 경계 유지).

## 7. 원칙
- **매번 다른 게임**이므로 고정 임포터가 아니라 **이 스킬로 판단·해석해서 빌드**한다.
- 스키마는 추가만(하위호환) — 모르는 필드는 무시하되, 핵심(좌표/frameType/블록/이벤트) 누락 시 사용자에게 확인.
- 코드 임팩트 최소(리스킨 우선), 에셋 기반 애니메이션(상태 스왑·트윈), 상업적 퀄리티.
