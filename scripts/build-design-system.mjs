// design-system/ の Markdown をスライド用デザインシステムのサイト（HTML）にする。
// build-pages.mjs から呼ばれ、dist/design-system/ に出す。単独でも動かせる。
//
// 使い方: node scripts/build-design-system.mjs [--base /slides/] [--out dist/design-system]
//
// 文書の置き方（design-system/）:
//   - 項目は1つにつき1ファイル。層ごとのフォルダ（base/ parts/ pages/ flows/ themes/）と skeleton/ に置く
//     頭に `---` で囲んだ id・name（ページの型は place も）を書く。本文は
//     「1行の定義 → ## 見本 → ## いつ使うか → ## 中身 → ## 気を付けること」の順。関連する項目は自動で作る
//   - 層の一覧ページは各フォルダの _index.md。頭の order に項目の並びを書き、`<!-- items -->` に一覧の表が入る
//   - README.md（トップ）、naming.md、decisions.md、research-sizes.md はそのままの1ページ
//
// 書き方の決まり:
//   - 見出し・段落・箇条書き（- / 1.）・表・コードブロック・**太字**・`コード`・[リンク](...)・![](画像) が使える
//   - `<!-- shots:<パターンのID> -->` の1行は、shots/manifest.json のそのパターンの写真に置き換わる
//   - `[名前](@<項目のID>)` は項目のページ、`[名前](@<フォルダ名>)` は層の一覧へのリンクになる
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

// 層。group 1 は置くもの（土台・コンポーネント・ページの型）、group 2 は選ぶ決め事（共通の骨組み・構成の型・全体の型）で「ストーリー」とまとめる。
// 目次ではまとまりごとに区切って並べる。名前を付けるのは group 2（ストーリー）だけ。body は項目ページの「中身」の欄の名前
const LAYERS = [
  { key: 'base', group: 1, body: '値' },
  { key: 'parts', group: 1, body: 'サイズ・値と実装' },
  { key: 'pages', group: 1, body: '置くコンポーネントと並び' },
  {
    key: 'skeleton',
    group: 2,
    body: '並びと使うページの型',
    title: '共通の骨組み',
    single: true,
  },
  { key: 'flows', group: 2, body: '並びと使うページの型' },
  { key: 'themes', group: 2, body: 'デッキ・背骨・主役のページ' },
];

// まとまりの名前。group 1 には付けない
const GROUP_LABELS = { 2: 'ストーリー' };

// 層の並びに入れない文書
const DOCS = [
  { file: 'README.md', out: 'index.html', nav: 'はじめに' },
  { file: 'naming.md', nav: 'デッキの名前（提案）', group: 'その他の文書' },
  { file: 'decisions.md', nav: '決めたこと', group: 'その他の文書' },
  { file: 'research-sizes.md', nav: 'サイズの調査メモ', group: 'その他の文書' },
];

// 項目ページの欄の並び（全層で同じ）
const SECTIONS = ['見本', 'いつ使うか', '中身', '気を付けること'];

// 写真の説明に出すデッキの略し方
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

// 変換中のページで使う、`@` のリンク先と問題の記録
let ctx = { items: new Map(), layers: new Map(), problems: [], where: '' };

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
  const shots = (id) => {
    if (!manifest[id]) {
      problems.push(`${ctx.where}: manifest に ${id} がない`);
      return '';
    }
    used.add(id);
    return shotsHtml(manifest[id], { base, decks });
  };

  const { items, layers } = loadItems(problems);
  ctx = { items, layers, problems, where: '' };
  const backlinks = new Map([...items.keys()].map((id) => [id, new Set()]));
  for (const it of items.values()) {
    for (const to of it.links) {
      if (to !== it.id && backlinks.has(to)) backlinks.get(to).add(it.id);
    }
  }

  mkdirSync(outDir, { recursive: true });
  let count = 0;
  const write = (file, html) => {
    writeFileSync(join(outDir, file), html);
    count++;
  };

  for (const doc of DOCS) {
    ctx.where = doc.file;
    const md = readFileSync(join(srcDir, doc.file), 'utf8');
    const title = md.match(/^# (.+)$/m)?.[1] ?? doc.nav;
    const current = doc.out ?? doc.file.replace(/\.md$/, '.html');
    write(current, layout({ title, body: render(md, { shots }), current }));
  }

  for (const layer of layers.values()) {
    if (layer.single) continue;
    ctx.where = `${layer.key}/_index.md`;
    const table = itemsTable(layer, manifest);
    const body = render(`# ${layer.title}\n\n${layer.intro}`, {
      shots,
      items: () => table,
    });
    write(
      `${layer.key}.html`,
      layout({ title: layer.title, body, current: `${layer.key}.html` }),
    );
  }

  for (const it of items.values()) {
    ctx.where = it.file;
    const related = new Set([...it.links, ...backlinks.get(it.id)]);
    related.delete(it.id);
    write(
      `${it.id}.html`,
      layout({
        title: it.name,
        body: itemHtml(it, { shots, related }),
        current: it.layer.single ? `${it.id}.html` : `${it.layer.key}.html`,
      }),
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
  console.log(`design-system: ${count} ページを ${outDir} に出した`);
  return problems;
}

// 項目のファイルと、層の一覧の _index.md を読む
function loadItems(problems) {
  const items = new Map();
  const layers = new Map();
  for (const def of LAYERS) {
    const dir = join(srcDir, def.key);
    const files = readdirSync(dir).filter(
      (f) => f.endsWith('.md') && f !== '_index.md',
    );
    const layer = { ...def, items: [], intro: '' };
    let order = files.map((f) => f.replace(/\.md$/, ''));
    if (!def.single) {
      const { meta, body } = frontMatter(
        readFileSync(join(dir, '_index.md'), 'utf8'),
      );
      layer.title = meta.title;
      layer.intro = body;
      order = (meta.order ?? '').split(/\s+/).filter(Boolean);
      const missing = files
        .map((f) => f.replace(/\.md$/, ''))
        .filter((id) => !order.includes(id));
      for (const id of missing)
        problems.push(`${def.key}/_index.md: order に ${id} がない`);
      order.push(...missing);
    }
    for (const id of order) {
      const file = `${def.key}/${id}.md`;
      if (!existsSync(join(srcDir, file))) {
        problems.push(`${def.key}/_index.md: order の ${id} のファイルがない`);
        continue;
      }
      const it = parseItem(
        file,
        readFileSync(join(srcDir, file), 'utf8'),
        problems,
      );
      it.layer = layer;
      layer.items.push(it);
      items.set(it.id, it);
    }
    layers.set(def.key, layer);
  }
  return { items, layers };
}

function frontMatter(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) return { meta: {}, body: md };
  const meta = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^([\w-]+):\s*(.*)$/);
    if (kv) meta[kv[1]] = kv[2].trim();
  }
  return { meta, body: md.slice(m[0].length) };
}

function parseItem(file, md, problems) {
  const { meta, body } = frontMatter(md);
  if (!meta.id || !meta.name) problems.push(`${file}: id か name がない`);
  if (`${meta.id}.md` !== file.split('/').pop())
    problems.push(`${file}: id とファイル名が合わない`);
  const parts = body.split(/^## /m);
  const definition = parts.shift().trim();
  if (!definition) problems.push(`${file}: 1行の定義がない`);
  const sections = new Map();
  let last = -1;
  for (const p of parts) {
    const [head, ...rest] = p.split('\n');
    const name = head.trim();
    const idx = SECTIONS.indexOf(name);
    if (idx < 0) problems.push(`${file}: 知らない欄「${name}」`);
    else if (idx < last) problems.push(`${file}: 欄「${name}」の位置が違う`);
    last = Math.max(last, idx);
    sections.set(name, rest.join('\n').trim());
  }
  const links = [...md.matchAll(/\]\(@([\w-]+)\)/g)].map((m) => m[1]);
  return { ...meta, file, definition, sections, links };
}

// 項目ページ: 名前 → 1行の定義 → 見本 → いつ使うか → 中身 → 関連する項目 → 気を付けること
function itemHtml(it, { shots, related }) {
  const layer = it.layer;
  const label = GROUP_LABELS[layer.group];
  const crumb =
    (label ? `${esc(label)} / ` : '') +
    (layer.single
      ? esc(layer.title)
      : `<a href="${layer.key}.html">${esc(layer.title)}</a>`);
  const out = [
    `<p class="crumb">${crumb}</p>`,
    `<h1>${inline(it.name)} <code class="id">${esc(it.id)}</code></h1>`,
    `<p class="definition">${inline(it.definition)}</p>`,
  ];
  const section = (title, html) => {
    if (!html) return;
    const id = slug(title);
    out.push(
      `<h2 id="${id}">${esc(title)} <a class="anchor" href="#${id}">#</a></h2>`,
      html,
    );
  };
  const md = (name) =>
    it.sections.get(name) ? render(it.sections.get(name), { shots }) : '';
  section('見本', md('見本'));
  section('いつ使うか', md('いつ使うか'));
  section(layer.body, md('中身'));
  section('関連する項目', relatedHtml(related));
  section('気を付けること', md('気を付けること'));
  return out.join('\n');
}

// 関連する項目（この項目が指すものと、この項目を指すもの）を層ごとに並べる
function relatedHtml(related) {
  const rows = [];
  for (const layer of ctx.layers.values()) {
    const list = layer.items.filter((it) => related.has(it.id));
    if (!list.length) continue;
    rows.push(
      `<li><span class="rel-layer">${esc(layer.title)}</span>${list
        .map((it) => `<a href="${it.id}.html">${inline(it.name)}</a>`)
        .join('、')}</li>`,
    );
  }
  return rows.length ? `<ul class="related">${rows.join('')}</ul>` : '';
}

// 層の一覧の表: 見本の写真1枚・名前・1行の説明。ページの型は骨組みの場所ごとに分ける
function itemsTable(layer, manifest) {
  const row = (it) => {
    const shot = manifest[it.id]?.[0];
    const thumb = shot
      ? `<img src="shots/${shot.file}" alt="" loading="lazy" class="${shot.strip ? 'thumb strip' : 'thumb'}">`
      : '<span class="thumb none">写真なし</span>';
    let desc = inline(it.definition);
    if (layer.key === 'themes') {
      const body = it.sections.get('中身') ?? '';
      const pick = (label) =>
        body.match(new RegExp(`^- \\*\\*${label}\\*\\*: (.+)$`, 'm'))?.[1];
      const spine = pick('背骨');
      const lead = pick('主役のページ');
      if (spine) desc += `<br><span class="sub">背骨: ${inline(spine)}</span>`;
      if (lead) desc += `<br><span class="sub">主役: ${inline(lead)}</span>`;
    }
    return `<tr><td class="t"><a href="${it.id}.html">${thumb}</a></td><td class="n"><a href="${it.id}.html">${inline(it.name)}</a><br><code class="id">${esc(it.id)}</code></td><td>${desc}</td></tr>`;
  };
  const tableOf = (list) =>
    `<div class="table"><table class="items"><thead><tr><th>見本</th><th>名前</th><th>説明</th></tr></thead><tbody>${list.map(row).join('')}</tbody></table></div>`;
  if (layer.key !== 'pages') return tableOf(layer.items);
  const places = [];
  for (const it of layer.items) {
    if (!it.place) ctx.problems.push(`${it.file}: place がない`);
    if (!places.includes(it.place)) places.push(it.place);
  }
  return places
    .map(
      (p) =>
        `<h2 id="${slug(p ?? '')}">${esc(p ?? '')}</h2>\n${tableOf(layer.items.filter((it) => it.place === p))}`,
    )
    .join('\n');
}

// `@<ID>` と `@<フォルダ名>` のリンク先
function resolveAt(name) {
  if (ctx.items.has(name)) return `${name}.html`;
  const layer = ctx.layers.get(name);
  if (layer) return layer.single ? `${layer.items[0].id}.html` : `${name}.html`;
  ctx.problems.push(`${ctx.where}: リンク先 @${name} がない`);
  return '#';
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

function render(md, { shots, items }) {
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
    if (items && /^<!--\s*items\s*-->$/.test(line.trim())) {
      out.push(items());
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
    const h = href.startsWith('@')
      ? resolveAt(href.slice(1))
      : href.replace(/^([\w-]+)\.md(#.*)?$/, (_, f, a = '') =>
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
  // 目次: はじめに → 土台・コンポーネント・ページの型 → ストーリー → その他の文書
  const link = (href, label) =>
    `<li><a href="${href}"${href === current ? ' class="current"' : ''}>${esc(label)}</a></li>`;
  const groups = [];
  for (const g of [1, 2]) {
    const links = [...ctx.layers.values()]
      .filter((l) => l.group === g)
      .map((l) =>
        l.single
          ? link(`${l.items[0].id}.html`, l.title)
          : link(`${l.key}.html`, l.title),
      );
    const label = GROUP_LABELS[g] ? `<span>${esc(GROUP_LABELS[g])}</span>` : '';
    groups.push(`<li class="group">${label}<ol>${links.join('')}</ol></li>`);
  }
  const others = DOCS.filter((d) => d.group).map((d) =>
    link(d.file.replace(/\.md$/, '.html'), d.nav),
  );
  groups.push(
    `<li class="group"><span>その他の文書</span><ol>${others.join('')}</ol></li>`,
  );
  const nav = [link('index.html', 'はじめに'), ...groups].join('\n        ');
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
      nav li.group { margin-top: .75rem; padding-top: .75rem; border-top: 1px solid var(--line); }
      nav li.group > span { display: block; padding: 0 .7rem .2rem; font-size: .78rem; font-weight: 700; color: var(--ink-mute); letter-spacing: .05em; }
      nav li.group ol { position: static; }
      .crumb { font-size: .85rem; color: var(--ink-mute); margin: 0 0 .25rem; }
      code.id { font-size: .55em; vertical-align: middle; color: var(--ink-mute); }
      td code.id { font-size: .75rem; }
      .definition { font-size: 1.08rem; padding: .75rem 1rem; background: var(--tint); border-radius: 8px; }
      ul.related { list-style: none; padding: 0; }
      ul.related li { margin: .3rem 0; }
      .rel-layer { display: inline-block; min-width: 9em; font-size: .85rem; color: var(--ink-mute); }
      table.items td.t { width: 200px; }
      table.items td.n { width: 13em; }
      img.thumb { width: 180px; aspect-ratio: 16 / 9; object-fit: cover; object-position: left top; display: block; border: 1px solid var(--line); border-radius: 4px; }
      .thumb.none { display: flex; width: 180px; aspect-ratio: 16 / 9; align-items: center; justify-content: center; font-size: .8rem; color: var(--ink-mute); border: 1px dashed var(--line); border-radius: 4px; }
      .sub { font-size: .85rem; color: var(--ink-mute); }
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
        nav li.group { margin-top: .25rem; width: 100%; }
        table.items td.t { width: 112px; }
        img.thumb, .thumb.none { width: 100px; }
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
