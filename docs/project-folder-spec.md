# 프로젝트 폴더 스펙 — 위치 설정 + 자체완결 개발폴더 (게임에디터 ver1.6+)

> **사용자 요청/버그**: "새 프로젝트 열 때 '위치설정하고 저장'이라 써있는데 실제 브라우즈가 안 열림(크리티컬)."
> 브라우즈로 경로를 고르면, **유니티 개발폴더처럼 HTML·에셋·config(json)가 한 폴더에 모이는
> 자체완결 프로젝트 폴더**가 그 경로에 자동 생성되어야 한다. 이후 작업은 그 폴더에 저장된다.

---

## 1. 새 프로젝트 플로우 (고쳐야 할 동작)

```
새 프로젝트
  → 이름 입력
  → [위치 설정]  ← showDirectoryPicker() 로 OS 파일탐색기 실제로 열림  (← 지금 안 열리는 버그)
  → 고른 경로 아래에 <프로젝트명>/ 폴더 트리 자동 생성 + 초기 project.pimm.json 기록
  → 디렉터리 핸들 저장(IndexedDB) → 이후 자동저장이 이 폴더에 씀 (localStorage 아님/병행)
```

- 재방문: **[프로젝트 열기] → 폴더 선택 → project.pimm.json 로드**. (핸들 재승인)
- 저장 위치가 **구글드라이브 데스크톱 동기폴더**면 팀 공유까지 그대로(배포모델과 정합).

## 2. 폴더 계층 (자체완결 · 유니티 개발폴더형)

```
<선택 경로>/<프로젝트명>/
  PIMMotion_Editor.html        # 이 에디터 HTML 사본 → 폴더만 있으면 더블클릭으로 편집 재개
  project.pimm.json            # ★ 마스터 config (기계 파싱): 메타 + 시퀀스/씬/박스 +
                               #    좌표(unity 앵커) + 트랙/클립 + 인터랙션 메모(성공/실패) + 상태/연속성
  assets/
    images/                    # 이미지·가변이미지·배경 원본  (파일명: <SEQ>_<scene>_<box>[_상태n].png, NFC)
    audio/
      bgm/                     # 배경음
      sfx/                     # 효과음
    reference/                 # 고급메뉴 레퍼런스 이미지(생성 참고자료)
  encode/                      # 인코딩(시퀀스 내보내기) 산출물
    <SEQ>.pimmgame.json        # 자체완결 번들(임베드) — encoding-and-build.md §2
    <SEQ>_artboards.svg        # 박스별 인덱스 아트보드
  .pimm/
    index.json                # 내부 메타(포맷버전·에셋 인덱스) — 수정 금지
```

- **HTML+에셋+json 한 폴더** = 자체완결. Drive 동기폴더에 두면 팀이 폴더째 열어 씀.
- 역할 분리: **좌표/씬/트랙/메모 = `project.pimm.json`**, **이미지/오디오 = `assets/`**, **인코딩 = `encode/`**.
- 코워크는 이 폴더(특히 `project.pimm.json` + `encode/`)를 읽어 유니티 빌드(encoding-and-build.md).

## 2.5. 저장용량 문제 & 해결 (자동저장 실패 — 중요)

> **증상(사용자)**: "자동저장 실패 — 저장용량 초과" 안내. 원인 = **localStorage 용량(~5MB)** 한계인데
> 이미지를 **data URI로 임베드**해 자동저장하니 이미지 몇 장이면 초과 → 저장 실패.

**해결 2축:**
1. **폴더 연결 시 = localStorage 대신 폴더 저장(정본)**: `project.pimm.json`(경량 config) + `assets/*`(이미지/오디오
   **파일**). 이미지는 data URI로 config에 박지 말고 **assets 파일 + 상대경로 참조**. → 용량 제한 사실상 없음.
2. **폴더 미연결 폴백 = IndexedDB 오프로드**: 무거운 이미지/오디오 blob을 **IndexedDB**(용량 수백MB)에 저장,
   localStorage엔 **경량 상태만**. → 폴더 없이도 자동저장이 안 터짐.

- **경량화 원칙**: localStorage(및 undo 스냅샷)에는 **data URI 대신 assetId/경로 참조**만. 실제 바이너리는 폴더/IndexedDB.
- **우아한 처리**: 쿼터 초과시 조용히 실패 금지 → "폴더 연결 또는 내보내기" 안내 + 폴더/IndexedDB로 폴백(작업물 보존).
- 우선순위: ver1.8(타임라인) 다음 **최우선**(작업물 저장 직결).

## 3. 저장 동작

- **자동저장**: 편집 시 `project.pimm.json`을 폴더에 기록(디바운스). 에셋 추가 시 바이너리를 `assets/*`에 기록하고 config는 상대경로 참조.
- **이미지/오디오 임포트**: 파일 추가하면 `assets/images|audio`로 복사(원본 보존), config엔 `assets/...` 상대경로.
- **localStorage 병행**: 폴더 미연결(폴백) 상태에선 기존처럼 localStorage. 폴더 연결되면 폴더가 정본, localStorage는 캐시.

## 4. 브라우저 지원 & 폴백

- `showDirectoryPicker()`/`getFileHandle(create)`/`createWritable()` = **Chromium(Chrome·Edge) 전용**.
- Firefox·Safari 미지원 → **폴백**: 기존 localStorage 유지 + "폴더 저장은 Chrome/Edge에서" 안내 +
  수동 내보내기(ZIP/다운로드)로 동일 트리 산출. 권한 거부/취소(AbortError)는 조용히 처리(에러 0).
- HTML 사본 기록: 자기 소스는 `fetch(location.href)` 텍스트로 시도, 실패 시 스킵(안내) — best-effort.

## 5. QA 유의

- 실제 파일탐색기(picker)는 **user gesture 필요 + 헤드리스 자동화 불가** → 자동 QA는 **로직/폴백/트리생성 함수 단위**로.
  (핸들 주입 모킹 또는 OPFS(`navigator.storage.getDirectory()`)로 트리 생성·기록·재로드 검증, 실제 picker는 수동 확인.)
- 검증: 트리 생성(폴더/파일 존재), project.pimm.json 라운드트립(기록→재로드 동일), 에셋 상대경로 정합,
  미지원 브라우저 폴백 경로, 취소/거부 예외 0, "위치 설정" 클릭이 **실제 picker 호출**로 배선됐는지.
