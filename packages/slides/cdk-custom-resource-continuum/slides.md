---
layout: title
drawings:
  persist: false
transition: fade
title: AWS CDKのカスタムリソースでContinuum（旧Security Agent）を実装した話
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

**JAWS-UG 茨城 #17 秋の推しAWSサービスLTまつり！**

<div class="text-xl font-bold opacity-90 mt-6">CloudFormation未対応でも諦めない！</div>

# <span style="font-size: 0.72em; line-height: 1.4; display: inline-block">AWS CDKのカスタムリソースで<br>Continuum（旧Security Agent）を実装した話</span>

2026.9.30（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/public/images/aboutme/eye-catch.png" class="h-36" />
</div>

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

---
transition: slide-left
---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDKとは？</h2>
</div>

**プログラミング言語**で**AWSリソース**を定義するIaCフレームワーク

<div class="flex gap-4 items-start justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">プログラミング言語</span>
    <span class="text-gray-400 text-center text-sm" style="line-height:1.5">コードからCloudFormation<br>テンプレートを合成</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2.6rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">CloudFormation</span>
    <span class="text-gray-400 text-center text-sm" style="line-height:1.5">リソースの状態と比較して<br>差分をデプロイ</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2.6rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">AWSリソース</span>
  </div>
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
  <h2><strong>Continuumコードスキャニング</strong>を<br>導入したときの話をします</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuumコードスキャニングとは？</h2>
</div>

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">
  <div>Continuum（Security Agentが改名）の機能の1つ</div>
  <div><strong>AIエージェント</strong>がソースコードをスキャンして脆弱性を検出する機能</div>
  <div class="mt-3">フルリポジトリスキャン</div>
</div>

<InlineSvg src="code-scanning.svg" label="Continuumコードスキャニングがリポジトリ全体を読み、見つかった脆弱性と修正案をスキャン結果として出す図" class="mx-auto mt-1" style="width: 620px" />

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html" title="Create a code review - AWS Security Agent (now part of AWS Continuum)" />

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuumコードスキャニングとは？</h2>
</div>

<div class="text-lg mt-2">リソース構成</div>

<InlineSvg src="continuum-code-review.svg" label="IntegrationがGitLabのアクセストークンでGitLabと接続し、AgentSpaceの中のCodeReviewがGitLabのリポジトリをスキャンする構成図。AgentSpaceはCloudFormation対応、IntegrationとCodeReviewはCloudFormation未対応" class="mx-auto mt-6" style="width: 800px" />

---
transition: slide-left
---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDKとは？（再）</h2>
</div>

**プログラミング言語**で**AWSリソース**を定義するIaCフレームワーク

<div class="flex gap-4 items-start justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">プログラミング言語</span>
    <span class="text-gray-400 text-center text-sm" style="line-height:1.5">コードからCloudFormation<br>テンプレートを合成</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2.6rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">CloudFormation</span>
    <span class="text-gray-400 text-center text-sm" style="line-height:1.5">リソースの状態と比較して<br>差分をデプロイ</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2.6rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-28"/>
  <div class="flex flex-col items-center gap-1 w-52 text-center">
    <span class="font-bold" style="font-size:1rem">AWSリソース</span>
  </div>
</div>

</div>

<Overlay>
  CloudFormation未対応のリソースは<br><strong>標準的な方法では</strong>CDKで定義できない
</Overlay>

---
layout: center
---

<div>
  ContinuumコードスキャニングをCDKで管理するため
  <h2><strong>カスタムリソース</strong>で定義しました！</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg">CloudFormationのライフサイクルに合わせて<strong>カスタムの処理を実行する</strong>仕組み</div>

<InlineSvg src="custom-resource-lifecycle.svg" label="StackやConstructの作成・プロパティ変更・削除に応じて、カスタムリソースの中でCloudFormationのリソースからLambda関数へCreate・Update・Deleteのイベントが届き、Lambda関数がAPIを呼んで実行結果をS3オブジェクトに書き込み、CloudFormationがその応答を待ち受ける図" class="mx-auto mt-2" style="width: 700px" />

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/template-custom-resources.html" title="カスタムリソースを使用してカスタムプロビジョニングロジックを作成する" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg mt-4">e.g. S3バケットを空にするカスタムリソース</div>

<div class="text-sm opacity-70 mt-1">Bucket（L2 Construct）で <code>autoDeleteObjects: true</code> にすると作られる</div>

<InlineSvg src="custom-resource-s3.svg" label="カスタムリソースのLambda関数が、CreateとUpdateでは何もせず、DeleteでS3バケットのオブジェクトを全て削除する図" class="mx-auto mt-4" style="width: 780px" />

---
transition: slide-left
---

<div class="text-sm opacity-70">実装が複雑になりそうだけど…</div>

## 何故そこまでしてCDKで定義したかったの？

<br>

- CloudFormationのライフサイクルで管理できる
- 定義したリソースを複製しやすい
  - e.g. リポジトリごとにCodeReviewを作れる
- 設定を設計意図と一緒にソースコードに残せる
  - <Kogoe>マネコンから作ると設計意図を残すには別途ドキュメントが必要</Kogoe>

<div class="mt-8 opacity-70">
  <div style="font-size: 1rem">ほかにも</div>
  <ul class="!mt-1">
    <li style="font-size: 1.05rem">他のリソースと合わせてCDKで統一できる</li>
    <li style="font-size: 1.05rem">CloudFormationが対応したらL1 Constructに取り込みやすい</li>
  </ul>
</div>

---
layout: center
---

<div>
  <Kogoe>それでは...</Kogoe>
  <h2>Continuumコードスキャニングを<br><strong>CDKのカスタムリソース</strong>を使って定義します</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0"><span style="font-size: 0.85em">Continuumコードスキャニングのリソース構成</span></h2>
</div>

<InlineSvg src="continuum-code-review.svg" label="IntegrationがGitLabのアクセストークンでGitLabと接続し、AgentSpaceの中のCodeReviewがGitLabのリポジトリをスキャンする構成図。AgentSpaceはCloudFormation対応、IntegrationとCodeReviewはCloudFormation未対応" class="mx-auto mt-6" style="width: 800px" />

<div class="text-lg mt-4">→ <strong>Integration・CodeReview</strong>をカスタムリソースで定義します！</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">CodeReviewを定義するためのポイント</h2>
</div>

<br>

- 連携したリポジトリをコードスキャンするためのリソース
- CloudFormationのイベントに対応したAPIが揃っている
  - Create: `CreateCodeReview`
  - Update: `UpdateCodeReview`
  - Delete: `BatchDeleteCodeReviews`

<div v-click class="mt-8 text-xl">
  → <strong>AwsCustomResource</strong>を利用する
</div>

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/APIReference/API_Operations.html" title="AWS Security Agent API Reference - Actions" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AwsCustomResourceとは？</h2>
</div>

CDKが提供しているカスタムリソースの作り方の1つ

- CloudFormationイベントごとにAWS SDKを1つだけ実行できる
- プロパティを渡すだけで簡単にカスタムリソースを作成できる
- 指定したAWS SDKからIAMポリシーを自動で生成する
  - <Kogoe>権限が足りない場合は自分で指定する必要あり</Kogoe>

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html" title="class AwsCustomResource (construct) · AWS CDK" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AwsCustomResourceとは？</h2>
</div>

<div class="text-lg mt-4">CodeReviewの定義例</div>

<InlineSvg src="awscr-codereview.svg" label="プロパティにonCreate・onUpdate・onDeleteのAWS SDKの呼び出しを渡すと、AwsCustomResourceのカスタムリソースで、CreateにCreateCodeReview、UpdateにUpdateCodeReview、DeleteにBatchDeleteCodeReviewsを割り当て、AwsCustomResourceが作成するLambda関数がCodeReviewを操作する図" class="mx-auto mt-4" style="width: 860px" />

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Integrationを定義するためのポイント</h2>
</div>

<br>

<div class="compact-list">

- リポジトリとContinuumを連携するためのリソース
- プロパティにアクセストークン（シークレット）を指定する必要がある
  - テンプレートやログからシークレットが流出してしまう
- 回避しようとすると単一のAWS SDK呼び出しでは実現できない
  - AwsCustomResourceは利用できない

</div>

<style>
.compact-list li { font-size: 1.2rem !important; }
</style>

<div v-click class="mt-6 text-xl">
  → <strong>カスタムリソースプロバイダーフレームワーク</strong>を利用する
</div>

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">プロバイダーフレームワークとは？</h2>
</div>

CDKが提供しているカスタムリソースの作り方の1つ

<div class="tight-list">

- CloudFormationイベントに合わせた処理をLambda関数で書ける
- 処理はソースコードで書くので、複雑な処理も任せられる
- カスタムリソースに必要な機能を簡単に使える
  - CloudFormationとのやり取り
  - エラーハンドリング
  - 非同期処理のポーリング <Kogoe>など…</Kogoe>
- 呼び出す処理に必要な権限は自分で付与する必要がある

</div>

<style>
.tight-list li { font-size: 1.15rem !important; line-height: 1.5 !important; margin-top: 0.1rem !important; margin-bottom: 0.1rem !important; }
</style>

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html#provider-framework" title="Provider Framework · AWS CDK" />

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">プロバイダーフレームワークとは？</h2>
</div>

<div class="text-lg mt-4">Integrationの定義例</div>

<div class="text-sm opacity-70 mt-1">※ 簡素化のためCreateイベントのみに省略</div>

<InlineSvg src="provider-integration.svg" label="プロバイダーフレームワークのカスタムリソースが、プロパティのsecretArnでSecrets ManagerのARNを受け取り、フレームワークが作成するフレームワーク用のLambda関数から自前の処理用Lambda関数にCreateを渡し、Secrets Managerからアクセストークンを取得してCreateIntegrationを呼び出す図" class="mx-auto mt-4" style="width: 860px" />

---
transition: slide-left
---

<h2>AwsCustomResourceと<br>プロバイダーフレームワークの使い分け</h2>

<div class="text-lg mt-2">基本は<strong>AwsCustomResource</strong>を使い、<br>実現できない要件があるときだけ<strong>プロバイダーフレームワーク</strong>を使う</div>

<div class="flex items-stretch gap-3 mt-5">
  <div class="rounded-xl border-2 border-gray-300 px-4 py-3" style="flex: 0 0 40%">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-8" />
      <span class="font-bold" style="font-size: 1.1rem; white-space: nowrap">AwsCustomResource</span>
    </div>
    <ul>
      <li style="font-size: 1rem; white-space: nowrap">AWS SDKの呼び出し1回で済む</li>
    </ul>
  </div>
  <div class="rounded-xl border-2 border-gray-300 px-4 py-3" style="flex: 1">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-8" />
      <span class="font-bold" style="font-size: 1.1rem; white-space: nowrap">プロバイダーフレームワーク</span>
    </div>
    <ul>
      <li style="font-size: 1rem">APIの呼び出しが1回に収まらない</li>
      <li style="font-size: 1rem">非同期処理の完了を待ちたい</li>
      <li style="font-size: 1rem">AWS SDKではできない処理をしたい</li>
    </ul>
  </div>
</div>

---
layout: center
transition: slide-left
---

<div>
  <Kogoe>おわりに</Kogoe>
  <h2><span style="font-size: 0.82em">カスタムリソースを使えば<br>CloudFormation未対応のサービスも<br>CDKで管理できる！</span></h2>
</div>

<br>

<div class="text-lg">その他にも...</div>

- CloudFormationで定義できないものを管理したい
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
transition: slide-left
---

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

