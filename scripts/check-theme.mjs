import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const css = readFileSync(new URL('../src/styles.css', import.meta.url), 'utf8');
const finalTheme = css.slice(css.indexOf('/* Artstudio Nala parent theme'));
const required = [
  '--background:48 100% 98%', '--foreground:45 20% 20%', '--card:0 0% 100%',
  '--primary:45 100% 65%', '--secondary:35 100% 75%', '--muted-theme:48 100% 90%',
  '--accent:55 100% 80%', '--border:45 80% 85%', '--input:45 80% 90%',
  '--radius:1.5rem', '#2b2118', '#ffd36e', '#fffdf8', '#ff8db3', '#93e7d4',
  '#fff8ef', '#7dd3fc', '#b7f7d1', '#ffe29a', '#ffc1d6',
  'color:#2b2118', 'hsla(45,100%,65%,.2)'
];
for (const token of required) assert.ok(finalTheme.includes(token), `Missing theme token: ${token}`);
for (const oldColor of ['#285f4e', '#17231f', '#d79066', '#9e432d']) {
  assert.ok(!finalTheme.toLowerCase().includes(oldColor), `Old identity color remains in final theme: ${oldColor}`);
}
console.log('Theme tokens and old-color ban: OK');
