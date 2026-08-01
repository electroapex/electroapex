// tools/build-readme.js
// Generates README.md as a clean, GitHub-safe dark profile:
//   - animated hero SVG (assets/hero.svg via <img>)
//   - shields.io `for-the-badge` badges for every section label (pill-shaped, GitHub-safe)
//   - standard live widgets (typing, quote, activity-graph, streak, trophies mirror,
//     profile-summary, snake, giphy) + exact Tech Stack badges.
// GitHub strips inline <svg>/<style>/@keyframes; shields badges and widget <img>s render.
// Run: node tools/build-readme.js

const fs = require('fs');
const path = require('path');
const A = 'https://raw.githubusercontent.com/electroapex/electroapex/main/assets/';
const USER = 'electroapex';
const GH = 'https://github.com/' + USER;
function enc(s){ return encodeURIComponent(String(s)); }

// static colored pill (logo optional)
function pill(label, color, logo = '', href = '') {
  let u = `https://img.shields.io/badge/${enc(label)}-${color}?style=for-the-badge`;
  if (logo) u += `&logo=${logo}&logoColor=white`;
  const img = `<img src="${u}" height="30" alt="${label}">`;
  return href ? `<a href="${href}" target="_blank">${img}</a>` : img;
}
// live dynamic count badge
function count(api, label, logo = '') {
  let u = `https://img.shields.io/${api}?style=for-the-badge&label=${enc(label)}&units=short`;
  if (logo) u += `&logo=${logo}&logoColor=white`;
  return `<img src="${u}" height="30" alt="${label}">`;
}

const L = [];
const line = (s='') => L.push(s);

/* ---------- Header ---------- */
line('<!-- Clean dark profile — shields.io badges (GitHub-safe) + animated hero + live widgets. Regenerate: node tools/build-readme.js -->');
line('');
line('<div align="center">');
line('  <img src="'+A+'hero.svg" width="900" alt="M Huzaifa Hafeez — Full-Stack & DevOps Engineer"/>');
line('</div>');
line('');
line('<div align="center">');
line('  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=3200&pause=900&color=00D4AA&center=true&vCenter=true&width=560&lines=Full-Stack+Web+Developer;REST+APIs+%7C+Authentication+%7C+DevOps;Docker+%7C+Kubernetes+%7C+CI%2FCD;Building+Production-Grade+Software" alt="Typing Animation"/>');
line('</div>');
line('');
line('## Professional Identity');
line('<p align="center">');
line('  '+pill('Full Stack Developer','00D4AA'));
line('  '+pill('DevOps Engineer','58A6FF'));
line('  '+pill('Cloud Native','BC8CFF'));
line('  '+pill('Open Source','3FB950'));
line('  '+pill('Docker','2496ED','docker'));
line('  '+pill('Kubernetes','326CE5','kubernetes'));
line('</p>');
line('');
line('---');
line('');

/* ---------- About ---------- */
line('## About Me');
line('<img align="right" src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="220px" alt="Coding"/>');
line('');
line('<p align="center">');
line('  '+pill('Design → Build → Ship','00D4AA'));
line('  '+pill('Node · React · Mongo','3FB950'));
line('  '+pill('Docker · Kubernetes','2496ED'));
line('</p>');
line('<p align="center">');
line('  '+pill('Location · Pakistan','6e7681'));
line('  '+pill('Open To Remote Work','6e7681'));
line('  '+pill('OS · Fedora Linux','6e7681','fedora'));
line('  '+pill('Core · Authentication','6e7681'));
line('</p>');
line('');
line('<details>');
line('<summary><b>Background</b></summary>');
line('<br>');
line('<p align="center">');
line('  '+pill('Foundation · C / C++ / Python','00599C','c'));
line('  '+pill('Specialty · JS Ecosystem','3178C6'));
line('  '+pill('Expansion · DevOps & Infra','2496ED','docker'));
line('  '+pill('Scope · Product & Security','BC8CFF'));
line('  '+pill('Building · ATS & Job Portal','00D4AA'));
line('</p>');
line('</details>');
line('');
line('---');
line('');

/* ---------- What I Build ---------- */
line('## What I Build');
line('');
const build = [
  ['Full Stack Applications','00D4AA',''],['Scalable REST APIs','009688',''],['Authentication Systems','3FB950',''],
  ['Production Ready Software','4E9E31',''],['Dockerized Applications','2496ED','docker'],['Kubernetes Deployments','326CE5','kubernetes'],
  ['CI/CD Pipelines','2088FF','githubactions'],['Admin Dashboards','BC8CFF',''],['Job Portals & ATS','FF9E64',''],
];
line('<p align="center">');
build.forEach(p=>line('  '+pill(p[0],p[1],p[2])));
line('</p>');
line('');

/* ---------- Experience ---------- */
line('## Professional Experience');
line('<p align="center">');
line('  '+pill('Full Stack · Concept → Deploy','00D4AA'));
line('  '+pill('Backend & API · REST · Auth','009688'));
line('  '+pill('DevOps & Deploy · CI/CD','326CE5'));
line('  '+pill('Freelance · Product & OSS','BC8CFF'));
line('</p>');
line('');
line('---');
line('');

/* ---------- Tech Stack (exact, unchanged) ---------- */
line('## Tech Stack');
line('');
const stack = {
 Frontend:[['HTML5','E34F26','html5','white'],['CSS3','1572B6','css3','white'],['JavaScript','F7DF1E','javascript','black'],['ES2025+','F7DF1E','javascript','black'],['TypeScript','3178C6','typescript','white'],['React.js','61DAFB','react','black'],['Next.js','000000','nextdotjs','white'],['Tailwind CSS','06B6D4','tailwindcss','white'],['Redux Toolkit','764ABC','redux','white'],['Vite','646CFF','vite','white'],['EJS','B4CA65','ejs','black']],
 Backend:[['Node.js','339933','nodedotjs','white'],['Express.js','000000','express','white'],['REST API','009688',''],['JWT','000000','jsonwebtokens','white'],['Session Auth','6DB33F',''],['Cookie Auth','FF8800',''],['Auth & Authorization','005571','']],
 Databases:[['MongoDB','47A248','mongodb','white'],['MySQL','4479A1','mysql','white']],
 DevOps:[['Docker','2496ED','docker','white'],['Kubernetes','326CE5','kubernetes','white'],['Nginx','009639','nginx','white'],['GitHub Actions','2088FF','githubactions','white'],['CI/CD','4E9E31',''],['PM2','2B037A',''],['Linux','FCC624','linux','black'],['Fedora','294172','fedora','white'],['VPS','8B5CF6',''],['Vercel','000000','vercel','white']],
 Languages:[['JavaScript','F7DF1E','javascript','black'],['TypeScript','3178C6','typescript','white'],['C','00599C','c','white'],['C++','00599C','cplusplus','white'],['Python','3776AB','python','white'],['Git','F05032','git','white'],['GitHub','181717','github','white'],['VS Code','007ACC','visualstudiocode','white'],['PhpStorm','000000','phpstorm','white'],['Postman','FF6C37','postman','white'],['Figma','F24E1E','figma','white'],['npm','CB3837','npm','white'],['pnpm','F69220','pnpm','white']]
};
const stackTitles = {Frontend:'Frontend',Backend:'Backend',Databases:'Databases',DevOps:'DevOps & Deployment',Languages:'Languages & Tools'};
for (const key of ['Frontend','Backend','Databases','DevOps','Languages']) {
  line(`<div align="center"><sub><b>${stackTitles[key]}</b></sub></div>`);
  line('<p align="center">');
  stack[key].forEach(([lbl,c,logo,txt]) => {
    let u = `https://img.shields.io/badge/${enc(lbl)}-${c}?style=for-the-badge`;
    if (logo) u += `&logo=${logo}&logoColor=${txt||'white'}`;
    line(`  <img src="${u}" height="30" alt="${lbl}"/>`);
  });
  line('</p>');
  line('');
}
line('---');
line('');

/* ---------- Development Workflow (11 steps) ---------- */
line('## Development Workflow');
line('');
line('<p align="center">');
line('  '+pill('Plan','00D4AA')+pill('→ Containerize','2496ED','docker')+pill('→ Orchestrate','326CE5','kubernetes')+pill('→ Ship','FF9E64'));
line('</p>');
line('');
line('<details>');
line('<summary><b>11-Step Pipeline</b></summary>');
line('<br>');
const steps = [
  [['01 · Planning & Architecture','00D4AA',''],['02 · Version Control','F05032','git'],['03 · Containerization','2496ED','docker'],['04 · Orchestration','326CE5','kubernetes']],
  [['05 · API Development','009688',''],['06 · Database Design','4479A1','mysql'],['07 · Testing & Debugging','3FB950',''],['08 · CI/CD Automation','2088FF','githubactions']],
  [['09 · Production Deployment','4E9E31',''],['10 · Monitoring & Maintenance','FF9E64',''],['11 · Security Review','005571','']]
];
steps.forEach(row=>{line('<p align="center">');row.forEach(p=>line('  '+pill(p[0],p[1],p[2])));line('</p>');});
line('</details>');
line('');
line('---');
line('');

/* ---------- Architecture / Security ---------- */
line('## Architecture & Best Practices');
line('<p align="center">');
line('  '+pill('Layered Architecture','00D4AA')+pill('REST Consistency','009688')+pill('Scalable Data','3FB950')+pill('Maintainability','326CE5')+pill('Performance','2088FF')+pill('Code Quality','BC8CFF'));
line('</p>');
line('');
line('## Security Practices');
line('<p align="center">');
line('  '+pill('Auth · First-Class Design','3FB950')+pill('Validation · Never Trust Client','00D4AA')+pill('Secrets · Environment Only','005571')+pill('Hardening · HTTPS & Headers','4E9E31')+pill('OWASP · Injection / XSS / CSRF','FF9E64'));
line('</p>');
line('');
line('---');
line('');

/* ---------- GitHub Analytics (live widgets) ---------- */
line('## GitHub Analytics');
line('<p align="center">');
line('  '+count(`github/followers/${USER}`,'Followers','github')+'  '+count(`github/stars/${USER}/${USER}`,'Stars','star')+'  '+count(`github/languages/${USER}/${USER}`,'Top Language')+'  '+count(`github/repo-size/${USER}/${USER}`,'Repo Size'));
line('</p>');
line('<p align="center">');
line('  <img height="170" src="https://streak-stats.demolab.com/?user='+USER+'&background=0d1117&border=00D4AA&stroke=00D4AA&ring=00D4AA&fire=00D4AA&currStreakLabel=00D4AA&currStreakNum=ffffff&sideNums=c9d1d9&sideLabels=c9d1d9" alt="GitHub Streak"/>');
line('</p>');
line('<details open>');
line('<summary><b>Trophies & Profile Summary</b></summary>');
line('<br>');
line('<p align="center">');
line('  <img src="https://github-profile-trophy-orcin-eta.vercel.app/?username='+USER+'&theme=nord_dark&no-frame=true&row=2&column=4&margin-w=12&margin-h=12" alt="GitHub Trophies"/>');
line('</p>');
line('<p align="center">');
line('  <img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username='+USER+'&theme=vue_dark" alt="Profile Summary"/>');
line('</p>');
line('</details>');
line('');

/* ---------- Contribution Activity (snake) ---------- */
line('## Contribution Activity');
line('<p align="center">');
line('  <img src="https://github-readme-activity-graph.vercel.app/graph?username='+USER+'&bg_color=0d1117&color=00d4aa&line=00d4aa&point=ffffff&area=true&hide_border=true&radius=8" alt="Contribution Graph"/>');
line('</p>');
line('<p align="center">');
line('  <!-- Snake animates once the "Generate Snake" workflow has run (writes to `output` branch). -->');
line('  <img src="https://raw.githubusercontent.com/electroapex/electroapex/output/github-contribution-grid-snake-dark.svg" alt="Snake Animation"/>');
line('</p>');
line('');
line('---');
line('');

/* ---------- Learning / Goals / Knowledge / Principles ---------- */
line('## Currently Learning');
line('<p align="center">');
line('  '+pill('Advanced Kubernetes','326CE5','kubernetes')+pill('Microservices','00D4AA')+pill('System Design','009688')+pill('Cloud Infrastructure','2088FF')+pill('Distributed Systems','3FB950')+pill('Web Security','FF9E64')+pill('Scalable Backends','BC8CFF'));
line('</p>');
line('');
line('## 2026 Goals');
line('<p align="center">');
line('  '+pill('Ship · Microservices on K8s','326CE5')+pill('Launch · 3 Production Apps','00D4AA')+pill('Contribute · 5+ Open Source','009688')+pill('Certify · CKA / CKAD','4E9E31')+pill('Release · ATS Platform','BC8CFF')+pill('Build · Documented OSS','FF9E64'));
line('</p>');
line('');
line('## Knowledge Areas');
line('<p align="center">');
line('  '+pill('Frontend Architecture','61DAFB','react')+pill('Backend Engineering','339933','node')+pill('Data & Storage','47A248','database')+pill('DevOps & Cloud','2496ED','docker')+pill('Security','005571')+pill('Tooling','F05032','git'));
line('</p>');
line('');
line('## Engineering Principles');
line('<p align="center">');
line('  '+pill('Simplicity · Readable','00D4AA')+pill('Architecture · Before Code','009688')+pill('Security · By Default','3FB950')+pill('Automation · Scripted','2088FF')+pill('Shipping · Production','4E9E31')+pill('Observability','BC8CFF'));
line('</p>');
line('');
line('---');
line('');

/* ---------- Projects / Open Source / Ask Me ---------- */
line('## Featured Projects');
line('<p align="center">');
line('  '+pill('Boiler Plate Generator','00D4AA')+pill('Accounting Application','00D4AA')+pill('Image & Video Editor','00D4AA')+pill('eCommerce Builder','00D4AA')+pill('Job Portal Platform','00D4AA')+pill('ATS Resume Optimization','00D4AA')+pill('Deployment Pipelines','BC8CFF'));
line('</p>');
line('<p align="center">');
line('  '+pill('All projects in active development','00D4AA'));
line('</p>');
line('');
line('## Open Source');
line('<p align="center">');
line('  '+pill('Open Source Contributor','00D4AA')+pill('Documented Code','00D4AA')+pill('PRs Welcome','00D4AA'));
line('</p>');
line('');
line('## Ask Me About');
line('<p align="center">');
line('  '+pill('Full Stack Development','00D4AA')+pill('REST API Design','009688')+pill('Authentication','3FB950')+pill('Docker & Kubernetes','326CE5')+pill('CI/CD Pipelines','4E9E31')+pill('Database Design','4479A1')+pill('Security Practices','005571'));
line('</p>');
line('');
line('---');
line('');

/* ---------- Contact ---------- */
line('## Contact');
line('<p align="center">');
line('  '+pill('GitHub','181717','github',GH)+pill('LinkedIn','0A66C2','linkedin','https://www.linkedin.com/in/m-huzaifa-hafeez-01b721375/'));
line('</p>');
line('<p align="center">');
line('  <!-- TODO: link Resume/Portfolio to real URLs -->');
line('  '+pill('Resume','00D4AA',GH)+pill('Portfolio','58A6FF',GH));
line('</p>');
line('<p align="center">');
line('  '+pill('Email','EA4335','gmail','mailto:official.huzaifa@gmail.com'));
line('</p>');
line('');
line('<br>');
line('<div align="center"><sub>© 2026 · M Huzaifa Hafeez · Full-Stack &amp; DevOps Engineer</sub></div>');

fs.writeFileSync(path.join(process.cwd(),'README.md'), L.join('\n')+'\n');
console.log('wrote README.md ('+L.length+' lines)');
