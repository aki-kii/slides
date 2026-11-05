// 全デッキを `slidev build` して dist/<デッキ>/ に置き、dist/index.html に一覧を作る。
// GitHub Pages（https://<user>.github.io/<repo>/）で公開するためのもの。
//
// 使い方: node scripts/build-pages.mjs [--base /slides/] [デッキ名 ...]
//   --base   サイトのルートのパス。既定は /slides/
//   デッキ名 指定したデッキだけビルドする（省略すると全部）

import { execFileSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { join, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const slidesDir = join(root, 'packages', 'slides');
const outDir = join(root, 'dist');

const args = process.argv.slice(2);
let base = '/slides/';
const only = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--base') base = args[++i];
  else only.push(args[i]);
}
if (!base.endsWith('/')) base += '/';

const decks = readdirSync(slidesDir, { withFileTypes: true })
  .filter(
    (d) => d.isDirectory() && existsSync(join(slidesDir, d.name, 'slides.md')),
  )
  .map((d) => d.name)
  .filter((name) => only.length === 0 || only.includes(name))
  .sort();

rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

const built = [];
const failed = [];
for (const name of decks) {
  const dir = join(slidesDir, name);
  console.log(`\n=== ${name}`);
  try {
    execFileSync(
      'pnpm',
      [
        'exec',
        'slidev',
        'build',
        '--base',
        `${base}${name}/`,
        '--out',
        join(outDir, name),
      ],
      { cwd: dir, stdio: 'inherit' },
    );
    rewritePublicPaths(
      join(outDir, name),
      join(dir, 'public'),
      `${base}${name}/`,
    );
    built.push({ name, title: readTitle(join(dir, 'slides.md')) ?? name });
  } catch {
    failed.push(name);
  }
}

writeFileSync(join(outDir, 'index.html'), indexHtml(built));
writeFileSync(join(outDir, '.nojekyll'), '');

console.log(`\nビルドした: ${built.length} / ${decks.length}`);
if (failed.length) {
  console.error(`失敗した: ${failed.join(', ')}`);
  process.exit(1);
}

// デッキの中では public/ のファイルを `/images/...` のような絶対パスで書いている
// （frontmatter の値、<img src>、Vue の props など Vite が base を付けない所が多い）。
// サブパスで公開すると見つからなくなるので、ビルドした JS・CSS・HTML の中だけ書き換える。
// 元のファイルは変えないので、dev と PDF の書き出しはこれまでどおり。
function rewritePublicPaths(deckOut, publicDir, prefix) {
  if (!existsSync(publicDir)) return;
  const entries = readdirSync(publicDir).map((e) =>
    e.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'),
  );
  if (entries.length === 0) return;
  // 引用符・括弧・バッククォートの直後に来る `/<public 直下の名前>` だけを対象にする
  const re = new RegExp(`(["'\`(])/(${entries.join('|')})(?=[/"'\`)?#])`, 'g');
  let count = 0;
  for (const file of walk(deckOut)) {
    if (!/\.(js|mjs|css|html)$/.test(file)) continue;
    const src = readFileSync(file, 'utf8');
    const out = src.replace(re, (_, q, e) => {
      count++;
      return `${q}${prefix}${e}`;
    });
    if (out !== src) writeFileSync(file, out);
  }
  console.log(`public のパスを ${count} か所書き換えた`);
}

function* walk(dir) {
  for (const d of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, d.name);
    if (d.isDirectory()) yield* walk(p);
    else yield p;
  }
}

function readTitle(file) {
  const m = readFileSync(file, 'utf8').match(/^---\n([\s\S]*?)\n---/);
  const t = m?.[1].match(/^title:\s*(.+)$/m)?.[1].trim();
  return t?.replace(/^['"]|['"]$/g, '');
}

function esc(s) {
  return s.replace(
    /[&<>"]/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c],
  );
}

function indexHtml(items) {
  const list = items
    .map(
      ({ name, title }) =>
        `      <li><a href="./${name}/"><span>${esc(title)}</span><code>${name}</code></a></li>`,
    )
    .join('\n');
  return `<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Slides</title>
    <style>
      body { font-family: 'Noto Sans JP', system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; color: #222; }
      h1 { font-size: 1.5rem; }
      ul { list-style: none; padding: 0; }
      li a { display: block; padding: .75rem 1rem; margin: .5rem 0; border: 1px solid #ddd; border-radius: 8px; text-decoration: none; color: inherit; }
      li a:hover { background: #f6f6f6; }
      li span { display: block; font-weight: 600; }
      li code { font-size: .8rem; color: #888; }
    </style>
  </head>
  <body>
    <h1>Slides</h1>
    <ul>
${list}
    </ul>
  </body>
</html>
`;
}
