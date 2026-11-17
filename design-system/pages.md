# ページの型

1枚の組み方の型。[構成の型](flows.md) の各所で選ぶ。どのページが主役になるかは [全体の型（テーマ）](themes.md) で決まる。文字の大きさは [土台のサイズ](foundation.md#base-size) に合わせる。

| 骨組みの場所 | ページの型 |
|---|---|
| 表紙・自己紹介 | [表紙](#page-title)、[自己紹介](#page-profile) |
| 導入 | [紙芝居型](#page-kamishibai)（言い切りを含む）、[ストーリー型](#page-story) |
| 章の区切り | [章扉](#page-chapter) |
| 本編 | [「〜とは？」（リストアップ型）](#page-what-is-list)、[「〜とは？」（図示型）](#page-what-is-figure)、[定義の使い回し](#page-definition-reuse)、[特徴・理由を1つずつ](#page-one-by-one)、[箇条書き＋結論](#page-list-conclusion)、[図＋結論](#page-figure-conclusion)、[2つを並べて比べる](#page-compare)、[お悩み → 解決](#page-onayami)、[Q&A](#page-qa) |
| まとめ以降 | [まとめ（言い切り）](#page-summary-statement)、[まとめ（箇条書き）](#page-summary-list)、[宣伝](#page-promo)、[Thank You](#page-thanks) |

---

## page-title 表紙

- **何の型か**: 青のグラデーションに、イベント名（小）・タイトル・日付と名前、右下にアイキャッチ
- **いつ使うか**: 1枚目。強調はキーワード1か所（初心者支部「表紙で強調するのは『IaC入門』のみ」2026-10-28）
- **部品・土台**: [強調](parts.md#part-strong)（表紙のキーワードだけ黄色）、[色](foundation.md#base-color)
- **写真**: continuum p.1、failed-ecs p.1、lt-40 p.1、zero-drift p.1

<!-- shots:page-title -->

## page-profile 自己紹介

- **何の型か**: 左に写真、右に名前と所属・推しサービス
- **いつ使うか**: 2枚目。中身は聞く人に合わせる（自由が丘.any は AWS ではなく趣味、2026-11-09）
- **写真**: continuum p.2

<!-- shots:page-profile -->

## page-kamishibai 紙芝居型

- **何の型か**: 小さい前置き＋大きい言い切り（SKILL.md「紙芝居のページ（`layout: center` の前置き＋言い切り）」）。話し言葉で書く（2026-10-19 本人「紙芝居は基本口語で書いてない？」）
- **前置きなしの形（言い切り）**: 前置きを付けず、真ん中に大きく1文だけを置く形もこの型に含める。問いかけ（「みなさんは〜できていますか？」）、困りごと（「〜が高い！！！」）、話の宣言（「〜の話をします」）（[決めたこと](decisions.md#q3)）
- **いつ使うか**: デッキの導入と、各部の導入（[部の頭に導入の紙芝居](flows.md#flow-part-intro)）。本編の説明には使わない（LT #40「紙芝居形式なのは導入だけ」2026-10-18、[決めたこと](decisions.md#q2)）。初心者支部では2部の冒頭で、クリックで2つ目の言い切りを出した（2026-10-29）
- **部品**: 前置きは [小声](parts.md#part-kogoe)、言い切りのキーワードは [強調](parts.md#part-strong)
- **写真**: 前置き＋言い切り（jaws-sonic-2026 p.4、bgnr-93 p.23、zero-drift p.21）、言い切りだけ（continuum p.4 宣言、failed-ecs p.3 困りごと、zero-drift p.3 問いかけ、cdk-3min p.4 宣言）

<!-- shots:page-kamishibai -->

## page-story ストーリー型

- **何の型か**: 画面（図やスクショ）に、話し言葉の字幕帯を付けて物語を進める（初心者支部、2026-10-28。本人「ストーリー型のテンプレートとしてありかも」）。紙芝居型とは別のもの（本人「それはストーリー型、紙芝居型とは違うよ」）
- **いつ使うか**: 導入のストーリーだけ。章扉より後では使わない（初心者支部、2026-10-29）
- **部品**: [字幕帯](parts.md#part-subtitle-band)
- **写真**: bgnr-93 p.5〜7

<!-- shots:page-story -->

## page-chapter 章扉

- **何の型か**: 章の名前だけを大きく置く1枚。紙芝居の形で「それでは／〜について解説していきます」と書くこともある（初心者支部、左寄せ、2026-10-29）
- **いつ使うか**: 章や部の始まり。特徴を並べる前のつなぎは Overlay ではなく章扉（初心者支部、2026-10-28）。宣伝の前にも「宣伝」の章扉（茨城 #17）
- **写真**: bgnr-93 p.11、cdk-day1 p.11、ecr-sbom p.7、jaws-sonic-2026 p.8、zero-drift p.23

<!-- shots:page-chapter -->

## page-what-is-list 「〜とは？」（リストアップ型）

- **何の型か**: アイコン付きの見出し「Xとは？」、定義のリード1文、その下に箇条書き（茨城 #17「リストアップ型（Markdown の箇条書き＋Kogoe の補足）」）
- **いつ使うか**: サービスや用語を初めて出すとき。役割を先に言い、解説はその直後に置く（コンテナ支部、2026-11-15）
- **部品**: [アイコン付きの見出し](parts.md#part-icon-heading)、[小声](parts.md#part-kogoe)、[出典のリンク](parts.md#part-bottomlink)
- **写真**: ecr-sbom p.8、lt-40 p.6

<!-- shots:page-what-is-list -->

## page-what-is-figure 「〜とは？」（図示型）

- **何の型か**: 見出し「Xとは？」、定義のリード1文、その下にアイコンと矢印で流れを描く（茨城 #17「図示型（アイコンと矢印で流れを描く。e.g. AWS CDKとは？）」）
- **いつ使うか**: 仕組みが流れで説明できるもの。アイコンを並べたカードで特徴を見せるのは本人の書き方ではない（2026-10-18）
- **部品・土台**: [アイコン付きの見出し](parts.md#part-icon-heading)、[図のスタイル](foundation.md#base-diagram)
- **写真**: continuum p.3、zero-drift p.4

<!-- shots:page-what-is-figure -->

## page-definition-reuse 定義の使い回し

- **何の型か**: 同じ公式の定義のページを何度も出し、毎回その回の話に関わる部分だけをハイライト・ピックアップ・取り消し線などで強調する（SKILL.md）
- **いつ使うか**: 1つの定義を軸に話すとき。章の区切りで定義に戻る（本人「今回のスライドで新しく出てきたのは、CDKの定義を使いまわすところやな」）
- **部品**: [Overlay](parts.md#part-overlay)、[出典のリンク](parts.md#part-bottomlink)
- **写真**: cdkd-talk p.3、p.7、p.12、p.21

<!-- shots:page-definition-reuse -->

## page-one-by-one 特徴・理由を1つずつ

- **何の型か**: 小さい前置き（「IaCの特徴 ①」）＋短い名詞句の見出し＋主語のあるリード1文＋図1枚、必要なら「→」の1行。`view-transition` でつなぐ（SKILL.md。本人「めっちゃよくなった」）
- **いつ使うか**: 特徴や理由をいくつか順に見せるとき。題名だけを並べた一覧ページは作らない（LT #40「特徴のところで題名並べるだけなんてしたことない」、初心者支部 2026-10-29）
- **部品**: [小声](parts.md#part-kogoe)（前置き）、[「→」の1行](parts.md#part-arrow-conclusion)
- **写真**: bgnr-93 p.18
- **写真の注記**: この写真は `@slides/ui` の InlineSvg の不具合で、図のアイコンが大きく崩れて写っている。見出し・リード・図の配置だけを見る。崩れないデッキに同じ型のページが無いため、差し替えていない

<!-- shots:page-one-by-one -->

## page-list-conclusion 箇条書き＋結論

- **何の型か**: 見出し、左端に点が出る箇条書き（茨城 #17「リストは左端に点が出る書き方にする」）、補足は薄い小さい文字、最後に「→」の1行
- **いつ使うか**: 問題点や手段をいくつか並べて、1つの結論につなぐとき
- **部品**: [小声](parts.md#part-kogoe)、[「→」の1行](parts.md#part-arrow-conclusion)
- **写真**: bgnr-93 p.10、continuum p.11

<!-- shots:page-list-conclusion -->

## page-figure-conclusion 図＋結論

- **何の型か**: アイコン付きの見出し、図1枚（またはグラフ）、下に「→」の1行
- **いつ使うか**: 構成や測った結果を見せて、そこから言えることを結ぶとき
- **部品・土台**: [「→」の1行](parts.md#part-arrow-conclusion)、[図のスタイル](foundation.md#base-diagram)
- **写真**: failed-ecs p.5、p.7、lt-40 p.13

<!-- shots:page-figure-conclusion -->

## page-compare 2つを並べて比べる

- **何の型か**: 2枚のカードを左右に並べ、行ごとに対比する
- **いつ使うか**: 2つの方法やサービスの違い・使い分けを見せるとき（LT #40「Event Functions と MicroVMs の違い」、初心者支部のツール紹介は「LT #40 と同じ、2枚のカード」2026-10-28）。茨城 #17 の使い分けのページは発表後に「いちばん強い」とされた（2026-10-01）
- **部品**: [色分けした下線](parts.md#part-underline)（使うかはデッキごと）
- **写真**: bgnr-93 p.14、continuum p.20、lt-40 p.7

<!-- shots:page-compare -->

## page-onayami お悩み → 解決

- **何の型か**: 1枚目に聞く人のお悩みを大きく書き「というお悩みを解決します」と小声で添え、2枚目に解決策を言い切る
- **いつ使うか**: プラクティスや解決策を1つずつ紹介するとき（cdk-day1 の5つのプラクティス）。life に記録はなく、デッキから拾った型（[決めたこと](decisions.md#q5)）
- **部品**: [小声](parts.md#part-kogoe)、[Overlay](parts.md#part-overlay)
- **写真**: cdk-day1 p.12、p.13

<!-- shots:page-onayami -->

## page-qa Q&A

- **何の型か**: 「Q.」の問いと「A.」の答えを大きく並べる。A は赤
- **いつ使うか**: 聞く人が持ちそうな疑問に答えるとき。小さい文字を使わない（初心者支部「Qの前置きも同じ大きさ」2026-10-29）
- **写真**: bgnr-93 p.30、jaws-sonic-2026 p.5、lt-40 p.11

<!-- shots:page-qa -->

## page-summary-statement まとめ（言い切り）

- **何の型か**: 小さく「まとめ」、その下にこの資料で話したことを言い切る1文（コンテナ支部「本人の他のデッキのまとめと同じ型（例: SBOMの発表の『横断で検索する仕組みを作ると影響調査が爆速で終わる！！！』）」2026-11-15）
- **いつ使うか**: 話の芯が1つのデッキの締め
- **部品**: [小声](parts.md#part-kogoe)（「まとめ」）、[強調](parts.md#part-strong)
- **写真**: continuum p.21、ecr-sbom p.13、jaws-sonic-2026 p.34

<!-- shots:page-summary-statement -->

## page-summary-list まとめ（箇条書き）

- **何の型か**: 見出し「まとめ」と、話したことの箇条書き
- **いつ使うか**: 部がいくつかあるデッキの締め（初心者支部「締めのまとめは3部に対応する3行で出す」）。話したこと全体をまとめるだけにして、新しい宣言は足さない（自由が丘.any、2026-11-10）
- **写真**: bgnr-93 p.32、failed-ecs p.13、lt-40 p.17、zero-drift p.37

<!-- shots:page-summary-list -->

## page-promo 宣伝

- **何の型か**: 章扉「宣伝」のあとに、イベントや会社の告知
- **いつ使うか**: まとめと Thank You の間（茨城 #17 で「宣伝」の章扉を足した、2026-09-28）
- **写真**: aws-oss p.14、continuum p.22

<!-- shots:page-promo -->

## page-thanks Thank You

- **何の型か**: 青のグラデーションに「Thank You!」と「＼ ご清聴ありがとうございました！ ／」、右下にアイキャッチ
- **いつ使うか**: 最後の1枚。それ以外は書かない（茨城 #17「いつもどおり」、aws-oss の形、2026-09-28）
- **写真**: aws-oss p.16、ecr-sbom p.18

<!-- shots:page-thanks -->
