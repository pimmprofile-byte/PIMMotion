// 최소 프리로드 — 에디터가 "데스크톱 앱에서 실행 중"임을 알 수 있게만 노출.
// (프로젝트 폴더는 File System Access API로 직접 처리하므로 별도 fs 브리지 불필요.)
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('pimmDesktop', {
  isDesktop: true,
  platform: process.platform, // 'win32' | 'darwin' | 'linux'
});
