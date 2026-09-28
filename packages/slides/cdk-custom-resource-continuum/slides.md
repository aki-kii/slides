---
layout: title
drawings:
  persist: false
transition: slide-left
title: CDK のカスタムリソースで Continuum（旧 Security Agent）を実装した話
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

**JAWS-UG 茨城 #17 秋の推しAWSサービスLTまつり！**

<div class="text-xl font-bold opacity-90 mt-6">CloudFormation 未対応でも諦めない！</div>

# <span style="font-size: 0.72em; line-height: 1.4; display: inline-block">CDK のカスタムリソースで<br>Continuum（旧 Security Agent）を実装した話</span>

2026.9.30（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/public/images/aboutme/eye-catch.png" class="h-36" />
</div>

---
layout: profile
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
---

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ（2025.9〜）">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK">

- CDK Conference 2025 Speaker
- CDK Contributor (7PRs merged)

</ProfileItem>

::footer::

<img src="/images/aboutme/jawsug-cdk-logo.png" />
<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---
transition: view-transition
---

<div style="view-transition-name: cdk-icon" class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？</h2>
</div>

**プログラミング言語**で**AWS リソース**を定義する IaC フレームワーク

<div class="flex gap-4 items-center justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">プログラミング言語で<br>AWSリソースを定義</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">前回との差分を<br>デプロイ</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">AWSリソース</span>
</div>

</div>

<div class="absolute left-14 bottom-3" style="font-size: 0.7rem; color: #333333; line-height: 1; white-space: nowrap;">
  Special Thanks! Shota Kawasaki (<a href="https://x.com/kawaaaas" target="_blank" rel="noopener noreferrer" style="color: deepskyblue; text-decoration: none;">@kawaaaas</a>)
</div>

---
layout: center
---

<div>
  プロジェクトで
  <h2><strong>Continuum コードスキャニング</strong>を<br>導入したときの話をします</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuum コードスキャニングとは？</h2>
</div>

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">
  <div>Continuum（Security Agent が改名）の機能の1つ</div>
  <div><strong>AI エージェント</strong>がソースコードをスキャンして脆弱性を検出する機能</div>
  <div class="mt-3">フルリポジトリスキャン</div>
</div>

<InlineSvg src="code-scanning.svg" label="Continuum コードスキャニングがリポジトリ全体を読み、見つかった脆弱性と修正案をスキャン結果として出す図" class="mx-auto mt-1" style="width: 620px" />

<BottomLinks>
  <BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/05/aws-security-agent-full-repository-code-review/" title="AWS Security Agent now supports full repository code reviews" />
  <BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/06/aws-continuum/" title="Introducing AWS Continuum for security at machine speed" />
</BottomLinks>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuum コードスキャニングとは？</h2>
</div>

<div class="text-lg mt-2">リソース構成</div>

<InlineSvg src="continuum-code-review.svg" label="Integration が GitLab のアクセストークンで GitLab と接続し、AgentSpace の中の CodeReview が GitLab のリポジトリをスキャンする構成図。AgentSpace は CloudFormation 対応、Integration と CodeReview は CloudFormation 未対応" class="mx-auto mt-6" style="width: 800px" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？（再）</h2>
</div>

CDK は CloudFormation テンプレートを生成してデプロイする

<div class="flex gap-4 items-center justify-center mt-6">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">CDK のコード</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">CloudFormation<br>テンプレート</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">AWS リソース</span>
</div>

</div>

<div class="text-center text-xl mt-10">
  CloudFormation が対応していないリソースは<br><strong>CDK でも標準の方法では定義できない</strong>
</div>

---
layout: center
transition: view-transition
---

<div style="view-transition-name: cfn-unsupported">
  Continuum コードスキャニングを CDK で管理するため
  <h2><strong>カスタムリソース</strong>で定義しました！</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg">CloudFormation のライフサイクルに合わせて<strong>カスタムの処理を実行する</strong>仕組み</div>

<InlineSvg src="custom-resource-lifecycle.svg" label="Stack や Construct の作成・プロパティ変更・削除に応じて、カスタムリソースの中で CloudFormation のリソースから Lambda 関数へ Create・Update・Delete のイベントが届き、Lambda 関数が API を呼んで実行結果を S3 オブジェクトに書き込み、CloudFormation がその応答を待ち受ける図" class="mx-auto mt-2" style="width: 700px" />

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/template-custom-resources.html" title="カスタムリソースを使用してカスタムプロビジョニングロジックを作成する" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg mt-4">e.g. DynamoDB にマスターデータを投入するカスタムリソース</div>

<InlineSvg src="custom-resource-dynamodb.svg" label="カスタムリソースの Lambda 関数が、Create で DynamoDB テーブルにマスターデータを投入し、Update で変更されたレコードを更新し、Delete で投入したデータを削除する図" class="mx-auto mt-4" style="width: 780px" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg mt-4">e.g. S3 バケットを空にするカスタムリソース（autoDeleteObjects）</div>

<InlineSvg src="custom-resource-s3.svg" label="カスタムリソースの Lambda 関数が、Create と Update では何もせず、Delete で S3 バケットのオブジェクトを全て削除する図" class="mx-auto mt-4" style="width: 780px" />

---

## 何故そこまでして CDK で定義したかったの？

<br>

- CloudFormation のライフサイクルで管理できる
- 定義したリソースを複製しやすい
  - e.g. リポジトリごとに CodeReview を作れる
- 設定を設計意図と一緒にソースコードに残せる
  - マネコンで作ると設計意図は別途ドキュメントが必要

<div class="mt-8 opacity-70">
  <div style="font-size: 1rem">ほかにも</div>
  <ul class="!mt-1">
    <li style="font-size: 1.05rem">他のリソースと合わせて CDK で統一できる</li>
    <li style="font-size: 1.05rem">CloudFormation が対応したら L1 Construct に取り込みやすい</li>
  </ul>
</div>

---
layout: center
---

<div>
  <h2>Continuum コードスキャニングを<br>カスタムリソースを使って CDK で定義します</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0"><span style="font-size: 0.85em">Continuum コードスキャニングのリソース構成</span></h2>
</div>

<InlineSvg src="continuum-code-review.svg" label="Integration が GitLab のアクセストークンで GitLab と接続し、AgentSpace の中の CodeReview が GitLab のリポジトリをスキャンする構成図。AgentSpace は CloudFormation 対応、Integration と CodeReview は CloudFormation 未対応" class="mx-auto mt-6" style="width: 800px" />

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">CodeReview のポイント</h2>
</div>

<br>

- 連携したリポジトリをコードスキャンするためのリソース
- CloudFormation のイベントに対応した API が揃っている
  - Create: `CreateCodeReview`
  - Update: `UpdateCodeReview`
  - Delete: `BatchDeleteCodeReviews`

<div v-click class="mt-8 text-xl">
  → <strong>AwsCustomResource</strong> を利用する
</div>

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/APIReference/API_Operations.html" title="AWS Security Agent API Reference - Actions" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AwsCustomResource とは？</h2>
</div>

<br>

- CloudFormation イベントごとに AWS SDK を1つだけ呼べる
- 処理を書かずに、プロパティを渡すだけで済む
- 呼び出す AWS SDK から IAM ポリシーを自動で作れる

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html" title="class AwsCustomResource (construct) · AWS CDK" />

---

## CodeReview のための AwsCustomResource

<InlineSvg src="awscr-codereview.svg" label="AwsCustomResource のカスタムリソースで、Create に CreateCodeReview、Update に UpdateCodeReview、Delete に BatchDeleteCodeReviews を割り当て、CDK が自動で作る Lambda 関数が CodeReview を操作する図" class="mx-auto mt-4" style="width: 840px" />

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Integration のポイント</h2>
</div>

<br>

- GitLab のアクセストークンと Continuum を連携するリソース
- プロパティにアクセストークンを渡す必要がある
  - テンプレートやログにアクセストークンが流出してしまう
- Secrets Manager の ARN だけ渡し、処理の中でトークンを取得する
  - API 呼び出しが2回必要

<div v-click class="mt-6 text-xl">
  → <strong>カスタムリソースプロバイダーフレームワーク</strong>を利用する
</div>

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">プロバイダーフレームワークとは？</h2>
</div>

<div class="text-sm opacity-70 mt-1">カスタムリソースプロバイダーフレームワーク</div>

- CloudFormation イベントに合わせた処理を Lambda 関数で書ける
- 処理はソースコードで書くので、複雑な処理も任せられる
- カスタムリソースに必要な機能を簡単に使える
  - CloudFormation への応答
  - エラーハンドリング
  - 非同期処理のポーリング
- 呼び出す処理に必要な権限は自分で付与する必要がある

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html#provider-framework" title="Provider Framework · AWS CDK" />

---

<h2><span style="font-size: 0.85em">Integration のためのプロバイダーフレームワーク</span></h2>

<div class="text-sm opacity-70 mt-1">※ 省略のため Create イベントのみ記載</div>

<InlineSvg src="provider-integration.svg" label="プロバイダーフレームワークのカスタムリソースが、プロパティで Secrets Manager の ARN を受け取り、CDK が作るフレームワーク用の Lambda 関数から自前の処理用 Lambda 関数に Create を渡し、Secrets Manager からアクセストークンを取得して CreateIntegration を呼び出す図" class="mx-auto mt-4" style="width: 840px" />

---

<h2>AwsCustomResource と<br>プロバイダーフレームワークの使い分け</h2>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="rounded-xl border-2 border-gray-300 p-5">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-9" />
      <span class="font-bold" style="font-size: 1.2rem; white-space: nowrap">AwsCustomResource</span>
    </div>
    <ul>
      <li style="font-size: 1.1rem">AWS SDK の呼び出し1回で済む</li>
      <li style="font-size: 1.1rem">機密情報を扱わない</li>
      <li style="font-size: 1.1rem">処理の完了を待たなくていい</li>
    </ul>
  </div>
  <div class="rounded-xl border-2 border-gray-300 p-5">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-9" />
      <span class="font-bold" style="font-size: 1.2rem; white-space: nowrap">プロバイダーフレームワーク</span>
    </div>
    <ul>
      <li style="font-size: 1.1rem">複数の処理が必要</li>
      <li style="font-size: 1.1rem">機密情報を扱う</li>
      <li style="font-size: 1.1rem">処理の完了を待ちたい</li>
      <li style="font-size: 1.1rem">AWS 以外の API を呼びたい</li>
    </ul>
  </div>
</div>

---
layout: center
---

<div>
  <Kogoe>おわりに</Kogoe>
  <h2><span style="font-size: 0.82em">カスタムリソースを使えば<br>CloudFormation 未対応のサービスも<br>CDK で管理できる！</span></h2>
</div>

<br>

<div class="text-lg">その他カスタムリソースを使いたくなるタイミング</div>

- CloudFormation で定義できないものを管理したい
- デプロイしたリソースにデータを投入したい
- デプロイフローに処理を差し込みたい
- デプロイ時に外部から情報を取得したい

---
layout: center
class: text-center
transition: fade
---

## 宣伝

---
src: ./pages/pr/mates/index.md
---

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

