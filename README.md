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

## GitHub Pages で公開

`main` に push すると `.github/workflows/pages.yml` が全デッキをビルドして `gh-pages` ブランチに置き、https://aki-kii.github.io/slides/ で見られる（デッキは `/slides/<name>/`）。

- 手元で同じものを作る: `pnpm build:pages`（`dist/` に出る。デッキ名を付けるとそれだけ作る）
- 一覧（`/slides/`）は登壇日の新しい順。登壇日は `slides.md` で最初に出てくる日付（表紙の `2026.10.29（木）` など）
- 載せないデッキは `scripts/build-pages.mjs` の `EXCLUDE` にフォルダ名を書く
- GitHub Pages はリロード時に SPA へ振り分けないので、各デッキの headmatter に `routerMode: hash` を入れている（URL は `/#/12` の形）
- デッキの中の `/images/...` などの絶対パスは、ビルド後の出力だけ `/slides/<name>/images/...` に書き換える。元のファイルは変えない
- 初回だけ Settings → Pages で Source を「Deploy from a branch」、ブランチを `gh-pages` / `/ (root)` にする
