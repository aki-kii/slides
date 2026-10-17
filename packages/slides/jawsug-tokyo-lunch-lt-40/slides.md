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

<img src="/images/voiceio-overview.svg" class="mx-auto mt-4" style="max-height: 380px" />

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

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda MicroVMsとは？</h2>
</div>

<div class="text-lg mt-4">小さな仮想マシンを好きなときに立てて、止めて、再開できるサービス（2026年6月〜）</div>

<div class="grid grid-cols-2 gap-4 mt-8" style="font-size: 1.1rem">
  <div class="feature">VMレベルの隔離</div>
  <div class="feature">起動が速い</div>
  <div class="feature">状態を保ったまま一時停止と再開</div>
  <div class="feature">最大8時間動かせる</div>
</div>

<style>
.feature { border: 1px solid #dee2e6; border-radius: 8px; padding: 0.8rem 1rem; }
</style>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda Event Functionsとの違い</h2>
</div>

<table class="mt-6 diff">
  <thead><tr><th></th><th>Event Functions</th><th>MicroVMs</th></tr></thead>
  <tbody>
    <tr><td>イベント</td><td>イベントが来たら動く</td><td>使いたいときに自分で立ち上げて、止めるまで動き続ける</td></tr>
    <tr><td>関数</td><td>呼ばれるたびに処理して結果を返す、関数の形で書く</td><td>どんなアプリケーションでも動かせる実行環境</td></tr>
  </tbody>
</table>

<style>
.diff td, .diff th { padding: 0.6rem 0.8rem; font-size: 1rem; }
.diff td:first-child { font-weight: bold; white-space: nowrap; }
</style>

---
layout: center
---

<div>
  起動しきった状態を<strong>スナップショット</strong>に取っておき
  <h2>そこから再開するので<strong>速い</strong></h2>
</div>

---
layout: center
---

<div>
  <Kogoe>試してみたら…</Kogoe>
  <h2>ボイスチャットに入ったように見えて<br>接続が切れる</h2>
</div>

---

## 原因はUDP

<div class="text-lg mt-6" style="line-height: 2">
  <div>Discordのボイスチャットは<strong>UDP</strong>で通信している</div>
  <div>Lambda MicroVMsの標準のネット接続では、外向きのUDPが通らない</div>
  <div>VPC経由で外に出れば、UDPが通る</div>
</div>

---
layout: center
---

<div>
  VPCに入れたら
  <h2>約<strong>10秒</strong>で起動！</h2>
</div>

---

## Fargateはどうしていたか

<div class="text-lg mt-6" style="line-height: 2">
  <div>パブリックサブネットに置いて、パブリックIPで外に出る</div>
  <div>セキュリティグループはアウトバウンドだけ許可して守る</div>
</div>

<Overlay>
  本当はプライベートサブネットが定石。個人利用なのでコストを優先
</Overlay>

---

## Lambda MicroVMsは同じ手が使えない

<div class="text-lg mt-6" style="line-height: 2">
  <div>Lambda MicroVMsは<strong>パブリックIPを持てない</strong></div>
  <div>パブリックサブネットに置いても、インターネットに出られない</div>
  <div>→ プライベートサブネットに置いて<strong>NAT</strong>で外に出るしかない</div>
</div>

---

## コストを比べると

<div class="text-sm opacity-70">月20時間使う場合（東京リージョン、オンデマンドの単価で計算）</div>

<div class="mt-8 flex flex-col gap-4">
  <div class="bar-row"><span class="bar-name">ECS Fargate（今）</span><span class="bar" style="width: 19px"></span><span>約2.6ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NATインスタンス</span><span class="bar" style="width: 102px"></span><span>約14ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NAT Gateway</span><span class="bar" style="width: 400px"></span><span>約55ドル</span></div>
</div>

<div class="text-lg mt-10">NATは使っていない間もずっと置いておく<strong>固定費</strong></div>

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

## 起動にかかる時間を見てみました

<img src="/images/charts/breakdown.png" class="mx-auto mt-6" style="max-width: 100%" />

---

## 改善したいのは2つ

<div class="text-lg mt-6" style="line-height: 2.2">
  <div>① イメージの取得に時間がかかっている</div>
  <div>② Discord botがほかのコンテナの起動を待っているから遅い</div>
  <div class="ml-8"><Kogoe>しかもほかのコンテナはヘルスチェック（30秒おき）を待っている</Kogoe></div>
</div>

---
layout: center
---

<div>
  ① イメージの取得に時間がかかっている
  <h2>イメージが<strong>大きい</strong>のかな？</h2>
</div>

---

## コンテナイメージの大きさ

<table class="mt-6 size">
  <thead><tr><th>コンテナ</th><th>イメージの大きさ（圧縮後）</th></tr></thead>
  <tbody>
    <tr><td>読み上げ（VOICEVOX）</td><td>約1.9GB</td></tr>
    <tr><td>Discord bot</td><td>約390MB</td></tr>
    <tr><td>文字起こし</td><td>約90MB</td></tr>
  </tbody>
</table>

<div class="text-lg mt-8">読み上げはVOICEVOXが提供しているイメージなので<br>仕組み上この大きさで、削りようがない</div>



<style>
.size td, .size th { padding: 0.5rem 1rem; font-size: 1.05rem; }
</style>

---
layout: center
---

<div>
  調べてみたら
  <h2><strong>SOCIインデックス</strong>が使える！</h2>
</div>

---

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<div class="text-lg mt-2">コンテナイメージを<strong>遅延読み込み</strong>できる仕組み（AWSが作ったOSS）</div>

<div class="mt-6" style="font-size: 1.05rem; line-height: 2">
  <div>イメージをダウンロードするとき、起動に必要なファイルだけ取得して起動を早くする</div>
  <div>その他のファイルは、順次もしくは必要になったタイミングでダウンロードする</div>
  <div>コンテナイメージとは別にECRリポジトリにSOCIインデックスを置くので、イメージの中身を作り直さずに使える</div>
</div>

<div class="mt-6 opacity-70" style="font-size: 1rem">サイズが大きいコンテナイメージで効果的。起動直後に多くのファイルを読むコンテナには不向き</div>

---

## 読み上げコンテナはSOCIと相性がいい

<div class="text-lg mt-6" style="line-height: 2">
  <div>VOICEVOXには話者ごとの音声モデルが入っているので<strong>大きい</strong></div>
  <div>起動のときは、モデルの本体は読まない</div>
  <div><Kogoe>ただし、全部のモデルのファイルに少しずつ触るので、そのぶん起動は延びる</Kogoe></div>
</div>

---

## SOCIインデックスを入れた結果

<img src="/images/charts/soci-simple.png" class="mx-auto mt-2" style="max-height: 400px" />

<Overlay>
  取得は37.5秒→3.3秒。ただし起動は延びた
</Overlay>

---
layout: center
---

<div>
  ② Discord botがほかのコンテナの起動を待っている
  <h2>読み上げの準備が遅くなったのに<br><strong>待っている</strong></h2>
</div>

---
layout: center
---

<div>
  Discord botがボイスチャットに入るだけなら
  <h2>読み上げは<strong>まだいらない</strong></h2>
</div>

---

## コンテナを待たずに起動する

<img src="/images/charts/nowait2.png" class="mx-auto mt-2" style="max-height: 360px" />

<div class="text-center mt-2" style="font-size: 1rem">準備ができていなくても声や文章はためておいて、準備できたら流す</div>

---

## まとめ

<div class="text-2xl mt-8 text-center">約105秒 → 約65秒 → <strong>約35秒</strong></div>
<div class="text-sm opacity-70 text-center mt-1">（約65秒はSOCIインデックスだけを入れた場合の推測）</div>

<div class="mt-10" style="font-size: 1.1rem; line-height: 2">
  <div>Lambda MicroVMsは起動が速いが、UDPとNATのコストで断念</div>
  <div>Fargateのまま、SOCIインデックスとコンテナを待たずに起動で短縮</div>
</div>

---

<div class="text-sm opacity-70">余談</div>

## 調べてるうちに見つけたCDKの便利な部品

<div class="mt-6" style="font-size: 1.1rem; line-height: 2.2">
  <div><code>ec2.NatInstanceProviderV2</code>：NATインスタンスを作れる（aws-cdk-lib）</div>
  <div><code>SociIndexV2Build</code>：SOCIインデックスを作れるビルド環境（@cdklabs/deploy-time-build）</div>
</div>


---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

