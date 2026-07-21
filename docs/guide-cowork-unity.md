# Cowork + Unity 실전 워크플로우 가이드 (ver2.0 워크플로우)

> 코워크(대화형 Claude)가 **설계자가 넘긴 프로젝트 폴더를 읽어** 핌플레이어(Unity)로 빌드하고,
> 팀이 유니티 Play로 QC하는 실전 루프. 설계·인코딩의 "손"은 게임에디터, 빌드/신규코드 파트너는 코워크.
> 인코딩 규격·빌드 절차는 `encoding-and-build.md`, 배포·데스크톱 앱은 `electron-app-spec.md` 참조.

---

## 0. 역할 분담

| 주체 | 역할 |
|---|---|
| **설계자(사용자)** | 구상 · 배치 · 에셋 정리 · 타임라인/상태/연속성 · 메모 · **인코딩** · 유니티 Play로 QC |
| **툴(게임에디터)** | 레이아웃/타임라인/에셋저장소/에셋에디터, 정렬, 상태, 프레임그래픽, **폴더 저장 + 인코딩** |
| **코워크(Claude)** | 폴더를 읽어 유니티 빌드(바이브코딩), 신규 C#은 플래그된 부분만 |
| **Unity(핌플레이어)** | config/에셋 임포트 → Play 시연 → Build |

분업 원칙: **툴 = 리스킨(껍데기·흐름·좌표), 코워크 = 빌드/신규 로직(뼈대), Unity = 검수.**
클라우드 세션의 코워크는 핌플레이어 소스 작성/push는 가능하나 **유니티 실행은 로컬 몫**입니다.

---

## 1. 코워크가 받는 것 = 프로젝트 폴더 하나

설계자가 넘기는 것은 **자체완결 프로젝트 폴더**입니다(드라이브 동기폴더에 있으면 자동 도착). 코워크는 이 폴더만 읽으면 됩니다.

```
<프로젝트명>/
  PIMMotion_Editor.html        # 에디터 HTML 사본(참고용)
  project.pimm.json            # ★ 마스터 config: 메타 + 시퀀스/씬/박스 + 좌표(unity 앵커)
                               #    + 트랙/클립 + 인터랙션 메모(성공/실패) + 상태/연속성 + templates[]
  assets/
    images/                    # 임포트 원본
    audio/ bgm/ sfx/           # 배경음 / 효과음
    reference/                 # 생성 참고 이미지
    assetsEdited/              # 에셋에디터가 배경제거·정리한 편집본(투명 PNG)
    assetsIngame/              # ★ 내보내기 시 최종 씬에 실제 올라간 에셋만 dedup 복사 (빌드용 정리본)
  encode/
    <SEQ#>.pimmgame.json       # ★ 자체완결 인코딩 번들(임베드) — encoding-and-build.md §2
    <SEQ#>_artboards.svg       # 박스별 인덱스 아트보드(교체 슬롯)
  README(폴더 안내)             # 코워크용: 무엇을·어떻게 빌드할지, 리스킨/신규 여부, 에셋 위치
```

**코워크가 먼저 읽는 3개**:
1. **폴더 README** — 이 프로젝트가 무엇이고 리스킨인지 신규인지, 어디부터 볼지 안내.
2. **`encode/<SEQ#>.pimmgame.json`** — 빌드에 필요한 모든 것이 담긴 자체완결 번들.
3. **`assets/assetsIngame/`** — 실제 게임에 쓰이는 에셋(중복 제거된 정리본).

> `project.pimm.json`은 편집/전체 맥락용, `encode/*.pimmgame.json`은 빌드용(임베드 자체완결)입니다. 빌드는 인코딩 번들 기준으로 하고, 폴더 전체는 재작업·에셋 교체용으로 둡니다.

---

## 2. 빌드 판단: 리스킨 vs 새 메커니즘 (제일 먼저)

인코딩 번들의 `sequence.prefabPath`(예: `COMBO/Games/Reflex`)와 리스킨 배지를 확인합니다.

- **리스킨(기본)**: `prefabPath`가 기존 메커니즘(Reflex/Logic/Coop/Memory/Control 등)에 매핑됨 → **config + 에셋만으로 빌드, C# 0줄.** 설계자 주도.
- **신규 메커니즘**: 번들이 기존에 없는 규칙/입력/모드를 요구 → 인코딩이 "신규 메커니즘 필요"(주황)로 플래그 → **코워크가 그 부분만 명시적으로 C# 추가.** 조용히 코드 생성 금지(리스킨 경계 유지).

> 원칙: **코드 임팩트 최소화.** 애니메이션은 상태 스프라이트 스왑·트윈 파라미터로 처리하고, 새 C#은 플래그된 부분에 국한.

---

## 3. 결정론적 빌드 절차 (요약 — 상세는 `encoding-and-build.md §3`)

1. **파싱 & 검증**: `pimmgame` 버전 확인, `prefabPath`가 기존 메커니즘에 매핑되는지 확인(리스킨/신규 판단).
2. **에셋 추출**: 번들의 `assets` data URI를 `assetArchive.map` 경로로 기록. `assetsIngame/`이 이미 정리본이므로 checksum 비교로 중복 스킵.
3. **StreamingAssets config 기록**: `theme_config.json`(phaseId/prefabPath/params), `config.json`(scenes=act, interactions 순서=진행, transition=act 전환, endMark=종료), `combo_input_registry.json`(G1~G6 입력 맵핑), `combo_defaults.json`(scoring/timing).
4. **레이아웃 적용**: 각 box의 `unity.anchorMin/Max`로 RectTransform 설정(Y-flip 계산 완료됨).
5. **상태/연속성/전환**: `states`=스프라이트 교체 슬롯(setState=이미지 스왑), `continuity:persist`+`crossSceneId`=오브젝트 재사용(깜빡임/BGM 재시작 방지), `transition`=기존 트랜지션 컴포넌트.
6. **오디오 배선**: `bgm`(시퀀스 지속) + interaction/prompt의 `sfxAssetId`(순간 재생).
7. **Play로 QC** → 8. **Build**.

핌플레이어 repo: **`pimmprofile-byte/PIMM_unityPIMMplayer`**(세션에 add하면 임포터·런타임 로더 구현 가능).

---

## 4. 프레임유형·클립·크롭의 Unity 매핑 (WYSIWYG의 근거)

에디터에서 본 구도가 유니티에서 그대로 나오도록, 각 값이 결정론적으로 매핑됩니다.

| 에디터 개념 | 번들 필드 | Unity 매핑 |
|---|---|---|
| **크롭프레임** | `frameType:"cropframe"` | 박스 W×H 스프라이트를 `unity.anchorMin/Max` 위치에 배치 |
| **풀프레임** | `frameType:"fullframe"` | 풀스크린 RectTransform(전체 앵커). 위치는 이미지에 구워짐, 박스 좌표는 "콘텐츠 영역 표시"용 |
| **프레임그래픽** | (박스=이미지, `object-fit:fill`) | 박스 크기=이미지 원본 크기 → 레터박스/드리프트 없이 정확 배치. 오브젝트 단위 권장 |
| **클립(도형)** | `clip:{type:rect\|roundrect\|ellipse}` | 사각·둥근=**RectMask2D** / 타원·커스텀=**SpriteMask(알파)** |
| **클립(마스크 박스/클리핑박스)** | `clip:{type:maskBox, maskBoxId}` + `maskRole:"mask"` | 마스크 박스 영역/모양으로 콘텐츠 클립(RectMask2D/SpriteMask) |
| **자르기(크롭)** | `crop:{x,y,w,h}` (비파괴) | 스프라이트 rect/uv 또는 RectMask2D로 동일 영역 재현 |

- 프레임그래픽/크롭프레임은 **박스 기준 클립**, 풀프레임은 **1920×1080 프레임 기준 클립**.
- SVG 아트보드(`<SEQ#>_artboards.svg`)에도 클립·크롭·프레임유형이 반영되어 교체 슬롯으로 씁니다.

---

## 5. WYSIWYG 보장 / 유일한 한계

- **완전 동일(픽셀)**: 좌표(unity 앵커)·z순서·클립·크롭·프레임유형·투명도 — 전부 config 데이터 → 임포터가 동일 재현. 프레임그래픽으로 드리프트 0.
- **유일한 차이(정직)**: 텍스트박스의 **폰트 렌더링**(자간/힌팅)은 브라우저 ↔ Unity TextMesh 사이 미세차가 있습니다. **위치·크기는 맞습니다.**
  - → 최종 텍스트는 유니티 Play에서 확인. 이미지/레이아웃/크롭/클립은 WYSIWYG.

---

## 6. 검수 (Play로 QC)

핌플레이어에서 config/에셋 임포트 → **Play로 직접 확인**:

- [ ] 좌표 정합(에디터와 동일 구도), z순서
- [ ] 이미지·상태 전환(setState 스왑), 프레임그래픽 정확도
- [ ] 입력 반응(G1~G6 신호 → 액션), SEQ# 라우팅
- [ ] SFX·BGM 타이밍, 씬 전환·연속성(persist 유지, 디졸브 없음)
- [ ] 클립/크롭 영역, 텍스트 위치(폰트 렌더는 여기서 최종 확인)
- 문제 발견 → 설계자가 툴로 돌아가 고치고 **재인코딩** → 다시 임포트. "신규 메커니즘 필요"로 뜬 부분만 코워크가 C# 처리.

---

## 7. 팀 흐름 = 구글드라이브를 서버 삼아 (서버·API 없음)

```
[구글드라이브 클라우드]  ← "서버"
        ▲ 자동 동기 ▼
[설계자 PC] Drive동기폴더/PIMM_Projects/<프로젝트>/   ← 에디터로 편집·인코딩
[코워크/팀 PC] 같은 폴더가 동기되어 보임               ← 폴더 읽어 유니티 빌드·QC
```

- 편집 = 로컬 폴더의 `project.pimm.json`·`assets/*`·`encode/*`에 저장 → 드라이브가 자동 동기 → 팀에게 도착.
- **되는 것**: 팀 공유·배포(자동), 버전 롤백(드라이브 버전기록). **안 되는 것**: 자동 머지 — 두 명이 **같은 파일** 동시 편집 시 "(충돌된 사본)" 생성.
- **충돌 최소화**: 씬/시퀀스 단위 파일 분리, `.pimm/lock.json` 소프트 잠금("○○님 편집 중" 경고), 마일스톤마다 `encode/`로 스냅샷, 원본/작업본 분리 관례.
- 상세: `collaboration-drive-sync.md`.

> **데스크톱 앱(2.0)**: 지금 폴더 기능은 File System Access API(크롬 전용)이지만, Electron 데스크톱 앱으로 감싸면 네이티브 파일시스템이 되어 드라이브 폴더를 안정적으로 읽고 씁니다(.exe/.dmg 듀얼빌드). → `electron-app-spec.md`.

---

## 8. 체크리스트 (한 루프)

- [ ] 폴더 도착 확인(README + `encode/*.pimmgame.json` + `assetsIngame/`)
- [ ] 리스킨 vs 신규 판단(`prefabPath` + 리스킨 배지)
- [ ] 파싱·검증 → 에셋 추출 → StreamingAssets config 기록
- [ ] 레이아웃(anchor) 적용 → 상태/연속성/전환 → 오디오 배선
- [ ] 프레임유형·클립·크롭 Unity 매핑 확인
- [ ] Play로 QC(좌표·상태·입력·소리·연속성·텍스트) → 수정 시 설계자 재인코딩
- [ ] 신규 메커니즘만 코워크가 플래그해 그 부분 C# 추가 → Build

## 9. 한 문장 요약

**설계자가 넘긴 프로젝트 폴더(project.pimm.json + assetsIngame + encode/*.pimmgame.json + README)를 코워크가 읽어, 리스킨이면 config·에셋만으로 빌드하고, 프레임유형·클립·크롭을 그대로 매핑해 WYSIWYG로 재현한 뒤(텍스트 폰트만 Play에서 확인), 팀이 드라이브로 공유하며 유니티에서 QC한다.**
