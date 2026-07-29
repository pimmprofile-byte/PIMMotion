# PIMM Launcher (Electron 데스크톱 셸)

> 팀원이 **PIMM Launcher HUB** 를 데스크톱 앱으로 실행. 맥·윈도우 픽셀 동일(Chromium 내장).
> **얇은 셸**: 콘텐츠(허브·툴·`poffice_board`)는 각자 **Drive-동기 `PIMM_Launcher` 폴더**에서 로드.
> 폴더를 한 번만 지정하면 이후 코워크/사용자가 폴더만 갱신해도 **앱 재배포 없이 즉시 반영**.

## 왜 이 구조
- `pimm://` 커스텀 **보안 오리진**으로 폴더를 서빙 → 툴 안에서 `fetch(poffice_board.json)`·File System Access API가 정상 동작(더블클릭 `file://` 제약 없음).
- 기기마다 경로가 달라도 **최초 1회 폴더 선택**으로 해결(경로는 이 기기에 기억).
- 앱 셸은 거의 안 바뀌므로 배포 부담이 작음(자동업데이트는 이후).

## 구조
```
desktop/
  package.json            electron + electron-builder
  main.js                 pimm:// 프로토콜로 '선택한 폴더' 서빙 + 창/메뉴/폴더피커
  settings.js             userData/settings.json 에 폴더 경로 저장
  preload.js              window.pimm.pickFolder / getFolder / isDesktop
  electron-builder.yml    win nsis(.exe) / mac dmg(.dmg), 무서명(내부)
  assets/setup.html       폴더 미선택 시 안내·선택 화면
  build/icon.png          앱 아이콘(1024) — electron-builder가 .ico/.icns 생성
.github/workflows/desktop-build.yml   윈도우+맥 러너 듀얼빌드 → Release/아티팩트
```

## 로컬 실행 (개발 확인)
```bash
cd desktop
npm install
npm start            # Electron 창 실행 → 첫 실행 시 PIMM_Launcher 폴더 선택
```

## 설치파일 빌드
```bash
npm run dist:win     # → release/PIMM Launcher-0.1.0-Setup.exe  (윈도우에서)
npm run dist:mac     # → release/PIMM Launcher-0.1.0.dmg         (맥에서)
```
> 각 OS 설치파일은 **그 OS(또는 해당 CI 러너)에서** 빌드해야 함. 아래 CI가 둘 다 자동 생성.

## CI 듀얼빌드 (권장 · 이 리눅스 환경에서도 가능)
`desktop-v*` 태그를 push하면 GitHub Actions가 **윈도우 러너 → .exe**, **맥 러너 → .dmg** 를 만들어
해당 태그의 **GitHub Release** 에 첨부(+ 아티팩트 업로드).
```bash
git tag desktop-v0.1.0 && git push origin desktop-v0.1.0
```

## 팀원 사용 흐름
1. Release에서 자기 OS 설치파일 다운로드 → 설치.
2. 첫 실행 → **PIMM_Launcher 폴더 선택**(Google Drive 동기 폴더 안, 허브·툴·`poffice_board` 가 든 곳).
3. 끝. 이후 코워크가 폴더의 `poffice_board.json`·툴 HTML을 갱신하면 **새로고침(Ctrl+R)** 으로 최신 반영.
   - 메뉴: **파일 → 폴더 선택/변경**, **보기 → 홈(허브)·새로고침·개발자 도구**.

## 무서명 안내 (내부 배포)
- 첫 실행 시 **Windows SmartScreen**("추가 정보 → 실행") / **macOS Gatekeeper**(우클릭 → 열기 → 열기) 경고를 우회.
- 서명·공증 원하면: Win 코드서명 인증서 + Apple 개발자 인증서·공증 secrets를 CI에 추가하고
  `electron-builder.yml`의 `win.certificateFile` / `mac.identity` + notarize 를 활성화.

## 이후 확정할 것
- [ ] (선택) 자동 업데이트: `electron-updater` + GitHub Releases (private repo면 토큰 또는 공개 releases repo).
- [ ] (선택) 코드서명·공증(윈 SmartScreen·맥 Gatekeeper 경고 제거).
- [ ] 아이콘 최종본 교체(`build/icon.png`, 1024² 권장) — 현재는 임시 P 마크.

## 검증 참고
- 이 스캐폴드는 로직 재작성 없이 **폴더의 허브/툴을 그대로 감싸는** 구조.
  실제 `npm start`/설치파일 빌드는 **데스크톱 OS/CI 러너**에서 확인해야 함(이 클라우드 세션엔 디스플레이·Electron 런타임 없음).
