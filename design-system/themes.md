# 全体の型（テーマ）

デッキ全体が「どんな話か」の型。スライドを作ると決まった時点で決まっている。テーマが [構成の型](flows.md)（背骨）と、主役になる [ページの型](pages.md) を選ぶ。

- テーマの分け方と各テーマのデッキは、本人が挙げた候補（2026-11-18）
- 各テーマの背骨と主役のページは、そのテーマのデッキで実際に使っている型から読み取った。本人の記録で決まったものではないので、デッキを作りながら直してよい
- どのテーマも [全体の骨組み](flows.md#flow-whole)（表紙 → 自己紹介 → 導入 → 本編 → まとめ →（宣伝）→ Thank You）の上に乗る

## テーマと構成・ページの対応

| テーマ | デッキ | 背骨（構成の型） | 主役のページの型 |
|---|---|---|---|
| [検証してみた系](#theme-verification) | container-31、failed-ecs、cdk-day1、ecr-sbom | [分析 → 改善 → 振り返り](flows.md#flow-analyze-improve-review) | [言い切り（紙芝居型）](pages.md#page-kamishibai)、[「〜とは？」（リストアップ型）](pages.md#page-what-is-list)、[図＋結論](pages.md#page-figure-conclusion)、[まとめ（言い切り）](pages.md#page-summary-statement) |
| [解説系](#theme-explainer) | continuum、aws-oss、whats-cloud-assembly | [定義に戻りながら進める](flows.md#flow-definition-return)、[疑問を湧かせてから解消する](flows.md#flow-question-answer) | [「〜とは？」（図示型）](pages.md#page-what-is-figure)、[定義の使い回し](pages.md#page-definition-reuse)、[箇条書き＋結論](pages.md#page-list-conclusion)、[2つを並べて比べる](pages.md#page-compare) |
| [入門・紹介系](#theme-intro) | bgnr-93 | [困りごと → 解決策](flows.md#flow-trouble-solution)、[部の頭に導入の紙芝居](flows.md#flow-part-intro) | [ストーリー型](pages.md#page-story)、[章扉](pages.md#page-chapter)、[特徴・理由を1つずつ](pages.md#page-one-by-one)、[2つを並べて比べる](pages.md#page-compare)、[Q&A](pages.md#page-qa)、[まとめ（箇条書き）](pages.md#page-summary-list) |
| [プラクティス紹介系](#theme-practice) | cdk-day1 | [お悩みを1つずつ解決](flows.md#flow-onayami) | [章扉](pages.md#page-chapter)、[お悩み → 解決](pages.md#page-onayami) |
| [体験談系](#theme-experience) | jiyugaoka-any-1、lt-40、zero-drift、jaws-sonic-2026 | [部の頭に導入の紙芝居](flows.md#flow-part-intro) | [紙芝居型](pages.md#page-kamishibai)、[図＋結論](pages.md#page-figure-conclusion)、[Q&A](pages.md#page-qa)、[まとめ（箇条書き）](pages.md#page-summary-list) |

候補に挙がっていないデッキ:

- cdkd-talk（「AWS CDKを理解するために公式の定義を深掘って解説してみる」）は、題名と [定義に戻りながら進める](flows.md#flow-definition-return) の元になったデッキなので、解説系として扱う
- cdk-3min（「AWS CDK 3分クッキング」）はデモが中心で、どのテーマにも入れていない
- cdk-day1 は、題名は技術検証の話で、組み方はプラクティス紹介。候補どおり両方に入れた

---

## theme-verification 検証してみた系

- **何のテーマか**: 何かを実際に試して、測った結果や分かったことを見せる話
- **デッキ**: container-31（「SOCIインデックスでコンテナの起動を速くしてみた」）、failed-ecs（「ECSアプリログをFireLensでコスト削減しようとしたけど諦めた話」）、cdk-day1（「最初からAWS CDKで技術検証してもいいんじゃない？」）、ecr-sbom（「ECR拡張スキャンでSBOMを収集してサプライチェーン攻撃の影響調査を爆速で終わらせてみた」）
- **背骨**: [分析 → 改善 → 振り返り](flows.md#flow-analyze-improve-review)。導入では困りごとを言い切る（failed-ecs「CloudWatch Logsの書き込み料金が高い！！！」）
- **主役のページ**: 困りごとの [言い切り](pages.md#page-kamishibai)、使うものの [「〜とは？」](pages.md#page-what-is-list)、構成や測った結果の [図＋結論](pages.md#page-figure-conclusion)、締めの [まとめ（言い切り）](pages.md#page-summary-statement)
- **気を付けること**: 悪くなった所も見せる（コンテナ支部、2026-11-15）。諦めた話も結果として見せてよい（failed-ecs）
- **写真**: failed-ecs の p.3 言い切り → p.5 図 → p.6 Overlay → p.7 図 → p.13 まとめ

<!-- shots:theme-verification -->

## theme-explainer 解説系

- **何のテーマか**: サービスや仕組み、考え方を説明する話
- **デッキ**: continuum（「AWS CDKのカスタムリソースでContinuum（旧Security Agent）を実装した話」）、aws-oss（「AWSはOSSをどのように思っているのか？」）、whats-cloud-assembly（`slides.md` がなく写真にできない）
- **背骨**: [定義に戻りながら進める](flows.md#flow-definition-return)、[疑問を湧かせてから解消する](flows.md#flow-question-answer)
- **主役のページ**: [「〜とは？」（図示型）](pages.md#page-what-is-figure)、[定義の使い回し](pages.md#page-definition-reuse)、[箇条書き＋結論](pages.md#page-list-conclusion)、[2つを並べて比べる](pages.md#page-compare)
- **気を付けること**: 茨城 #17 の使い分けのページは発表後に「いちばん強い」とされた（2026-10-01）
- **写真**: continuum の p.3 「〜とは？」 → p.4 言い切り → p.11 疑問 → p.12 小声 → p.20 使い分け → p.21 まとめ

<!-- shots:theme-explainer -->

## theme-intro 入門・紹介系

- **何のテーマか**: 初めての人に、技術を紹介して入口に立ってもらう話
- **デッキ**: bgnr-93（「AI時代のIaC入門 〜なぜインフラをコードで管理したいのか？〜」）
- **背骨**: [困りごと → 解決策](flows.md#flow-trouble-solution)。部がいくつかあるので [部の頭に導入の紙芝居](flows.md#flow-part-intro) も使う
- **主役のページ**: 導入の [ストーリー型](pages.md#page-story)、部の [章扉](pages.md#page-chapter)、[特徴・理由を1つずつ](pages.md#page-one-by-one)、[2つを並べて比べる](pages.md#page-compare)、[Q&A](pages.md#page-qa)、[まとめ（箇条書き）](pages.md#page-summary-list)
- **気を付けること**: 本人「こんなことに困ってない？？ってきいて解決策を出す方が刺さりそう」（2026-10-24）
- **写真**: bgnr-93 の p.5 ストーリー → p.10 問題点 → p.11 章扉 → p.14 比べる → p.30 Q&A → p.32 まとめ

<!-- shots:theme-intro -->

## theme-practice プラクティス紹介系

- **何のテーマか**: いくつかのやり方（プラクティス）を、1つずつ紹介する話
- **デッキ**: cdk-day1（「最初からAWS CDKで技術検証してもいいんじゃない？」）
- **背骨**: [お悩みを1つずつ解決](flows.md#flow-onayami)
- **主役のページ**: プラクティスごとの [章扉](pages.md#page-chapter)（「① 〜するべし」）、[お悩み → 解決](pages.md#page-onayami)
- **気を付けること**: life に記録はなく、デッキから拾った型
- **写真**: cdk-day1 の p.10 → p.11 章扉 → p.12 お悩み → p.13 解決

<!-- shots:theme-practice -->

## theme-experience 体験談系

- **何のテーマか**: 自分がやってきたこと・作ったものの体験を話す
- **デッキ**: jiyugaoka-any-1（「MuseをAI秘書にして健康管理を任せてみた」）、lt-40（「自作Discord音声botをLambda MicroVMsに移行した話」）、zero-drift（「ドリフトを絶対に許さない（？）CDK運用」）、jaws-sonic-2026（「cdk deploy JawsSonic 〜MARATHONしながらAWSリソースをデプロイしてみよう〜」）
- **背骨**: [部の頭に導入の紙芝居](flows.md#flow-part-intro)
- **主役のページ**: 導入の [紙芝居型](pages.md#page-kamishibai)、仕組みの [図＋結論](pages.md#page-figure-conclusion)、[Q&A](pages.md#page-qa)、[まとめ（箇条書き）](pages.md#page-summary-list)
- **気を付けること**: 自己紹介の中身は聞く人に合わせる（自由が丘.any は AWS ではなく趣味、2026-11-09）
- **写真**: jaws-sonic-2026 の p.4 紙芝居 → p.5 Q&A → p.6 図 → p.8 章扉 → p.34 まとめ

<!-- shots:theme-experience -->
