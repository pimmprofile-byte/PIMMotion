// 프리로드 — 렌더러(허브/툴/설정 화면)에 최소 안전 API 노출.
// 툴 HTML은 자체완결이라 이 API를 안 써도 되고, 설정 화면(setup.html)만 pickFolder 사용.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('pimm', {
  isDesktop: true,
  platform: process.platform,        // 'win32' | 'darwin' | 'linux'
  pickFolder: () => ipcRenderer.invoke('pick-folder'),
  getFolder: () => ipcRenderer.invoke('get-folder'),
});
