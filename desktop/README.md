# PIMMotion 데스크톱 앱 (Electron) — 준비 스캐폴드

> 게임에디터 HTML을 **Electron으로 감싼 데스크톱 앱**. 맥·윈도우 프론트뷰 픽셀 동일(Chromium 내장),
> 프로젝트 폴더 기능(File System Access API)이 보안 컨텍스트(`pimm://`)에서 그대로 동작.
> **현재 = 준비 스캐폴드.** 실제 로고/아이콘/실행가이드·배포는 **2.0 마스터링**에서.

## 구조
```
desktop/
  package.json            electron + electron-builder, scripts
  main.js                 pimm:// 커스텀 보안 프로토콜로 에디터 HTML 서빙 + BrowserWindow
  preload.js              최소(window.pimmDesktop)
  electron-builder.yml    win nsis(.exe) / mac dmg(.dmg), 무서명(내부)
  scripts/sync-renderer.mjs   tool/ 최신 에디터 → renderer/index.html 복사
  renderer/index.html     (sync가 생성 — git 미포함, 단일 소스 tool/ 유지)
  assets/                 icon.ico / icon.icns  ← 2.0 로고 자리
.github/workflows/desktop-build.yml   윈도우+맥 러너 듀얼빌드 → 산출물 업로드
```

## 로컬 실행 (개발 확인)
```bash
cd desktop
npm install
npm start          # sync(최신 에디터 복사) 후 Electron 창 실행
```

## 설치파일 빌드
```bash
npm run dist:win   # → dist/PIMMotion Setup x.y.z.exe   (윈도우에서)
npm run dist:mac   # → dist/PIMMotion-x.y.z.dmg          (맥에서)
```
> 각 OS 설치파일은 **그 OS(또는 해당 CI 러너)에서** 빌드해야 함. 아래 CI가 둘 다 자동 생성.

## CI 듀얼빌드 (권장)
`desktop-v*` 태그를 push하면 GitHub Actions가 **윈도우 러너 → .exe**, **맥 러너 → .dmg**를 만들어 아티팩트로 올림.
```bash
git tag desktop-v0.1.0 && git push origin desktop-v0.1.0
```

## 프로젝트 폴더 / Drive
- Electron Chromium이 File System Access API를 지원 → `위치 설정`(showDirectoryPicker)·폴더 자동저장·
  IndexedDB 핸들이 그대로 작동(그래서 `pimm://` 보안 오리진으로 서빙). Drive 동기폴더를 프로젝트 위치로
  잡으면 팀 공유(`docs/collaboration-drive-sync.md`).

## 무서명 안내 (내부 배포)
- 첫 실행 시 **Windows SmartScreen** / **macOS "확인되지 않은 개발자"** 경고 → "추가 정보→실행" / "열기"로 진행.
- 서명·공증 원하면: Win 코드서명 인증서 + Apple 공증 secrets를 CI에 추가하고 `electron-builder.yml`의 서명 항목 활성화.

## 2.0 마스터링에서 확정할 것 (남겨둔 자리)
- [ ] `assets/icon.ico` · `assets/icon.icns` = 핌 로고
- [ ] 실행 가이드(팀 온보딩: 설치·첫 실행 경고·Drive 폴더 연결)
- [ ] (선택) 자동 업데이트(electron-updater), 서명·공증

## 검증 참고
- 이 스캐폴드는 **로직 재작성 없이** 최신 `tool/` 에디터를 감싸는 구조. 실제 `npm start`/설치파일 빌드는
  **데스크톱 OS/CI 러너**에서 확인해야 함(이 클라우드 세션엔 디스플레이·Electron 런타임 없음).
- File System Access API가 `pimm://`에서 정상 동작하는지는 실기(로컬 실행)에서 최종 확인 권장.
