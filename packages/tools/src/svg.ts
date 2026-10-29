/**
 * SVG の図を文字列で組み立てるヘルパー。
 *
 *   const kit = createDiagramKit({ iconsDir, icons: { waf: 'Arch_AWS-WAF_64.svg' } });
 *   kit.svg(600, 300, [kit.icon('waf', 10, 10, 48), kit.text(80, 40, 'WAF')], 'WAF の図');
 *
 * アイコンは AWS Architecture Icons などの SVG を、ファイル名でアイコン置き場から探して埋め込む。
 * 埋め込むたびに id とクラス名へ連番の接頭辞を付けて、同じページの別の図とぶつからないようにする。
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, join } from 'node:path';

/** 図で使う色（life の tasks/speaking/diagram-style.md に合わせた既定） */
export const palette = {
  INK: '#2c3e50',
  SUB: '#6b7684',
  LINE: '#c9d0d9',
  GREEN: '#0E8A6E',
  GREEN_BG: '#e9f5f1',
  RED: '#DD344C',
  RED_BG: '#fdecee',
  GRAY: '#8a94a3',
} as const;

export const fonts = {
  JP: "'Noto Sans JP', 'Hiragino Sans', sans-serif",
  MONO: "'Fira Code', monospace",
} as const;

/** 矢じり（marker）の id と色。arrow() の色はここにあるものだけ使える */
const DEFAULT_MARKERS: Record<string, string> = {
  i: palette.INK,
  g: palette.GREEN,
  r: palette.RED,
  x: palette.GRAY,
};

export interface DiagramKitOptions {
  /** アイコンの SVG を置いたフォルダ。下の階層も含めてファイル名で探す */
  iconsDir?: string;
  /** 図の中で使う名前 → アイコンのファイル名 */
  icons?: Record<string, string>;
  /** 各 SVG の先頭に入れるコメント（アイコンの版など） */
  note?: string;
  markers?: Record<string, string>;
}

export interface TextOptions {
  size?: number;
  weight?: string;
  color?: string;
  anchor?: 'start' | 'middle' | 'end';
  mono?: boolean;
}

export interface ArrowOptions {
  color?: string;
  width?: number;
  dash?: string;
}

export interface ServiceOptions {
  sub?: string;
  size?: number;
  monoSub?: boolean;
  /** 名前の文字サイズ */
  fs?: number;
  /** 補足の文字サイズ */
  ss?: number;
}

/** パッケージのフォルダ名の揺れ（カテゴリ名など）に強くするため、ファイル名だけで探す */
function findFile(dir: string, name: string): string | undefined {
  for (const entry of readdirSync(dir)) {
    if (entry === '__MACOSX') continue;
    const path = join(dir, entry);
    if (statSync(path).isDirectory()) {
      const found = findFile(path, name);
      if (found) return found;
    } else if (entry === name) {
      return path;
    }
  }
  return undefined;
}

export function createDiagramKit(options: DiagramKitOptions = {}) {
  const icons = options.icons ?? {};
  const markers = options.markers ?? DEFAULT_MARKERS;
  const markerOf = Object.fromEntries(
    Object.entries(markers).map(([id, color]) => [color, id]),
  );
  const cache = new Map<string, string>();
  let n = 0;

  function iconSource(key: string): string {
    const file = icons[key];
    if (!file) throw new Error(`アイコン "${key}" が icons にありません`);
    if (!cache.has(file)) {
      if (!options.iconsDir) {
        throw new Error(
          'アイコン置き場が指定されていません（--icons または環境変数 AWS_ICONS）',
        );
      }
      const path = findFile(options.iconsDir, basename(file));
      if (!path) throw new Error(`アイコンが見つかりません: ${file}`);
      cache.set(file, readFileSync(path, 'utf8'));
    }
    return cache.get(file)!;
  }

  /** アイコンを (x, y) に size 四方で埋め込む。id とクラス名に接頭辞を付ける */
  function icon(key: string, x: number, y: number, size: number): string {
    n += 1;
    const prefix = `${key}${n}-`;
    const s = iconSource(key).replace(/<\?xml[^>]*\?>/g, '');
    const viewBox = /viewBox="([^"]+)"/.exec(s)![1];
    let body = /<svg[^>]*>([\s\S]*)<\/svg>/.exec(s)![1];
    for (const id of new Set(
      [...body.matchAll(/id="([^"]+)"/g)].map((m) => m[1]),
    )) {
      body = body
        .replaceAll(`id="${id}"`, `id="${prefix}${id}"`)
        .replaceAll(`url(#${id})`, `url(#${prefix}${id})`);
    }
    body = body
      .replace(/\.cls-(\d)/g, `.${prefix}cls-$1`)
      .replaceAll('class="cls-', `class="${prefix}cls-`)
      .replace(/<title>[\s\S]*?<\/title>/g, '');
    return `<svg x="${x}" y="${y}" width="${size}" height="${size}" viewBox="${viewBox}">${body.trim()}</svg>`;
  }

  function text(x: number, y: number, s: string, o: TextOptions = {}): string {
    const family = o.mono ? fonts.MONO : fonts.JP;
    return (
      `<text x="${x}" y="${y}" font-family="${family}" font-size="${o.size ?? 15}" ` +
      `font-weight="${o.weight ?? 'normal'}" fill="${o.color ?? palette.INK}" ` +
      `text-anchor="${o.anchor ?? 'middle'}">${s}</text>`
    );
  }

  function arrow(d: string, o: ArrowOptions = {}): string {
    const color = o.color ?? palette.INK;
    const id = markerOf[color];
    if (!id) throw new Error(`矢じりの色 ${color} が markers にありません`);
    const dash = o.dash ? ` stroke-dasharray="${o.dash}"` : '';
    return (
      `<path d="${d}" fill="none" stroke="${color}" stroke-width="${o.width ?? 2.5}"${dash} ` +
      `stroke-linejoin="round" stroke-linecap="round" marker-end="url(#a-${id})"/>`
    );
  }

  /** アイコンと、その下に名前（と補足）を置く */
  function service(
    key: string,
    cx: number,
    cy: number,
    name: string,
    o: ServiceOptions = {},
  ): string[] {
    const size = o.size ?? 64;
    const fs = o.fs ?? 18;
    const ss = o.ss ?? 15;
    const half = Math.floor(size / 2);
    const out = [icon(key, cx - half, cy - half, size)];
    const y = cy + half + fs + 4;
    out.push(text(cx, y, name, { size: fs, weight: 'bold' }));
    if (o.sub) {
      out.push(
        text(cx, y + ss + 6, o.sub, {
          size: ss,
          color: palette.SUB,
          mono: o.monoSub,
        }),
      );
    }
    return out;
  }

  /** 1 枚の SVG にまとめる。label は aria-label（スライドの読み上げ用） */
  function svg(w: number, h: number, body: string[], label: string): string {
    const defs = Object.entries(markers)
      .map(
        ([id, color]) =>
          `<marker id="a-${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" ` +
          `orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="${color}"/></marker>`,
      )
      .join('');
    const note = options.note ? `\n<!-- ${options.note} -->` : '';
    return (
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="100%" role="img" ` +
      `aria-label="${label}">${note}\n<defs>${defs}</defs>\n` +
      body.join('\n') +
      '\n</svg>\n'
    );
  }

  return { icon, text, arrow, service, svg };
}

export type DiagramKit = ReturnType<typeof createDiagramKit>;

/** 図の定義ファイル（default export）の形。build は「ファイル名 → SVG」を返す */
export interface DiagramsDefinition {
  icons?: Record<string, string>;
  note?: string;
  build(kit: DiagramKit): Record<string, string>;
}

export function defineDiagrams(
  definition: DiagramsDefinition,
): DiagramsDefinition {
  return definition;
}
