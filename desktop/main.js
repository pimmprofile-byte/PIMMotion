// PIMM Launcher — Electron 메인 프로세스
// 아키텍처: 얇은 셸. 콘텐츠(허브·툴·poffice_board)는 각자 Drive-동기 'PIMM_Launcher' 폴더에서 로드.
//  · 최초 실행 시 폴더를 한 번 선택(userData/settings.json 저장) → 이후 그 폴더를 pimm:// 로 서빙.
//  · 코워크/사용자가 폴더만 갱신하면 앱 재배포 없이 즉시 반영.
//  · pimm:// = 보안·표준 오리진 → 툴 안에서 fetch(poffice_board.json)·File System Access API 정상 동작.
const { app, BrowserWindow, protocol, shell, dialog, ipcMain, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const { getFolder, setFolder } = require('./settings');

const SCHEME = 'pimm';
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.ico': 'image/x-icon', '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf',
  '.map': 'application/json', '.txt': 'text/plain' };

// 앱 준비 전에 등록해야 보안 컨텍스트가 확보됨.
protocol.registerSchemesAsPrivileged([
  { scheme: SCHEME, privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true, stream: true } },
]);

let win = null;

// 폴더 안에서 허브 진입 파일 찾기: PIMMotion_Hub.ver{N.M}.html 중 최신 버전.
function findHubEntry(dir) {
  let files = [];
  try { files = fs.readdirSync(dir); } catch { return null; }
  const ver = (s) => (s.match(/ver([\d.]+)/i) || [0, '0'])[1].split('.').map(Number);
  const hubs = files.filter((f) => /^PIMMotion_Hub\.ver[\d.]+\.html$/i.test(f));
  if (hubs.length) {
    hubs.sort((a, b) => { const av = ver(a), bv = ver(b);
      for (let i = 0; i < Math.max(av.length, bv.length); i++) { const d = (av[i] || 0) - (bv[i] || 0); if (d) return d; } return 0; });
    return hubs[hubs.length - 1];
  }
  return files.find((f) => /hub.*\.html$/i.test(f)) || files.find((f) => /\.html$/i.test(f)) || null;
}
function folderValid(dir) { try { return !!dir && fs.existsSync(dir) && !!findHubEntry(dir); } catch { return false; } }

function loadContent() {
  const dir = getFolder();
  if (folderValid(dir)) {
    win.loadURL(`${SCHEME}://app/${findHubEntry(dir)}`);
  } else {
    win.loadFile(path.join(__dirname, 'assets', 'setup.html'));
  }
}

async function pickFolder() {
  const r = await dialog.showOpenDialog(win, {
    title: 'PIMM_Launcher 폴더 선택 (허브·툴·poffice_board 가 있는 Drive 폴더)',
    properties: ['openDirectory'],
  });
  if (r.canceled || !r.filePaths[0]) return { ok: false, canceled: true };
  const dir = r.filePaths[0];
  if (!folderValid(dir)) return { ok: false, error: '이 폴더에서 허브(PIMMotion_Hub.verX.html)를 찾지 못했어요. 허브·툴이 들어있는 PIMM_Launcher 폴더를 선택하세요.' };
  setFolder(dir);
  loadContent();
  buildMenu();
  return { ok: true, dir };
}

function buildMenu() {
  const dir = getFolder();
  const template = [
    { label: '파일', submenu: [
      { label: 'PIMM_Launcher 폴더 선택/변경…', accelerator: 'CmdOrCtrl+O', click: () => pickFolder() },
      { type: 'separator' },
      { role: 'quit', label: '종료' },
    ] },
    { label: '보기', submenu: [
      { label: '홈(허브)', accelerator: 'CmdOrCtrl+H', enabled: folderValid(dir), click: () => loadContent() },
      { label: '새로고침', accelerator: 'CmdOrCtrl+R', click: () => win && win.webContents.reload() },
      { type: 'separator' },
      { role: 'togglefullscreen', label: '전체화면' },
      { role: 'toggleDevTools', label: '개발자 도구' },
      { type: 'separator' },
      { role: 'resetZoom', label: '기본 배율' }, { role: 'zoomIn', label: '확대' }, { role: 'zoomOut', label: '축소' },
    ] },
    { label: '정보', submenu: [
      { label: `PIMM Launcher v${app.getVersion()}`, enabled: false },
      { label: dir ? `폴더: ${dir}` : '폴더 미선택', enabled: false },
      { type: 'separator' },
      { label: '핌아트웍스 홈페이지 열기', click: () => shell.openExternal('https://pimmartworks.com') },
    ] },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

function createWindow() {
  win = new BrowserWindow({
    width: 1440, height: 960, minWidth: 1024, minHeight: 700,
    backgroundColor: '#0f1115', title: 'PIMM Launcher',
    icon: path.join(__dirname, 'build', 'icon.png'),
    webPreferences: { contextIsolation: true, nodeIntegration: false, preload: path.join(__dirname, 'preload.js') },
  });
  buildMenu();
  loadContent();
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:/.test(url)) { shell.openExternal(url); return { action: 'deny' }; }
    return { action: 'allow' };
  });
}

app.whenReady().then(() => {
  // 개발 실행(npm start)에서도 Dock 아이콘을 핌 로고로. (빌드본은 Info.plist에 이미 구워짐)
  if (process.platform === 'darwin' && app.dock) {
    try { app.dock.setIcon(path.join(__dirname, 'build', 'icon.png')); } catch {}
  }

  protocol.handle(SCHEME, async (req) => {
    const dir = getFolder();
    if (!dir) return new Response('폴더 미선택', { status: 404 });
    const url = new URL(req.url);
    let rel = decodeURIComponent(url.pathname).replace(/^\/+/, '');
    if (!rel) rel = findHubEntry(dir) || 'index.html';
    const base = path.resolve(dir);
    const filePath = path.resolve(base, rel);
    if (filePath !== base && !filePath.startsWith(base + path.sep)) return new Response('403 Forbidden', { status: 403 });
    try {
      const data = await fs.promises.readFile(filePath);
      const mime = MIME[path.extname(filePath).toLowerCase()] || 'application/octet-stream';
      return new Response(data, { headers: { 'content-type': mime } });
    } catch {
      return new Response('404 Not Found', { status: 404 });
    }
  });

  ipcMain.handle('pick-folder', () => pickFolder());
  ipcMain.handle('get-folder', () => getFolder());

  createWindow();
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
