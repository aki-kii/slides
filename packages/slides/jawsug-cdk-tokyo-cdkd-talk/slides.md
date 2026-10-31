---
layout: title
drawings:
  persist: false
transition: fade
title: AWS CDK とは？
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="kari">仮：発表タイトルは未定</div>

<div class="text-2xl font-normal opacity-90">JAWS-UG CDK支部 × 東京支部コラボ cdkdハンズオン</div>

# AWS CDK とは？

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
仮: #93 と同じ中身。入れるかは未決。
-->

---
chapter: 導入
transition: fade
---

<ChapterLabel />

## AWS CDK とは？

<div class="definition mt-8">

AWS Cloud Development Kit (AWS CDK) は、<br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースのソフトウェア開発フレームワークです。

</div>

<div class="source-note">AWS CDK v2 デベロッパーガイドより</div>

<!--
公式の定義: https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html （根拠 10-30 01:30）
-->

---
chapter: IaC
transition: fade
---

<ChapterLabel />

## AWS CDK とは？

<div class="definition mt-8 faded">

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コードでクラウドインフラストラクチャを定義し、</em><br>
AWS CloudFormation を通じて<em>プロビジョニングするための、</em><br>
オープンソースの<em>ソフトウェア開発フレームワークです</em>。

</div>

<!--
根拠 10-30 01:45。
-->

---
layout: center
class: text-center
chapter: IaC
transition: fade
---

<ChapterLabel />

<div class="definition">コードでクラウドインフラストラクチャを定義し、<br>プロビジョニングするための、<br>ソフトウェア開発フレームワークです。</div>

<div class="big-accent mt-10">IaC（Infrastructure as Code）の定義です！</div>

<!--
抜き出しは 10-31 12:00 の形。「AWS CloudFormation を通じて」はここには入れない（12:02）。
-->

---
layout: center
class: text-center
chapter: IaC
---

<ChapterLabel />

<div class="question">定義する → 何を？</div>

<div class="big-accent mt-4">あるべき姿を定義する</div>

<div class="pd-card pd-iac declarative mt-6">
<div class="pd-title">宣言型のデプロイ</div>
<ul>
  <li>リソースの「あるべき姿」を宣言するデプロイ方法</li>
  <li>作成・変更・削除の操作は書かず、最終的な設定だけを書く</li>
  <li>例：コードにメモリサイズと環境変数を書いてデプロイした</li>
</ul>
</div>

<!--
根拠 10-30 01:53、01:54、10-31 12:03。宣言型の説明はここで一緒にする。手続き型は話さない（01:50）。カードの文は #93 の本人の言葉（2026-10-29 16:45）。
-->

---
chapter: IaC
---

<ChapterLabel />

## プロビジョニングする → どうやって？

<div class="text-lg mt-2">あるべき姿との<span class="accent">差分をデプロイ</span>する</div>

<InlineSvg src="iac-diff.svg" label="IaCのツールが、コードのあるべき姿と現在の状態を比較し、その差分だけを実リソースへデプロイする" class="mx-auto mt-4 fig-iac" />

<!--
問いかけは 10-30 01:53。図は #93 の iac-diff を流用。
-->

---
chapter: IaC
---

<ChapterLabel />

<div class="kari">仮：置き場所は未定</div>

## IaC の特徴

<div class="feature-grid mt-10">
  <div>再現性の高さ</div>
  <div>変更管理ができること</div>
  <div>構造を把握しやすい</div>
  <div>再利用のしやすさ</div>
</div>

<!--
仮: タイトルだけを見せて、中身は話さない（10-30 01:11）。置き場所は未決。題は #93 のスライドから。
-->

---
layout: center
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="definition">

コードでクラウドインフラストラクチャを定義し、<br>
プロビジョニングするための、<br>
ソフトウェア開発フレームワークです。

</div>

<!--
前に抜き出した IaC の定義の文。次のページでこの文に「AWS CloudFormation を通じて」を足す（10-31 12:04）。ここだけ全文からは出さない。
-->

---
layout: center
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="definition">

コードでクラウドインフラストラクチャを定義し、<br>
<span class="accent font-bold">AWS CloudFormation を通じて</span>プロビジョニングするための、<br>
ソフトウェア開発フレームワークです。

</div>

<div class="question text-center mt-12">CDK は CloudFormation とどう関わってるの？</div>

<!--
デプロイフローの説明に入る直前で、定義文に「AWS CloudFormation を通じて」を足して見せる（10-31 09:22、12:02）。問いかけは 10-30 15:59。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## デプロイフロー

<InlineSvg src="deploy-flow.svg" label="CDK Bootstrap で先に作ったものを使い、synth、publish、deploy の順に進む流れ" class="mx-auto fig-flow" />

<div class="arrow-note">→ cdk deploy の中で synth、publish、deploy が順に動く</div>

<!--
全体を先に見せる。ここから同じ図の一部を順に強調する。根拠 10-30 16:06、10-31 09:22。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

<div class="kari">仮：bootstrap を話すかは未定</div>

## CDK Bootstrap

<InlineSvg src="deploy-flow-bootstrap.svg" label="CDK Bootstrap の枠を強調した図" class="mx-auto fig-flow" />

<div class="arrow-note">→ デプロイに使うものを先に作っておく</div>

<!--
仮: 下書きの案A（bootstrap を話す）の中身。今回の流れで使うものだけ並べ、ルックアップ用ロールや SSM パラメータはまとめた。
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

## アセット

<InlineSvg src="deploy-flow-assets.svg" label="アセットの枠を強調した図。テンプレートだけ赤で目立たせている" class="mx-auto fig-flow" />

<div class="arrow-note">→ テンプレートと、パブリッシュするものの元。いちばん大事なのはテンプレート</div>

<!--
cdk.out（公式の呼び名は cloud assembly）には manifest.json などもあるが、パブリッシュされないので図から外した。ファイルの大きさでは manifest.json のほうがテンプレートより大きいことがある。synth の時点では zip も Docker イメージも作られない。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## パブリッシュ

<InlineSvg src="deploy-flow-publish.svg" label="テンプレートとファイルを S3 バケットへ、コンテナイメージを ECR リポジトリへパブリッシュする部分を強調した図" class="mx-auto fig-flow" />

<div class="arrow-note">→ テンプレートとファイルは S3 バケットへ、コンテナイメージは ECR リポジトリへ</div>

<!--
*.assets.json の一覧で確かめた。テンプレートも S3 へ上げるファイルとして載っている。コンテナイメージは synth では作らず、ここでビルドして push する。
-->

---
chapter: デプロイフロー
transition: fade
---

<ChapterLabel />

## デプロイ

<InlineSvg src="deploy-flow-deploy.svg" label="新しいテンプレートとスタックの状態を比べて変更セットを作り、スタックに反映する部分を強調した図" class="mx-auto fig-flow" />

<div class="arrow-note">→ 新しいテンプレートとスタックの状態を比べる。実際のリソースを見に行くわけではない</div>

<!--
公式は「スタックと、送った変更を比べる」。実際のリソースまで比べるのは drift-aware change set（cdk deploy --revert-drift）のとき。
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html
ロールバックと承認ゲートは扱わない。
-->

---
chapter: デプロイフロー
---

<ChapterLabel />

## デプロイ

<InlineSvg src="deploy-flow-deploy.svg" label="変更セットを確認してスタックに反映する部分を強調した図。反映には CloudFormation 実行ロールを使う" class="mx-auto fig-flow" />

<div class="arrow-note">→ 変更セットを確認してスタックに反映すると、AWS リソースが作られる</div>

<!--
リソースの話はこの章でする（10-31 09:39）。
-->

---
chapter: プログラミング言語とフレームワーク
transition: fade
---

<ChapterLabel />

## AWS CDK とは？

<div class="definition mt-8 faded">

AWS Cloud Development Kit (AWS CDK) は、<br>
<em>コードで</em>クラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
オープンソースのソフトウェア開発<em>フレームワーク</em>です。

</div>

<!--
全文から一部をハイライトして抜き出す（10-31 12:04）。公式の文なので「コードで」のまま強調し、次のページで「プログラミング言語で」と見せる（10-30 16:15、16:16）。
-->

---
layout: center
class: text-center
chapter: プログラミング言語とフレームワーク
transition: fade
---

<ChapterLabel />

<div class="big-accent">プログラミング言語で</div>

<div class="big-accent mt-8">フレームワーク</div>

<div class="source-note">公式の定義では「コードで」</div>

<!--
定義文のこの 2 語だけを残す（10-30 16:16）。公式は「コードで」だが、スライドでは「プログラミング言語で」に書き換える（16:15）。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari">仮：コードの例は仮</div>

## ループとパラメータ化

```ts
const stages = ['dev', 'stg', 'prod'];

for (const stage of stages) {
  new ApiStack(app, `Api-${stage}`, {
    memorySize: memoryOf(stage),
  });
}
```

<div class="arrow-note">→ 同じものを環境の数だけ作り、違いは引数で渡す</div>

<!--
根拠 10-31 09:32。公式のベストプラクティスは、CloudFormation の Conditions や Parameters より、言語の機能で合成時に決めるよう勧めている。
CloudFormation にも Fn::ForEach はあるので「できない」とは言わない。使える値や操作は言語のほうがずっと多い、と言う。
https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari">仮：入れるかは未定</div>

## カスタムリソース

<div class="text-xl mt-4">CloudFormation にない操作を、デプロイのときに自分のコードで動かす</div>

<div class="pair-grid mt-8">
  <div><b>AwsCustomResource</b><span>API を 1 回呼ぶだけなら</span></div>
  <div><b>Provider framework</b><span>自分で処理を書くなら</span></div>
</div>

<div class="arrow-note">→ もとは CloudFormation の機能。CDK だと簡単に書ける</div>

<!--
仮: 10-31 09:39 で本人は迷い中。テンプレートだけでも使える機能なので、CDK の良さとして言うなら簡単に書ける点。
https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari">仮：足すかは確認待ち</div>

## AWS CDK のつくり

<div class="triple-grid mt-10">
  <div><b>Construct Library</b><span>AWS が用意した部品</span></div>
  <div><b>CDK CLI</b><span>cdk deploy などのコマンド</span></div>
  <div><b>6 つの言語</b><span>TypeScript、JavaScript、Python、Java、C#、Go</span></div>
</div>

<!--
仮: Construct Library、CDK CLI、多言語対応を足すかは確認待ち（10-31 09:41）。
https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/home.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## コンストラクト

<div class="levels mt-6">
  <div class="level l1"><b>L1</b><span>CloudFormation の<br>リソースそのまま</span><code>CfnBucket</code></div>
  <div class="level l2"><b>L2</b><span>安全な初期値つき</span><code>s3.Bucket</code></div>
  <div class="level l3"><b>L3</b><span>複数のリソースの<br>構成一式</span><code>ApplicationLoad<br>BalancedFargateService</code></div>
</div>

<div class="arrow-note">→ レベルが上がるほど抽象化も上がる</div>

<!--
この章の主役。抽象化はコンストラクトと 1 つの話（10-31 09:39）。
https://docs.aws.amazon.com/cdk/v2/guide/constructs.html
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

## アプリもスタックもコンストラクト

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

<div class="kari">仮：コードの例は仮</div>

## 条件分岐

```ts
if (stage === 'prod') {
  new MonitoringStack(app, 'Monitoring');
}
```

<div class="arrow-note">→ 環境ごとの違いを if でそのまま書ける</div>

<!--
仮: フレームワークとしての特徴として話す（10-31 09:32）。コードの例は仮。
-->

---
chapter: プログラミング言語とフレームワーク
---

<ChapterLabel />

<div class="kari">仮：口頭で話す 1〜2 個は未定</div>

## 好きな CDK コンストラクト

<div class="rows mt-4">
  <div><b>DockerImageAsset</b><span>ビルドしたコンテナイメージを CDK Toolkit の ECR リポジトリに置く</span></div>
  <div><b>S3Deployment</b><span>静的サイトのデプロイをいい感じにして、CloudFront のキャッシュの無効化までしてくれる</span></div>
  <div><b>NAT インスタンスのコンストラクト</b><span>NAT インスタンスを構築する</span></div>
  <div><b>DeployTimeBuild（個人の OSS）</b><span>tmokmss さんのコンストラクト</span></div>
</div>

<!--
仮: 10-30 16:29 では全部 AWS 公式としていたが、npm の deploy-time-build のリポジトリは tmokmss/deploy-time-build で、作者も tmokmss。残すかは本人が決める。
DockerImageAsset の説明は本人のメモより短くした。
-->

---
chapter: オープンソース
transition: fade
---

<ChapterLabel />

## AWS CDK とは？

<div class="definition mt-8 faded">

AWS Cloud Development Kit (AWS CDK) は、<br>
コードでクラウドインフラストラクチャを定義し、<br>
AWS CloudFormation を通じてプロビジョニングするための、<br>
<em>オープンソースの</em>ソフトウェア開発フレームワークです。

</div>

<!--
全文から一部をハイライトして抜き出す（10-31 12:04）。
-->

---
chapter: オープンソース
---

<ChapterLabel />

## AWS CDK は OSS

<div class="oss-flow mt-16">
  <div>AWS CDK は OSS</div>
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

<div class="kari">仮：口頭で話す 3 つは未定</div>

## 関連する OSS（公式側）

<div class="oss-list mt-2">
  <div><b>BLEA</b><span>安全なベースライン環境を作る CDK テンプレート</span></div>
  <div><b>cdk-nag</b><span>ルールで CDK アプリを確かめる</span></div>
  <div><b>jsii</b><span>CDK を TypeScript 以外の言語から使えるようにする</span></div>
  <div><b>cdk-from-cfn</b><span>CloudFormation テンプレートを CDK のコードに変換する</span></div>
  <div><b>cdk8s</b><span>Kubernetes のアプリをコードで定義する</span></div>
  <div><b>AWS Solutions Constructs</b><span>検証済みの構成のコンストラクト集</span></div>
  <div><b>cdk-monitoring-constructs</b><span>監視を簡単に作るコンストラクト集</span></div>
</div>

<!--
仮: スライドには全部載せ、口頭では 3 つくらいに絞る（10-30 01:05）。一覧は 10-30 16:24。説明は各リポジトリの説明から書いた。
-->

---
chapter: オープンソース
---

<ChapterLabel />

<div class="kari">仮：口頭で話す 3 つは未定</div>

## 関連する OSS（日本・海外）

<div class="oss-two mt-2">
<div>
<div class="oss-head">日本</div>
<div class="oss-list">
  <div><b>cdkd（後藤さん）</b><span>CloudFormation を通さず AWS SDK を直接呼ぶ CDK CLI</span></div>
  <div><b>cdk-real-drift（後藤さん）</b><span>テンプレートに書いていないプロパティまでドリフトを検出する</span></div>
  <div><b>awscdk-lint（山梨さん）</b><span>CDK 用のリントのプラグイン</span></div>
  <div><b>cdk-preflight（くらいやーさん）</b><span>デプロイ時の失敗を synth の時点で見つける</span></div>
  <div><b>cfn-exec-policy（くらいやーさん）</b><span>CloudFormation 実行ロールを最小権限にする</span></div>
  <div><b>cfn-idle-cost（くらいやーさん）</b><span>アクセスがなくてもかかる月額を出す</span></div>
</div>
</div>
<div>
<div class="oss-head">海外</div>
<div class="oss-list">
  <div><b>projen</b><span>プロジェクトの設定をコードで管理する</span></div>
  <div><b>cdk-dia</b><span>構成図を自動で作る</span></div>
  <div><b>awesome-cdk</b><span>CDK 関連の OSS や記事のまとめ</span></div>
</div>
</div>
</div>

<!--
仮: 一覧は 10-30 16:24。口頭で話す 3 つは未決。
-->

---
layout: center
class: text-center
chapter: 締め
---

<ChapterLabel />

<div class="kari">仮：締め方と渡し方は未定</div>

<div class="closing">ここからは後藤さんの cdkd へ</div>

<div class="text-xl mt-6 opacity-70">CloudFormation を通さず、AWS SDK を直接呼ぶ CDK CLI</div>

<!--
仮: ここは決まっていない。ブリーフの「締め=後藤さん cdkd へ渡す」をもとにした仮の文。
-->
