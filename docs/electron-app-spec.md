# 데스크톱 앱(Electron) 준비 스펙 — 2.0 배포용 스캐폴드

> **목표**: 완성된 게임에디터 HTML을 **Electron으로 감싸 데스크톱 앱**(.exe/.dmg)으로. 프론트뷰 맥·윈도우
> 픽셀 동일. **이 문서는 배포 준비(스캐폴드·CI·가이드)** — 실제 패키징은 기능 프리즈 후(2.0) 실행.
> 관련: `collaboration-drive-sync.md`(Drive 공유·Electron 결정), `project-folder-spec.md`(프로젝트 폴더).

---

## 1. 왜 Electron & 무엇이 쉬운가
- **Chromium 내장** → 맥·윈도우 미리보기(프론트뷰) 픽셀 동일(사용자 결정). 용량(~100MB)은 Drive 1회 설치라 수용.
- **File System Access API가 Electron의 Chromium에서 그대로 동작** → 프로젝트 폴더(`showDirectoryPicker`/IndexedDB
  핸들)가 **코드 수정 거의 없이** 네이티브급으로 작동. (별도 Node fs 브리지 최소.)
- 기존 단일 HTML을 로드만 하면 됨 → 로직 재작성 거의 0.

## 2. 스캐폴드 구조 (repo `desktop/`)
```
desktop/
  package.json            # electron + electron-builder, scripts(start/build), build 타깃(win nsis, mac dmg)
  main.js                 # BrowserWindow 생성 → 앱 내 HTML 로드(1600x1000, 메뉴 최소)
  preload.js              # 최소(contextIsolation), 필요시 app 버전/경로 노출
  renderer/               # 앱이 로드할 HTML (빌드 시 tool/ 최신 에디터 복사)
    index.html            #   = 최신 PIMM_UnityGameCreator.verX.html (또는 허브)
  assets/
    icon.ico  icon.icns   # 앱 아이콘(핌 로고 — 2.0 마스터링 때 확정)
  electron-builder.yml    # appId, productName "PIMMotion", win/mac 타깃, 무서명(내부)
.github/workflows/
  desktop-build.yml       # windows+macos 러너 듀얼빌드 → .exe/.dmg 릴리스 첨부
```

- **앱 진입 = 허브(런처)** (사용자 확정): 앱 첫 화면 = **PIMMotion 허브**(맨 앞 바로가기/런처) → 카드 클릭으로 에디터 진입.
  허브 + 에디터들을 **모두 번들**하므로 폴더 co-location 문제 없음(브라우저·상대경로 걱정 소멸).
- **HTML 소스**: 빌드 스텝에서 `tool/`의 **최신 허브(`PIMMotion_Hub.verX.html`) → `renderer/index.html`** + 최신 에디터(들) → `renderer/`에 함께 복사(허브의 상대경로 링크가 앱 안에서 작동).

## 3.5 마법사 설치 배포 (사용자 아이디어 = 이 계획의 완성형)
- **윈도우 = NSIS 설치 마법사(.exe)**: 환영 → 설치 위치 → 설치 → 완료 + **바탕화면 바로가기**. 실행 시 허브로 시작.
- **맥 = .dmg**(드래그 설치, 맥 표준). GitHub Actions 듀얼빌드로 둘 다 자동 생성.
- 무서명 내부배포(첫 실행 경고 우회) → 필요 시 서명·공증. 2.0 마스터링에서 로고·아이콘·실행가이드 확정.

## 3. GitHub Actions 듀얼빌드 (무서명 내부배포)
```
릴리스 태그 push
  └▶ desktop-build.yml
       ├─ windows-latest 러너 → electron-builder → PIMMotion-Setup-x.y.z.exe
       └─ macos-latest 러너   → electron-builder → PIMMotion-x.y.z.dmg
  └▶ 두 산출물 릴리스에 자동 첨부 → 팀원은 자기 OS 것 다운로드
```
- **무서명**: 첫 실행 경고(Win SmartScreen / macOS "확인되지 않은 개발자")는 "실행/열기"로 우회. 팀 온보딩 한 줄 안내.
- 나중에 서명 원하면: Win 코드서명 인증서 + Apple 공증 secrets 추가(워크플로우에 훅만).

## 4. 프로젝트 폴더 & Drive (그대로 작동)
- Electron Chromium이 File System Access API 지원 → `위치 설정`(showDirectoryPicker)·폴더 자동저장·IndexedDB
  핸들 모두 그대로. Drive 동기폴더를 프로젝트 위치로 잡으면 팀 공유(collaboration-drive-sync.md).
- 크로스OS 하우스키핑: 한글 파일명 **NFC**·경로 `/`·줄바꿈 **LF** (앱에서도 강제 — 이미 에디터에 반영 예정).

## 5. 실행 타이밍 & 절차 (인수인계 후 2.0)
1. **기능 프리즈**(에디터 verN 확정) 후 스캐폴드 생성 → `renderer/index.html`에 최신 에디터 복사.
2. 로컬 `cd desktop && npm i && npm start`로 창 동작 확인.
3. 릴리스 태그 push → Actions가 .exe/.dmg 생성 → 릴리스 첨부.
4. 팀원: 자기 OS 설치파일 다운로드 → 실행(첫 경고 우회) → Drive 폴더로 프로젝트.
- **아이콘/실행가이드/로고 = 2.0 마스터링**에서 확정(이 스캐폴드에 끼워넣음).

## 6. 지금 준비(이 문서) vs 나중 실행
- **지금(준비)**: 본 스펙 확정. (선택) 스캐폴드 파일 골격 생성 — 단, `renderer/index.html`은 최신 에디터로 갱신 필요.
- **나중(2.0, 사용자/코워크)**: 로고·아이콘·실행가이드 마스터링 + 태그 push로 듀얼빌드 배포.
- 에디터 HTML은 계속 진화하므로 스캐폴드는 **"최신 tool/ HTML 복사"** 방식으로 연결(버전 종속 최소).
