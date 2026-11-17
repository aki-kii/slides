# スライドのデザインシステム

本人のデッキで繰り返し使っている作り方に名前を付けて、次のデッキでも同じ形で使えるようにしたもの。中身（何を言うか）は毎回本人が決めるので、ここでは形だけを決める。

## 5つの層

上から順に決まっていく。上の層が下の層を選ぶ。

| 層 | 何を決めるか | いつ決まるか | ページ |
|---|---|---|---|
| 1. 全体の型（テーマ） | どんな話か（検証してみた系、解説系 など） | スライドを作ると決まった時点 | [全体の型](themes.md) |
| 2. 構成の型 | ページの並べ方（話の流れ、背骨） | テーマで選ぶ | [構成の型](flows.md) |
| 3. ページの型 | 1枚の組み方 | 構成の各所で選ぶ。主役のページはテーマで決まる | [ページの型](pages.md) |
| 4. 部品 | ページの中に置く1つの要素 | ページの型が使う | [部品](parts.md) |
| 5. 土台 | 全ページに共通する決まり（色、書体、文、図、サイズ） | いつも同じ | [土台](foundation.md) |

### テーマが選ぶもの

全体の型（テーマ）は、スライドを作ると決まった時点で決まっている。登壇の話が来た時点で「何をやってみた話か」「何を解説する話か」は決まっているからだ。

テーマは次の2つを選ぶ。

- **構成の型（背骨）**: そのテーマの話をどの順で進めるか。どのテーマも [全体の骨組み](flows.md#flow-whole) の上に乗る
- **主役になるページの型**: そのテーマで一番多く出てくる、話の芯を運ぶページ

```
全体の型（テーマ）
 ├─ 構成の型（背骨）…… 全体の骨組み ＋ テーマの流れ
 └─ 主役のページの型 ── 部品 ── 土台
```

対応の一覧は [全体の型](themes.md#テーマと構成ページの対応) にある。

## 使い方

1. 話が決まったら、[全体の型](themes.md) からテーマを選ぶ
2. テーマの背骨（構成の型）に沿って、ページの並びを決める
3. 各ページを [ページの型](pages.md) から選んで組む。主役のページはテーマに書いてあるもの
4. ページの中は [部品](parts.md) で組み、[土台](foundation.md) の色・文・図・サイズの決まりに合わせる
5. 新しいデッキの名前は [デッキの名前（提案）](naming.md) に沿って付ける

## 写真について

- 写真は `design-system/shots/<パターンのID>/<デッキ>-p<ページ番号>.png`。フォルダ名がパターンの ID。どの写真がどのページかは `shots/manifest.json`
- ページ番号は `slides.md` の並び（クリックを含めない番号）。写真はクリックをすべて出した状態。写真を押すと公開中のデッキのそのページが開く
- 構成の型とテーマの写真は、ページを左から右に並べた1枚の帯
- 最近の2デッキ（jawsug-container-31、jiyugaoka-any-1）はまだ直す余地があるので、見本の写真にはできるだけ使わない。代わりのデッキが無い [分析 → 改善 → 振り返り](flows.md#flow-analyze-improve-review) だけ、jawsug-container-31 の帯を1枚使っている
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
- 写真を差し込む所は `<!-- shots:<パターンのID> -->` の1行で書く。manifest にある ID がどのページにも出てこないとビルドが失敗する
