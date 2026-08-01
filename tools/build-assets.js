// tools/build-assets.js
// Generates the single animated hero SVG as a self-contained file.
//
// WHY a file (not inline SVG): GitHub's README sanitizer strips ALL inline
// <svg> markup from markdown (rect/circle/defs/animate -> 0 in rendered HTML),
// but it renders external <img src="...svg"> WITHOUT sanitizing, and SMIL
// <animate> keeps running inside <img>-loaded SVGs (same mechanism as the
// contribution snake). So the animated hero is assets/hero.svg → <img>.
//
// Run: node tools/build-assets.js   → writes assets/hero.svg

const fs = require('fs');
const path = require('path');
const OUT = path.join(process.cwd(), 'assets');
fs.mkdirSync(OUT, { recursive: true });

const T = '#e6edf3';
function glassGrad(id) {
  return `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">` +
    `<stop offset="0%" stop-color="#ffffff" stop-opacity="0.10"/>` +
    `<stop offset="100%" stop-color="#ffffff" stop-opacity="0.02"/>` + `</linearGradient>`;
}

function hero() {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 900 90" width="900" height="90" xmlns="http://www.w3.org/2000/svg">
  <defs>
    ${glassGrad('h_bg')}
    <linearGradient id="h_wave" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00D4AA" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00D4AA" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#00D4AA" stop-opacity="0"/>
      <animate attributeName="x1" values="0%;100%;0%" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="100%;0%;100%" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="h_name" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00D4AA"/>
      <stop offset="50%" stop-color="#58A6FF"/>
      <stop offset="100%" stop-color="#00D4AA"/>
      <animate attributeName="x1" values="0%;100%;0%" dur="4s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="100%;0%;100%" dur="4s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect width="900" height="90" fill="url(#h_bg)"/>
  <path d="M0,55 Q120,85 240,55 T480,55 T720,55 T900,55 L900,90 L0,90 Z" fill="url(#h_wave)" opacity="0.6"/>
  <text x="450" y="36" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="27" font-weight="700" fill="url(#h_name)">M Huzaifa Hafeez</text>
  <text x="450" y="66" text-anchor="middle" font-family="'Segoe UI',sans-serif" font-size="12" fill="#8b949e" letter-spacing="0.8">Full-Stack &amp; DevOps Engineer · Pakistan</text>
</svg>`;
}

const content = hero();
fs.writeFileSync(path.join(OUT, 'hero.svg'), content);
console.log('wrote assets/hero.svg (' + content.length + ' bytes)');
