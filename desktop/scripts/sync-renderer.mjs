// tool/ 의 최신 PIMM_UnityGameCreator.verX.html 을 renderer/index.html 로 복사.
// 에디터 HTML은 단일 소스(tool/)에 두고, 데스크톱은 빌드 시 최신본을 감싼다(버전 종속 최소).
import { copyFileSync, mkdirSync, readdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const toolDir = join(__dirname, '..', '..', 'tool');
const rendererDir = join(__dirname, '..', 'renderer');
mkdirSync(rendererDir, { recursive: true });

const files = readdirSync(toolDir).filter((f) => /^PIMM_UnityGameCreator\.ver[\d.]+\.html$/.test(f));
if (!files.length) { console.error('tool/ 에서 에디터 HTML을 찾지 못했습니다.'); process.exit(1); }

// 버전(ver1.10 > ver1.9 …) 숫자 비교로 최신 선택.
const ver = (s) => s.match(/ver([\d.]+)/)[1].split('.').map(Number);
files.sort((a, b) => { const av = ver(a), bv = ver(b);
  for (let i = 0; i < Math.max(av.length, bv.length); i++) { const d = (av[i] || 0) - (bv[i] || 0); if (d) return d; } return 0; });
const latest = files[files.length - 1];

copyFileSync(join(toolDir, latest), join(rendererDir, 'index.html'));
console.log(`synced ${latest} → renderer/index.html`);
