# スライドのデザインシステム

本人のデッキで繰り返し使っている作り方に名前を付けて、次のデッキでも同じ形で使えるようにしたもの。中身（何を言うか）は毎回本人が決めるので、ここでは形だけを決める。

## 使い方

1. 話が決まったら、[全体の型（テーマ）](@themes) からテーマを選ぶ
2. テーマの背骨（[構成の型](@flows)）に沿って、[共通の骨組み](@flow-whole) の上にページの並びを決める
3. 各ページを [ページの型](@pages) から選んで組む。主役のページはテーマに書いてあるもの
4. ページの中は [コンポーネント](@parts) で組み、[土台](@base) の色・文・図・サイズの決まりに合わせる
5. 新しいデッキの名前は [デッキの名前（提案）](naming.md) に沿って付ける

## 材料と話の型

項目は「材料（置くもの）」と「話の型（選ぶもの）」の2つのグループに分かれる。材料は小さいものから大きいものへ積み上がる。話の型は、材料の中から組み合わせを選ぶ決め事で、材料とは別の軸にある。

テーマは、構成の型（背骨）と主役になるページの型を選ぶ。

```
全体の型（テーマ） ──選ぶ──▶ 構成の型（背骨）
        │
        └──────選ぶ──▶ 主役のページの型
```

## 材料（置くもの）

| 層 | 役割 |
|---|---|
| [土台](@base) | 全ページに共通する値と決まり（色、文の書き方、図のスタイル、サイズ） |
| [コンポーネント](@parts) | ページの中に置く1つの要素 |
| [ページの型](@pages) | 1枚のページの組み方 |

## 話の型（選ぶもの）

| 層 | 役割 |
|---|---|
| [共通の骨組み](@flow-whole) | すべてのテーマが乗る流れ。表紙 → 自己紹介 → 導入 → 本編 → まとめ →（宣伝）→ Thank You |
| [構成の型](@flows) | ページの並べ方（話の流れ） |
| [全体の型（テーマ）](@themes) | デッキ全体がどんな話かの型。構成の型（背骨）と主役のページの型を選ぶ |

## その他の文書

- [デッキの名前（提案）](naming.md)
- [決めたこと](decisions.md)
- [サイズの調査メモ](research-sizes.md)

## 写真について

- 写真は `design-system/shots/<パターンのID>/<デッキ>-p<ページ番号>.png`。フォルダ名がパターンの ID。どの写真がどのページかは `shots/manifest.json`
- ページ番号は `slides.md` の並び（クリックを含めない番号）。写真はクリックをすべて出した状態。写真を押すと公開中のデッキのそのページが開く
- 共通の骨組み、構成の型、テーマの写真は、ページを左から右に並べた1枚の帯
- 最近の2デッキ（jawsug-container-31、jiyugaoka-any-1）はまだ直す余地があるので、見本の写真にはできるだけ使わない。代わりのデッキが無い [分析 → 改善 → 振り返り](@flow-analyze-improve-review) だけ、jawsug-container-31 の帯を1枚使っている
- `@slides/ui` の InlineSvg の不具合で、図の中の AWS のアイコンが大きく崩れて写る写真がある。その写真には注記を付けた（[決めたこと](decisions.md#見つけた不具合)）

## 言葉の出典

言葉は本人の記録から取り、創作しない。かっこ内の日付はその記録の日付。

- life の `.claude/skills/slides/SKILL.md`（以下 SKILL.md）
- life の `tasks/speaking/diagram-style.md`（以下 diagram-style.md）
- life の `tasks/speaking/` の各回の README

デッキの略し方: container-31 = jawsug-container-31（コンテナ支部）、bgnr-93 = jawsug-bgnr-93（初心者支部で登壇したスライド）、continuum = cdk-custom-resource-continuum（茨城 #17）、cdkd-talk = jawsug-cdk-tokyo-cdkd-talk（CDK 支部×東京支部）、lt-40 = jawsug-tokyo-lunch-lt-40（ランチタイム LT #40）、ecr-sbom = ecr-sbom-supply-chain-investigation、failed-ecs = failed-ecs-log-cost-reduction、zero-drift = zero-drift-cdk-ops、cdk-day1 = cdk-day1-experiment、aws-oss = aws-oss-perspective、cdk-3min = cdk-3min-cooking

## サイトの作り方

- このフォルダの Markdown を `scripts/build-design-system.mjs` が HTML にする。`pnpm build:pages` でスライドと一緒に `dist/design-system/` に出る（GitHub Pages の `/slides/design-system/`）
- これだけ作り直すときは `pnpm build:ds`
- 項目は1つにつき1ファイル。層ごとのフォルダ（`base/`、`parts/`、`pages/`、`flows/`、`themes/`）と、共通の骨組みの `skeleton/` に置く。ファイル名は項目の ID
- 項目のファイルは、頭に `id` と `name`（ページの型は骨組みの場所の `place` も）を書き、本文は「1行の定義 → `## 見本` → `## いつ使うか` → `## 中身` → `## 気を付けること`」の順に書く。「関連する項目」は項目どうしのリンクから作られる
- 層の一覧ページは各フォルダの `_index.md`。`order` に項目の並びを書き、`<!-- items -->` の所に一覧の表が入る
- 項目へのリンクは `[名前](@<ID>)`、一覧へのリンクは `[名前](@<フォルダ名>)` と書く
- 写真を差し込む所は `<!-- shots:<パターンのID> -->` の1行で書く。manifest にある ID がどの項目にも出てこないとビルドが失敗する
