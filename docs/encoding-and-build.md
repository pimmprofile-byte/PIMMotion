# 인코딩 & 빌드 레시피 — 게임인코딩파일 → 핌플레이어

> 이 문서는 두 가지를 고정한다.
> 1. **인코딩 번들(`.pimmgame.json`) 스키마** — 툴이 내보내는 자체완결 게임 파일.
> 2. **코워크(바이브코딩) 결정론적 빌드 절차** — {인코딩파일 + Unity + 핌플레이어 프로젝트} → 게임.
>
> 원칙: **코드 변환 임팩트 최소화(리스킨 우선) + 에셋 기반 애니메이션 + 상업적 퀄리티.**
> 관련: `tool-concept.md`(개념), `distribution-and-build.md`(배포/임포터), `backend-architecture.md`(DB).

---

## 1. 인코딩(Encoding)이란

프리미어의 "내보내기"처럼, **시퀀스(게임씬 1종)를 골라 인코딩**하면 그 게임에 필요한 모든 것이
하나로 묶여 **자체완결 파일**이 된다. 인코딩 = 데이터화된 게임 한 편.

```
인코딩 대상: 시퀀스 1개(SEQ#) [또는 프로젝트 전체]
포함물     : 에셋이미지 + 오디오(BGM/SFX) + 씬·인터랙션 흐름 + 연속성 + 상태 +
             전환 + 좌표(unity 앵커) + 프리팹 정의 + 논코딩 메모/프롬프트
결과       : SEQ#.pimmgame.json  (+ 에셋 아카이빙 폴더)
```

---

## 2. 번들 스키마 (`.pimmgame.json`)

자체완결(임베드) + 기계 파싱 우선. 필드명은 툴 내보내기(레이아웃 JSON)와 정합하며 **추가만** 한다.

```jsonc
{
  "pimmgame": "1.0",                    // 인코딩 포맷 버전
  "encodedAt": "<타임스탬프>",           // 툴이 스탬프(스크립트 밖에서)
  "project": { "id", "name", "themeId" },
  "sequence": {
    "sequenceId": "SEQ4",               // 코드명(불변, 아두이노/시리얼 파싱 키)
    "phaseId": "SEQ06A",                // theme_config phaseId
    "label": "순발력",
    "prefabPath": "COMBO/Games/Reflex", // 기존 메커니즘 매핑(리스킨 대상)
    "resolution": [1920, 1080],
    "bgm": { "assetId", "loop": true },

    "scenes": [                          // 씬 = 화면 단위(파포 슬라이드)
      { "sceneId", "name": "PressAnyKey", "order": 0,
        "boxes": [ /* 아래 box 스키마 */ ] }
    ],
    "interactions": [                    // 타임라인 가로축 = 인터랙션 순서(시간 아님)
      { "id", "label": "인터랙션1", "note",
        "action": { "type": "transition|setState|sfx|advanceScene|endMark|none",
                    "transition": { "kind": "cut|fade|dissolve|fadeBlack", "memo" },
                    "targetSceneId", "sfxAssetId",
                    "setState": { "targetBoxId", "stateId", "stateName" } } }
    ]
  },

  "prefabs": [                           // 공유 프리팹 정의(인스턴스가 참조)
    { "prefabId", "name", "assetId", "w", "h",
      "states": [ { "id", "name": "상태1", "assetId", "hasImage" } ],
      "defaultStateId" }
  ],

  "assets": {                            // 임베드(자체완결) — data URI
    "images": [ { "assetId", "name", "mime", "w", "h", "dataUri" } ],
    "audio":  [ { "assetId", "name", "mime", "role": "bgm|sfx", "dataUri" } ]
  },
  "assetArchive": {                      // 폴더로 풀 때의 경로 규칙(§4)
    "root": "PIMMplayer_JSON/<project>/<SEQ#>/",
    "map": [ { "assetId", "path": "images/bg_01.png" } ]
  }
}
```

### box 스키마 (씬 내부 요소)
```jsonc
{
  "index", "id", "kind": "text|image|prefab",
  "role": "background|button|image|text",
  "x", "y", "w", "h",                    // 1920×1080 논리좌표
  "unity": { "anchorMin": {x,y}, "anchorMax": {x,y} },   // Y-flip 계산 완료
  "z", "locked", "hidden", "opacity",
  // 연속성(씬/인터랙션 넘어 유지 여부)
  "continuity": "persist|change|enter|exit",
  "span": { "fromInteraction", "toInteraction" },
  "crossSceneId",                        // persist면 런타임 오브젝트 재사용 키
  // 텍스트
  "textMode": "static|dynamic",
  "variants": [ { "condition", "text" } ],   // dynamic
  // 이미지/프리팹 상태(배리에이션 = 교체 슬롯)
  "states": [ { "id", "name", "assetId", "hasImage" } ],
  "defaultStateId", "activeStateId",
  "prefabId", "stateId",                 // 프리팹 인스턴스
  // 클리핑마스크(ver1.7, 추가만·기본 없음) — §3.3
  "clip": { "type": "rect|roundrect|ellipse|maskBox",
            "radius",                    // roundrect(또는 마스크 도형이 둥근사각)일 때
            "maskBoxId",                 // type=maskBox: 마스크 박스 id
            "shape",                     // maskBox일 때 마스크 도형(rect|roundrect|ellipse)
            "geometry": { "x","y","w","h" },   // 도형=박스 자기 rect / maskBox=마스크 박스 rect
            "unityMask": "RectMask2D|SpriteMask",   // 사각·둥근=RectMask2D / 타원·커스텀=SpriteMask(알파)
            "unityMaskNote" },
  "maskRole": "mask",                    // 이 박스가 마스크 박스일 때(렌더 숨김)
  "maskFor": [ "<contentBoxId>" ],       // maskRole=mask: 클립하는 콘텐츠 박스들
  "renderHidden", "maskShape",           // 마스크 박스: 렌더 숨김 + 마스크 도형
  // 프레임유형(ver1.7, 추가만·기본 cropframe) — §3.4
  "frameType": "cropframe|fullframe",    // cropframe=파일이 박스크기(좌표배치) / fullframe=이미지 1920×1080 전체
  "frameTypeUnity": { "fit": "boxSprite|fullscreen", "anchorMin", "anchorMax", "note" },
  // 논코딩 메모(기능/상호작용/프롬프트)
  "prompts": [ { "label", "text", "kind", "sfxAssetId", "trigger" } ]
}
```

---

## 3. 코워크 결정론적 빌드 절차 (바이브코딩)

입력: `SEQ#.pimmgame.json` + Unity + 핌플레이어 프로젝트. 아래를 순서대로 실행(임포터가 자동화).

1. **파싱 & 검증**: `pimmgame` 버전 확인, `prefabPath`가 기존 메커니즘(Reflex/Logic/Coop/Memory/Control 등)에 매핑되는지 확인.
2. **에셋 추출**: `assets.images/audio`의 data URI를 `assetArchive.map` 경로로 프로젝트에 기록(§4). 이미 있으면 checksum 비교로 스킵.
3. **StreamingAssets config 기록** (repo 실제 스키마와 정합):
   - `theme_config.json`: 이 시퀀스의 phaseId/prefabPath/params 갱신·추가.
   - `config.json`(SeqData/ActEntry): scenes·interactions를 **쇼 흐름**으로 변환(씬=act, interaction 순서=진행, transition=act 전환, endMark=시퀀스 종료).
   - `combo_input_registry.json`: 인풋 맵핑(메모의 G1~G6 신호) 반영.
   - `combo_defaults.json`: scoring/timing/ambient.
4. **레이아웃 적용**: 각 box의 `unity.anchorMin/Max`로 RectTransform 설정. (런타임 레이아웃 로더가 있으면 config만, 없으면 프리팹 인스펙터에 반영.)
5. **상태/연속성/전환 = 에셋 기반 애니메이션**:
   - `states`(배리에이션)를 **스프라이트 교체 슬롯**으로 등록 → setState는 이미지 스왑(코드 아님).
   - `continuity:persist` + `crossSceneId` → 오브젝트를 파괴/재생성하지 말고 재사용(배경 깜빡임·BGM 재시작 방지).
   - `transition`(fade/dissolve) → 기존 트랜지션 컴포넌트/머티리얼로 처리(신규 C# 지양).
6. **오디오 배선**: `bgm`(시퀀스 지속) + interaction/prompt의 `sfxAssetId`(순간 재생).
7. **Play로 QC**: 팀원이 직접 시연(입력·전환·판정·소리). 문제 시 툴로 돌아가 재인코딩.
8. **Build**.

### 코드 임팩트 최소화 규칙 (핵심)
- **리스킨(기존 메커니즘 + config + 에셋)만으로 되면 C# 0줄.** 애니메이션은 상태 스프라이트 스왑·트윈 파라미터로.
- 번들이 **기존에 없는 메커니즘/입력/모드**를 요구하면 → 임포터/코워크가 **명시적으로 플래그**하고 그 부분만 C# 추가. **조용히 코드 생성 금지**(리스킨 경계 유지).

---

## 4. 에셋 아카이빙 폴더 (최종 산출의 반쪽)

핸드오프(번들)와 함께, 에셋을 **교체·버전관리 쉽게** 폴더로 정리한다.

```
PIMMplayer_JSON/<project>/<SEQ#>/
  SEQ#.pimmgame.json          # 인코딩 번들(임베드 자체완결본)
  SEQ#_layout.json            # 레이아웃(좌표·씬·인터랙션)
  SEQ#_artboards.svg          # 좌표이미지(박스별 인덱스 = 교체 슬롯)
  images/  bg_01.png, btn_start_상태1.png, btn_start_상태2.png, ...
  audio/   bgm_main.mp3, sfx_correct.wav, ...
```

- 파일명에 **상태(배리에이션)·박스 인덱스**를 반영 → SVG 아트보드/`states`와 1:1 → 나중에 그림만 갈아끼우기 쉬움.
- 한글 파일명은 NFC 정규화. Drive 동기폴더(로컬 경로) 그대로 사용.
- 번들은 자체완결(임베드)이라 단독 전달 가능하고, 아카이브 폴더는 편집·재작업용. 둘은 같은 assetId로 연결.

---

## 5. PART 9(인코딩 기능) 구현 체크리스트 (툴 측)
- [ ] 시퀀스 선택 → "인코딩" 다이얼로그(프리미어식): 대상 시퀀스, 임베드 여부, 저장 위치.
- [ ] 위 번들 스키마로 `.pimmgame.json` 생성(에셋 data URI 임베드) + 아카이브 폴더 구조(서버 있으면 `/api/export/save`로, 없으면 다운로드/showSaveFilePicker).
- [ ] 좌표이미지(SVG) 씬별 생성 옵션.
- [ ] 리스킨 정합 사전점검: prefabPath가 기존 메커니즘인지 표시, 아니면 "신규 메커니즘 필요" 경고.
- [ ] Chromium 검증: 번들 JSON.parse·필수필드·assetId 정합·씬/인터랙션/상태/연속성 포함, 앱 콘솔에러 0.
