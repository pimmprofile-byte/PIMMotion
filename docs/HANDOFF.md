# PIMMotion 인수인계 문서

> **한 줄**: 비개발자가 익숙한 툴(일러스트·프리미어) 사용감으로 게임을 **설계·정리**하고, 그 결과 폴더를
> **코워크가 유니티로 빌드**, **팀이 유니티에서 QC**하는 파이프라인. 이 문서는 지금까지 만든 것과
> 이어서 할 것을 한 장에 정리한다.

---

## 1. 전체 워크플로우 (역할 분담)

```
① 레이아웃 뷰     씬 구성(박스 배치·정렬·클립·크롭·프레임그래픽·소리·이벤트 메모)  ← 사용자 (일러스트식)
② 타임라인 뷰     블록(씬/인터랙션/영상) 순서 + 연속성 연장                        ← 사용자 (프리미어식)
③ 에셋저장소/에셋에디터  이미지 정리(배경제거) + 편집본·템플릿 빠른 접근            ← 사용자 (에셋 준비)
④ 에셋맵핑 뷰     쇼오더·오디오·인풋 레지스트리 (🚧 미구현)                        ← 사용자 (config 정리)
        │  = 자동저장(project.pimm.json, 폴더) + 인코딩(encode/*.pimmgame.json)
        ▼
⑤ 코워크          폴더(project.pimm.json + assetsIngame + encode/*)를 읽어 유니티 빌드  ← 코워크 (로컬 유니티)
        ▼
⑥ 유니티          재생하며 버그 잡기 (QC)                                        ← 사용자/팀 (로컬 유니티)
```

- **이 툴(①②③④)** = 설계·정리까지. **실제 유니티 빌드(⑤)** = 코워크. **구동·QC(⑥)** = 로컬 유니티.
- 클라우드 세션의 코워크는 핌플레이어 **소스코드 작성/push**는 가능하나 **유니티 실행은 불가**(로컬 몫).

## 2. 지금까지 만든 것 (LIVE = ver1.11)

### 게임 에디터 — `tool/PIMM_UnityGameCreator.ver1.11.html` (단일 HTML, 설치 0)
| 영역 | 기능 |
|---|---|
| 하이어라키(좌) | 시퀀스그룹▸시퀀스▸씬▸박스, 유니티식 드래그·이름변경·우클릭 생성·접기, z-order(위=앞/배경 맨뒤) |
| 레이아웃 뷰 | 박스 배치·정렬, **파워포인트 스마트 가이드**(균등간격·여백 스냅), 원클릭 균등배치, **클리핑박스**·**자르기(크롭)**, **프레임유형(크롭/풀프레임)**, 레퍼런스 이미지 |
| 타임라인 뷰 | 프리미어식(게임뷰 상단+트랙 하단), **블록 시퀀스(씬/인터랙션/영상)**, **클립 연장=연속성**(하이어라키 자동복사+디졸브 없음), 성공/실패 텍스트 메모, **트랙 높이 조절**, 속성창 연동 |
| 재생(▶) | 전체화면 게임뷰(ESC 복귀). 레이아웃=상태이미지 스프라이트 프리뷰 / 타임라인=플레이헤드 스윕 |
| 이벤트 | 박스별 실행조건+명령(논코딩), 이미지박스 상태(배리에이션) |
| 저장 | **자동저장**(이미지=IndexedDB 오프로드로 용량 안 터짐) + **프로젝트 폴더**(위치 설정→자체완결 폴더, 저장 라우팅 + 폴더 README) |
| 산출 | **인코딩(encode/*.pimmgame.json)** 자체완결 + 에셋 아카이빙 폴더 (핸드오프) |

- **허브** `tool/PIMMotion_Hub.ver0.2.html` — Forge/Track 진입점(게임에디터 LIVE, 나머지 🚧).
- 전 버전 tool/에 보존(ver1.0~1.11). 버전업마다 파일명 bump(캐시 회피) + 허브 링크 갱신.

### 진행 중 (통합 A=ver1.12 / 통합 B=ver1.13 — 스펙 확정, 빌드 중)
스펙이 정본이며 아래대로 동작하도록 구현 중. 큐를 2개 통합 빌드로 묶어 최종 파일 한 번에 확인. (최종 툴과의 미세차는 코디네이터가 대조.)

- **통합 A (ver1.12) — 에셋 정확도 파이프라인**(큰 변경, 마이그레이션·회귀 철저):
  - **이미지박스 통합(A안)**: "가변이미지박스" 제거 → **이미지박스 하나 + "상태 추가"**로 전환 이미지. 무손실 마이그레이션. → `template-spec.md`
  - **에셋에디터**: **자동 배경제거**(단색 flood-fill + 격자 가짜투명→진짜 alpha), 크롭/트림/리사이즈/회전/합치기/기본조정 → `assetsEdited/` 투명 PNG. → `asset-pipeline-spec.md §2`
  - **에셋저장소**(구 템플릿 탭 대체): `assetsEdited` + 템플릿 **자동 표시**, 씬 드롭(이미지=프레임그래픽, 템플릿=복사 삽입). → `asset-pipeline-spec.md §3`
  - **프레임그래픽**(드리프트 0): 박스=이미지 원본 크기, `object-fit:fill`, 비율 락/언락. frameType 3모드(크롭/풀/**프레임그래픽**). → §4
  - 폴더 assetsEdited/assetsIngame(내보내기 dedup) + 이미지 임베드 SVG + 1920×1080 합성 렌더. **탭**: 레이아웃 › 타임라인 › 에셋저장소 › 에셋에디터.
- **통합 B (ver1.13) — UX/단축키**(A 다음, 같은 파일):
  - **단축키 시스템**: Adobe 정렬 + **커스터마이징 패널**(에셋저장소 옆 "⌨ 단축키"). 생성계열 **Alt**(브라우저 안전), 편집 **Ctrl**, 뷰 Alt+1~n, 재생 Alt+P. → `shortcuts-spec.md`
  - **로고 영역 + 허브 이동 확인창**, **시작 화면 로직**(진행 중 프로젝트→에디터 직행, 없으면 런처), **캔버스 네비**(휠 줌·스페이스 팬). → `tool-concept.md §3.5~3.7`

### 데스크톱 앱 준비 — `desktop/` + `.github/workflows/desktop-build.yml`
- Electron 스캐폴드(준비 완료). `pimm://` 보안 프로토콜로 서빙 → 프로젝트 폴더 기능 그대로 동작.
- `desktop-v*` 태그 push → GitHub Actions가 **.exe(윈도우)+.dmg(맥) 듀얼빌드**. 무서명 내부배포.
- **실제 패키징/로고/실행가이드 = 2.0 마스터링에서.** (`desktop/README.md`, `docs/electron-app-spec.md`)

## 3. 폴더 구조 (자체완결 프로젝트 폴더)

```
<프로젝트명>/
  PIMMotion_Editor.html        # 에디터 HTML 사본 (폴더만 있으면 더블클릭 재개)
  project.pimm.json            # ★ 마스터 config: 메타 + 시퀀스/씬/박스 + 좌표(unity 앵커)
                               #    + 트랙/클립 + 인터랙션 메모(성공/실패) + 상태/연속성 + templates[]
  assets/
    images/  audio/(bgm,sfx)/  reference/    # 임포트 원본·소리·참고
    assetsEdited/              # 에셋에디터 편집본(배경제거된 투명 PNG) — 에셋저장소가 여기서 자동 표시
    assetsIngame/              # 내보내기 시 최종 씬에 실제 올라간 에셋만 dedup 복사(빌드용 정리본)
  encode/
    <SEQ#>.pimmgame.json       # 자체완결 인코딩 번들(임베드)
    <SEQ#>_artboards.svg       # 박스별 인덱스 아트보드(교체 슬롯)
  README(폴더 안내)             # 코워크용: 무엇을·어떻게 빌드할지, 리스킨/신규 여부, 에셋 위치
  .pimm/index.json             # 내부 메타(수정 금지)
```

- **원본(assets/images) → 편집본(assetsEdited) → 게임투입본(assetsIngame)** 3단 분리.
- 좌표/씬/트랙/메모 = `project.pimm.json`, 이미지/오디오 = `assets/`, 인코딩 = `encode/`.
- HTML+에셋+json이 **한 폴더** = 자체완결. Drive 동기폴더에 두면 팀이 폴더째 열어 씀. → `project-folder-spec.md`

## 4. 저장·공유 모델 (서버 없음)
- **구글드라이브 = 서버.** 프로젝트 폴더를 Drive 동기폴더에 두면 팀 자동 공유(깃 유사). 동시-같은파일 편집만 주의(파일분리 + 소프트잠금으로 우회). → `collaboration-drive-sync.md`
- 자동저장: 폴더 연결 시 **폴더가 정본**(경량 config + assets 파일 참조), 미연결 폴백은 무거운 blob을 **IndexedDB**에 오프로드(localStorage는 경량 참조만) → 용량 안 터짐. → `project-folder-spec.md`
- **데스크톱 앱(2.0, Electron)**: 폴더/파일시스템을 네이티브급으로 → 브라우저 제약 없이 드라이브 폴더 안정 사용. .exe/.dmg 듀얼빌드. → `electron-app-spec.md`

## 5. 코워크가 빌드하는 법 (폴더 → 핌플레이어)
- 입력: 프로젝트 폴더의 **README + `encode/<SEQ#>.pimmgame.json`(자체완결) + `assets/assetsIngame/`**. 결정론적 절차·스키마 → `docs/encoding-and-build.md`.
- 핌플레이어 repo: **`pimmprofile-byte/PIMM_unityPIMMplayer`**(세션에 add하면 임포터·런타임 로더 구현 가능).
- **리스킨**(기존 메커니즘 + config + 에셋)이면 **C# 0줄**. 새 메커니즘만 코워크가 플래그하고 그 부분만 추가.
- 프레임유형·클립·크롭 → Unity 매핑(RectMask2D/SpriteMask, anchor). WYSIWYG 보장, 텍스트 폰트만 Play에서 확인. → `guide-cowork-unity.md`

## 6. 이어서 할 것 (로드맵)
- 🚧 **에셋 파이프라인 완성**(ver1.13): 에셋에디터·에셋저장소·프레임그래픽·이미지박스 통합 빌드/회귀.
- 🚧 **단축키 시스템**(ver1.14): 기본 매핑 + 커스터마이징 패널.
- 🚧 **에셋맵핑 뷰**: 쇼오더→combo_show_config, 오디오 BGM/SFX 레지스트리, 인풋 combo_input_registry(G1~G6).
- 🚧 **전체 검수**: 전 기능 시연 · 파포 페르소나 사용성 · 회귀 → 종합 피드백.
- 🚧 **핌플레이어 인코딩 임포터 + 런타임 로더**(repo add 후).
- 🚧 **2.0 마스터링**: 핌 로고·아이콘·실행가이드 + **Electron 데스크톱 배포**(.exe/.dmg).

## 7. 문서 색인 (`docs/`)
- `tool-concept.md` — 툴 개념(일러스트/프리미어/유니티 결합, 스마트가이드·클립·크롭·WYSIWYG·점진적 복잡도·캔버스 네비·시작로직)
- `timeline-view-spec.md` — 타임라인(블록 씬/인터랙션/영상·연속성 연장·트랙 높이·속성창)
- `asset-pipeline-spec.md` — 에셋에디터(자동 배경제거) · 에셋저장소 · 프레임그래픽 · assetsEdited/assetsIngame
- `template-spec.md` — 이미지박스 통합(A안) + 템플릿(복사 삽입)
- `shortcuts-spec.md` — 단축키 시스템(Adobe 정렬·Alt 생성·커스터마이징 패널)
- `encoding-and-build.md` — 인코딩 스키마 + 코워크 빌드 절차
- `project-folder-spec.md` — 프로젝트 폴더 + 자동저장 용량 해결
- `collaboration-drive-sync.md` — Drive 공유 모델(서버 없음)
- `electron-app-spec.md` — 데스크톱 앱(Electron) 계획
- `distribution-and-build.md` — 팀원 직접 빌드 배포 모델
- `pimmotion-platform.md` / `track-lifecycle.md` — 허브·플랫폼·Track 5공정
- `guide-nodev-build.md` / `guide-cowork-unity.md` — 사용자 가이드 2종(무개발 설계 / 코워크·유니티 빌드)

## 8. 개발 규칙 (유지보수용)
- 브랜치 `claude/pimmotion-coworking-review-lq2flo`. 버전업마다 파일명 bump(캐시 회피) + 허브 링크 갱신.
- 각 빌드: qc_v* + 회귀 전체 **3라운드 FAIL=0**, 콘솔에러 0, 직전 원본 md5 보존.
- **트윈 동기**: `tool/PIMM_UnityGameCreator.verX.html` ↔ `UnityGameLayout.html`은 **바이트 동일**(md5 일치) 유지.
- 스키마는 **추가만**(하위호환). 인코딩은 자체완결 유지. 마이그레이션(가변→이미지박스 통합 등)은 무손실.
