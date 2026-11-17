// design-system/ の Markdown をスライド用デザインシステムのサイト（HTML）にする。
// build-pages.mjs から呼ばれ、dist/design-system/ に出す。単独でも動かせる。
//
// 使い方: node scripts/build-design-system.mjs [--base /slides/] [--out dist/design-system]
//
// 書き方の決まり（design-system/*.md）:
//   - 見出し・段落・箇条書き（- / 1.）・表・コードブロック・**太字**・`コード`・[リンク](...)・![](画像) が使える
//   - `<!-- shots:<パターンのID> -->` の1行は、shots/manifest.json のそのパターンの写真に置き換わる
//   - `xxx.md` へのリンクは `xxx.html` に書き換わる

import {
  cpSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  writeFileSync,
} from 'node:fs';
import { join, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const srcDir = join(root, 'design-system');

// サイトに載せるページと並び。5層は「全体の型 → 構成の型 → ページの型 → 部品 → 土台」の順
export const PAGES = [
  { file: 'README.md', out: 'index.html', nav: 'はじめに' },
  { file: 'themes.md', nav: '全体の型（テーマ）' },
  { file: 'flows.md', nav: '構成の型' },
  { file: 'pages.md', nav: 'ページの型' },
  { file: 'parts.md', nav: '部品' },
  { file: 'foundation.md', nav: '土台' },
  { file: 'naming.md', nav: 'デッキの名前（提案）' },
  { file: 'research-sizes.md', nav: 'サイズの調査メモ' },
  { file: 'decisions.md', nav: '決めたこと' },
];

// 写真の説明に出すデッキの略し方（patterns-definition.md と同じ）
const SHORT = {
  'jawsug-container-31': 'container-31',
  'jawsug-bgnr-93': 'bgnr-93',
  'cdk-custom-resource-continuum': 'continuum',
  'jawsug-cdk-tokyo-cdkd-talk': 'cdkd-talk',
  'jawsug-tokyo-lunch-lt-40': 'lt-40',
  'ecr-sbom-supply-chain-investigation': 'ecr-sbom',
  'failed-ecs-log-cost-reduction': 'failed-ecs',
  'zero-drift-cdk-ops': 'zero-drift',
  'cdk-day1-experiment': 'cdk-day1',
  'aws-oss-perspective': 'aws-oss',
  'cdk-3min-cooking': 'cdk-3min',
};

/**
 * @param {{ outDir: string, base?: string, decks?: string[] }} opts
 *   decks: Pages に載っているデッキ。写真からそのページへリンクする
 */
export function buildDesignSystem({ outDir, base = '/slides/', decks = [] }) {
  const manifest = JSON.parse(
    readFileSync(join(srcDir, 'shots', 'manifest.json'), 'utf8'),
  );
  const used = new Set();
  const problems = [];

  mkdirSync(outDir, { recursive: true });
  for (const page of PAGES) {
    const md = readFileSync(join(srcDir, page.file), 'utf8');
    const body = render(md, {
      shots: (id) => {
        if (!manifest[id]) {
          problems.push(`${page.file}: manifest に ${id} がない`);
          return '';
        }
        used.add(id);
        return shotsHtml(manifest[id], { base, decks });
      },
    });
    const title = md.match(/^# (.+)$/m)?.[1] ?? page.nav;
    writeFileSync(
      join(outDir, outName(page)),
      layout({ title, body, current: page }),
    );
  }
  for (const id of Object.keys(manifest)) {
    if (!used.has(id))
      problems.push(`manifest の ${id} がどのページにも出てこない`);
  }
  cpSync(join(srcDir, 'shots'), join(outDir, 'shots'), {
    recursive: true,
    filter: (p) => !p.endsWith('manifest.json'),
  });
  for (const p of problems) console.warn(`design-system: ${p}`);
  console.log(`design-system: ${PAGES.length} ページを ${outDir} に出した`);
  return problems;
}

// routerMode: hash のデッキは /<デッキ>/#/<ページ> でページを開く
const routerCache = new Map();
function hashRouter(deck) {
  if (!routerCache.has(deck)) {
    const md = join(root, 'packages', 'slides', deck, 'slides.md');
    const head = existsSync(md)
      ? (readFileSync(md, 'utf8').match(/^---\n([\s\S]*?)\n---/)?.[1] ?? '')
      : '';
    routerCache.set(deck, /^routerMode:\s*['"]?hash/m.test(head));
  }
  return routerCache.get(deck);
}

function outName(page) {
  return page.out ?? page.file.replace(/\.md$/, '.html');
}

function shotsHtml(entries, { base, decks }) {
  const items = entries
    .map((e) => {
      const short = SHORT[e.deck] ?? e.deck;
      const pages = e.pages ?? [e.page];
      const caption = e.strip
        ? `${short} p.${pages.join('・')}`
        : `${short} p.${e.page}`;
      const img = `<img src="shots/${e.file}" alt="${esc(caption)}" loading="lazy">`;
      const href = decks.includes(e.deck)
        ? `${base}${e.deck}/${hashRouter(e.deck) ? '#/' : ''}${pages[0]}`
        : undefined;
      const fig = href
        ? `<a href="${href}">${img}</a><figcaption><a href="${href}">${esc(caption)}</a></figcaption>`
        : `${img}<figcaption>${esc(caption)}</figcaption>`;
      return `<figure class="${e.strip ? 'strip' : 'shot'}">${fig}</figure>`;
    })
    .join('\n');
  return `<div class="shots">\n${items}\n</div>`;
}

// ---- 小さな Markdown の変換（このフォルダの文書に要る分だけ） ----

function render(md, { shots }) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;
  const slugs = new Map();

  while (i < lines.length) {
    const line = lines[i];

    const shot = line.match(/^<!--\s*shots:([\w-]+)\s*-->$/);
    if (shot) {
      out.push(shots(shot[1]));
      i++;
      continue;
    }
    if (/^<!--.*-->$/.test(line.trim())) {
      i++;
      continue;
    }
    if (line.startsWith('```')) {
      const buf = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```'))
        buf.push(lines[i++]);
      i++;
      out.push(`<pre><code>${esc(buf.join('\n'))}</code></pre>`);
      continue;
    }
    const h = line.match(/^(#{1,4}) (.+)$/);
    if (h) {
      const level = h[1].length;
      const text = h[2];
      const idm = text.match(/^([a-z][\w-]*) /);
      let id = idm ? idm[1] : slug(text);
      const n = slugs.get(id) ?? 0;
      slugs.set(id, n + 1);
      if (n) id += `-${n}`;
      out.push(
        `<h${level} id="${id}">${inline(text)}${level > 1 ? ` <a class="anchor" href="#${id}">#</a>` : ''}</h${level}>`,
      );
      i++;
      continue;
    }
    if (/^---+$/.test(line)) {
      out.push('<hr>');
      i++;
      continue;
    }
    if (line.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|'))
        rows.push(lines[i++]);
      out.push(table(rows));
      continue;
    }
    if (line.startsWith('> ')) {
      const buf = [];
      while (i < lines.length && lines[i].startsWith('>'))
        buf.push(lines[i++].replace(/^> ?/, ''));
      out.push(`<blockquote>${render(buf.join('\n'), { shots })}</blockquote>`);
      continue;
    }
    if (/^\s*([-*]|\d+\.) /.test(line)) {
      const buf = [];
      while (
        i < lines.length &&
        (/^\s*([-*]|\d+\.) /.test(lines[i]) || /^\s{2,}\S/.test(lines[i]))
      )
        buf.push(lines[i++]);
      out.push(list(buf));
      continue;
    }
    if (line.trim() === '') {
      i++;
      continue;
    }
    const buf = [];
    while (
      i < lines.length &&
      lines[i].trim() !== '' &&
      !/^(#{1,4} |```|\||> |\s*([-*]|\d+\.) |<!--)/.test(lines[i])
    )
      buf.push(lines[i++]);
    const text = buf.join('\n');
    out.push(
      /^!\[[^\]]*\]\([^)]+\)$/.test(text.trim())
        ? `<p class="img">${inline(text)}</p>`
        : `<p>${inline(text).replace(/\n/g, '<br>')}</p>`,
    );
  }
  return out.join('\n');
}

function list(lines) {
  const indent = (l) => l.match(/^\s*/)[0].length;
  const base = indent(lines[0]);
  const ordered = /^\s*\d+\. /.test(lines[0]);
  const items = [];
  for (const l of lines) {
    if (indent(l) === base && /^\s*([-*]|\d+\.) /.test(l)) {
      items.push({ text: l.replace(/^\s*([-*]|\d+\.) /, ''), children: [] });
    } else if (items.length) {
      items.at(-1).children.push(l);
    }
  }
  const tag = ordered ? 'ol' : 'ul';
  return `<${tag}>${items
    .map((it) => {
      const nested = it.children.filter((c) => /^\s*([-*]|\d+\.) /.test(c));
      const cont = it.children.filter((c) => !/^\s*([-*]|\d+\.) /.test(c));
      const text = [it.text, ...cont.map((c) => c.trim())].join('<br>');
      return `<li>${inline(text)}${nested.length ? list(it.children) : ''}</li>`;
    })
    .join('')}</${tag}>`;
}

function table(rows) {
  const cells = (r) =>
    r
      .replace(/^\||\|$/g, '')
      .split('|')
      .map((c) => c.trim());
  const [head, , ...body] = rows;
  return `<div class="table"><table><thead><tr>${cells(head)
    .map((c) => `<th>${inline(c)}</th>`)
    .join('')}</tr></thead><tbody>${body
    .map(
      (r) =>
        `<tr>${cells(r)
          .map((c) => `<td>${inline(c)}</td>`)
          .join('')}</tr>`,
    )
    .join('')}</tbody></table></div>`;
}

function inline(s) {
  const codes = [];
  s = s.replace(/`([^`]+)`/g, (_, c) => {
    codes.push(c);
    return `\uE000${codes.length - 1}\uE000`;
  });
  // <br> だけは書けるようにする
  s = esc(s).replace(/&lt;br&gt;/g, '<br>');
  s = s.replace(
    /!\[([^\]]*)\]\(([^)]+)\)/g,
    (_, alt, src) => `<img src="${src}" alt="${alt}" loading="lazy">`,
  );
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, href) => {
    const h = href.replace(/^([\w-]+)\.md(#.*)?$/, (_, f, a = '') =>
      f === 'README' ? `index.html${a}` : `${f}.html${a}`,
    );
    return `<a href="${h}">${text}</a>`;
  });
  s = s.replace(
    /(^|[\s（(、])(https?:\/\/[^\s<）)、]+)/g,
    (_, pre, url) => `${pre}<a href="${url}">${url}</a>`,
  );
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(
    /\uE000(\d+)\uE000/g,
    (_, n) => `<code>${esc(codes[n])}</code>`,
  );
  return s;
}

function slug(text) {
  return (
    text
      .toLowerCase()
      .replace(/<[^>]+>|[`*[\]()（）「」、。：:・?？!！]/g, '')
      .trim()
      .replace(/\s+/g, '-') || 'section'
  );
}

function esc(s) {
  return String(s).replace(
    /[&<>"]/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c],
  );
}

function layout({ title, body, current }) {
  const nav = PAGES.map((p) => {
    const cls = p === current ? ' class="current"' : '';
    return `<li><a href="${outName(p)}"${cls}>${esc(p.nav)}</a></li>`;
  }).join('\n        ');
  return `<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${esc(title)} | スライドのデザインシステム</title>
    <style>
      :root { --ink: #2c3e50; --ink-mute: #5f6b76; --line: #dee2e6; --brand: #0283b2; --brand-deep: #015d7d; --accent: #c0392b; --tint: #f4f8fa; }
      * { box-sizing: border-box; }
      body { margin: 0; font-family: 'Noto Sans JP', system-ui, sans-serif; color: var(--ink); background: #fff; line-height: 1.75; }
      header { background: linear-gradient(155deg, #015d7d 0%, #0283b2 60%, #1aa9d1 100%); color: #fff; padding: .9rem 1.25rem; }
      header a { color: #fff; text-decoration: none; font-weight: 700; }
      header small { opacity: .85; margin-left: .75rem; }
      .wrap { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 2rem; max-width: 1200px; margin: 0 auto; padding: 1.5rem 1.25rem 4rem; }
      nav ol { list-style: none; padding: 0; margin: 0; position: sticky; top: 1rem; counter-reset: n; }
      nav li a { display: block; padding: .4rem .7rem; border-radius: 6px; color: inherit; text-decoration: none; font-size: .95rem; }
      nav li a:hover { background: var(--tint); }
      nav li a.current { background: var(--tint); font-weight: 700; color: var(--brand-deep); }
      main { min-width: 0; }
      h1 { font-size: 1.8rem; margin: 0 0 1rem; }
      h2 { font-size: 1.35rem; margin: 2.75rem 0 .75rem; padding-bottom: .3rem; border-bottom: 2px solid var(--line); }
      h3 { font-size: 1.12rem; margin: 2.25rem 0 .5rem; }
      h4 { font-size: 1rem; margin: 1.5rem 0 .4rem; }
      .anchor { color: var(--line); text-decoration: none; font-weight: 400; margin-left: .25rem; }
      h2:hover .anchor, h3:hover .anchor { color: var(--ink-mute); }
      a { color: var(--brand-deep); }
      strong { color: var(--ink); }
      code { font-family: 'Fira Code', ui-monospace, monospace; font-size: .88em; background: var(--tint); padding: .05em .35em; border-radius: 4px; }
      pre { background: var(--tint); padding: .9rem 1rem; border-radius: 8px; overflow-x: auto; }
      pre code { background: none; padding: 0; }
      blockquote { margin: 1rem 0; padding: .25rem 1rem; background: var(--tint); border-radius: 8px; }
      hr { border: 0; border-top: 1px solid var(--line); margin: 2.5rem 0; }
      .table { overflow-x: auto; }
      table { border-collapse: collapse; margin: 1rem 0; font-size: .92rem; }
      th, td { border: 1px solid var(--line); padding: .45rem .7rem; text-align: left; vertical-align: top; }
      th { background: var(--tint); }
      .shots { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0 1.5rem; }
      .shots figure { margin: 0; }
      .shots figure.strip { grid-column: 1 / -1; }
      .shots img { width: 100%; height: auto; display: block; border: 1px solid var(--line); border-radius: 6px; }
      .shots figure.strip a, .shots figure.strip > img { display: block; overflow-x: auto; }
      figcaption { font-size: .82rem; color: var(--ink-mute); margin-top: .3rem; }
      @media (max-width: 760px) {
        .wrap { grid-template-columns: 1fr; gap: 1rem; padding: 1rem 16px 3rem; }
        nav ol { position: static; display: flex; flex-wrap: wrap; gap: .25rem; }
        nav li a { padding: .3rem .55rem; font-size: .85rem; }
      }
    </style>
  </head>
  <body>
    <header><a href="index.html">スライドのデザインシステム</a><small><a href="../">スライド一覧へ</a></small></header>
    <div class="wrap">
      <nav><ol>
        ${nav}
      </ol></nav>
      <main>
${body}
      </main>
    </div>
  </body>
</html>
`;
}

// 単独で動かしたとき
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  let base = '/slides/';
  let out = join(root, 'dist', 'design-system');
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--base') base = args[++i];
    else if (args[i] === '--out') out = resolve(args[++i]);
  }
  if (!base.endsWith('/')) base += '/';
  const slidesDir = join(root, 'packages', 'slides');
  const decks = readdirSync(slidesDir).filter(
    (d) =>
      existsSync(join(slidesDir, d, 'slides.md')) && d !== 'cdk-3min-cooking',
  );
  const problems = buildDesignSystem({ outDir: out, base, decks });
  if (problems.length) process.exit(1);
}
