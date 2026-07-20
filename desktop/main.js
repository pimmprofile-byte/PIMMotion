// PIMMotion 데스크톱 앱 — Electron 메인 프로세스
// 핵심: 커스텀 보안 프로토콜(pimm://)로 에디터 HTML을 서빙 → File System Access API
// (showDirectoryPicker 등, 프로젝트 폴더 기능)가 보안 컨텍스트에서 그대로 동작.
// file://로 직접 로드하면 showDirectoryPicker가 막히므로 이 방식을 쓴다.
const { app, BrowserWindow, protocol, shell } = require('electron');
const path = require('path');
const fs = require('fs');

const RENDERER_DIR = path.join(__dirname, 'renderer');
const SCHEME = 'pimm';

// 보안·표준 오리진으로 등록(앱 준비 전에 호출해야 함) → 보안 컨텍스트 확보.
protocol.registerSchemesAsPrivileged([
  { scheme: SCHEME, privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2' };

function createWindow() {
  const win = new BrowserWindow({
    width: 1600, height: 1000, minWidth: 1024, minHeight: 700,
    backgroundColor: '#1e1e1e',
    title: 'PIMMotion',
    // icon: path.join(__dirname, 'assets', process.platform === 'win32' ? 'icon.ico' : 'icon.png'), // 2.0 로고
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, 'preload.js'),
    },
  });
  win.removeMenu(); // 에디터 크롬 최소화(유니티/어도비식)
  win.loadURL(`${SCHEME}://app/index.html`);

  // 외부 http(s) 링크는 시스템 기본 브라우저로.
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:/.test(url)) { shell.openExternal(url); return { action: 'deny' }; }
    return { action: 'allow' };
  });
}

app.whenReady().then(() => {
  protocol.handle(SCHEME, (req) => {
    const url = new URL(req.url);
    let rel = decodeURIComponent(url.pathname);
    if (rel === '/' || rel === '') rel = '/index.html';
    const filePath = path.normalize(path.join(RENDERER_DIR, rel));
    // 디렉터리 탈출 방지
    if (!filePath.startsWith(RENDERER_DIR)) return new Response('403 Forbidden', { status: 403 });
    try {
      const data = fs.readFileSync(filePath);
      const mime = MIME[path.extname(filePath).toLowerCase()] || 'application/octet-stream';
      return new Response(data, { headers: { 'content-type': mime } });
    } catch {
      return new Response('404 Not Found', { status: 404 });
    }
  });

  createWindow();
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});

app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
