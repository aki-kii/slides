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

<div class="kari">仮：入れるかは未定</div>

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK">

- JAWS-UG CDK支部
- AWS Community Builders<br><span style="font-size:0.7em">Dev Tools, 2026〜</span>

</ProfileItem>

<!--
仮: 初心者支部で登壇したスライドと同じ中身。入れるかは未決。
-->

---
chapter: 導入
transition: fade
---

<ChapterLabel />

## AWS CDKとは？

<div class="official-quote mt-5">
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

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
AWS CloudFormation を通じて<em>プロビジョニングするための、</em><br>
オープンソースの<em>ソフトウェア開発フレームワークです</em>。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<div v-click class="reveal-line mt-3">→ これはIaCのことを説明しています！</div>

<!--
根拠 10-30 01:45。抜き出しの文は 10-31 12:00 の形で、下の一文と合わせてこの 1 枚にまとめた（12:46）。「AWS CloudFormation を通じて」はここでは強調しない（12:02）。
-->

---
chapter: IaC
transition: fade
---

<ChapterLabel />

## IaC（Infrastructure as Code）とは？

<div class="iac-sentence mt-3"><span class="accent">コード</span>で<span class="accent">インフラストラクチャ</span>を<span class="accent">定義</span>し、<br><span class="accent">プロビジョニング</span>するための<span class="accent">ソフトウェア開発フレームワーク</span></div>

<InlineSvg src="iac-define.svg" label="コードでインフラストラクチャを定義し、IaCのツールがそれを読んで実際のインフラストラクチャをプロビジョニングする" class="mx-auto mt-5 fig-iac-define" />


<!--
2026-11-03 01:52 本人: 前の「定義する → 何を？」「宣言型のデプロイ」「プロビジョニングする → どうやって？」の 3 枚をこの 2 枚に置き換えた。文を図解する。図は iac-diff と同じ部品（diagrams/iac_define.py）。
-->

---
chapter: IaC
---

<ChapterLabel />

## IaCのデプロイの仕組み

<div class="text-lg mt-1"><span class="accent font-bold">あるべき姿</span>をコードで定義し、<span class="replaced">現在の状態との差分</span>をデプロイする</div>

<InlineSvg src="iac-diff-ideal.svg" label="IaCのツールが、コードのあるべき姿と現在の状態を比較し、その差分だけを実リソースへデプロイする。コード（あるべき姿）の枠を強調している" class="mx-auto mt-4 fig-iac" />

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

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
<span v-click="1" class="cfn-red">AWS CloudFormation を通じて</span><em>プロビジョニングするための、</em><br>
オープンソースの<em>ソフトウェア開発フレームワークです</em>。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<div v-click="2" class="reveal-question mt-3">CloudFormationとの関わりを見ていきます</div>

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

<div class="iac-sentence mt-3 not-own"><span class="accent">CloudFormationテンプレート</span>であるべき姿を定義し、<br><span class="accent">スタック</span>としてまとめてプロビジョニングする</div>

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

<InlineSvg src="cfn-deploy.svg" label="CloudFormationが新しいテンプレートとスタックの現在の状態を比較し、差分の変更セットをスタックの実リソースへ反映する" class="mx-auto mt-3 fig-iac" />

<div class="arrow-note">→ <span class="not-own">テンプレートとスタックの状態を比べて変更セットを作り、スタックに反映する</span></div>

<!--
2026-11-03 本人「CloudFormationのデプロイも説明しよう。CloudFormationのデプロイってタイトルにしようね」。round 5 で、図を「IaCのデプロイの仕組み」と同じ形にしてリソース（AWS WAF、ALB、Amazon ECS）も描いた（diagrams/iac_variants.py）。
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

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
<span class="cfn-red">AWS CloudFormation を通じて</span><em>プロビジョニングするための、</em><br>
オープンソースの<em>ソフトウェア開発フレームワークです</em>。

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

<InlineSvg src="deploy-flow.svg" label="synth、publish、deploy の順に進む cdk deploy の枠。deploy は CloudFormation のアイコンだけで表す" class="mx-auto fig-flow" />

<div class="arrow-note">→ <span class="not-own">cdk deployの中でsynth、publish、deployが順に動く</span></div>

<!--
全体を先に見せる。ここから同じ図の一部を順に強調する。cdk deploy が全体を順に動かす。根拠 10-30 16:06、10-31 09:22。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## synth

<InlineSvg src="deploy-flow-synth.svg" label="synth の枠を強調した図" class="mx-auto fig-flow" />

<div class="arrow-note">→ ソースコードから合成して、アセットを作る</div>

<!--
synth は合成（シンセサイズ）。「ビルド」とは書かない。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## パブリッシュ

<InlineSvg src="deploy-flow-publish.svg" label="テンプレートとファイルを S3 バケットへ、コンテナイメージを ECR リポジトリへパブリッシュする部分を強調した図" class="mx-auto fig-flow" />

<div class="arrow-note">→ <span class="not-own">テンプレートとファイルはS3バケットへ、コンテナイメージはECRリポジトリへ</span></div>

<!--
*.assets.json の一覧で確かめた。テンプレートも S3 へ上げるファイルとして載っている。コンテナイメージは synth では作らず、ここでビルドして push する。
-->

---
chapter: デプロイフロー
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## デプロイ

<InlineSvg src="deploy-flow-deploy.svg" label="deploy の部分を強調した図。CloudFormation でデプロイする" class="mx-auto fig-flow" />

<div class="arrow-note">→ <span class="not-own">パブリッシュしたテンプレートを使って、CloudFormationのデプロイをする</span></div>

<!--
2026-11-03 本人「CDKのデプロイ、図はCloudFormationのデプロイは前に紹介してるから省略形にする」。変更セットとスタックの説明は「CloudFormationのデプロイ」のページへ移したので、デプロイの 2 枚を 1 枚にした。
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

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コード</em>でクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースの<em>ソフトウェア開発フレームワーク</em>です。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
全文からハイライトして抜き出す（10-31 12:04、12:52）。「で」と「オープンソースの」は含めない。
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

AWS Cloud Development Kit (AWS CDK) は、<br>
<s class="struck">コード</s><span class="replaced">プログラミング言語</span>でクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースの<em>ソフトウェア開発フレームワーク</em>です。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
公式の「コード」を取り消し線で残し、直後に「プログラミング言語」を赤で見せる（10-30 16:15、10-31 12:52、13:16）。注記は付けない。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：中身は本人が決める</div></div>

## <span class="not-own">プログラミング言語だと何がうれしい？</span>

<!--
仮: 中身は本人がまだ決めていない（10-31 12:52）。本文は書いていない。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：コードの例は仮</div></div>

## <span class="not-own">数の分だけ用意できる</span>

```ts
const stages = ['dev', 'stg', 'prod'];

for (const stage of stages) {
  new ApiStack(app, `Api-${stage}`);
}
```

<div class="arrow-note">→ <span class="not-own">指定した個数ではなく、何かの数の分だけ何かを用意する処理が書ける</span></div>

<!--
仮: コードの例は仮。根拠 10-31 12:54。CloudFormation にも Fn::ForEach はあるので「できない」とは言わない。
https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：コードの例は仮</div></div>

## <span class="not-own">環境によって作らない</span>

```ts
if (stage !== 'dev') {
  new MonitoringStack(app, 'Monitoring');
}
```

<div class="arrow-note">→ 環境によって、このリソースは作らないと指定できる</div>

<!--
仮: コードの例は仮。根拠 10-31 12:54。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari">仮：入れるかは未定</div>

## カスタムリソース

<div class="text-2xl mt-16 text-center font-bold">プログラムで実際に何かを作る処理ができる</div>

<!--
仮: 10-31 09:39 で本人は迷い中。仕組みの説明は消した（12:54）。もとは CloudFormation の機能で、テンプレートだけでも使える。
https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## コンストラクト

<ul class="construct-points">
  <li>1つ以上のAWSリソースの設定が定義されているコンポーネント</li>
  <li>リソースの抽象度によってレベル分けがされている</li>
</ul>

<InlineSvg src="construct-levels.svg" label="抽象度が小さい順に L1、L2、L3 の Construct と、それぞれが作るリソース" class="mx-auto fig-construct" />

<!--
本人の旧資料「AWS CDKの推しポイントN選」の推しポイント⑦ Constructの 18 枚目（10-31 13:12）。この章の主役（10-31 09:39）。https://speakerdeck.com/akihisaikeda/aws-cdknotui-sipointonxuan
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## L1 Construct（抽象度：小）

<ul class="construct-points">
  <li>リソースのプロパティがCloudFormationのプロパティと1:1で対応している</li>
</ul>

<InlineSvg src="construct-l1.svg" label="CloudFormation テンプレートと CfnBucket のコードが 1:1 で対応している図" class="mx-auto fig-construct" />

<!--
本人の旧資料「AWS CDKの推しポイントN選」の推しポイント⑦ Constructの 19 枚目。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## L2 Construct（抽象度：中）

<ul class="construct-points">
  <li>リソースのプロパティが扱いやすいように抽象化されている</li>
</ul>

<InlineSvg src="construct-l2.svg" label="Bucket のコードとテンプレートの対応、抽象化、KMS Key の自動作成の図" class="mx-auto fig-construct" />

<!--
本人の旧資料「AWS CDKの推しポイントN選」の推しポイント⑦ Constructの 20 枚目。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## L2 Construct

<InlineSvg src="construct-l2-examples.svg" label="VPC の例（ソースコード 15 行、テンプレート 266 行）と、Lambda 関数の例（実行ロール、IAM Policy、CloudWatch Logs が自動で作られる）" class="mx-auto fig-construct-wide" />

<!--
本人の旧資料「AWS CDKの推しポイントN選」の推しポイント⑦ Constructの 21、22 枚目を 1 枚にまとめた。VPC の図のサブネットなどのリソース一覧は省いた。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## 自作Construct

<ul class="construct-points">
  <li>L1やL2などのConstructを組み合わせて自作のConstructを定義できる</li>
  <li>自作Constructも他の自作Constructに組み込める</li>
</ul>

<InlineSvg src="construct-custom.svg" label="MyConstruct のコードから S3 バケットと Lambda 関数が作られる図" class="mx-auto fig-construct" />

<!--
本人の旧資料「AWS CDKの推しポイントN選」の推しポイント⑦ Constructの 23 枚目。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div></div>

## <span class="not-own">アプリもスタックもコンストラクト</span>

<div class="nest-app mt-4">
  <div class="nest-title">アプリ</div>
  <div class="nest-stack">
    <div class="nest-title ink">スタック</div>
    <div class="nest-row">
      <div>コンストラクト</div>
      <div>コンストラクト</div>
      <div>コンストラクト</div>
    </div>
  </div>
</div>

<!--
スタックとアプリはコンストラクトの説明の中で触れる（10-31 09:39）。
https://docs.aws.amazon.com/cdk/v2/guide/apps.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：口頭で話す1〜2個は未定</div></div>

## 好きなCDKコンストラクト

<div class="rows mt-4">
  <div class="row-icon"><img src="/images/icons/ecr.svg" alt="Amazon ECR" /><div><p class="row-head"><b>DockerImageAsset</b><code>aws-cdk-lib/aws-ecr-assets</code></p><span class="not-own">コンテナイメージをビルドして、CDK ToolkitのECRリポジトリに置く</span></div></div>
  <div class="row-icon"><img src="/images/icons/s3.svg" alt="Amazon S3" /><div><p class="row-head"><b>BucketDeployment</b><code>aws-cdk-lib/aws-s3-deployment</code></p><span class="not-own">静的サイトのデプロイをいい感じにして、CloudFrontのキャッシュの無効化までしてくれる</span></div></div>
  <div class="row-icon"><img src="/images/icons/ec2.svg" alt="Amazon EC2" /><div><p class="row-head"><b>NatProvider.instanceV2</b><code>aws-cdk-lib/aws-ec2</code></p><span class="not-own">NATゲートウェイの代わりに、NATインスタンスを構築する</span></div></div>
  <div class="row-icon"><img src="/images/icons/codebuild.svg" alt="AWS CodeBuild" /><div><p class="row-head"><b>@cdklabs/deploy-time-build</b><code>cdklabs</code></p><span class="not-own">デプロイのときにビルドを走らせる（フロントエンドの静的ファイル、コンテナイメージなど）</span></div></div>
</div>

<!--
仮: 口頭で話す 1〜2 個は未定。
BucketDeployment は本人のメモの「S3Deployment」の正式な名前。
NAT は aws-cdk-lib の NatProvider.instanceV2（クラスは NatInstanceProviderV2）で、本人のイメージと合っている（10-31 13:07）。NAT インスタンスは EC2 インスタンスなので EC2 のアイコンにした。
deploy-time-build はもとは tmokmss さんの個人の OSS で、今は cdklabs に移っている（@cdklabs/deploy-time-build）。
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

AWS Cloud Development Kit (AWS CDK) は、<br>
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

<div class="oss-flow mt-16">
  <div>AWS CDKはOSS</div>
  <span>→</span>
  <div>外からの<br>コントリビュートを<br>受け付けている</div>
  <span>→</span>
  <div class="accent-box">良いコンストラクトが<br>作られていく</div>
</div>

<!--
軽く流す（10-31 09:25）。
-->

---
chapter: オープンソース
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：口頭で話す3つは未定</div></div>

## 関連するOSS

<div class="rows oss-rows mt-2">
  <div><p class="row-head"><b>baseline-environment-on-aws（BLEA）</b><i>aws-samples</i></p><span class="not-own">安全なベースライン環境を作るCDKテンプレート</span></div>
  <div><p class="row-head"><b>cdk-nag</b><i>cdklabs</i></p><span class="not-own">ルールでCDKアプリを確かめる</span></div>
  <div><p class="row-head"><b>cdk8s</b><i>cdk8s-team</i></p><span class="not-own">Kubernetesのアプリをコードで定義する</span></div>
  <div><p class="row-head"><b>aws-solutions-constructs</b><em class="kari-inline">仮：入れるか確認中</em><i>awslabs</i></p><span class="not-own">検証済みの構成のコンストラクト集</span></div>
  <div><p class="row-head"><b>cdk-monitoring-constructs</b><em class="kari-inline">仮：入れるか確認中</em><i>cdklabs</i></p><span class="not-own">監視を簡単に作るコンストラクト集</span></div>
</div>

<!--
仮: スライドには全部載せ、口頭では 3 つくらいに絞る（10-30 01:05）。作成者は各リポジトリの持ち主を確かめた。AWS Solutions Constructs と cdk-monitoring-constructs は本人が話したか確認中（10-31 12:58）。
-->

---
chapter: オープンソース
---

<ChapterLabel />

<div class="kari-row"><div class="kari kari-not-own">仮：本人の言葉じゃない</div><div class="kari">仮：口頭で話す3つは未定</div></div>

## 関連するOSS

<div class="rows oss-rows mt-2">
  <div><p class="row-head"><b>cdkd</b><i>go-to-k</i></p><span class="not-own">CloudFormationを通さずAWS SDKを直接呼ぶCDK CLI</span></div>
  <div><p class="row-head"><b>cdk-real-drift</b><i>go-to-k</i></p><span class="not-own">テンプレートに書いていないプロパティまでドリフトを検出する</span></div>
  <div><p class="row-head"><b>awscdk-lint</b><i>ren-yamanashi</i></p><span class="not-own">CDK用のリントのプラグイン</span></div>
  <div><p class="row-head"><b>cdk-preflight</b><i>badmintoncryer</i></p><span class="not-own">デプロイ時の失敗をsynthの時点で見つける</span></div>
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

<div class="definition summary tight">

AWS Cloud Development Kit (AWS CDK) は、<br>
<s class="struck">コード</s><span class="replaced">プログラミング言語</span>で<em>クラウドインフラストラクチャを定義し、</em><br>
<em>AWS CloudFormation を通じてプロビジョニングするための、</em><br>
<em>オープンソースのソフトウェア開発フレームワーク</em>です。

</div>

<div class="official-source">出典：AWS CDK v2 デベロッパーガイド「AWS CDK とは」</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html" />

<!--
最後のまとめで定義をもう一度出す（10-31 13:21）。発表で取り上げた部分を全部ハイライトする。「コード」は 16 枚目と同じ差し替え。
-->

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
