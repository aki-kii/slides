---
layout: title
drawings:
  persist: false
transition: fade
title: Discord音声botをLambda MicroVMsに乗り換えずFargateのまま起動を速めた話
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="text-3xl font-bold opacity-90">Discord音声botを</div>

# <span style="font-size: 0.95em; line-height: 1.4; display: inline-block"><span style="color:#ffd54f">Lambda MicroVMs</span>に乗り換えず<br><span style="color:#ffd54f">Fargate</span>のまま起動を速めた話</span>

<div class="opacity-70">

2026.10.21（水）\
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
---

<div>
  Discordのボイスチャットで
  <h2>Claude Codeと<strong>通話</strong>しています</h2>
</div>

---

## voiceioの構成

<InlineSvg src="voiceio-overview.svg" label="Discordのボイスチャットとテキストチャットを、読み上げと文字起こしでClaude Codeとつなぐvoiceioの構成図" class="mx-auto mt-4" style="width: 820px" />

---

## Discord botの構成

<img src="/images/voiceio-bot.png" class="mx-auto mt-2" style="max-height: 400px" />

---
layout: center
---

<div>
  /vcを打ってからボイスチャットに入るまで
  <h2>約<strong>105秒</strong>かかる</h2>
</div>

---
layout: center
---

<div>
  <Kogoe>今すぐ話したいのに</Kogoe>
  <h2>そんなに待ってられるか！</h2>
</div>

---
layout: center
---

<div>
  真っ先に取り組んだのは
  <h2>起動が速いと噂の<strong>Lambda MicroVMs</strong></h2>
</div>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda MicroVMsとは？</h2>
</div>

<div class="text-lg mt-2">小さな<strong>仮想マシン</strong>を好きなときに立てて、止めて、再開できるサービス（2026年6月〜）</div>

<div class="flex gap-6 items-start justify-center mt-10">

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/shield.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-44 text-center">
    <span class="font-bold" style="font-size:1rem">VMレベルの隔離</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">仮想マシンごとに<br>分かれている</span>
  </div>
</div>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/lambda-function.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-44 text-center">
    <span class="font-bold" style="font-size:1rem">起動が速い</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">スナップショットから<br>再開する</span>
  </div>
</div>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/recover.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-44 text-center">
    <span class="font-bold" style="font-size:1rem">一時停止と再開</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">状態を保ったまま<br>止めて再開できる</span>
  </div>
</div>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/server.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-44 text-center">
    <span class="font-bold" style="font-size:1rem">最大8時間</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">一時停止を含めて<br>最大8時間動かせる</span>
  </div>
</div>

</div>

<BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/06/aws-lambda-microvms/" title="AWS introduces Lambda MicroVMs for isolated execution of user and AI-generated code" />

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">Lambda関数は「Event Functions」と呼ばれるようになった</div>

## Lambda Event Functionsとの違い

<div class="flex gap-10 justify-center mt-8">

<div class="flex flex-col items-center gap-3 w-96">
  <img src="/images/aws/lambda-function.svg" class="h-16"/>
  <span class="font-bold" style="font-size:1.1rem">Event Functions</span>
  <div class="text-center" style="line-height:1.8">
    <div><strong>イベント</strong>が来たら動く</div>
    <div class="text-gray-400 text-sm">呼ばれるたびに処理して結果を返す、<br><strong>関数</strong>の形で書く</div>
  </div>
</div>

<div class="flex flex-col items-center gap-3 w-96">
  <img src="/images/aws/server.svg" class="h-16"/>
  <span class="font-bold" style="font-size:1.1rem">MicroVMs</span>
  <div class="text-center" style="line-height:1.8">
    <div>使いたいときに<strong>自分で立ち上げて</strong>、止めるまで動き続ける</div>
    <div class="text-gray-400 text-sm">どんな<strong>アプリケーション</strong>でも動かせる実行環境</div>
  </div>
</div>

</div>

<BottomLink href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html" title="What is AWS Lambda? - How Lambda compute primitives compare" />

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">なぜ起動が速いのか</div>

## 起動しきった状態から再開する

- イメージを作るときに、アプリを起動しきった状態を<strong>スナップショット</strong>に取っておく
- 立てるたびに、そのスナップショットから再開するので<strong>速い</strong>

<BottomLink href="https://docs.aws.amazon.com/lambda/latest/dg/microvms-images.html" title="Lambda MicroVM images" />

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">試してみたら…</div>

## ボイスチャットに入ったように見えて接続が切れる

<br>

- Discordのボイスチャットは<strong>UDP</strong>で通信している
- Lambda MicroVMsの標準のネット接続では、外向きのUDPが通らない
- VPC経由で外に出れば、UDPが通る

<Overlay>
  VPCに入れたら約10秒で起動！
</Overlay>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">VPCに置くなら、インターネットへの出方が問題に</div>

## Fargateはどうしていたか

<div class="flex gap-4 items-start justify-center mt-8">

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/fargate.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">Fargateのタスク</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">パブリックサブネット<br>パブリックIPを持つ</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/internet-gateway.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">Internet Gateway</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/internet.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">インターネット</span>
  </div>
</div>

</div>

<div class="text-center mt-6">セキュリティグループはアウトバウンドだけ許可して守る</div>

<Overlay>
  本当はプライベートサブネットが定石。個人利用なのでコストを優先
</Overlay>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

## Lambda MicroVMsは同じ手が使えない

<div class="flex gap-4 items-start justify-center mt-8">

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/lambda.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">Lambda MicroVMs</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">プライベートサブネット<br>パブリックIPを持てない</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/nat-gateway.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">NAT</span>
    <span class="text-gray-400 text-sm" style="line-height:1.5">NAT Gateway<br>またはNATインスタンス</span>
  </div>
</div>

<span class="text-3xl" style="margin-top:2rem">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/internet.svg" class="h-20"/>
  <div class="flex flex-col items-center gap-1 w-48 text-center">
    <span class="font-bold">インターネット</span>
  </div>
</div>

</div>

- パブリックサブネットに置いても、インターネットに出られない
- プライベートサブネットに置いて<strong>NAT</strong>で外に出るしかない

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">NATを置くと</div>

## コストを比べると

<Kogoe>月20時間使う場合（東京リージョン、オンデマンドの単価で計算）</Kogoe>

<div class="mt-8 flex flex-col gap-4">
  <div class="bar-row"><span class="bar-name">ECS Fargate（今）</span><span class="bar" style="width: 19px"></span><span>約2.6ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NATインスタンス</span><span class="bar" style="width: 102px"></span><span>約14ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NAT Gateway</span><span class="bar" style="width: 400px"></span><span>約55ドル</span></div>
</div>

<div class="mt-8">NATは使っていない間もずっと置いておく<strong>固定費</strong></div>

<BottomLink href="https://aws.amazon.com/lambda/pricing/" title="AWS Lambda pricing" />

<style>
.bar-row { display: flex; align-items: center; gap: 0.8rem; font-size: 1rem; white-space: nowrap; }
.bar-name { width: 18rem; flex: none; }
.bar { display: inline-block; height: 1.4rem; background: #3498db; border-radius: 3px; flex: none; }
</style>

---
layout: center
---

<div>
  <h2>Lambda MicroVMsは<strong>断念</strong>！</h2>
</div>

---
layout: center
---

<div>
  Lambda MicroVMsはコストに見合わなかった
  <h2>そもそも<strong>コンテナの起動</strong>を<br>速くできないの？</h2>
</div>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

## 起動にかかる時間を見てみました

<InlineSvg src="chart-breakdown.svg" label="チューニング前の起動の内訳。準備約25秒、イメージの取得37.5秒、取得後8.0秒のあと、Discord botは読み上げと文字起こしのヘルスチェック合格を30.0秒待ってから起動し、合計約103秒" class="mx-auto mt-10" style="width: 960px" />

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

## 改善したいのは2つ

<br>

- ① イメージの取得に時間がかかっている
- ② Discord botがほかのコンテナの起動を待っているから遅い
  - <Kogoe>しかもほかのコンテナはヘルスチェック（30秒おき）を待っている</Kogoe>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">① イメージの取得に時間がかかっている</div>

## イメージが大きいのかな？

<div class="flex gap-10 items-start justify-center mt-8">

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/ecs-container.svg" class="h-16"/>
  <span class="font-bold">読み上げ</span>
  <span class="text-gray-400 text-sm">約1.9GB</span>
</div>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/ecs-container.svg" class="h-16"/>
  <span class="font-bold">Discord bot</span>
  <span class="text-gray-400 text-sm">約390MB</span>
</div>

<div class="flex flex-col items-center gap-2">
  <img src="/images/aws/ecs-container.svg" class="h-16"/>
  <span class="font-bold">文字起こし</span>
  <span class="text-gray-400 text-sm">約90MB</span>
</div>

</div>

<div class="text-center mt-8">読み上げはVOICEVOXが提供しているイメージなので、仕組み上この大きさ</div>
<div class="text-center"><Kogoe>削りようがない</Kogoe></div>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">調べてみたら、SOCIインデックスが使える！</div>

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<div class="text-lg mt-2">コンテナイメージを<strong>遅延読み込み</strong>できる仕組み（AWSが作ったOSS）</div>

<InlineSvg src="soci-concept.svg" label="ふつうはイメージを全部ダウンロードしてから起動する。SOCIインデックスがあると起動に必要な分だけ取って起動し、残りのファイルはあとで取ってくる" class="mx-auto mt-6" style="width: 640px" />

<div class="mt-4 text-sm" style="line-height:1.8">
  <div>コンテナイメージとは別にECRリポジトリにSOCIインデックスを置くので、イメージの中身を作り直さずに使える</div>
  <Kogoe>サイズが大きいコンテナイメージで効果的。起動直後に多くのファイルを読むコンテナには不向き</Kogoe>
</div>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

## 読み上げコンテナはSOCIと相性がいい

<br>

- VOICEVOXには話者ごとの音声モデルが入っているので<strong>大きい</strong>
- 起動のときは、モデルの本体は読まない
  - <Kogoe>ただし、全部のモデルのファイルに少しずつ触るので、そのぶん起動は延びる</Kogoe>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="SOCIなしはイメージの取得37.5秒で全部立ち上がるまで約64秒。SOCIありは取得3.3秒で約37秒。ただしDiscord botの起動は1.5秒から4.7秒、読み上げの起動は0.8秒から9.1秒に延びた" class="mx-auto" style="width: 700px" />

<Overlay>
  取得は37.5秒→3.3秒。ただし起動は延びた
</Overlay>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">② Discord botがほかのコンテナの起動を待っている</div>

## 読み上げの準備が遅くなったのに待っている

<br>

- Discord botがボイスチャットに入るだけなら、読み上げは<strong>まだいらない</strong>

---
chapter: Fargateの起動を速くする
---

<ChapterLabel />

## コンテナを待たずに起動する

<InlineSvg src="chart-nowait.svg" label="全部のコンテナを待つと、Discord botは読み上げのヘルスチェック合格まで30.0秒待ってから起動して約66秒。Discord botだけ待つと約36秒" class="mx-auto" style="width: 940px" />

<div class="text-center mt-2">準備ができていなくても声や文章はためておいて、準備できたら流す</div>

---

## まとめ

<div class="text-2xl mt-8 text-center">約105秒 → 約65秒 → <strong>約35秒</strong></div>
<div class="text-center mt-1"><Kogoe>約65秒はSOCIインデックスだけを入れた場合の推測</Kogoe></div>

<br>

- Lambda MicroVMsは起動が速いが、UDPとNATのコストで断念
- Fargateのまま、SOCIインデックスとコンテナを待たずに起動で短縮

---

<div class="text-sm opacity-70">余談</div>

## 調べてるうちに見つけたCDKの便利な部品

<br>

- `ec2.NatInstanceProviderV2`
  - <Kogoe>NATインスタンスを作れる（aws-cdk-lib）</Kogoe>
- `SociIndexV2Build`
  - <Kogoe>SOCIインデックスを作れるビルド環境（@cdklabs/deploy-time-build）</Kogoe>


---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

