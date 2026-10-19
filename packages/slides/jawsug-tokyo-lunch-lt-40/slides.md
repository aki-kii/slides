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
  ぼくは今、Discordのボイスチャットで
  <h2>Claude Codeと<strong>通話</strong>しています</h2>
  <div class="mt-6">走りながらでも、画面の前にいなくても<br>声で話しかけるとClaude Codeが返事をして、それを読み上げてくれる</div>
</div>

---

<div class="text-sm opacity-70">これを動かしているのが、voiceioというDiscord bot</div>

## voiceioの構成

<div class="text-lg mt-2">ボイスチャットの声を<strong>文字起こし</strong>して、返ってきた文章を<strong>読み上げる</strong></div>

<InlineSvg src="voiceio-overview.svg" label="Discordのボイスチャットとテキストチャットを、読み上げと文字起こしでClaude Codeとつなぐvoiceioの構成図" class="mx-auto mt-4" style="width: 760px" />

---

## Discord botの構成

<div class="mt-2" style="font-size: 0.95rem; white-space: nowrap">ECSのFargateで動いていて、/vcというスラッシュコマンドを打ったときだけ起動する</div>

<img src="/images/voiceio-bot.png" class="mx-auto mt-2" style="max-height: 360px" />

---
layout: center
---

<div>
  ただ、/vcを打ってからボイスチャットに入るまで
  <h2><strong>100秒以上</strong>かかっていました</h2>
  <Kogoe class="mt-8">今すぐ話したいのに</Kogoe>
  <h2>そんなに待ってられるか！</h2>
  <div class="mt-6">ということで、速くすることにしました</div>
</div>

---
layout: center
---

<div>
  真っ先に取り組んだのは
  <h2>起動が速いと噂の<strong>Lambda MicroVMs</strong></h2>
</div>

---
chapter: Lambda MicroVMsとは？
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda MicroVMsとは？</h2>
</div>

<div class="text-lg mt-2">小さな<strong>仮想マシン</strong>を好きなときに立てて、止めて、また再開できるサービス</div>

<Kogoe>今年の6月に出た新しいサービス</Kogoe>

<div class="tight-list">

- 起動しきった状態のスナップショットから再開するので、すぐ動き出せる
- 状態を保ったまま一時停止して、あとで続きから再開できる
- 一時停止している時間も含めて、最大8時間動かせる

</div>

<style>
.tight-list li { font-size: 1.1rem !important; line-height: 1.4 !important; margin-top: 0.05rem !important; margin-bottom: 0.05rem !important; }
</style>

<BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/06/aws-lambda-microvms/" title="AWS introduces Lambda MicroVMs for isolated execution of user and AI-generated code" />

---
chapter: Lambda MicroVMsとは？
clicks: 3
---

<ChapterLabel />

## Lambda Functionsとの違い

<div class="ecards grid grid-cols-2 gap-6 mt-4" :class="{ 'on-ev': $clicks === 2, 'on-fn': $clicks === 3 }">
<div class="card">
<div class="card-title">
  <img src="/images/aws/lambda.svg" class="h-9" />
  <span class="nm"><span>Lambda</span><span class="ev" :class="{ show: $clicks >= 1, red: $clicks <= 2 }">Event</span><span class="fnw">Functions</span></span>
</div>
<ul>
  <li class="row-ev" :class="{ off: $clicks < 2 }"><strong>イベント</strong>が来たら動く</li>
  <li class="row-fn" :class="{ off: $clicks < 3 }">呼ばれるたびに処理をして結果を返す、<strong>関数</strong>の形で書く</li>
</ul>
</div>
<div class="card">
<div class="card-title"><img src="/images/aws/lambda.svg" class="h-9" /><span>Lambda MicroVMs</span></div>
<ul>
  <li class="row-ev" :class="{ off: $clicks < 2 }">使いたいときに<strong>自分で立ち上げて</strong>、止めるまで動き続ける</li>
  <li class="row-fn" :class="{ off: $clicks < 3 }">関数の形に縛られず、どんな<strong>アプリケーション</strong>でも動かせる</li>
</ul>
</div>
</div>

<div class="h-6 mt-2 text-center"><Kogoe v-if="$clicks === 1">Lambdaの関数は、最近「Event Functions」と呼ばれるようになった</Kogoe></div>

<BottomLink href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html" title="What is AWS Lambda? - How Lambda compute primitives compare" />

<style>
.card { border: 2px solid #d5d8dc; border-radius: 14px; padding: 0.8rem 1.2rem; min-height: 11rem; }
.card-title { display: flex; align-items: center; gap: 0.8rem; font-weight: bold; font-size: 1.2rem; margin-bottom: 0.4rem; white-space: nowrap; }
.card-title span { transition: all 0.5s ease; }
.card-title .nm span + span { margin-left: 0.3em; }
.card-title .ev { display: inline-block; max-width: 0; opacity: 0; overflow: hidden; vertical-align: bottom; }
.card-title .nm .ev:not(.show) { margin-left: 0; }
.card-title .ev.show { max-width: 6em; opacity: 1; }
.card-title .ev.red { color: #e74c3c; }
.ecards.on-ev .ev, .ecards.on-fn .fnw { color: #e74c3c; text-decoration: underline; text-underline-offset: 0.2em; }
.card li { font-size: 0.95rem !important; line-height: 1.5 !important; transition: opacity 0.4s; }
.card li.off { opacity: 0; }
.card li strong { color: inherit; font-weight: normal; transition: color 0.3s; }
.ecards.on-ev .row-ev strong, .ecards.on-fn .row-fn strong, .ecards:not(.on-ev):not(.on-fn) li:not(.off) strong { color: #e74c3c; font-weight: bold; }
.ecards.on-ev .row-fn, .ecards.on-fn .row-ev { opacity: 0.35; }
</style>

---
layout: center
---

<div>
  さっそく
  <h2>Discordのbotを<strong>Lambda MicroVMs</strong>に<br>載せ替えて試した</h2>
</div>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">ところが、ボイスチャットに入ったように見えて接続が切れる</div>

## 問題① UDPで接続できない

<div class="net-cmp">
  <div><div class="net-label">VPCに置かない</div><img src="/images/net/netv-egress.svg" style="height: 340px" /></div>
  <div><div class="net-label">VPCに置く</div><img src="/images/net/netv-nat-gateway.svg" style="height: 340px" /></div>
</div>

<style>
.net-cmp { display: flex; justify-content: center; align-items: flex-start; gap: 2.5rem; margin-top: 0.2rem; }
.net-label { font-weight: bold; font-size: 0.95rem; margin-bottom: 0.2rem; }
</style>

<Overlay>
  VPCの中に入れたら約10秒で起動！
</Overlay>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">でも、VPCの中からインターネットに出るにはNATが要る。NATは高いので、Fargateと同じ方法を考えた</div>

## Fargateはどうしていたか

<div class="flex items-center justify-center gap-8 mt-2">
  <img src="/images/net/netv-fargate.svg" style="height: 340px" />
  <div class="w-64"><Kogoe>本当はプライベートサブネットに置くのが定石。個人で使うツールなので、コストを優先している</Kogoe></div>
</div>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">Lambda MicroVMsも同じようにパブリックサブネットに置こうとしたけど</div>

## 問題② パブリックIPを付けられない

<div class="net-cmp">
  <div><div class="net-label">パブリックサブネットに置く</div><img src="/images/net/netv-microvms-public.svg" style="height: 340px" /></div>
  <div v-click><div class="net-label">NATを通す</div><img src="/images/net/netv-nat.svg" style="height: 340px" /></div>
</div>

<style>
.net-cmp { display: flex; justify-content: center; align-items: flex-start; gap: 2.5rem; margin-top: 0.2rem; }
.net-label { font-weight: bold; font-size: 0.95rem; margin-bottom: 0.2rem; }
</style>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

## コストを比べると

<Kogoe>月20時間使う場合</Kogoe>

<div class="mt-8 flex flex-col gap-4">
  <div class="bar-row"><span class="bar-name">ECS Fargate（今）</span><span class="bar" style="width: 19px"></span><span>約2.6ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NATインスタンス</span><span class="bar" style="width: 102px"></span><span>約14ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NAT Gateway</span><span class="bar" style="width: 400px"></span><span>約55ドル</span></div>
</div>

<br>

- Lambda MicroVMs自体は少し高いくらい
- NATはいつ呼ばれてもいいように、一か月ずっと立てておく<strong>固定費</strong>になる

<BottomLink href="https://aws.amazon.com/lambda/pricing/" title="AWS Lambda pricing" />

<Overlay>
  ということでLambda MicroVMsを<strong>断念</strong>！
</Overlay>

<style>
.bar-row { display: flex; align-items: center; gap: 0.8rem; font-size: 1rem; white-space: nowrap; }
.bar-name { width: 18rem; flex: none; }
.bar { display: inline-block; height: 1.4rem; background: #3498db; border-radius: 3px; flex: none; }
</style>

---
layout: center
---

<div>
  Lambda MicroVMsはコストに見合わなかった。けど
  <h2>そもそも<strong>コンテナの起動</strong>を<br>速くできないの？</h2>
</div>

---
chapter: 起動にかかる時間を見る
---

<ChapterLabel />

<div class="text-sm opacity-70">そこで</div>

## 起動にかかる時間を見てみました

<InlineSvg src="chart-breakdown.svg" label="チューニング前の起動の内訳。準備約25秒、イメージの取得37.5秒、取得後8.0秒のあと、Discord botは読み上げと文字起こしのヘルスチェック合格を30.0秒待ってから起動し、合計約103秒" class="mx-auto" style="width: 780px" />

<div class="kaizen">
  <div v-click>① <strong>イメージの取得</strong>に時間がかかっている</div>
  <div v-click>② Discord botが<strong>ほかのコンテナの起動を待っている</strong>から遅い</div>
  <div v-after class="pl-8"><Kogoe>しかも、ほかのコンテナはヘルスチェックを待っている</Kogoe></div>
</div>

<style>
.kaizen { margin-top: 0.6rem; font-size: 1.1rem; line-height: 1.7; }
</style>

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">まず、① イメージの取得</div>

## イメージが大きいのかな？

<br>

- 読み上げが<strong>約1.9GB</strong>
- Discord botが約390MB
- 文字起こしが約90MB

<br>

- 読み上げはVOICEVOXが提供しているイメージを使っているので、仕組み上この大きさ
  - <Kogoe>削りようがない</Kogoe>

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">調べてみたら、重いコンテナイメージのダウンロードを改善するのに、SOCIインデックスが使える！</div>

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<div class="text-lg mt-2">コンテナイメージを<strong>遅延読み込み</strong>できる仕組み<Kogoe>（AWSが作ったOSS）</Kogoe></div>

<InlineSvg src="soci-concept.svg" label="ふつうはイメージを全部ダウンロードしてから起動する。SOCIインデックスがあると起動に必要な分だけ取って起動し、残りのファイルはあとで取ってくる" class="mx-auto mt-2" style="width: 640px" />

<div class="tight-list">

- ダウンロードするときに、起動に必要なファイルだけ取得して、起動を早くできる
- その他のファイルは、順次、もしくは必要になったタイミングでダウンロードする

</div>

<style>
.tight-list li { font-size: 1.05rem !important; line-height: 1.5 !important; margin-top: 0.1rem !important; margin-bottom: 0.1rem !important; }
</style>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<br>

- コンテナイメージとは別に、ECRリポジトリにSOCIインデックスを置く
  - イメージの中身を作り直さずに使える
- サイズが大きいコンテナイメージで効果的
  - <Kogoe>起動直後に多くのファイルを読むコンテナには不向き</Kogoe>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

## 読み上げコンテナはSOCIと相性がいい

<br>

- 読み上げのVOICEVOXには、話者ごとの音声モデルが入っているので<strong>大きい</strong>
- 起動のときは、モデルの本体は読まない

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">入れてみると</div>

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="SOCIなしはイメージの取得37.5秒で全部立ち上がるまで約64秒。SOCIありは取得3.3秒で約37秒。ただしDiscord botの起動は1.5秒から4.7秒、読み上げの起動は0.8秒から9.1秒に延びた" class="mx-auto" style="width: 780px" />

<div class="text-center text-lg">イメージの取得は37.5秒から<strong>3.3秒</strong>になった</div>

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">ただし</div>

## 起動は延びた

<br>

- 読み上げは0.8秒から<strong>9.1秒</strong>
- Discord botは1.5秒から<strong>4.7秒</strong>
- 足りないファイルを、起動しながら取りに行くから

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

<div class="text-sm opacity-70">次に、② Discord botがほかのコンテナの起動を待っている</div>

## 読み上げの準備が遅くなったのに待っている

<br>

- 読み上げの準備が遅くなったのに、Discord botはそれを待っている
- でも、Discord botがボイスチャットに入るだけなら、読み上げは<strong>まだいらない</strong>
- 読み上げがいるのは、誰かが話して、それを読み上げるときだけ

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

<div class="text-sm opacity-70">ヘルスチェックを5秒にする手もあるけど、そもそも待たなければいい</div>

## Discord botだけ先に起動する

<br>

- Discord botだけ先に起動して、ボイスチャットに入るようにした
- 準備ができていなくても、声や文章はためておいて、準備できたら流す

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

## コンテナを待たずに起動した結果

<InlineSvg src="chart-nowait.svg" label="全部のコンテナを待つと、Discord botは読み上げのヘルスチェック合格まで30.0秒待ってから起動して約66秒。Discord botだけ待つと約36秒" class="mx-auto" style="width: 720px" />

<div class="text-center text-lg">全部のコンテナを待つと約66秒、Discord botだけなら<strong>約36秒</strong></div>

---

## まとめ

<div class="text-2xl mt-6 text-center">約105秒が、<strong>約35秒</strong>になりました</div>

<br>

- Lambda MicroVMsは起動がめちゃくちゃ速くていい
  - <Kogoe>けど、制約が多くてお金がかかりそうなので断念した</Kogoe>
- Fargateの起動時間のチューニングをやると、かなり短縮できる
  - <Kogoe>特にSOCIインデックスはすごかった</Kogoe>

---

<div class="text-sm opacity-70">余談</div>

## 調べてるうちに見つけたCDKの便利な部品

<br>

- `NatInstanceProviderV2`
  - <Kogoe>NATインスタンスを作れる</Kogoe>
- `SociIndexV2Build`
  - <Kogoe>SOCIインデックスを作れる（@cdklabs/deploy-time-build）</Kogoe>

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

