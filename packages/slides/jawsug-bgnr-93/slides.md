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

<div>
  <h2>これから本番リリースを始めます（？）</h2>
</div>

---
transition: fade
---

<InlineSvg src="story-architecture.svg" label="取引先からのアクセスをWAFのIPセットで許可している構成" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">お客様であるA社がオフィス移転したので、<br>業務システムのWAFのIPセットを変更します</div>

---
transition: fade
---

<InlineSvg src="story-manual.svg" label="手順書を開いて、手順書通りに進める" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">手順書通りに進めていきたいと思います</div>

---
transition: fade
---

<InlineSvg src="story-old-manual.svg" label="手順書の画面と今のコンソールの画面が違う" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">WAFのコンソールを開いて…あれ？<br>手順書と画面が違うので、IPセットの編集がありませんね…？</div>

---
transition: fade
---

<InlineSvg src="story-ip-set.svg" label="IPセットの編集画面で、A社だと思った行を置き換える" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">たくさんIPアドレスが並んでるけど…これっぽいかな<br>手順書からコピーした値で、元のIPアドレスを置き換えちゃいましょう</div>

---
transition: fade
---

<InlineSvg src="story-incident.svg" label="A社からもB社からも、つながらないと連絡が来る" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">完了！めでたしめでたし…っと、、、あれ？<br>A社からもB社からも、連絡が…！？</div>

---
transition: fade
---

<InlineSvg src="story-lost.svg" label="元の値も経緯も、どこにも記録がない" class="mx-auto mt-2" style="width: 900px" />

<div class="subtitle-band">置き換え元が間違えてる！<br>元の値ってなんだったっけ…どこで設定してたっけな………</div>

---
layout: center
---

<div>
  恐怖ですね…
  <h2>みなさんもどこかドキッとしたところは<br>ありませんでしたか？</h2>
</div>

---

<h2 class="pain-head">このリリースには辛いポイントが何個もありました</h2>

<div class="mt-8 pain-list">

- マネコンが手順書と変わっていて手間取った
- 変更先の設定を見間違えて、想定の設定と異なる設定をしてしまった
- 設定を戻そうとしても元の値を探す必要があり手間取った

</div>

<div class="mt-10 pain-close">IaCならこれらの間違いが起こらないような安全なデプロイができます！</div>

<style>
.pain-head { white-space: nowrap; font-size: 1.9rem !important; }
.pain-list li { font-size: 1.25rem !important; line-height: 2 !important; }
.pain-close { font-size: 1.4rem; white-space: nowrap; }
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

<ChapterLabel />

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
  <h2>インフラの<span style="color: var(--accent-warm)">あるべき姿</span>をコードで宣言して、<br><span style="color: var(--accent-warm)">現状との差分</span>を元にリソースをあるべき姿に合わせる仕組み</h2>
</div>

---
chapter: IaCとは？
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/tools/code.svg" class="h-12" />
  <h2 class="!m-0">手続き型 vs 宣言型</h2>
</div>

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">リソースのデプロイ方法には、手続き型と宣言型があります</div>

<div class="pd-cards grid grid-cols-2 gap-6 mt-6">
<div class="pd-card">
<div class="pd-title">手続き型</div>
<div class="pd-sub">マネコン、CLI、SDK</div>
<ul>
  <li>現在のリソースに対して</li>
  <li>設定を作成・更新して変更する</li>
</ul>
</div>
<div class="pd-card pd-iac">
<div class="pd-title">宣言型</div>
<div class="pd-sub">IaC</div>
<ul>
  <li>リソースの<span style="color: var(--accent-warm)">あるべき姿</span>を</li>
  <li>宣言して設定を決める</li>
</ul>
</div>
</div>

---
chapter: IaCとは？
---

<ChapterLabel />

## IaCのデプロイの仕組み

<div class="text-lg mt-2">あるべき姿をコードで定義し、現在の状態との差分をデプロイする</div>

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

<ChapterLabel />

<div style="view-transition-name: iac-feature">
  IaCの特徴 ①
  <h2>再現性の高さ</h2>
</div>

<div class="mt-2" style="font-size: 1.05rem; white-space: nowrap">コードに定義されている通りにデプロイされるため、誰が何回やっても同じ結果になる</div>

<div class="feature-grid mt-3" style="grid-template-columns: 430px 1fr">
<InlineSvg src="feature-reproducibility.svg" label="手作業では1回のデプロイの中で設定変更を繰り返すのでどこかで間違えるが、IaCは誰がやっても同じ結果になる" />
<div class="feature-list">

- 設定を一つ一つ手で変えていくと<br>どこかで間違える
- 新人でもベテランでも<br>同じ結果になる

<Kogoe>状態に依存するので、<br>絶対とは言い切れません</Kogoe>

</div>
</div>

---
chapter: IaCとは？
transition: view-transition
---

<ChapterLabel />

<div style="view-transition-name: iac-feature">
  IaCの特徴 ②
  <h2>変更管理ができること</h2>
</div>

<div class="text-lg mt-2">IaCはコードで定義するためGit管理ができる</div>

<InlineSvg src="feature-change-management.svg" label="レビューしたソースコードをデプロイし、戻したくなったら前のコミットを戻して再度デプロイする" class="mx-auto mt-4" style="width: 560px" />

---
chapter: IaCとは？
transition: view-transition
---

<ChapterLabel />

<div style="view-transition-name: iac-feature">
  IaCの特徴 ③
  <h2>構造を把握しやすい</h2>
</div>

<div class="text-lg mt-2">構成はコードに全部書かれているので、コードを見れば全体像と関連が分かる</div>

<InlineSvg src="feature-structure.svg" label="WAF・ALB・ECSの関連が分かる構成と、ALBを定義したAWS CDKのコード。あえてHTTPを許可する設定に、その意図をコメントで残している" class="mx-auto mt-4" style="width: 540px" />

---
chapter: IaCとは？
---

<ChapterLabel />

<div style="view-transition-name: iac-feature">
  IaCの特徴 ④
  <h2>再利用のしやすさ</h2>
</div>

<div class="text-lg mt-2">同じコードのまま、別の環境にもデプロイできる</div>

<InlineSvg src="feature-reuse.svg" label="同じコードでWAF・ALB・ECSの構成を開発環境と本番環境にデプロイでき、ALBとECSの共通パターンを他の構成に組み込める" class="mx-auto mt-4" style="width: 460px" />

---
chapter: IaCとは？
---

<ChapterLabel />

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

## AIとIaC

---
layout: center
chapter: AIとIaC
---

<ChapterLabel />

<div>
  ところで最近は
  <h2>どんな仕事でもAIに任せられるように<br>なってきましたね</h2>
  <div class="mt-8">IaCも例外ではありません</div>
  <h2>むしろ、他のデプロイ方法と比べても<br>AIに任せるのが得意とも言えます</h2>
</div>

---
chapter: AIとIaC
---

<ChapterLabel />

## 何でIaCはAIに向いてるの？

<div class="mt-8 reason-list">

1. コンテキストを渡しやすい
2. 変更を検証できる仕組みがある
3. AIにデプロイ権限を渡さなくて済む

</div>

---
chapter: AIとIaC
transition: view-transition
---

<ChapterLabel />

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

<ChapterLabel />

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ②
  <h2>変更を検証できる仕組みがある</h2>
</div>

<div class="text-lg mt-2">AIが検証して自分で直せて、人間もデプロイ前に差分を見られる</div>

<InlineSvg src="ai-validation.svg" label="AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする" class="mx-auto mt-6" style="width: 800px" />

---
chapter: AIとIaC
---

<ChapterLabel />

<div style="view-transition-name: ai-reason">
  IaCがAIに向いている理由 ③
  <h2>AIにデプロイ権限を渡さなくて済む</h2>
</div>

<div class="text-lg mt-2">AIにはコードを書いてもらうだけにして、デプロイはCI/CDに任せられる</div>

<InlineSvg src="ai-permission.svg" label="AIはコードを書くだけで、デプロイはCI/CDが行う。AIにAWSの権限を渡さなくて済む" class="mx-auto mt-8" style="width: 760px" />

---
chapter: AIとIaC
---

<ChapterLabel />

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

<ChapterLabel />

<div>
  IaCも今後全部AIで書くと思うけど
  <h2>本当に学んだ方がいいの？</h2>
</div>

<v-click>

<div class="mt-8">
  個人の一意見として
  <h2>何ができるかを知るために<br>一度試してみるのがよさそう</h2>
  <Kogoe>IaCの書き方・読み方を理解しなくてもいい世界には近づいてきている</Kogoe>
</div>

</v-click>

---
chapter: IaCの学習
---

<ChapterLabel />

## まずはAIと一緒に触ってみる

<div class="text-lg mt-2">例として、サーバーレスアーキテクチャをAIと一緒に組んでみる</div>

<InlineSvg src="learning-steps.svg" label="AIと一緒にサーバーレス構成を少しずつ育てる" class="mx-auto mt-6" style="width: 900px" />

---
chapter: IaCの学習
hide: true
---

<ChapterLabel />

## ハンズオンや書籍もおすすめ


---

## まとめ

<div class="mt-8 summary-list">

- IaCとは、インフラのあるべき姿をコードで宣言して、<br>現状との差分を元にリソースをあるべき姿に合わせる仕組み
- IaCはAIから利用しやすい形式で、<br>最近はAIのための機能開発も行われている
- AIと一緒にIaCを学習してみようー

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
