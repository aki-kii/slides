// デッキを PDF に書き出し、出力先にコピーして、ページを PNG にする。
// 前回の PDF があれば、見た目が変わったページを挙げる（ページが前後にずれても追える）。
//
//   pnpm export-check <デッキのディレクトリ> [--name 名前] [--pages 3,7-9 | --pages changed | --pages all]
//                     [--out /workspace/slides-out] [--dpi 60] [--wait 500]
//
// 例: pnpm export-check packages/slides/jawsug-cdk-tokyo-cdkd-talk --name cdk-talk
//
// 書き出しはデッキの `pnpm export` を使う（--with-clicks などはデッキの設定に従う）。
// 各ページを撮る前に --wait ミリ秒待つ。待たないと、クリックで出すオーバーレイがアニメーションの途中で写ることがある。
// pdfinfo、pdftoppm、pdftotext（poppler-utils）が要る。
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, join, resolve } from 'node:path';

function usage(msg) {
  if (msg) console.error(`Error: ${msg}`);
  console.error('使い方: pnpm export-check <デッキのディレクトリ> [--name 名前] [--pages 3,7-9|changed|all] [--out ディレクトリ] [--dpi 60] [--wait 500]');
  process.exit(2);
}

const args = process.argv.slice(2);
const opts = { out: '/workspace/slides-out', dpi: 60, pages: 'changed', wait: 500 };
let deck;
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (['--name', '--pages', '--out', '--dpi', '--wait'].includes(a)) {
    if (args[i + 1] === undefined) usage(`${a} に値がありません`);
    opts[a.slice(2)] = args[++i];
  } else if (a === '-h' || a === '--help') usage();
  else if (a.startsWith('-')) usage(`知らないオプション: ${a}`);
  else if (deck) usage('デッキのディレクトリは 1 つだけ指定してください');
  else deck = a;
}
if (!deck) usage('デッキのディレクトリを指定してください');
deck = resolve(deck);
if (!existsSync(join(deck, 'slides.md'))) usage(`${deck} に slides.md がありません`);
const name = opts.name ?? basename(deck);
if (!/^[A-Za-z0-9._-]+$/.test(name)) usage(`名前に使えない文字があります: ${name}`);
if (!['all', 'changed'].includes(opts.pages) && !/^\d+(-\d+)?(,\d+(-\d+)?)*$/.test(opts.pages.replace(/\s/g, ''))) usage(`--pages の書き方が違います: ${opts.pages}`);
const wait = Number(opts.wait);
if (!Number.isInteger(wait) || wait < 0 || wait > 10000) usage('--wait は 0〜10000 の整数（ミリ秒）にしてください');
const dpi = Number(opts.dpi);
if (!Number.isInteger(dpi) || dpi < 20 || dpi > 300) usage('--dpi は 20〜300 の整数にしてください');

function run(cmd, cmdArgs, cwd) {
  const r = spawnSync(cmd, cmdArgs, { cwd, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.error) throw r.error;
  return r;
}

function pageCount(pdf) {
  const m = run('pdfinfo', [pdf]).stdout.match(/^Pages:\s+(\d+)/m);
  if (!m) throw new Error(`${pdf} のページ数を読めません`);
  return Number(m[1]);
}

// 全ページを低い解像度の灰色で描いて、ページごとの画素を取る
function pageImages(pdf) {
  const dir = mkdtempSync(join(tmpdir(), 'export-check-'));
  try {
    const r = run('pdftoppm', ['-r', '20', '-gray', pdf, join(dir, 'p')]);
    if (r.status !== 0) throw new Error(`pdftoppm が失敗しました: ${r.stderr.trim()}`);
    return readdirSync(dir)
      .filter((f) => f.endsWith('.pgm'))
      .sort((a, b) => Number(a.match(/(\d+)\.pgm$/)[1]) - Number(b.match(/(\d+)\.pgm$/)[1]))
      .map((f) => {
        const buf = readFileSync(join(dir, f));
        const m = buf.toString('latin1', 0, 64).match(/^P5\s+(\d+)\s+(\d+)\s+\d+\s/);
        return buf.subarray(m[0].length);
      });
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

// ページごとの文字。見た目の比べ方では拾えない小さな文字の違いを拾う
function pageTexts(pdf) {
  const r = run('pdftotext', ['-layout', pdf, '-']);
  if (r.status !== 0) throw new Error(`pdftotext が失敗しました: ${r.stderr.trim()}`);
  return r.stdout.split('\f').map((t) => t.replace(/\s+/g, ' ').trim());
}

// 書き出すたびに文字の縁などがわずかにずれるので、ずれた画素が 0.3% 未満なら同じ見た目とみなす
function sameLook(a, b) {
  if (a.length !== b.length) return false;
  let moved = 0;
  for (let i = 0; i < a.length; i++) if (Math.abs(a[i] - b[i]) > 24) moved++;
  return moved / a.length < 0.003;
}

function parsePages(spec, total) {
  const pages = new Set();
  for (const part of spec.split(',')) {
    const m = part.trim().match(/^(\d+)(?:-(\d+))?$/);
    if (!m) usage(`--pages の書き方が違います: ${part}`);
    const from = Number(m[1]);
    const to = Number(m[2] ?? m[1]);
    for (let p = from; p <= to; p++) if (p >= 1 && p <= total) pages.add(p);
  }
  return [...pages].sort((a, b) => a - b);
}

// 1. 書き出し
console.log(`書き出し: ${deck}`);
const exp = run('pnpm', ['export', '--wait', String(wait)], deck);
const log = `${exp.stdout}\n${exp.stderr}`;
const lines = log.split('\n');
const errors = lines.filter((l) => /\berror\b|failed|✗/i.test(l) && !/Assets in public directory/.test(l));
const warnings = lines.filter((l) => /\bwarn(ing)?\b|Assets in public directory/i.test(l));
const exported = log.match(/exported to (\S+\.pdf)/);
if (exp.status !== 0 || !exported) {
  console.error(lines.slice(-30).join('\n'));
  console.error(`書き出しに失敗しました（終了コード ${exp.status}）`);
  process.exit(1);
}
const pdf = resolve(deck, exported[1]);

// 2. 前回の PDF と比べるため、上書きする前にハッシュを取る
mkdirSync(opts.out, { recursive: true });
const outPdf = join(opts.out, `${name}.pdf`);
const before = existsSync(outPdf) ? { images: pageImages(outPdf), texts: pageTexts(outPdf) } : null;
copyFileSync(pdf, outPdf);
const total = pageCount(outPdf);

let changed = null;
if (before) {
  // 前のどのページとも見た目が違うページを、変わったページとする（ページが前後にずれても追える）
  const images = pageImages(outPdf);
  const texts = pageTexts(outPdf);
  const same = (i, j) => texts[i] === before.texts[j] && sameLook(images[i], before.images[j]);
  changed = images.flatMap((_, i) => (before.images.some((_, j) => same(i, j)) ? [] : [i + 1]));
}

// 3. PNG
let pages;
if (opts.pages === 'all') pages = parsePages(`1-${total}`, total);
else if (opts.pages === 'changed') pages = changed ?? parsePages(`1-${total}`, total);
else pages = parsePages(opts.pages, total);
const pngDir = join(opts.out, 'png', name);
rmSync(pngDir, { recursive: true, force: true });
mkdirSync(pngDir, { recursive: true });
const width = String(total).length;
for (const p of pages) {
  const target = join(pngDir, `p${String(p).padStart(width, '0')}`);
  const r = run('pdftoppm', ['-r', String(dpi), '-png', '-singlefile', '-f', String(p), '-l', String(p), outPdf, target]);
  if (r.status !== 0) throw new Error(`p${p} の PNG を作れません: ${r.stderr.trim()}`);
}

// 4. 結果
console.log(`PDF: ${outPdf}（${total} ページ）`);
if (changed === null) console.log('変わったページ: 前回の PDF が無いので比べていない');
else console.log(`変わったページ: ${changed.length ? changed.join(', ') : 'なし'}（前回の ${before.images.length} ページと比べた）`);
console.log(`PNG: ${pngDir}（${pages.length} 枚${pages.length ? `: ${pages.join(', ')}` : ''}）`);
console.log(`警告: ${warnings.length} 件`);
for (const w of [...new Set(warnings)].slice(0, 10)) console.log(`  ${w.trim()}`);
console.log(`エラー: ${errors.length} 件`);
for (const e of [...new Set(errors)].slice(0, 10)) console.log(`  ${e.trim()}`);
process.exit(errors.length ? 1 : 0);
