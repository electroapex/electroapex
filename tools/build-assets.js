// tools/build-assets.js
// Generates self-contained, GitHub-safe animated SVG asset files.
//
// WHY: GitHub's README sanitizer strips ALL inline <svg> markup from markdown
// (verified: 0 rect/circle/animate/text survive in the rendered HTML). It only
// renders external <img src="...svg"> images WITHOUT sanitizing their contents,
// and SMIL <animate> keeps running inside <img>-loaded SVGs (this is how the
// GitHub contribution snake works). So every premium pill/button/card/wave/
// diagram becomes its own self-contained .svg file in assets/ and is referenced
// from README.md as <img>. Gradients use per-file <defs> (ids prefixed by the
// file name) so each file is independent.
//
// Run: node tools/build-assets.js   (re-generates every file in assets/)
// Then commit assets/ to main. Re-run after editing the data tables below.

const fs = require('fs');
const path = require('path');
const OUT = path.join(process.cwd(), 'assets');
fs.mkdirSync(OUT, { recursive: true });

const T = '#e6edf3', MUT = '#8b949e';

function glassGrad(id) {
  return `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">` +
    `<stop offset="0%" stop-color="#ffffff" stop-opacity="0.10"/>` +
    `<stop offset="100%" stop-color="#ffffff" stop-opacity="0.02"/>` +
    `</linearGradient>`;
}
function sheenGrad(id) {
  return `<linearGradient id="${id}" x1="0" y1="0" x2="1" y2="0">` +
    `<stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>` +
    `<stop offset="50%" stop-color="#ffffff" stop-opacity="0.07"/>` +
    `<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>` +
    `</linearGradient>`;
}
function solidGrad(id, hi, lo) {
  return `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">` +
    `<stop offset="0%" stop-color="${hi}" stop-opacity="0.95"/>` +
    `<stop offset="100%" stop-color="${lo}" stop-opacity="0.7"/>` +
    `</linearGradient>`;
}

function wrap(name, width, height, inner) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">${inner}
</svg>`;
}

// Generic pill renderer (matches the original glass-pill style exactly).
// pills: [{label,color,dot}]  layout: {w,h,rx,sheenH,perRow,gapX,gapY,hasDot,dotR,dotAnim,dotCxOff}
function pillRow(name, pills, layout) {
  const { w, h, rx, sheenH = 20, perRow = 3, gapX = 10, gapY = 8,
        hasDot = false, dotR = 3.5, dotAnim = false, dotCxOff = 30 } = layout;
  const cols = perRow;
  const rows = Math.ceil(pills.length / cols);
  const W = cols * w + (cols - 1) * gapX;
  const H = rows * h + (rows - 1) * gapY;
  const g = [];
  g.push(glassGrad(`${name}_bg`));
  g.push(sheenGrad(`${name}_sh`));
  pills.forEach((p, i) => {
    g.push(solidGrad(`${name}_f${i}`, p.color, '#000'));
  });
  const defs = `<defs>${g.join('')}</defs>`;
  let body = '';
  let x = 0, y = 0, col = 0;
  pills.forEach((p, i) => {
    const dot = hasDot
      ? `<circle cx="${x + dotCxOff}" cy="${y + h / 2}" r="${dotR}" fill="${p.color}">` +
        (dotAnim
          ? `<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/>`
          : '') +
        `</circle>`
      : '';
    body +=
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${p.color}" opacity="0.10"/>` +
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="url(#${name}_f${i})"/>` +
      `<rect x="${x - 1}" y="${y + 1}" width="${w - 2}" height="${h - 2}" rx="${rx - 1}" fill="none" stroke="${p.color}" stroke-opacity="0.5" stroke-width="1"/>` +
      `<rect x="${x}" y="${y}" width="${w}" height="${sheenH}" rx="${sheenH}" fill="url(#${name}_sh)"/>` +
      dot +
      `<text x="${x + w / 2}" y="${y + h * 0.62}" text-anchor="middle" fill="${T}" font-size="12.5" letter-spacing="0.6" font-family="'Segoe UI',sans-serif">${p.label}</text>`;
    col++;
    if (col >= cols) { col = 0; x = 0; y += h + gapY; } else { x += w + gapX; }
  });
  return wrap(name, W, H, `${defs}${body}`);
}

// ===== HERO: animated wave + animated-gradient name =====
function hero() {
  return wrap('hero', 900, 90,
    `<defs>${glassGrad('h_bg')}
<linearGradient id="h_wave" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#00D4AA" stop-opacity="0"/>
<stop offset="50%" stop-color="#00D4AA" stop-opacity="0.6"/>
<stop offset="100%" stop-color="#00D4AA" stop-opacity="0"/>
<animate attributeName="x1" values="0%;100%;0%" dur="8s" repeatCount="indefinite"/>
<animate attributeName="x2" values="100%;0%;100%" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="h_name" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#00D4AA"/><stop offset="50%" stop-color="#58A6FF"/><stop offset="100%" stop-color="#00D4AA"/>
<animate attributeName="x1" values="0%;100%;0%" dur="4s" repeatCount="indefinite"/>
<animate attributeName="x2" values="100%;0%;100%" dur="4s" repeatCount="indefinite"/>
</linearGradient></defs>
<rect width="900" height="90" fill="url(#h_bg)"/>
<path d="M0,60 Q112,90 224,60 T672,60 T896,60 L900,90 L0,90 Z" fill="url(#h_wave)" opacity="0.6"/>
<text x="450" y="36" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="27" font-weight="700" fill="url(#h_name)">M Huzaifa Hafeez</text>
<text x="450" y="64" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="12" fill="#8b949e" letter-spacing="0.8">Full-Stack &amp; DevOps Engineer</text>`);
}

// ===== Bottom wave =====
function waveBottom() {
  return wrap('wave-bottom', 900, 50,
    `<defs>
<linearGradient id="wb_wave" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#00D4AA" stop-opacity="0"/>
<stop offset="50%" stop-color="#00D4AA" stop-opacity="0.55"/>
<stop offset="100%" stop-color="#00D4AA" stop-opacity="0"/>
<animate attributeName="x1" values="0%;100%;0%" dur="9s" repeatCount="indefinite"/>
<animate attributeName="x2" values="100%;0%;100%" dur="9s" repeatCount="indefinite"/>
</linearGradient></defs>
<path d="M0,10 Q75,30 150,10 T600,10 T900,10 L900,50 L0,50 Z" fill="url(#wb_wave)" opacity="0.7"/>
<path d="M0,25 Q75,45 150,25 T600,25 T900,25 L900,50 L0,50 Z" fill="#00D4AA" opacity="0.2"/>`);
}

// ===== CTA / contact buttons (clickable individually in README) =====
const BTN_W = 176, BTN_H = 52;
const buttons = [
  { name: 'resume', label: 'RESUME', color: '#00D4AA', hi: '#00D4AA', lo: '#00A3A0' },
  { name: 'portfolio', label: 'PORTFOLIO', color: '#58A6FF', hi: '#58A6FF', lo: '#316DCA' },
  { name: 'linkedin', label: 'LINKEDIN', color: '#0A66C2', hi: '#0077B5', lo: '#0A66C2' },
  { name: 'email', label: 'EMAIL', color: '#F78166', hi: '#F78166', lo: '#D1242F' },
  { name: 'github', label: 'GITHUB', color: '#8b949e', hi: '#21262D', lo: '#161B22' },
];
function button(b) {
  return wrap(`btn_${b.name}`, BTN_W, BTN_H,
    `<defs>${glassGrad(`g`)} ${solidGrad('bg', b.hi, b.lo)} ${sheenGrad('sh')}</defs>
<rect x="2" y="4" width="172" height="44" rx="22" fill="${b.hi}" opacity="0.32"/>
<rect width="${BTN_W}" height="${BTN_H}" rx="26" fill="url(#bg)"/>
<rect x="1" y="1" width="174" height="50" rx="25" fill="none" stroke="${b.color}" stroke-opacity="0.6" stroke-width="1.2"/>
<rect width="${BTN_W}" height="24" rx="24" fill="url(#sh)"/>
<circle cx="34" cy="26" r="4" fill="#ffffff"><animate attributeName="opacity" values="1;0.5;1" dur="2.2s" repeatCount="indefinite"/></circle>
<text x="100" y="31" text-anchor="middle" fill="#ffffff" font-size="14.5" letter-spacing="1.4" font-weight="600" font-family="'Segoe UI',sans-serif">${b.label}</text>`);
}

// ===== Stat cards (baked real counts: Followers 1, Repos 2) =====
const STATS_W = 208, STATS_H = 48;
const stats = [
  { name: 'views', label: 'PROFILE VIEWS', value: '—', color: '#00D4AA' },
  { name: 'followers', label: 'FOLLOWERS', value: '1', color: '#58A6FF' },
  { name: 'repos', label: 'REPOSITORIES', value: '2', color: '#FF9E64' },
];
function statCard(s) {
  return wrap(`stat_${s.name}`, STATS_W, STATS_H,
    `<defs>${glassGrad('g')} ${solidGrad('bg', s.color, '#000')} ${sheenGrad('sh')}</defs>
<rect x="2" y="2" width="204" height="44" rx="22" fill="${s.color}" opacity="0.08"/>
<rect width="${STATS_W}" height="${STATS_H}" rx="24" fill="url(#bg)"/>
<rect x="1" y="1" width="206" height="46" rx="23" fill="none" stroke="${s.color}" stroke-opacity="0.5" stroke-width="1.1"/>
<rect width="${STATS_W}" height="24" rx="24" fill="url(#sh)"/>
<circle cx="30" cy="24" r="7" fill="none" stroke="${s.color}" stroke-width="1.4"><animate attributeName="r" values="6;8;6" dur="2.6s" repeatCount="indefinite"/></circle>
<text x="52" y="24" fill="#8b949e" font-size="12.5" letter-spacing="0.6" font-family="'Segoe UI',sans-serif">${s.label}</text>
<text x="200" y="42" text-anchor="end" fill="#e6edf3" font-size="12" font-weight="600" font-family="'Segoe UI',sans-serif">${s.value}</text>`);
}

// ===== Nav pills (decorative row; section anchors exist on headings) =====
const navItems = [
  { label: 'ABOUT', color: '#00D4AA' }, { label: 'BUILD', color: '#009688' },
  { label: 'EXPERIENCE', color: '#326CE5' }, { label: 'STACK', color: '#BC8CFF' },
  { label: 'WORKFLOW', color: '#2088FF' }, { label: 'ARCHITECTURE', color: '#00D4AA' },
  { label: 'SECURITY', color: '#3FB950' }, { label: 'ANALYTICS', color: '#FF9E64' },
  { label: 'LEARNING', color: '#BC8CFF' }, { label: 'PROJECTS', color: '#3FB950' },
];
function nav() {
  const W = 128, H = 40, gap = 10;
  const total = navItems.length * W + (navItems.length - 1) * gap;
  const gDefs = navItems.map((n, i) =>
    `<linearGradient id="ng${i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="${n.color}" stop-opacity="0.14"/><stop offset="100%" stop-color="${n.color}" stop-opacity="0.07"/></linearGradient>`
  ).join('');
  let x = 0;
  const pills = navItems.map((n, i) => {
    const d = `<rect x="${x}" y="2" width="124" height="36" rx="18" fill="${n.color}" opacity="0.12"/>`;
    const mid = `<rect x="${x}" y="0" width="${W}" height="${H}" rx="64" fill="url(#ng${i})"/>`;
    const stroke = `<rect x="${x-1}" y="1" width="${W-2}" height="${H-2}" rx="63" fill="none" stroke="${n.color}" stroke-opacity="0.5" stroke-width="1.1"/>`;
    const dot = `<circle cx="${x+24}" cy="20" r="3" fill="${n.color}"/>`;
    const txt = `<text x="${x+W/2}" y="25" text-anchor="middle" fill="#e6edf3" font-size="12.5" letter-spacing="1.2" font-family="'Segoe UI',sans-serif">${n.label}</text>`;
    x += W + gap;
    return [d, mid, stroke, dot, txt].join('');
  }).join('');
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 ${total} ${H}" width="${total}" height="${H}" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="nav_sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity="0"/><stop offset="50%" stop-color="#ffffff" stop-opacity="0.07"/><stop offset="100%" stop-color="#ffffff" stop-opacity="0"/></linearGradient>${gDefs}</defs>
<rect width="${total}" height="${H}" rx="20" fill="url(#nav_sheen)"/>
<g>${pills}</g></svg>`;
}

// ===== Divider =====
function divider() {
  return wrap('divider', 200, 12,
    `<line x1="0" y1="6" x2="88" y2="6" stroke="#00D4AA" stroke-width="1" opacity="0.4"/>` +
    `<line x1="112" y1="6" x2="200" y2="6" stroke="#00D4AA" stroke-width="1" opacity="0.4"/>` +
    `<circle cx="100" cy="6" r="3" fill="#00D4AA">` +
    `<animate attributeName="r" values="2;4;2" dur="1.6s" repeatCount="indefinite"/>` +
    `<animate attributeName="opacity" values="0.6;1;0.6" dur="1.6s" repeatCount="indefinite"/>` +
    `</circle>`);
}

// ===== Workflow diagram =====
function workflowDiagram() {
  return wrap('workflow-diagram', 900, 130,
    `<defs>
<linearGradient id="wd_bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#161B22" stop-opacity="0.95"/><stop offset="100%" stop-color="#0d1117" stop-opacity="0.9"/></linearGradient>
<linearGradient id="wd_sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity="0"/><stop offset="50%" stop-color="#ffffff" stop-opacity="0.07"/><stop offset="100%" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>
<rect width="900" height="130" rx="14" fill="url(#wd_bg)" stroke="#00D4AA" stroke-opacity="0.5" stroke-width="1.5"/>
<rect x="1" y="1" width="898" height="30" rx="13" fill="url(#wd_sheen)"/>
` +
    ['Plan','Containerize','Orchestrate'].map((lbl, i) => {
      const cx = 85 + i*280;
      return `<rect x="${cx-65}" y="35" width="130" height="50" rx="10" fill="#161B22" stroke="#00D4AA" stroke-width="1.5"/>` +
        `<text x="${cx}" y="57" text-anchor="middle" fill="#e6edf3" font-size="13" font-family="sans-serif" font-weight="bold">${lbl}</text>` +
        `<text x="${cx}" y="73" text-anchor="middle" fill="#8b949e" font-size="10" font-family="sans-serif">${['Architecture','Docker','Kubernetes'][i]}</text>`;
    }).join('') +
    `<circle cx="740" cy="60" r="6" fill="#00D4AA"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>` +
    `<text x="865" y="64" text-anchor="middle" fill="#00D4AA" font-size="11" font-family="sans-serif">Ship</text>` +
    `<text x="85" y="110" text-anchor="middle" fill="#8b949e" font-size="10" font-family="sans-serif">Git · API · DB</text>` +
    `<text x="365" y="110" text-anchor="middle" fill="#8b949e" font-size="10" font-family="sans-serif">CI/CD · Test</text>` +
    `<text x="645" y="110" text-anchor="middle" fill="#8b949e" font-size="10" font-family="sans-serif">Deploy · Monitor</text>` +
    `<line x1="150" y1="60" x2="288" y2="60" stroke="#00D4AA" stroke-width="2" stroke-dasharray="6 6"/>` +
    `<line x1="430" y1="60" x2="568" y2="60" stroke="#00D4AA" stroke-width="2" stroke-dasharray="6 6"/>` +
    `<line x1="710" y1="60" x2="828" y2="60" stroke="#00D4AA" stroke-width="2" stroke-dasharray="6 6"/>`);
}

// ===== Section data tables =====
const identity = [
  { label: 'Full Stack Developer', color: '#00D4AA' },
  { label: 'DevOps Engineer', color: '#58A6FF' },
  { label: 'Cloud Native', color: '#BC8CFF' },
  { label: 'Open Source', color: '#3FB950' },
  { label: 'Docker', color: '#2496ED' },
  { label: 'Kubernetes', color: '#326CE5' },
];
const learning = [
  { label: 'Advanced Kubernetes', color: '#326CE5' },
  { label: 'Microservices', color: '#00D4AA' },
  { label: 'System Design', color: '#009688' },
  { label: 'Cloud Infrastructure', color: '#2088FF' },
  { label: 'Distributed Systems', color: '#3FB950' },
  { label: 'Web Security', color: '#FF9E64' },
  { label: 'Scalable Backends', color: '#BC8CFF' },
];
const goals = [
  { label: 'Ship · Microservices on K8s', color: '#326CE5' },
  { label: 'Launch · 3 Production Apps', color: '#00D4AA' },
  { label: 'Contribute · 5+ Open Source', color: '#009688' },
  { label: 'Certify · CKA / CKAD', color: '#4E9E31' },
  { label: 'Release · ATS Platform', color: '#BC8CFF' },
  { label: 'Build · Documented OSS', color: '#FF9E64' },
];
const knowledge = [
  { label: 'Frontend Architecture', color: '#61DAFB' },
  { label: 'Backend Engineering', color: '#339933' },
  { label: 'Data & Storage', color: '#47A248' },
  { label: 'DevOps & Cloud', color: '#2496ED' },
  { label: 'Security', color: '#005571' },
  { label: 'Tooling', color: '#F05032' },
];
const principles = [
  { label: 'Simplicity · Readable', color: '#00D4AA' },
  { label: 'Architecture · Before Code', color: '#009688' },
  { label: 'Security · By Default', color: '#3FB950' },
  { label: 'Automation · Scripted', color: '#2088FF' },
  { label: 'Shipping · Production', color: '#4E9E31' },
  { label: 'Observability', color: '#BC8CFF' },
];
const architecture = [
  { label: 'Layered Architecture', color: '#00D4AA' },
  { label: 'REST Consistency', color: '#009688' },
  { label: 'Scalable Data', color: '#3FB950' },
  { label: 'Maintainability', color: '#326CE5' },
  { label: 'Performance', color: '#2088FF' },
  { label: 'Code Quality', color: '#BC8CFF' },
];
const security = [
  { label: 'Auth · First-Class Design', color: '#3FB950' },
  { label: 'Validation · Never Trust Client', color: '#00D4AA' },
  { label: 'Secrets · Environment Only', color: '#005571' },
  { label: 'Hardening · HTTPS & Headers', color: '#4E9E31' },
  { label: 'OWASP · Injection / XSS / CSRF', color: '#FF9E64' },
];
const projects = [
  { label: 'Boiler Plate Generator', color: '#00D4AA' },
  { label: 'Accounting Application', color: '#00D4AA' },
  { label: 'Image & Video Editor', color: '#00D4AA' },
  { label: 'eCommerce Builder', color: '#00D4AA' },
  { label: 'Job Portal Platform', color: '#00D4AA' },
  { label: 'ATS Resume Optimization', color: '#00D4AA' },
  { label: 'Deployment Pipelines', color: '#BC8CFF' },
];
const opensource = [
  { label: 'Open Source Contributor', color: '#00D4AA' },
  { label: 'Documented Code', color: '#00D4AA' },
  { label: 'PRs Welcome', color: '#00D4AA' },
];
const askme = [
  { label: 'Full Stack Development', color: '#00D4AA' },
  { label: 'REST API Design', color: '#009688' },
  { label: 'Authentication', color: '#3FB950' },
  { label: 'Docker & Kubernetes', color: '#326CE5' },
  { label: 'CI/CD Pipelines', color: '#4E9E31' },
  { label: 'Database Design', color: '#4479A1' },
  { label: 'Security Practices', color: '#005571' },
];
const workflowSteps = [
  { label: '01 · Planning & Architecture', color: '#00D4AA' },
  { label: '02 · Version Control', color: '#F05032' },
  { label: '03 · Containerization', color: '#2496ED' },
  { label: '04 · Orchestration', color: '#326CE5' },
  { label: '05 · API Development', color: '#009688' },
  { label: '06 · Database Design', color: '#4479A1' },
  { label: '07 · Testing & Debugging', color: '#3FB950' },
  { label: '08 · CI/CD Automation', color: '#2088FF' },
  { label: '09 · Production Deployment', color: '#4E9E31' },
  { label: '10 · Monitoring & Maintenance', color: '#FF9E64' },
  { label: '11 · Security Review', color: '#005571' },
];

// ===== File registry =====
const files = {
  'hero.svg': hero(),
  'wave-bottom.svg': waveBottom(),
  'divider.svg': divider(),
  'workflow-diagram.svg': workflowDiagram(),
  'nav.svg': nav(),
  ...Object.fromEntries(buttons.map((b) => [`btn-${b.name}.svg`, button(b)])),
  ...Object.fromEntries(stats.map((s) => [`stat-${s.name}.svg`, statCard(s)])),
  'identity.svg': pillRow('identity', identity, { w: 168, h: 40, rx: 20, perRow: 3, hasDot: true, dotCxOff: 32 }),
  'about-identity.svg': pillRow('aboutid', [
    { label: 'Design → Build → Ship', color: '#00D4AA' },
    { label: 'Node · React · Mongo', color: '#3FB950' },
    { label: 'Docker · Kubernetes', color: '#2496ED' },
  ], { w: 168, h: 40, rx: 20, perRow: 3, hasDot: true, dotCxOff: 30, dotAnim: false }),
  'about-location.svg': pillRow('aboutloc', [
    { label: 'Location · Pakistan', color: '#00D4AA' },
    { label: 'Open To Remote Work', color: '#00D4AA' },
    { label: 'OS · Fedora Linux', color: '#00D4AA' },
    { label: 'Core · Authentication', color: '#00D4AA' },
  ], { w: 140, h: 32, rx: 16, perRow: 4, hasDot: false }),
  'about-background.svg': pillRow('aboutbg', [
    { label: 'Foundation · C / C++ / Python', color: '#00599C' },
    { label: 'Specialty · JS Ecosystem', color: '#3178C6' },
    { label: 'Expansion · DevOps & Infra', color: '#2496ED' },
    { label: 'Scope · Product & Security', color: '#BC8CFF' },
    { label: 'Building · ATS & Job Portal', color: '#00D4AA' },
  ], { w: 150, h: 32, rx: 16, perRow: 3, hasDot: false }),
  'build.svg': pillRow('build', [
    { label: 'Full Stack Applications', color: '#00D4AA' },
    { label: 'Scalable REST APIs', color: '#009688' },
    { label: 'Authentication Systems', color: '#3FB950' },
    { label: 'Production Ready Software', color: '#4E9E31' },
    { label: 'Dockerized Applications', color: '#2496ED' },
    { label: 'Kubernetes Deployments', color: '#326CE5' },
    { label: 'CI/CD Pipelines', color: '#2088FF' },
    { label: 'Admin Dashboards', color: '#BC8CFF' },
    { label: 'Job Portals & ATS', color: '#FF9E64' },
  ], { w: 172, h: 32, rx: 16, perRow: 3, hasDot: false }),
  'experience.svg': pillRow('exp', [
    { label: 'Full Stack · Concept → Deploy', color: '#00D4AA' },
    { label: 'Backend & API · REST · Auth', color: '#009688' },
    { label: 'DevOps & Deploy · CI/CD', color: '#326CE5' },
    { label: 'Freelance · Product & OSS', color: '#BC8CFF' },
  ], { w: 170, h: 32, rx: 16, perRow: 4, hasDot: false }),
  'allprojects.svg': pillRow('note', [
    { label: 'All projects in active development', color: '#00D4AA' },
  ], { w: 200, h: 32, rx: 16, perRow: 1, hasDot: false }),
  'learning.svg': pillRow('learning', learning, { w: 168, h: 32, rx: 16, perRow: 4, hasDot: false }),
  'goals.svg': pillRow('goals', goals, { w: 170, h: 32, rx: 16, perRow: 3, hasDot: false }),
  'knowledge.svg': pillRow('knowledge', knowledge, { w: 160, h: 32, rx: 15, perRow: 3, hasDot: false }),
  'principles.svg': pillRow('principles', principles, { w: 160, h: 32, rx: 15, perRow: 3, hasDot: false }),
  'architecture.svg': pillRow('architecture', architecture, { w: 160, h: 32, rx: 15, perRow: 3, hasDot: false }),
  'security.svg': pillRow('security', security, { w: 168, h: 32, rx: 16, perRow: 3, hasDot: false }),
  'projects.svg': pillRow('projects', projects, { w: 186, h: 40, rx: 20, perRow: 3, hasDot: false }),
  'opensource.svg': pillRow('opensource', opensource, { w: 176, h: 40, rx: 20, perRow: 3, hasDot: false }),
  'askme.svg': pillRow('askme', askme, { w: 152, h: 32, rx: 16, perRow: 4, hasDot: false }),
  'workflow-steps.svg': pillRow('wsteps', workflowSteps, { w: 158, h: 32, rx: 15, perRow: 4, hasDot: false }),
};

for (const [name, content] of Object.entries(files)) {
  fs.writeFileSync(path.join(OUT, name), content);
  console.log(`wrote assets/${name}`);
}
console.log(`\nTotal: ${Object.keys(files).length} files`);
