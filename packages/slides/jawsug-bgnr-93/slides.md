---
layout: title
drawings:
  persist: false
transition: fade
title: AI時代のIaC入門 〜なぜインフラをコードで管理したいのか？〜
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="text-2xl font-normal opacity-90">JAWS-UG初心者支部 #93</div>

# <span style="font-size: 1.05em; line-height: 1.4; display: inline-block; font-weight: normal">AI時代の<span style="color:#ffd54f; font-weight: bold">IaC入門</span><br><span style="font-size: 0.6em">〜なぜインフラをコードで管理したいのか？〜</span></span>

<div class="opacity-70">

2026.10.29（木）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

</div>

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
layout: center
transition: fade
---

<!-- 話し言葉ルールの例外：本人の指定で、この1枚だけは字幕帯を使わず画面全体に大きく出す -->
<div class="w-full text-center">
  <h2 style="font-size: 2.2rem; line-height: 1.4; white-space: nowrap; text-align: center">これから本番リリースを始めます（？）</h2>
</div>

---
transition: fade
---

<InlineSvg src="story-architecture.svg" label="取引先からのアクセスをWAFのIPセットで許可している構成" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">お客様であるA社がオフィス移転したので、<br>業務システムのWAFのIPセットを変更します</div>

---
transition: fade
---

<img src="/images/story/manual-steps-console.png" alt="本番作業手順書の作業手順。No.1 作業開始の連絡から No.5 IPアドレスの書き換えまで。手順3にIPセットの画面が貼ってある" class="mx-auto shot" style="height: 395px" />

<div class="subtitle-band">手順書通りに進めていきたいと思います。<br>それではWAFのコンソールでIPセットを開きます…</div>

---
transition: fade
---

<div class="shot-pair mt-2">
  <figure>
    <figcaption>手順書の画面（旧コンソール）</figcaption>
    <div class="shot-wrap">
      <img src="/images/story/old-ipset-detail.png" alt="旧コンソールのIPセット詳細。DeleteとAdd IP addressのボタンがある" class="shot" />
      <span class="shot-mark" style="left: 72.5%; top: 46.5%; width: 23%; height: 7%"></span>
    </div>
  </figure>
  <figure>
    <figcaption>今の画面（新コンソール）</figcaption>
    <div class="shot-wrap">
      <img src="/images/story/new-ipset-detail.png" alt="新コンソールのIPセット詳細。日本語の画面で、ボタンの名前は削除とアドレスを追加。上にIPセットを編集のボタンもある" class="shot" />
      <span class="shot-mark" style="left: 82%; top: 0.3%; width: 16.8%; height: 6.6%"></span>
      <span class="shot-mark" style="left: 72.4%; top: 60%; width: 24%; height: 6.6%"></span>
      <span class="shot-anno" style="right: 1%; bottom: 100%">ここから書き換える ↓</span>
    </div>
  </figure>
</div>

<div class="subtitle-band">開いてみると…手順書の画面と見た目が全然違いますね…</div>

---
transition: fade
---

<div class="shot-edit mt-2">
  <div>
    <div class="shot-wrap">
      <img src="/images/story/new-ipset-edit.png" alt="新コンソールのIPセットを編集の画面。IPアドレスが7行並んでいる" class="shot" />
      <span class="shot-mark" style="left: 1.6%; top: 76.8%; width: 97.4%; height: 9.2%"></span>
    </div>
  </div>
  <div class="manual-card">
    <div class="manual-card-head">手順書</div>
    <img src="/images/story/manual-step5.png" alt="A社の行（203.0.113.12/32）にチェックを入れてDeleteで削除し、Add IP addressで新しいIPアドレス（198.51.100.200/32）を追加する" class="shot" style="width: 100%" />
  </div>
</div>

<div class="subtitle-band">対応したIPアドレスがあったので(嘘)、手順書の値に書き換えます<br>※ 間違った値を書き換えています</div>

---
transition: fade
---

<InlineSvg src="story-incident.svg" label="IPセットの編集画面。B社の行が消えて、A社の新しい値が入っている。A社は接続でき、B社は接続できない" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">設定変更完了しました！<br>おや？B社から苦情が来てますね…</div>

---
transition: fade
---

<InlineSvg src="story-lost.svg" label="IPセットの編集画面。A社の旧と新のIPアドレスが両方残り、B社の行が消えている" class="mx-auto mt-2" style="width: 576px" />

<div class="subtitle-band" style="font-size: 0.92rem">改めて設定を見ると、A社のIPアドレスが新旧どちらも残っていて、B社のIPアドレスが消えてました<br>元の値ってどこに載ってたかな……</div>

---

<h2 class="pain-head">リリースの振り返り</h2>

<div class="mt-8 pain-list">

- マネコンが手順書と変わっていて困った
- 設定を見間違えて事故を起こしてしまった
- 復旧しようとしても元の値を探す必要があった

</div>

<div class="mt-10 pain-close">→ IaCでデプロイすればこのような間違いが起きづらく、<br>&emsp;より安全なデプロイができます！</div>

<style>
.pain-head { white-space: nowrap; font-size: 1.9rem !important; }
.pain-list li { font-size: 1.25rem !important; line-height: 2 !important; }
.pain-close { font-size: 1.35rem; line-height: 1.6; white-space: nowrap; }
</style>

---
layout: center
class: text-center
---

<div>
  それでは
  <h2>IaCについて解説していきます</h2>
</div>

---
chapter: IaCとは？
---

## AWSリソースをデプロイする主な選択肢

<div class="dm-grid mt-4">
<div class="dm-cell">
  <div class="dm-icon"><img src="/images/tools/management-console.svg" /><span>マネジメント<br>コンソール</span></div>
  <div class="dm-body">
    <div class="dm-cap">マネジメントコンソールから画面操作</div>
    <img class="dm-panel dm-shot" src="/images/tools/management-console-screen.jpg" alt="マネジメントコンソールのバケットを作成する画面" />
  </div>
</div>
<div class="dm-cell">
  <div class="dm-icon"><img src="/images/tools/tools-and-sdks.svg" /><span>SDK</span></div>
  <div class="dm-body">
    <div class="dm-cap">アプリケーションからSDKを呼び出し</div>
    <div class="dm-panel dm-term"><span class="k">await</span> s3.send(<span class="k">new</span> CreateBucketCommand({<br>&nbsp;&nbsp;Bucket: <span class="s">"my-bucket"</span>,<br>}));</div>
  </div>
</div>
<div class="dm-cell">
  <div class="dm-icon"><img src="/images/tools/command-line-interface.svg" /><span>CLI</span></div>
  <div class="dm-body">
    <div class="dm-cap">CLIでコマンド操作</div>
    <div class="dm-panel dm-term">$ aws s3api create-bucket \<br>&nbsp;&nbsp;--bucket my-bucket</div>
  </div>
</div>
<div class="dm-cell">
  <div class="dm-icon dm-iac"><img src="/images/tools/code.svg" /><span>IaC</span></div>
  <div class="dm-body">
    <div class="dm-cap">IaCでデプロイ</div>
    <div class="dm-panel dm-term"><span class="k">MyBucket:</span><br>&nbsp;&nbsp;Type: AWS::S3::Bucket<br>&nbsp;&nbsp;Properties:<br>&nbsp;&nbsp;&nbsp;&nbsp;BucketName: <span class="s">my-bucket</span></div>
  </div>
</div>
</div>

---
layout: center
---

<div>
  IaC（Infrastructure as Code）とは？
  <h2>インフラの<span style="color: var(--accent-warm)">あるべき姿</span>をコードで宣言して、<br><span style="color: var(--accent-warm)">現在の状態との差分</span>を元に<br>リソースをあるべき姿に合わせる仕組み</h2>
</div>

---
chapter: IaCとは？
---

<h2>手続き型 vs 宣言型</h2>

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">リソースのデプロイ方法には、手続き型と宣言型がある</div>

<div class="pd-cards grid grid-cols-2 gap-6 mt-6">
<div class="pd-card">
<div class="pd-title">手続き型</div>
<div class="pd-sub">マネコン、CLI、SDK</div>
<ul>
  <li>「どうやるか」の設定手順を1つずつ指示するデプロイ方法</li>
  <li>現在のリソースに対して、作成・変更・削除の操作を都度実行する</li>
  <li>例：マネコンからLambda関数のメモリサイズを変更して、環境変数を追加した</li>
</ul>
</div>
<div class="pd-card pd-iac">
<div class="pd-title">宣言型</div>
<div class="pd-sub">IaC</div>
<ul>
  <li>リソースの「<span style="color: var(--accent-warm)">あるべき姿</span>」を宣言するデプロイ方法</li>
  <li>作成・変更・削除の操作は書かず、最終的な設定だけを書く</li>
  <li>例：コードにメモリサイズと環境変数を書いてデプロイした</li>
</ul>
</div>
</div>

---
chapter: IaCとは？
---

## IaCのデプロイの仕組み

<div class="text-lg mt-2">あるべき姿をコードで定義し、<span style="color: var(--accent-warm); font-weight: bold">現在の状態との差分</span>をデプロイする</div>

<InlineSvg src="iac-diff.svg" label="IaCのツールが、コードのあるべき姿と現在の状態を比較し、その差分だけを実リソースへデプロイする" class="mx-auto mt-6" style="width: 900px" />

---
layout: center
class: text-center
chapter: IaCとは？
---

## IaCの特徴

---
chapter: IaCとは？
transition: view-transition
---

<div style="view-transition-name: iac-feature">
  IaCの特徴 ①
  <h2>再現性の高さ</h2>
</div>

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">コードに定義されている通りにデプロイされるため、誰が何回やっても同じ結果になる</div>

<InlineSvg src="feature-reproducibility.svg" label="手作業では1回のデプロイの中で設定変更を繰り返すのでどこかで間違えるが、IaCは誰がやっても同じ結果になる" class="mx-auto mt-3" style="width: 470px" />

---
chapter: IaCとは？
transition: view-transition
---

<div style="view-transition-name: iac-feature">
  IaCの特徴 ②
  <h2>変更管理ができること</h2>
</div>

<div class="text-lg mt-2">IaCはコードで定義するためGitで変更管理ができる</div>

<div class="fig-pair mt-4">
  <div>
    <div class="fig-head">レビューしたソースコードをデプロイ</div>
    <InlineSvg src="feature-cm-deploy.svg" label="レビューしたソースコードを、WAF・ALB・ECSへデプロイする" />
  </div>
  <div>
    <div class="fig-head">戻すときは、前のコミットに戻して再度デプロイ</div>
    <InlineSvg src="feature-cm-rollback.svg" label="戻すときは、前のコミットに戻して、WAF・ALB・ECSへ再度デプロイする" />
  </div>
</div>

---
chapter: IaCとは？
transition: view-transition
---

<div style="view-transition-name: iac-feature">
  IaCの特徴 ③
  <h2>構造を把握しやすい</h2>
</div>

<div class="text-lg mt-2">構成はコードに全部書かれているので、コードを見れば全体像と関連が分かる</div>

<InlineSvg src="feature-structure.svg" label="WAF・ALB・ECSの関連が分かる構成と、ALBを定義したAWS CDKのコード。あえてHTTPを許可する設定に、その意図をコメントで残している" class="mx-auto mt-3" style="width: 660px" />

---
chapter: IaCとは？
---

<div style="view-transition-name: iac-feature">
  IaCの特徴 ④
  <h2>再利用のしやすさ</h2>
</div>

<div class="text-lg mt-2">インフラの共通部分を切り出して再利用できる</div>

<InlineSvg src="feature-reuse-parts.svg" label="ALBとECSの共通する部分を切り出して、DynamoDBを使う他の構成に組み込む" class="mx-auto mt-4" style="width: 420px" />

---
chapter: IaCとは？
---

<div class="flex items-center gap-4">
  <img src="/images/tools/code.svg" class="h-12" />
  <h2 class="!m-0">IaCのツールとは？</h2>
</div>

<div class="tc-cards grid grid-cols-2 gap-6 mt-5">
<div class="tc-card">
<div class="tc-title"><img src="/images/tools/terraform.svg" />Terraform</div>
<ul>
  <li>HashiCorp社のIaCツール</li>
  <li>HCLという独自の言語で<br>リソースを定義できる</li>
  <li>stateという作ったリソースの記録を<br>自分で持つファイルがあり、<br>置き場所や管理は自分たちで決める</li>
  <li>AWS以外のクラウドやSaaSも<br>まとめて管理できる</li>
</ul>
</div>
<div class="tc-card">
<div class="tc-title"><img src="/images/tools/cdk.svg" />AWS CDK</div>
<ul>
  <li>AWS公式のOSSツール</li>
  <li>CloudFormationを<br>プログラミング言語で書ける
    <div class="tc-box">
      <div class="tc-box-title"><img src="/images/tools/cloudformation.svg" />CloudFormation</div>
      <div>AWSのマネージドなIaCツール</div>
      <div>リソースのデプロイの安定性が高い</div>
    </div>
  </li>
  <li>よく使う構成が部品として<br>用意されていて、<br>少ないコードで書ける</li>
</ul>
</div>
</div>

<style>
.tc-card { border: 2px solid #d5d8dc; border-radius: 14px; padding: 0.7rem 1.1rem; }
.tc-title { display: flex; align-items: center; gap: 0.6rem; font-weight: bold; font-size: 1.3rem; margin-bottom: 0.3rem; white-space: nowrap; }
.tc-title img { height: 2.1rem; }
.tc-card li { font-size: 1rem !important; line-height: 1.55 !important; margin-bottom: 0.35rem !important; }
.tc-box { margin: 0.35rem 0 0.1rem; padding: 0.35rem 0.8rem; border-radius: 10px; background: #f3f4f6; font-size: 0.9rem; line-height: 1.55; }
.tc-box-title { display: flex; align-items: center; gap: 0.45rem; font-weight: bold; }
.tc-box-title img { height: 1.3rem; }
</style>

---
layout: center
class: text-center
---

## AI時代のIaCについて

---
layout: center
chapter: AIとIaC
---

<!-- 紙芝居型（本人OKの例外）：前置き（小）＋大きい一文。クリックで2つ目の文を出す -->
<div>
  最近は
  <h2>どんな仕事もAIに任せられるように<br>なってきましたね</h2>
  <h2 v-click class="mt-8">IaCも例外ではなく、<br>むしろ他のデプロイ方法より<br>AIに任せやすいです！</h2>
</div>

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ①
  <h2>コンテキストを渡しやすい</h2>
</div>

<div class="text-lg mt-2">ソースコードにインフラ設定・設計意図が含まれているため、<br>AIにとっても必要な情報が揃っている</div>

<InlineSvg src="ai-context.svg" label="CDKのコードにはアーキテクチャ全体と設定の意図が書いてあり、AIにはコードを渡せば伝わる。AWSをMCPやCLIで読みに行くと時間もトークンもかかる" class="mx-auto mt-6" style="width: 820px" />

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ②
  <h2>変更を検証できる仕組みがある</h2>
</div>

<div class="text-lg mt-2">AI自身が生成したソースコードを検証できる仕組みが整っている</div>

<InlineSvg src="ai-validation.svg" label="AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする" class="mx-auto mt-6" style="width: 800px" />

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ③
  <h2>AIにデプロイ権限を渡さなくて済む</h2>
</div>

<div class="text-lg mt-2">デプロイの権限をAIから分離できるので、AIに強い権限を与えずに済む</div>

<InlineSvg src="ai-permission.svg" label="AIはコードを実装するだけで、デプロイはCI/CDが行う。AIにはAWSの読み取り権限は渡すが、書き込み・デプロイ権限は渡さない" class="mx-auto mt-6" style="width: 760px" />

---
chapter: AIとIaC
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ④
  <h2>インフラの安全性を検証できる</h2>
</div>

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">ソースコードをスキャン（静的解析）することでセキュリティホールを見つけられる</div>

<InlineSvg src="ai-safety.svg" label="セキュリティグループで22番ポートを0.0.0.0/0に開けているCDKのコードを、実装中はcdk-nag、セキュリティスキャンではContinuumコードレビューなどでスキャンし、全世界からのSSHを許可していると指摘される" class="mx-auto mt-3" style="width: 740px" />

<div class="text-base mt-2 text-center">→ インフラ設定がソースコードに載っているため、<br>アプリのコードと同時にセキュリティスキャンできる</div>

---
chapter: AIとIaC
---

## IaCツールもAI向けに進化している

<div class="text-lg mt-2">AIが自分で書いたコードを、自分で検証できる範囲が広がってきている</div>

<div class="update-grid mt-6">
<InlineSvg src="ai-updates.svg" label="IaCのツールのアップデートを古い順に並べた年表。cdk diagnose（プレビュー）を強調している" />
<div class="update-card">
  <div class="update-card-title">cdk diagnose（プレビュー）</div>
  <ul>
    <li>デプロイに失敗した理由が確認できるコマンド</li>
    <li>理由をもとにAIが修正しやすくなった</li>
  </ul>
</div>
</div>

---
layout: center
class: text-center
---

## IaCの学習

---
layout: center
chapter: IaCの学習
---

<!-- Q&A 形式（jaws-sonic-2026 の intro の Q&A と同じ見せ方：Q. / A. と、前置き（小）・言い切り（大）・補足（小）） -->
<div class="qa-body">
  <div class="qa-row">
    <span class="qa-mark qa-lead">Q.</span>
    <div class="qa-lead">今後もIaCはAIが書くのであれば、<br>本当にIaCについて学ぶ必要はある？</div>
  </div>
  <div class="qa-row" v-click>
    <span class="qa-mark qa-lead"><strong>A.</strong></span>
    <div class="qa-lead">IaCで何ができるかを知るためにも<br>学んでおいた方がよさそう</div>
    <span></span>
    <div class="qa-note">※ 個人の意見</div>
  </div>
</div>

---
chapter: IaCの学習
transition: fade
---

## AIと一緒にIaCを学んでみよう

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">いきなり作り始めるのではなく、少しづつ作る範囲を広げていくのがおすすめ</div>
<div class="mt-1" style="font-size: 0.95rem; color: #6b7684">例: サーバーレスアーキテクチャ</div>

<InlineSvg src="learning-arch.svg" label="サーバーレスアーキテクチャの全体像。Amazon API Gateway から AWS Lambda、Amazon DynamoDB へつながる" class="mx-auto mt-6" style="width: 760px" />

---
chapter: IaCの学習
transition: fade
---

## AIと一緒にIaCを学んでみよう

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">いきなり作り始めるのではなく、少しづつ作る範囲を広げていくのがおすすめ</div>
<div class="mt-1" style="font-size: 0.95rem; color: #6b7684">例: サーバーレスアーキテクチャ</div>

<InlineSvg src="learning-step1.svg" label="まず AWS Lambda だけを作る。API Gateway と DynamoDB はまだ作っていない" class="mx-auto mt-6" style="width: 760px" />

<div class="learn-step">① まずLambda関数だけ作る</div>

---
chapter: IaCの学習
transition: fade
---

## AIと一緒にIaCを学んでみよう

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">いきなり作り始めるのではなく、少しづつ作る範囲を広げていくのがおすすめ</div>
<div class="mt-1" style="font-size: 0.95rem; color: #6b7684">例: サーバーレスアーキテクチャ</div>

<InlineSvg src="learning-step2.svg" label="API Gateway を追加して、Lambda につなぐ。DynamoDB はまだ作っていない" class="mx-auto mt-6" style="width: 760px" />

<div class="learn-step">② API Gatewayを追加</div>

---
chapter: IaCの学習
---

## AIと一緒にIaCを学んでみよう

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">いきなり作り始めるのではなく、少しづつ作る範囲を広げていくのがおすすめ</div>
<div class="mt-1" style="font-size: 0.95rem; color: #6b7684">例: サーバーレスアーキテクチャ</div>

<InlineSvg src="learning-arch.svg" label="DynamoDB を追加して、全体ができあがる" class="mx-auto mt-6" style="width: 760px" />

<div class="learn-step">③ DynamoDBを追加</div>

---
chapter: IaCの学習
---

<!-- Bパターン（比較用）：直前のサーバーレス4枚（Aパターン）と見比べるために置く -->
<h2>AIに聞きながら、自分で触って覚える</h2>

<div class="mt-3" style="font-size: 1.05rem; line-height: 1.7; white-space: nowrap">「何ができるの？」をAIに聞いて、設定を変えたりコマンドを打ったりしてみる。<br>わからなかったら、またAIに聞く</div>

<InlineSvg src="learning-loop.svg" label="AIに聞くことと、自分で設定や操作を触ることをくり返す" class="mx-auto mt-6" style="width: 560px" />

<div class="learn-step">手順はハンズオンで。ここでは「聞く→触る」をくり返すのがコツ</div>

---
chapter: IaCの学習
hide: true
---

## ハンズオンや書籍もおすすめ


---

## まとめ

<div class="mt-8 summary-list">

- IaCとは、インフラのあるべき姿をコードで宣言して、<br>現状との差分を元にリソースをあるべき姿に合わせる仕組み
- IaCはAIから利用しやすい形式で、<br>最近はAIのための機能開発も行われている
- まずはAIと一緒にIaCを学習してみる

</div>

<style>
.summary-list li { font-size: 1.3rem !important; line-height: 1.6 !important; margin-bottom: 0.8rem !important; }
</style>

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
