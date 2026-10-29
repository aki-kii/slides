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
  <h2 style="font-size: 3.4rem; line-height: 1.4; white-space: nowrap; text-align: center">これから本番リリースを<br>始めます（？）</h2>
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

<div class="subtitle-band">手順書通りに進めていきたいと思います<br>それではWAFのコンソールでIPセットを開きます…</div>

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

<div class="subtitle-band">開いてみると…あれ？手順書の画面と見た目が全然違いますね…<br>ボタンの名前も場所も違うし、どこから書き換えればいいんだろう…？</div>

---
transition: fade
---

<div class="shot-edit mt-2">
  <div>
    <div class="shot-wrap">
      <img src="/images/story/new-ipset-edit.png" alt="新コンソールのIPセットを編集の画面。IPアドレスが7行並んでいる" class="shot" />
      <span class="shot-mark" style="left: 1.6%; top: 76.8%; width: 97.4%; height: 9.2%"></span>
    </div>
    <div class="shot-note">※ 間違った値を書き換えています</div>
  </div>
  <div class="manual-card">
    <div class="manual-card-head">手順書</div>
    <img src="/images/story/manual-step5.png" alt="A社の行（203.0.113.12/32）にチェックを入れてDeleteで削除し、Add IP addressで新しいIPアドレス（198.51.100.200/32）を追加する" class="shot" style="width: 100%" />
  </div>
</div>

<div class="subtitle-band">対応したIPアドレスがあったので、手順書の値に書き換えます</div>

---
transition: fade
---

<InlineSvg src="story-incident.svg" label="IPセットの編集画面。B社の行が消えて、A社の新しい値が入っている。A社は接続でき、B社は接続できない" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">設定変更完了しました！<br>おや？B社から苦情が来てますね…</div>

---
transition: fade
---

<InlineSvg src="story-lost.svg" label="IPセットの編集画面。A社の旧と新のIPアドレスが両方残り、B社の行が消えている。手順4で控えるはずだったB社の元の値は、どこにも残っていない" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">改めて設定を見ると、A社のIPアドレスが新旧どちらも残っていて、<br>B社のIPアドレスが消えてました<br>元の値ってどこに載ってたかな……</div>

---

<h2 class="pain-head">リリースの振り返り</h2>

<div class="mt-8 pain-list">

- マネコンが手順書と変わっていて困った
- 設定を見間違えて事故を起こしてしまった
- 復旧しようとしても元の値を探す必要があった

</div>

<div class="mt-10 pain-close">→ IaCでデプロイすればこのような間違いが起こらず、<br>&emsp;より安全なデプロイができます！</div>

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

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">リソースのデプロイ方法には、手続き型と宣言型があります</div>

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

<div class="text-lg mt-2">同じコードのまま、別の環境にもデプロイできる</div>

<div class="fig-pair mt-4">
  <div>
    <div class="fig-head">同じコードのまま、別の環境にもデプロイ</div>
    <InlineSvg src="feature-reuse-envs.svg" label="同じコードのまま、WAF・ALB・ECSの構成を開発環境と本番環境にデプロイする" />
  </div>
  <div>
    <div class="fig-head">共通する部分を切り出して、他の構成に組み込む</div>
    <InlineSvg src="feature-reuse-parts.svg" label="ALBとECSの共通する部分を切り出して、DynamoDBを使う他の構成に組み込む" />
  </div>
</div>

---
chapter: IaCとは？
---

<div class="flex items-center gap-4">
  <img src="/images/tools/code.svg" class="h-12" />
  <h2 class="!m-0">IaCのツールとは？</h2>
</div>

<div class="tc-sub">TerraformとAWS CDK</div>

<div class="tc-cards grid grid-cols-2 gap-6 mt-3">
<div class="tc-card">
<div class="tc-title"><img src="/images/tools/terraform.svg" />Terraform</div>
<ul>
  <li>HashiCorp社が出しているツール</li>
  <li>HCLという独自の言語で<br>リソースを定義する</li>
  <li>AWS以外のクラウドにも対応している</li>
</ul>
</div>
<div class="tc-card">
<div class="tc-title"><img src="/images/tools/cdk.svg" />AWS CDK</div>
<ul>
  <li>AWS公式のOSSツール</li>
  <li>CloudFormationの設定を<br>プログラミング言語で書ける</li>
  <li>よく使う設定をまとめた部品がある</li>
</ul>
<div class="tc-cfn">
<div class="tc-cfn-title"><img src="/images/tools/cloudformation.svg" />CloudFormation</div>
<ul>
  <li>リソースの記録はAWS側が持つ</li>
  <li>失敗したときは前の状態に戻る</li>
</ul>
</div>
</div>
</div>

<style>
.tc-sub { font-size: 1.4rem; font-weight: bold; margin-top: 0.5rem; white-space: nowrap; }
.tc-card { border: 2px solid #d5d8dc; border-radius: 14px; padding: 0.6rem 1.2rem; }
.tc-title { display: flex; align-items: center; gap: 0.6rem; font-weight: bold; font-size: 1.2rem; margin-bottom: 0.4rem; white-space: nowrap; }
.tc-title img { height: 2rem; }
.tc-card li { font-size: 0.95rem !important; line-height: 1.6 !important; }
.tc-cfn { margin-top: 0.5rem; padding: 0.4rem 0.8rem; border-radius: 10px; background: #f3f4f6; }
.tc-cfn-title { display: flex; align-items: center; gap: 0.5rem; font-weight: bold; font-size: 0.95rem; }
.tc-cfn-title img { height: 1.4rem; }
.tc-cfn li { font-size: 0.85rem !important; line-height: 1.5 !important; }
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

<!-- 紙芝居型（本人OKの例外）：前置き（小）＋大きい一文 -->
<div>
  最近は
  <h2>どんな仕事もAIに任せられるように<br>なってきましたね</h2>
</div>

---
layout: center
chapter: AIとIaC
---

<!-- 紙芝居型（本人OKの例外）：大きい一文 -->
<div>
  <h2>IaCも例外ではなく、<br>むしろ他のデプロイ方法より<br>AIに任せやすいです！</h2>
</div>

---
chapter: AIとIaC
---

## なぜIaCはAIに向いているのか

<div class="mt-8 reason-list">

1. コンテキストを渡しやすい
2. 変更を検証できる仕組みがある
3. インフラの安全性を検証できる
4. AIにデプロイ権限を渡さなくて済む

</div>

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ①
  <h2>コンテキストを渡しやすい</h2>
</div>

<div class="text-lg mt-2">アーキテクチャ全体も設定の意図もコードにあるので、渡すだけでAIに伝わる</div>

<InlineSvg src="ai-context.svg" label="CDKのコードにはアーキテクチャ全体と設定の意図が書いてあり、AIにはコードを渡せば伝わる。AWSをMCPやCLIで読みに行くと時間もトークンもかかる" class="mx-auto mt-6" style="width: 820px" />

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ②
  <h2>変更を検証できる仕組みがある</h2>
</div>

<div class="text-lg mt-2">AIが検証して自分で直せて、人間もデプロイ前に差分を見られる</div>

<InlineSvg src="ai-validation.svg" label="AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする" class="mx-auto mt-6" style="width: 800px" />

---
chapter: AIとIaC
transition: view-transition
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ③
  <h2>インフラの安全性を検証できる</h2>
</div>

<div class="text-lg mt-2">コードスキャン（静的解析）で、インフラの危うい設定を見つけられる</div>

<InlineSvg src="ai-safety.svg" label="セキュリティグループで22番ポートを0.0.0.0/0に開けているCDKのコードを、書いているときはcdk-nag、あとでレビューするときはCheckovなどでスキャンし、全世界からのSSHを許可していると指摘される" class="mx-auto mt-3" style="width: 740px" />

<div class="text-base mt-2 text-center">→ マネコンの環境は画面で一つずつ見るしかないが、コードならまとめてスキャンできる</div>

---
chapter: AIとIaC
---

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ④
  <h2>AIにデプロイ権限を渡さなくて済む</h2>
</div>

<div class="text-lg mt-2">AIにはコードを書いてもらうだけにして、デプロイはCI/CDに任せられる</div>

<InlineSvg src="ai-permission.svg" label="AIはコードを書くだけで、デプロイはCI/CDが行う。AIにAWSの権限を渡さなくて済む" class="mx-auto mt-8" style="width: 760px" />

---
chapter: AIとIaC
---

## IaCのツールもAI向けに進化している

<div class="text-lg mt-2">AIがIaCのツールを使いやすくなるアップデートが、これだけ続いている</div>

<InlineSvg src="ai-updates.svg" label="AIがIaCのツールを使いやすくなるアップデート" class="mx-auto mt-6" style="width: 900px" />

---
layout: center
class: text-center
---

## IaCの学習

---
layout: center
chapter: IaCの学習
---

<div>
  IaCも今後はAIが書くとしたら
  <h2>本当に学ぶ必要はあるのか？</h2>
</div>

<v-click>

<div class="mt-8">
  個人の意見
  <h2>何ができるかを知るために<br>一度試してみるのがよい</h2>
  <Kogoe>IaCの書き方・読み方を理解しなくてもよい世界には近づいている</Kogoe>
</div>

</v-click>

---
chapter: IaCの学習
---

## まずはAIと一緒に触ってみる

<div class="text-lg mt-2">例として、サーバーレスアーキテクチャをAIと一緒に組んでみる</div>

<InlineSvg src="learning-steps.svg" label="AIと一緒にサーバーレス構成を少しずつ育てる" class="mx-auto mt-6" style="width: 900px" />

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
