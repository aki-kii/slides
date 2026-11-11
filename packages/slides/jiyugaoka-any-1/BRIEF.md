# ブリーフ: 自由が丘.any #1 LT スライドの組み直し

## ゴール

`packages/slides/jiyugaoka-any-1` の Slidev デッキを、リポジトリの既存コンポーネントと作法で正しく組み直し、全ページが正しく描画される PDF を書き出す。

## 必読

- life のスライド作成スキル: `~/workspace/life/.claude/skills/slides/SKILL.md`
- 図のスタイル: `~/workspace/life/tasks/speaking/diagram-style.md`
- 文章の書き方: `~/workspace/life/docs/writing-style.md`
- 内容の正（本人の決めた構成と言葉）: `~/workspace/life/tasks/speaking/2026-11-jiyugaoka-any-1/README.md`
- お手本デッキ: `packages/slides/jaws-sonic-2026`（Statement / StatementList / ChapterLabel の使い方）、`packages/slides/cdk-day1-experiment`

## 現在の状態と問題

- 現在の `slides.md` は2版目。export-check の書き出し自体は通る（エラー0）が、序章ページ（3ページ目、StatementList）が真っ白に描画される。みのるん式ページでは画像 `/images/minorun-slide-4.jpg` が表示されず、左下に小さく欠片だけ出る。
- 原因の特定から始めてほしい。`components/Statement.vue` と `components/StatementList.vue` は jaws-sonic-2026 からコピー済みで、style.css 末尾に `.intro-*` のスタイルを追加済み。

## 方針

- 紙芝居型は1枚に寄せる（JAWS SONIC の序章とまとめの組み方）。序章は StatementList で1枚にし、クリックで3ブロック出す。
- 章ラベルは ChapterLabel で統一する（frontmatter の `chapter` を読む部品）。
- みのるん式は、みのるんさんのスライドそのものを参照して見せる形にする（`public/images/minorun-slide-4.jpg` を大きく表示し、出典を添える）。ポイント3つのページは作らない。
- モノレポの図は InlineSvg で埋め込み、Overlay で「このAI秘書に健康管理を任せました」を出す。
- Muse の特徴の「（隠し：倫理観がない）」は Kogoe でクリック表示にする。
- 文言は本人の言葉を変えない。助詞・助動詞・接続詞が不自然になる組み替えをしない（`docs/writing-style.md`）。
- 台本はデッキ内の `script.md` に分けて持ち、スライドに登壇者ノートは入れない。

## 環境

- mise は無い。Node は system の v24。pnpm は `npx -y pnpm` で使う。

## 完了条件

- リポジトリルートで `npx -y pnpm export-check packages/slides/jiyugaoka-any-1 --name jiyugaoka-any-1` がエラー0で通る。
- 書き出された PNG（`/workspace/slides-out/png/jiyugaoka-any-1/`）を全ページ目で見て、真っ白、はみ出し、画像の欠けがないことを確認する。
- 最後に、直した内容と PDF の置き場所を簡潔に報告する。
