// design-system/ の Markdown をスライド用デザインシステムのサイト（HTML）にする。
// build-pages.mjs から呼ばれ、dist/design-system/ に出す。単独でも動かせる。
//
// 使い方: node scripts/build-design-system.mjs [--base /slides/] [--out dist/design-system]
//
// 文書の置き方（design-system/）:
//   - 項目は1つにつき1ファイル。層ごとのフォルダ（base/ parts/ pages/ flows/ themes/）と skeleton/ に置く
//     頭に `---` で囲んだ id・name（テンプレートは place も）を書く。本文は
//     「1行の定義 → ## 見本 → ## いつ使うか → ## 中身 → ## 気を付けること」の順。関連する項目は自動で作る
//   - 層の一覧ページは各フォルダの _index.md。頭の order に項目の並びを書き、`<!-- items -->` に一覧の表が入る
//   - README.md（トップ）、naming.md、decisions.md、research-sizes.md はそのままの1ページ
//
// 書き方の決まり:
//   - 見出し・段落・箇条書き（- / 1.）・表・コードブロック・**太字**・`コード`・[リンク](...)・![](画像) が使える
//   - `<!-- shots:<項目のID> -->` の1行は、shots/manifest.json のその項目の写真に置き換わる
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

const REPO = 'https://github.com/aki-kii/slides';
const assetsDir = join(import.meta.dirname, 'design-system-site');

const root = resolve(import.meta.dirname, '..');
const srcDir = join(root, 'design-system');

// 層。group 1 は置くもの（ファウンデーション・コンポーネント・テンプレート）、group 2 は選ぶ決め事（共通の骨組み・パターン・テーマ）で「ストーリー」とまとめる。
// 目次ではまとまりごとに区切って並べる。名前を付けるのは group 2（ストーリー）だけ。body は項目ページの「中身」の欄の名前
const LAYERS = [
  { key: 'base', group: 1, body: '値', desc: '全ページに共通する値と決まり' },
  {
    key: 'parts',
    group: 1,
    body: 'サイズ・値と実装',
    desc: 'ページの中に置く1つの要素',
  },
  {
    key: 'pages',
    group: 1,
    body: '置くコンポーネントと並び',
    desc: '1枚のページの組み方',
  },
  {
    key: 'skeleton',
    group: 2,
    body: '並びと使うテンプレート',
    title: '共通の骨組み',
    single: true,
  },
  { key: 'flows', group: 2, body: '並びと使うテンプレート' },
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
    write(
      current,
      layout({
        title,
        body: render(md, { shots }),
        current,
        src: `design-system/${doc.file}`,
      }),
    );
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
      layout({
        title: layer.title,
        body,
        current: `${layer.key}.html`,
        src: `design-system/${layer.key}/_index.md`,
      }),
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
        current: `${it.id}.html`,
        src: `design-system/${it.file}`,
      }),
    );
  }

  for (const id of Object.keys(manifest)) {
    if (!used.has(id))
      problems.push(`manifest の ${id} がどのページにも出てこない`);
  }
  cpSync(assetsDir, join(outDir, 'assets'), { recursive: true });
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
  const out = [
    `<h1>${inline(it.name)} <code class="id">${esc(it.id)}</code></h1>`,
    `<p class="comp-lead">${inline(it.definition)}</p>`,
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

// 層の一覧の表: 見本の写真1枚・名前・1行の説明。テンプレートは骨組みの場所ごとに分ける
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
    `<div class="table-wrap"><table class="items"><thead><tr><th>見本</th><th>名前</th><th>説明</th></tr></thead><tbody>${list.map(row).join('')}</tbody></table></div>`;
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
      out.push(`<pre class="code"><code>${esc(buf.join('\n'))}</code></pre>`);
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
  return `<div class="table-wrap"><table><thead><tr>${cells(head)
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

// 目次の並び。グループごとに、開くページ（href）と、小見出し（sub）を並べる
function navGroups() {
  const groups = [
    {
      id: 'start',
      title: 'はじめに',
      entries: [{ href: 'index.html', label: 'はじめに' }],
    },
  ];
  const itemEntries = (layer) =>
    layer.items.map((it) => ({ href: `${it.id}.html`, label: it.name, layer }));
  for (const layer of ctx.layers.values()) {
    if (layer.group !== 1) continue;
    groups.push({
      id: layer.key,
      title: layer.title,
      desc: layer.desc,
      entries: [
        {
          href: `${layer.key}.html`,
          label: `${layer.title}の一覧`,
          list: layer,
        },
        ...itemEntries(layer),
      ],
    });
  }
  const story = [...ctx.layers.values()].filter((l) => l.group === 2);
  const storyEntries = [];
  for (const layer of story) {
    if (layer.single) {
      storyEntries.push(...itemEntries(layer));
      continue;
    }
    storyEntries.push(
      { sub: layer.title },
      { href: `${layer.key}.html`, label: `${layer.title}の一覧`, list: layer },
      ...itemEntries(layer),
    );
  }
  groups.push({
    id: 'story',
    title: GROUP_LABELS[2],
    desc: story.map((l) => l.title).join('・'),
    entries: storyEntries,
  });
  groups.push({
    id: 'docs',
    title: 'その他の文書',
    entries: DOCS.filter((d) => d.group).map((d) => ({
      href: d.file.replace(/\.md$/, '.html'),
      label: d.nav,
    })),
  });
  return groups;
}

const ICONS = {
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
  x: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
};

// 外枠: 固定ヘッダー（ブランド・層へのピル）、左の目次、パンくず、白い本文、前後のページ、元の文書へのリンク
function layout({ title, body, current, src }) {
  const groups = navGroups();
  const group = groups.find((g) => g.entries.some((e) => e.href === current));
  const entry = group?.entries.find((e) => e.href === current);

  const navItem = (e) =>
    e.sub
      ? `<li class="side-sub">${esc(e.sub)}</li>`
      : `<li><a href="${e.href}"${e.href === current ? ' aria-current="page"' : ''}>${esc(e.label)}</a></li>`;
  const side = groups
    .map((g) => {
      const cur = g === group;
      return `<details class="side-group${cur ? ' is-current' : ''}"${cur ? ' open' : ''}><summary class="side-summary"><span class="side-title">${esc(g.title)}</span>${g.desc ? `<span class="side-desc">${esc(g.desc)}</span>` : ''}</summary><ul>${g.entries.map(navItem).join('')}</ul></details>`;
    })
    .join('');

  const global = groups
    .filter((g) => g.id !== 'start')
    .map((g) => {
      const top = g.entries.find((e) => e.href).href;
      return `<li><a href="${top}"${g === group ? ' aria-current="true"' : ''}>${esc(g.title)}</a></li>`;
    })
    .join('');

  // パンくず: トップ / （ストーリー） / 層の一覧 / このページ
  const crumbs = [];
  if (current !== 'index.html') {
    crumbs.push('<li><a href="index.html">トップ</a></li>');
    if (group?.id === 'story' || group?.id === 'docs')
      crumbs.push(`<li>${esc(group.title)}</li>`);
    const layer = entry?.layer;
    if (layer && !layer.single)
      crumbs.push(
        `<li><a href="${layer.key}.html">${esc(layer.title)}</a></li>`,
      );
    const here = entry?.list ? entry.list.title : (entry?.label ?? title);
    crumbs.push(`<li aria-current="page">${esc(here)}</li>`);
  }

  // 前後のページ: 同じグループの目次の並び
  let pager = '';
  const seq = group ? group.entries.filter((e) => e.href) : [];
  const at = seq.findIndex((e) => e.href === current);
  if (seq.length > 1 && at >= 0) {
    const prev = seq[at - 1];
    const next = seq[at + 1];
    pager = `<nav class="pager" aria-label="前後のページ">${prev ? `<a class="pager-prev" href="${prev.href}"><span>前へ</span>${esc(prev.label)}</a>` : ''}${next ? `<a class="pager-next" href="${next.href}"><span>次へ</span>${esc(next.label)}</a>` : ''}</nav>`;
  }

  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${current === 'index.html' ? 'スライド用デザインシステム' : `${esc(title)} | スライド用デザインシステム`}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400..900&family=Noto+Sans+JP:wght@400..900&display=swap">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">本文へ移動</a>
<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-name">スライド用デザインシステム</span></a>
    <nav class="global-nav" aria-label="サイト全体"><ul>${global}</ul></nav>
    <div class="header-tools">
      <a class="header-link" href="../">スライド一覧へ</a>
      <button class="tool-btn menu-btn" type="button" aria-expanded="false" aria-controls="side" aria-label="目次を開く" title="目次を開く" data-menu-toggle><span data-menu-icon="open">${ICONS.menu}</span><span data-menu-icon="close" hidden>${ICONS.x}</span></button>
    </div>
  </div>
</header>
<div class="site-body">
  <nav class="side" id="side" aria-label="目次"><p class="side-head">目次</p>${side}</nav>
  <main id="main" class="main">
    ${crumbs.length ? `<ol class="crumbs" aria-label="現在地">${crumbs.join('')}</ol>` : ''}
    <article class="doc">
${body}
    </article>
    ${pager}
    <footer class="page-foot"><p><a href="${REPO}/blob/main/${src}" rel="noopener">GitHub で元の文書を見る（${esc(src)}）</a></p></footer>
  </main>
</div>
<script src="assets/site.js" defer></script>
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
