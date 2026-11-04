---
layout: title
drawings:
  persist: false
transition: fade
title: AWS CDKを理解するために公式の定義を深掘って解説してみる
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="text-2xl font-normal opacity-90">JAWS-UG CDK支部 × 東京支部コラボ cdkdハンズオン</div>

# AWS CDKを理解するために<br>公式の定義を深掘って解説してみる

<div class="opacity-70">

2026.11.05（木）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

</div>

<div class="absolute right-8 bottom-8">
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

<!--
仮: 発表タイトルと肩書きの書き方は未決。
-->

---
layout: profile
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
transition: slide-left
---

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK">

- JAWS-UG CDK支部
- AWS Community Builders<br><span style="font-size:0.7em">Dev Tools, 2026〜</span>

</ProfileItem>

<!--
初心者支部で登壇したスライドと同じ中身。2026-11-04 本人: このまま入れる。
-->

---
chapter: 導入
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote compact mt-2">
<div class="official-label">AWS公式の定義</div>

<div class="definition">

AWS Cloud Development Kit (AWS CDK) は、<br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<Overlay clickStart=1>
  定義の一部を抜き出して深掘りしていきます
</Overlay>

<!--
公式の定義: https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html （根拠 10-30 01:30）
クリックで「定義の一部を抜き出して深掘りしていきます」を重ねる（2026-11-03 01:52 本人、文言は 11:xx の round 5）。
-->

---
chapter: IaC
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote compact mt-2">
<div class="official-label">AWS公式の定義</div>

<div class="definition faded">

<span class="def-subject">AWS Cloud Development Kit (AWS CDK) は、</span><br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
AWS CloudFormation を通じて<em>プロビジョニングする</em>ための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<Overlay clickStart=1>
  これはIaCのことを説明しています！
</Overlay>

<!--
根拠 10-30 01:45。抜き出しの文は 10-31 12:00 の形で、下の一文と合わせてこの 1 枚にまとめた（12:46）。「AWS CloudFormation を通じて」はここでは強調しない（12:02）。
-->

---
chapter: IaC
transition: fade
---

<ChapterLabel />

## IaC（Infrastructure as Code）とは？

<div class="mt-3" style="font-size: 1.25rem; font-weight: 700; white-space: nowrap">コードでクラウドインフラストラクチャを定義し、プロビジョニングする</div>

<InlineSvg src="iac-define.svg" label="コードでインフラストラクチャを定義し、IaCのツールがそれを読んでAWSアカウントにプロビジョニングする" class="mx-auto mt-5 fig-iac-define" />


<Overlay clickStart=1>
  もう少し詳しく見ていきます
</Overlay>

<!--
2026-11-03 01:52 本人: 前の「定義する → 何を？」「宣言型のデプロイ」「プロビジョニングする → どうやって？」の 3 枚をこの 2 枚に置き換えた。文を図解する。図は iac-diff と同じ部品（diagrams/iac_define.py）。
-->

---
chapter: IaC
---

<ChapterLabel />

## IaCの仕組み

<div class="mt-1" style="font-size: 1.05rem; white-space: nowrap">コードでインフラの<span class="replaced">あるべき姿</span>を定義し、<span class="replaced">現在の状態との差分</span>をプロビジョニングする</div>

<InlineSvg src="iac-diff-ideal.svg" label="IaCのツールが、コードのあるべき姿と更新前のAWSアカウントを比較し、その差分をプロビジョニングして更新後のAWSアカウントにする。コード（あるべき姿）の枠を強調している" class="mx-auto mt-4 fig-iac" />

<Overlay clickStart=1>
  あらためてCDKの定義（IaC部分）を確認します
</Overlay>

<!--
2026-11-03 本人（round 5）: 「宣言型のデプロイ手法」のページはカットし、「IaCのデプロイの仕組み」をそのまま書く。「あるべき姿」もハイライトする（文と左上の枠）。図は初心者支部で登壇したスライドの iac-diff に、あるべき姿の枠の強調を足したもの（diagrams/iac_variants.py）。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote compact mt-2">
<div class="official-label">AWS公式の定義</div>

<div class="definition faded">

<span class="def-subject">AWS Cloud Development Kit (AWS CDK) は、</span><br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
<span v-click="1" class="cfn-red">AWS CloudFormation を通じて</span><em>プロビジョニングする</em>ための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<Overlay clickStart=2>
  → CloudFormationについて説明していきます！
</Overlay>

<!--
2026-11-03 本人「CloudFormationを通じてを書く時はp5の状態から赤文字でCloudFormationを通じてを強調するって意味。定義で使ってない部分を省略しないでね」。IaC の抜き出しのページと同じ状態から、クリックで「AWS CloudFormation を通じて」を赤にする。問いかけは 10-30 15:59。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## AWS CloudFormationとは？

<div class="mt-3" style="font-size: 1.1rem; font-weight: 700; white-space: nowrap">コードでAWSリソースを定義し、AWSアカウントにプロビジョニングするサービス</div>

<InlineSvg src="cfn-define.svg" label="CloudFormationテンプレートであるべき姿を定義し、CloudFormationがそれを読んでスタックとしてリソースをプロビジョニングする" class="mx-auto mt-5 fig-iac-define" />

<!--
2026-11-03 本人（round 5）: 「CloudFormationのデプロイ」の前に CloudFormation の説明を足す。「IaCとは？」の図を CloudFormation 版にし、テンプレートとスタックを図に入れる。上の文はエージェントが書いた。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## CloudFormationのデプロイ

<div class="text-lg mt-1 cfn-lead"><span class="u-tpl">CloudFormationテンプレート</span>でAWSリソースのあるべき姿を定義し、<br><span class="u-stack">スタック</span>が持つ現在の状態との差分を<span class="u-cs">変更セット</span>として抽出し、<br>それを元にAWSアカウントにプロビジョニングする</div>

<InlineSvg src="cfn-deploy.svg" label="CloudFormationが新しいテンプレートとスタックの現在の状態を比較し、差分の変更セットをスタックの実リソースへ反映する" class="mx-auto mt-6 fig-cfn-deploy" />

<!--
2026-11-03 本人「CloudFormationのデプロイも説明しよう。CloudFormationのデプロイってタイトルにしようね」。round 5 で、図を「IaCのデプロイの仕組み」と同じ形にしてリソース（2026-11-04 から API Gateway、Lambda、DynamoDB）も描いた（diagrams/iac_variants.py）。
公式は「スタックと、送った変更を比べる」。実際のリソースまで比べるのは drift-aware change set（cdk deploy --revert-drift）のとき。
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html
ロールバックと承認ゲートは扱わない。リソースの話はこの章でする（10-31 09:39）。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote compact mt-2">
<div class="official-label">AWS公式の定義</div>

<div class="definition faded">

<span class="def-subject">AWS Cloud Development Kit (AWS CDK) は、</span><br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
<span class="cfn-red">AWS CloudFormation を通じて</span><em>プロビジョニングする</em>ための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<Overlay clickStart=1>
  CloudFormationを“通じて”
</Overlay>

<!--
2026-11-03 本人（round 5）: CDK のデプロイの前に、もう一度 CDK の定義に戻る。IaC に当たる部分（緑）と「AWS CloudFormation を通じて」（赤）を出したうえで、「CloudFormationを“通じて”」を重ねる。CDK のデプロイのページにあった「CDKはCloudFormationを通じてデプロイしている」は、これと重なるので外した。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## CDKのデプロイ

<div class="text-lg mt-2"><code>cdk deploy</code>はCloudFormationを通じてデプロイしている</div>

<InlineSvg src="deploy-flow.svg" label="synth、publish、deploy の順に進む cdk deploy の枠。deploy は CloudFormation のアイコンだけで表す" class="mx-auto fig-flow" />


<div class="source-note" style="bottom: 0.7rem">※ bootstrapと書いてあるものはcdk bootstrapによって作られたリソースです</div>

<!--
全体を先に見せる。ここから同じ図の一部を順に強調する。cdk deploy が全体を順に動かす。根拠 10-30 16:06、10-31 09:22。
-->

---
chapter: プログラミング言語とフレームワーク
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote mt-5">
<div class="official-label">AWS公式の定義</div>

<div class="definition tight">

AWS Cloud Development Kit (AWS CDK) は、<br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
2026-11-03 本人（round 6）: CDK のデプロイフローのあとは、まず定義の全文をそのまま見せる（ピックアップなし）。
-->

---
chapter: プログラミング言語とフレームワーク
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote mt-5">
<div class="official-label">AWS公式の定義</div>

<div class="definition faded tight">

<span class="def-subject">AWS Cloud Development Kit (AWS CDK) は、</span><br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースの<em>ソフトウェア開発フレームワークです</em>。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<Overlay clickStart=1>
  フレームワーク「AWS CDK」としての特徴を説明します！
</Overlay>

<!--
2026-11-04 本人（round 19）: 見出しだけのページ「ソフトウェア開発フレームワーク「AWS CDK」の特徴」はやめ、ここにオーバーレイ「フレームワーク「AWS CDK」としての特徴を説明します！」を出す。このあと ①〜③ を view-transition でつなぐ。round 17: この章のピックアップは「ソフトウェア開発フレームワークです」だけにする。「（プログラミング言語で）クラウドインフラストラクチャを定義し」は拾わない。取り消し線のページはやめ、プログラミング言語の話は特徴 ① にした。定義の全文はどのページでも同じ。
-->

---
chapter: プログラミング言語とフレームワーク
transition: view-transition
---

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：コードの例は仮</div></div>

<div style="view-transition-name: cdk-benefit">
  <span class="not-own">CDKの特徴①</span>
  <h2>プログラミング言語で書ける</h2>
</div>

<div class="text-lg mt-2">TypeScriptなどの使い慣れたプログラミング言語でAWSリソースを定義できます</div>

<div class="text-base mt-1">（TypeScript / JavaScript / Python / Java / C# / Go など…）</div>

<div class="code-narrow mt-3">

```ts
const fn = new NodejsFunction(this, 'Function', {
  entry: 'lambda/index.ts',
  handler: 'handler',
  runtime: Runtime.NODEJS_22_X,
  memorySize: 512,
  timeout: Duration.seconds(30),
  environment: { TABLE_NAME: table.tableName },
});
```

</div>

<div v-click class="mt-3">
  <div style="font-size: 0.9rem; white-space: nowrap">ただし、AIが書くのでプログラミング言語で書けることが直接的にはメリットになりづらくなってきました</div>
  <div class="text-lg mt-1">→ AI時代でもCDKのメリットとなる特徴を紹介します！</div>
</div>

<!--
2026-11-04 本人（round 17）: 特徴の ① を「プログラミング言語で書ける」にし、前の ①② を ②③ にずらした。round 20: リードと最後の一文は本人の文。コードの例は NodejsFunction（エージェントが書いた）。対応している言語は https://docs.aws.amazon.com/cdk/v2/guide/languages.html
-->

---
chapter: プログラミング言語とフレームワーク
transition: view-transition
---

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

<div style="view-transition-name: cdk-benefit">
  <span class="not-own">CDKの特徴②</span>
  <h2>インフラの設定を抽象化している</h2>
</div>

<div class="text-lg mt-2">適切な抽象化により少ない実装で意図を伝えられる</div>

<InlineSvg src="benefit-abstract.svg" label="AWS CDKのコード myBucket.grantRead(myFunction) の1行で、Lambda関数の実行ロールにS3バケットを読み取るIAMポリシーが付く。CloudFormationテンプレートでは読み取りの権限を並べたIAMポリシーになる" class="mx-auto mt-2 fig-benefit-wide" />

<div class="text-base mt-1">
  <div>AIにとって読みやすく</div>
  <div>→ 人間にもAIにも設定の意図が伝わりやすい</div>
</div>

<!--
2026-11-03 本人（round 8〜9）: 例は bucket.grants.write(taskRole) か myBucket.grantRead(myFunction)。よく知られている grantRead にした。右は grantRead が作るポリシーの中身を抜き出したもの。図は diagrams/benefit_abstract.py。2026-11-04 本人（round 20）: ぼやけて見えるので文字を大きくして縮めずに出し、作られるリソースを図にした。
-->

---
chapter: プログラミング言語とフレームワーク
---

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

<div style="view-transition-name: cdk-benefit">
  <span class="not-own">CDKの特徴③</span>
  <h2>デプロイ前の検証手段が豊富</h2>
</div>

<div class="text-lg mt-2 not-own">AIが書いたコードを、デプロイする前にAI自身が検証して直せる</div>

<InlineSvg src="ai-validation.svg" label="AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする" class="mx-auto mt-4 fig-benefit" />

<BottomLink href="https://speakerdeck.com/akihisaikeda/cdk-deploy-jawssonic-marathon-shi-nagara-aws-risosu-o-shi-te-miyou" title="検証しながらデプロイする話は「cdk deploy JawsSonic #MARATHONしながらAWSリソースをデプロイしてみよう」で" />

<!--
2026-11-03 本人（round 8〜9）: 検証手段は Linter、型チェック、単体テスト、cdk synth、cdk diff、cdk validate など。図は初心者支部で登壇したスライドの「IaCがAIに向いている理由 ②」の ai-validation.svg をそのまま使った（検証の下に「lint・validateなど」）。
-->

---
chapter: オープンソース
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote mt-5">
<div class="official-label">AWS公式の定義</div>

<div class="definition faded">

<span class="def-subject">AWS Cloud Development Kit (AWS CDK) は、</span><br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
<em>オープンソースの</em>ソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
全文から一部をハイライトして抜き出す（10-31 12:04）。
-->

---
chapter: オープンソース
---

<ChapterLabel />

## AWS CDKはOSS

<div class="oss-grid mt-4">
<div class="oss-text">
  <div class="oss-sec">OSSとは？</div>
  <p>誰でも使える・読める・直せるソフトウェア</p>
  <div class="oss-sec">CDKはAWSだけで作っているわけじゃない</div>
  <ul>
    <li>AWSの社員でなくても、誰でも機能追加やバグ修正ができる</li>
    <li>コミットの約半分はコミュニティから</li>
    <li>必要なのは高度なコードより、AWSの知識</li>
  </ul>
  <div v-click="1" class="oss-mine">
    <p class="accent">僕のコードも入っています！</p>
  </div>
</div>
<div v-click="1" class="oss-shot">
  <a class="pr-shot" href="https://github.com/aws/aws-cdk/pull/35328" target="_blank" rel="noopener"><img src="/images/pr-35328.png" alt="aws/aws-cdk のプルリクエスト #35328「feat(appsync): add EnhancedMetricsConfigProperty for GraphQL api」。Merged。aki-kii のコメントと説明の冒頭" /></a>
  <div class="oss-pr"><a href="https://github.com/aws/aws-cdk/pull/35328" target="_blank" rel="noopener">aws/aws-cdk#35328</a></div>
</div>
</div>

<Overlay clickStart=2>
  → CDKの周りにもOSSが広がっています
</Overlay>

<!--
2026-11-04 本人（round 22）「OSSのページ図にするのは無理あるな。k.gotoさんの資料のように文字だけにするか」: 図をやめ、文字だけにした。round 23 で本人の文に差し替えた。「コミットの約半分はコミュニティから」は出典を確認中（CONTRIBUTING.md には数字が無く、community contributions significantly impact とだけある）。
2026-11-04 本人（round 24）: PR は https://github.com/aws/aws-cdk/pull/35328 （feat(appsync): add EnhancedMetricsConfigProperty for GraphQL api、2026-03-03 にマージ、作者 aki-kii）に決めた。画面は GitHub のページを headless Chromium（幅 520 のスマホくらいの幅、ライトテーマ）で撮って、タイトルから aki-kii のコメントと説明の冒頭までを切り抜いた（public/images/pr-35328.png）。round 25 で右に縦長に置いた。
-->

---
chapter: オープンソース
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：口頭で話す3つは未定</div></div>

<div style="view-transition-name: cdk-oss">
  関連するOSS ①
  <h2><span class="not-own">作るとデプロイを助けるOSS</span></h2>
</div>

<div class="text-lg mt-2 not-own">環境やリソースの定義と、デプロイの手間を減らすOSS</div>

<div class="rows oss-rows oss-compact mt-3">
  <div><p class="row-head"><b>baseline-environment-on-aws（BLEA）</b><i>aws-samples</i></p><span class="not-own">安全なベースライン環境を作るCDKテンプレート</span></div>
  <div><p class="row-head"><b>cdk8s</b><i>cdk8s-team</i></p><span class="not-own">Kubernetesのアプリをコードで定義する</span></div>
  <div><p class="row-head"><b>aws-solutions-constructs</b><em class="kari-inline">仮：入れるか確認中</em><i>awslabs</i></p><span class="not-own">検証済みの構成のコンストラクト集</span></div>
  <div><p class="row-head"><b>cdk-monitoring-constructs</b><em class="kari-inline">仮：入れるか確認中</em><i>cdklabs</i></p><span class="not-own">監視を簡単に作るコンストラクト集</span></div>
  <div><p class="row-head"><b>cdkd</b><i>go-to-k</i></p><span class="not-own">CloudFormationを通さずAWS SDKを直接呼ぶCDK CLI</span></div>
</div>

<!--
仮: スライドには全部載せ、口頭では 3 つくらいに絞る（10-30 01:05）。作成者は各リポジトリの持ち主を確かめた。AWS Solutions Constructs と cdk-monitoring-constructs は本人が話したか確認中（10-31 12:58）。
2026-11-03 本人（round 11）: 資料の型に合わせ、2枚を「関連するOSS ①②」の前置き＋見出し＋リードにした。分け方は出どころ（AWS か個人か）ではなく役割にした（10-31 12:58「日本・海外は分けない」）。見出しとリードはエージェントが書いた。
-->

---
chapter: オープンソース
transition: view-transition
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：口頭で話す3つは未定</div></div>

<div style="view-transition-name: cdk-oss">
  関連するOSS ②
  <h2><span class="not-own">確かめるのを助けるOSS</span></h2>
</div>

<div class="text-lg mt-2 not-own">デプロイの前と後で、CDKアプリやスタックを確かめるOSS</div>

<div class="rows oss-rows oss-compact mt-3">
  <div><p class="row-head"><b>cdk-nag</b><i>cdklabs</i></p><span class="not-own">ルールでCDKアプリを確かめる</span></div>
  <div><p class="row-head"><b>awscdk-lint</b><i>ren-yamanashi</i></p><span class="not-own">CDK用のリントのプラグイン</span></div>
  <div><p class="row-head"><b>cdk-preflight</b><i>badmintoncryer</i></p><span class="not-own">デプロイ時の失敗をsynthの時点で見つける</span></div>
  <div><p class="row-head"><b>cdk-real-drift</b><i>go-to-k</i></p><span class="not-own">テンプレートに書いていないプロパティまでドリフトを検出する</span></div>
  <div><p class="row-head"><b>cfn-exec-policy</b><i>badmintoncryer</i></p><span class="not-own">CloudFormation実行ロールを最小権限にする</span></div>
  <div><p class="row-head"><b>cfn-idle-cost</b><i>badmintoncryer</i></p><span class="not-own">アクセスがなくてもかかる月額を出す</span></div>
</div>

<!--
仮: 口頭で話す 3 つは未定。作成者は各リポジトリの持ち主を確かめた。
-->

---
chapter: まとめ
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote mt-5">
<div class="official-label">AWS公式の定義</div>

<div class="definition tight">

AWS Cloud Development Kit (AWS CDK) は、<br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
最後のまとめで定義をもう一度出す（10-31 13:21）。2026-11-04 本人: 強調も取り消し線も付けず、全文を黒のまま見せる。
-->

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
