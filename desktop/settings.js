// 최소 설정 저장 — userData/settings.json 에 선택한 PIMM_Launcher 폴더 경로 보관.
// (외부 의존 없이 fs 로만. app.getPath는 app ready 이후 호출됨.)
const { app } = require('electron');
const path = require('path');
const fs = require('fs');

function file() { return path.join(app.getPath('userData'), 'settings.json'); }
function read() { try { return JSON.parse(fs.readFileSync(file(), 'utf8')); } catch { return {}; } }
function write(obj) { try { fs.writeFileSync(file(), JSON.stringify(obj, null, 2)); } catch (e) { console.error('settings write 실패', e); } }

function getFolder() { return read().folder || null; }
function setFolder(dir) { const o = read(); o.folder = dir; write(o); }

module.exports = { getFolder, setFolder };
