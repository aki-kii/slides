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

## GitHub Pages で公開

`main` に push すると `.github/workflows/pages.yml` が全デッキをビルドして `gh-pages` ブランチに置き、https://aki-kii.github.io/slides/ で見られる（デッキは `/slides/<name>/`）。

- 手元で同じものを作る: `pnpm build:pages`（`dist/` に出る。デッキ名を付けるとそれだけ作る）
- 一覧（`/slides/`）は登壇日の新しい順。登壇日は `slides.md` で最初に出てくる日付（表紙の `2026.10.29（木）` など）
- GitHub Pages はリロード時に SPA へ振り分けないので、各デッキの headmatter に `routerMode: hash` を入れている（URL は `/#/12` の形）
- デッキの中の `/images/...` などの絶対パスは、ビルド後の出力だけ `/slides/<name>/images/...` に書き換える。元のファイルは変えない
- 初回だけ Settings → Pages で Source を「Deploy from a branch」、ブランチを `gh-pages` / `/ (root)` にする
