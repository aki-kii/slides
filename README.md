# Slides

pnpm monorepo for Slidev presentations.

## Setup

```bash
mise install
pnpm install
```

## Adding a new slide deck

1. `packages/slides/<name>/` を作成
2. `package.json` と `slides.md` を配置
3. `pnpm install` を実行

## Exporting and checking a deck

`pnpm export-check <deck-dir> [--name <name>] [--pages 3,7-9|changed|all] [--out <dir>] [--dpi 60] [--wait 500]`

デッキの `pnpm export` で PDF を書き出し、`<out>/<name>.pdf`（既定は `/workspace/slides-out/<デッキ名>.pdf`）にコピーして、ページを `<out>/png/<name>/` に PNG で出す。前回の PDF があれば、見た目が変わったページを挙げ、既定ではそのページだけ PNG にする。最後にページ数と、書き出しの警告・エラーを出す。poppler-utils（`pdfinfo`、`pdftoppm`、`pdftotext`）が要る。前回と比べるときは、ページの見た目と文字の両方を見る。

```bash
pnpm export-check packages/slides/jawsug-cdk-tokyo-cdkd-talk --name cdk-talk
```
