/**
 * デッキの図とスクショを書き出す CLI。
 *
 *   slides-tools diagrams <定義.ts> --out <出力フォルダ> [--icons <アイコン置き場>]
 *   slides-tools shots <定義.ts> --in <スクショのフォルダ> --out <出力フォルダ>
 *
 * --icons を省いたときは環境変数 AWS_ICONS を使う。
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { createDiagramKit, type DiagramsDefinition } from './svg.ts';
import { createShots, type ShotsDefinition } from './shots.ts';

const usage = `使い方:
  slides-tools diagrams <定義.ts> --out <出力フォルダ> [--icons <アイコン置き場>]
  slides-tools shots <定義.ts> --in <スクショのフォルダ> --out <出力フォルダ>`;

const { positionals, values } = parseArgs({
  allowPositionals: true,
  options: {
    out: { type: 'string' },
    in: { type: 'string' },
    icons: { type: 'string' },
  },
});

const [command, definitionPath] = positionals;

function fail(message: string): never {
  console.error(`Error: ${message}\n\n${usage}`);
  process.exit(1);
}

if (!command || !definitionPath)
  fail('コマンドと定義ファイルを指定してください。');
if (!values.out) fail('--out を指定してください。');

const outDir = resolve(values.out);
const mod = await import(pathToFileURL(resolve(definitionPath)).href);
mkdirSync(outDir, { recursive: true });

if (command === 'diagrams') {
  const definition = mod.default as DiagramsDefinition;
  const kit = createDiagramKit({
    iconsDir: values.icons ?? process.env.AWS_ICONS,
    icons: definition.icons,
    note: definition.note,
  });
  for (const [name, content] of Object.entries(definition.build(kit))) {
    writeFileSync(join(outDir, name), content);
    console.log(name);
  }
} else if (command === 'shots') {
  if (!values.in) fail('--in にスクショのフォルダを指定してください。');
  const definition = mod.default as ShotsDefinition;
  await definition(createShots(resolve(values.in), outDir));
} else {
  fail(`知らないコマンドです: ${command}`);
}
