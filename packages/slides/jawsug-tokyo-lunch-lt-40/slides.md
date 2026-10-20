---
layout: title
drawings:
  persist: false
transition: fade
title: 自作Discord音声botをLambda MicroVMsに移行してみた話
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="text-3xl font-bold opacity-90">自作Discord音声botを</div>

# <span style="font-size: 0.95em; line-height: 1.4; display: inline-block"><span style="color:#ffd54f">Lambda MicroVMs</span>に<br>移行してみた話</span>

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
  自作のDiscord音声bot（ECS Fargate）の
  <h2><strong>起動時間を縮める</strong>ために<br>試行錯誤した時の話をします</h2>
</div>

---

## 自作のDiscord音声bot

<div class="text-lg mt-2">Discordのボイスチャットで、<strong>Claude Codeと通話</strong>している</div>

<img src="/images/bot-overview.svg" class="mx-auto mt-2" style="width: 720px" />

---

## 自作のDiscord音声bot

<img src="/images/bot-task.svg" class="mx-auto mt-6" style="width: 800px" />

<div class="text-center text-lg mt-6">コストを抑えるため、botは<strong>必要なときだけ起動する</strong>仕組み</div>

---
layout: center
---

<div>
  <h2>必要なときだけ起動するので<br>使う前に起動を待つ必要があります</h2>
  <h2 v-click class="mt-6">起動に<strong>100秒以上</strong>かかるのがとてもツラかったので<br>起動時間を縮めるため改善していきます</h2>
</div>

---
layout: center
---

<div>
  起動が速いと噂の
  <h2><strong>Lambda MicroVMs</strong>を検証してみた</h2>
</div>

---
chapter: Lambda MicroVMsとは？
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda MicroVMsとは？</h2>
</div>

<div class="text-lg mt-2">状態を保ったまま止めて、また再開できる<strong>隔離された実行環境</strong></div>

<img src="/images/microvm-lifecycle.svg" class="mx-auto mt-4" style="width: 740px" />

<div class="tight-list">

- スナップショットから起動するので、<strong>起動時間が短い</strong>
- 一時停止して、<strong>止めたところから再開できる</strong>
- 一時停止も含めて、<strong>最大8時間</strong>使える

</div>

<style>
.tight-list li { font-size: 1.1rem !important; line-height: 1.4 !important; margin-top: 0.05rem !important; margin-bottom: 0.05rem !important; }
</style>

<BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/06/aws-lambda-microvms/" title="AWS introduces Lambda MicroVMs for isolated execution of user and AI-generated code" />

---
chapter: Lambda MicroVMsとは？
hide: true
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/lambda.svg" class="h-12" />
  <h2 class="!m-0">Lambda MicroVMsとは？</h2>
</div>

<div class="sub-title">Lambda <span class="u-ev">Event</span> <span class="u-fn">Functions</span><span style="font-size: 0.7em; font-weight: normal">（旧Lambda Functions）</span>との違い</div>

<div class="ecards grid grid-cols-2 gap-6 mt-6">
<div class="card">
<div class="card-title">Lambda Event Functions</div>
<ul>
  <li><span class="u-ev">イベントが来たら動く</span></li>
  <li><span class="u-fn">関数の形で書く</span></li>
  <li>最大15分</li>
  <li>使い捨ての実行環境</li>
</ul>
</div>
<div class="card">
<div class="card-title">Lambda MicroVMs</div>
<ul>
  <li><span class="u-ev">自分で立ち上げて、止めるまで動く</span></li>
  <li><span class="u-fn">どんなアプリケーションでも動かせる</span></li>
  <li>最大8時間（一時停止を含む）</li>
  <li>止めても、同じ環境にまた戻れる</li>
</ul>
</div>
</div>

<BottomLink href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html" title="What is AWS Lambda? - How Lambda compute primitives compare" />

<style>
.sub-title { font-size: 1.4rem; font-weight: bold; margin-top: 1rem; white-space: nowrap; }
.u-ev { text-decoration: underline; text-decoration-color: #2F6FB3; text-decoration-thickness: 3px; text-underline-offset: 0.25em; }
.u-fn { text-decoration: underline; text-decoration-color: #E67E22; text-decoration-thickness: 3px; text-underline-offset: 0.25em; }
.card { border: 2px solid #d5d8dc; border-radius: 14px; padding: 0.8rem 1.2rem; }
.card-title { font-weight: bold; font-size: 1.2rem; margin-bottom: 0.4rem; white-space: nowrap; }
.card li { font-size: 0.95rem !important; line-height: 1.7 !important; }
</style>
---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<h2><span style="font-size: 0.85em">検証ポイント① 使えるコンテナは1つだけ</span></h2>

<div class="text-lg mt-2">Lambda MicroVMsで動かせるのは、<strong>1つのコンテナだけ</strong></div>

<div class="one-cmp">
<div>
<div class="one-label">ECS Fargate（今）</div>
<div class="one-frame">
<div class="one-box">Discord bot</div>
<div class="one-box">読み上げ</div>
<div class="one-box">文字起こし</div>
</div>
<div class="one-cap">1つのタスクに<br>コンテナが3つ</div>
</div>
<div class="one-arrow">→</div>
<div>
<div class="one-label">Lambda MicroVMs</div>
<div class="one-frame">
<div class="one-box one-big">Discord bot<br>＋ 読み上げ<br>＋ 文字起こし</div>
</div>
<div class="one-cap"><strong>1つのコンテナ</strong>にまとめる</div>
</div>
</div>

<div class="text-center mt-4">
別のサービスに切り出す案もあったけど、<strong>ネットワークの遅延</strong>が大きい
</div>

<style>
.one-cmp { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 1rem; }
.one-label { font-weight: bold; font-size: 0.85rem; margin-bottom: 0.3rem; text-align: center; }
.one-frame { border: 2px dashed #7f8c8d; border-radius: 12px; padding: 0.5rem; display: flex; gap: 0.35rem; justify-content: center; }
.one-box { border: 2px solid #3498db; border-radius: 8px; padding: 0.45rem 0.55rem; font-size: 0.8rem; background: rgba(52,152,219,0.1); white-space: nowrap; }
.one-big { padding: 1rem 0.8rem; white-space: normal; text-align: center; width: 9.5rem; }
.one-arrow { font-size: 1.6rem; }
.one-cap { text-align: center; font-size: 0.9rem; margin-top: 0.4rem; }
</style>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<h2><span style="font-size: 0.85em">検証ポイント① 使えるコンテナは1つだけ</span></h2>

<div class="text-lg mt-6">3つを1つにまとめたら、<strong>起動が遅くなるのでは？</strong></div>

<div v-click class="mt-8 text-lg">

- スナップショットは、<strong>起動した状態</strong>で撮っている
- だから、コンテナが増えても、<strong>起動に時間はかからない</strong>

</div>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<h2><span style="font-size: 0.85em">検証ポイント② 標準ではUDP接続が失敗していた</span></h2>

<div class="net-side">
<img src="/images/net/netv-egress.svg" style="height: 340px" />
<div class="net-note">

- Discordのボイスチャットにbotを入れてみたら、<strong>接続に失敗</strong>した
- 原因をたどると、音声を送受信する<strong>UDP</strong>の接続が失敗していた
- 標準のネット接続（INTERNET_EGRESS）では、外向きのUDPが通らない

</div>
</div>

<style>
.net-side { display: flex; align-items: center; justify-content: center; gap: 2.5rem; margin-top: 0.2rem; }
.net-note { width: 22rem; }
.net-note li { font-size: 1rem !important; line-height: 1.6 !important; }
</style>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<h2><span style="font-size: 0.85em">検証ポイント② 標準ではUDP接続が失敗していた</span></h2>

<div class="net-cmp">
<div><div class="net-label">INTERNET_EGRESS（標準）</div><img src="/images/net/netv-egress.svg" style="height: 320px" /></div>
<div><div class="net-label">VPC_EGRESS</div><img src="/images/net/netv-nat-gateway.svg" style="height: 320px" /></div>
</div>

<div class="text-center text-xl mt-2"><strong>VPC_EGRESS</strong>なら、UDP接続ができる</div>

<style>
.net-cmp { display: flex; justify-content: center; align-items: flex-start; gap: 2.5rem; margin-top: 0.4rem; }
.net-label { font-weight: bold; font-size: 0.95rem; margin-bottom: 0.2rem; }
</style>

---
layout: center
---

<div>
  <h2>VPC_EGRESSにすると、<br>ボイスチャットに入れました</h2>
  <h2 v-click class="mt-6">100秒以上かかっていたbotの起動時間が<br><strong>約10秒</strong>に………！</h2>
  <h2 v-click class="mt-6">でも、<img src="/images/aws/nat-gateway.svg" class="inline h-12 align-middle" /> <strong>NAT Gateway</strong>が高すぎて…</h2>
</div>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

## 悩みどころ コストが見合わない

<div class="net-side">
<img src="/images/net/netv-nat-gateway.svg" style="height: 340px" />
<div class="net-note">

- NAT Gatewayは、いつ呼ばれてもいいように<strong>1か月ずっと置いておく</strong>
- 1か月のコスト
  - (0.062 ＋ パブリックIPv4 0.005) ドル × 730時間
  - ≒ <strong>約49ドル</strong>（＋通信量）
- 今のFargateは月約2.6ドル。個人で使うには<strong>高すぎる</strong>
  - <Kogoe>東京リージョン、オンデマンドの単価</Kogoe>

</div>
</div>

<style>
.net-side { display: flex; align-items: center; justify-content: center; gap: 2.5rem; margin-top: 0.2rem; }
.net-note { width: 24rem; }
.net-note li { font-size: 1rem !important; line-height: 1.6 !important; }
</style>

<style>
.net-side { display: flex; align-items: center; justify-content: center; gap: 2.5rem; margin-top: 0.2rem; }
.net-note { width: 22rem; }
.net-note li { font-size: 1rem !important; line-height: 1.6 !important; }
</style>


---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">NAT Gatewayを使わずに済まないか。Fargateではどうしていたかというと</div>

## Fargateはどうしていたか

<div class="net-side">
<img src="/images/net/netv-fargate.svg" style="height: 340px" />
<div class="net-note">

- パブリックサブネットに置いて、<strong>パブリックIP</strong>で外に出ていた（NATなし）
- アウトバウンドだけ許す<strong>セキュリティグループ</strong>で守っていた
  - <Kogoe>本当はプライベートサブネットに置くのが定石。個人で使うツールなので、コストを優先している</Kogoe>

</div>
</div>

<style>
.net-side { display: flex; align-items: center; justify-content: center; gap: 2.5rem; margin-top: 0.2rem; }
.net-note { width: 22rem; }
.net-note li { font-size: 1rem !important; line-height: 1.6 !important; }
</style>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

<div class="text-sm opacity-70">Lambda MicroVMsも同じ手でいこうと思ったら</div>

## Lambda MicroVMsはパブリックIPを持てない

<div class="net-side">
<img src="/images/net/netv-microvms-public.svg" style="height: 340px" />
<div class="net-note">

- Lambda MicroVMsは<strong>パブリックIPを持てない</strong>
  - <Kogoe>Lambda関数ではENIにElastic IPを付ける非推奨の方法があったけど、MicroVMsはENIがアカウントから見えず、それもできない</Kogoe>
- パブリックサブネットに置いても、インターネットに出られない
- インターネットにアクセスするために<strong>NAT</strong>が必要になる

</div>
</div>

<style>
.net-side { display: flex; align-items: center; justify-content: center; gap: 2.5rem; margin-top: 0.2rem; }
.net-note { width: 22rem; }
.net-note li { font-size: 1rem !important; line-height: 1.6 !important; }
</style>

---
chapter: Lambda MicroVMsを試す
---

<ChapterLabel />

## コストを比べると

<Kogoe>月20時間使う場合</Kogoe>

<div class="mt-3 flex flex-col gap-2">
  <div class="bar-row"><span class="bar-name">ECS Fargate（今）</span><span class="bar" style="width: 19px"></span><span>約2.6ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NATインスタンス</span><span class="bar" style="width: 102px"></span><span>約14ドル</span></div>
  <div class="bar-row"><span class="bar-name">Lambda MicroVMs＋NAT Gateway</span><span class="bar" style="width: 400px"></span><span>約55ドル</span></div>
</div>

<div class="cost-note">

- Lambda MicroVMs自体は少し高いくらい
- NATはいつ呼ばれてもいいように、一か月ずっと立てておく<strong>固定費</strong>になる
  - <Kogoe>必要なときだけNATを立てると起動が遅くなる。使う時間を絞っても、本当に使わないのは寝ている2:00〜7:00くらい</Kogoe>

</div>

<BottomLink href="https://aws.amazon.com/lambda/pricing/" title="AWS Lambda pricing" />

<Overlay>
  ということで、<strong>コストで悩んでいます</strong>…
</Overlay>

<style>
.bar-row { display: flex; align-items: center; gap: 0.8rem; font-size: 0.95rem; white-space: nowrap; }
.cost-note { margin-top: 0.8rem; padding-left: 1.6rem; }
.cost-note ul ul { padding-left: 1.6rem; }
.cost-note li { font-size: 0.95rem !important; line-height: 1.5 !important; margin: 0.1rem 0 !important; }
.bar-name { width: 18rem; flex: none; }
.bar { display: inline-block; height: 1.4rem; background: #3498db; border-radius: 3px; flex: none; }
</style>

---
layout: center
hide: true
---

<div>
  Fargateのままチューニングしたら
  <h2><strong>100秒以上</strong> → <strong>約30秒</strong>に！</h2>
  <Kogoe class="mt-6">その話はまたどこかで</Kogoe>
</div>

---
layout: center
hide: true
---

<div>
  Lambda MicroVMsはコストに見合わなかったけど…
  <h2>そもそも<strong>コンテナの起動</strong>って<br>速くできないの？</h2>
</div>

---
chapter: 起動にかかる時間を見る
hide: true
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
hide: true
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
hide: true
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
hide: true
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
hide: true
---

<ChapterLabel />

## 読み上げコンテナはSOCIと相性がいい

<br>

- 読み上げのVOICEVOXには、話者ごとの音声モデルが入っているので<strong>大きい</strong>
- 起動のときは、モデルの本体は読まない

---
chapter: イメージの取得を速くする
hide: true
---

<ChapterLabel />

<div class="text-sm opacity-70">入れてみると</div>

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="SOCIなしはイメージの取得37.5秒で全部立ち上がるまで約64秒。SOCIありは取得3.3秒で約37秒。ただしDiscord botの起動は1.5秒から4.7秒、読み上げの起動は0.8秒から9.1秒に延びた" class="mx-auto" style="width: 780px" />

<div class="text-center text-lg">イメージの取得は37.5秒から<strong>3.3秒</strong>になった</div>

---
chapter: イメージの取得を速くする
hide: true
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
hide: true
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
hide: true
---

<ChapterLabel />

<div class="text-sm opacity-70">ヘルスチェックを5秒にする手もあるけど、そもそも待たなければいい</div>

## Discord botだけ先に起動する

<br>

- Discord botだけ先に起動して、ボイスチャットに入るようにした
- 準備ができていなくても、声や文章はためておいて、準備できたら流す

---
chapter: ほかのコンテナを待たない
hide: true
---

<ChapterLabel />

## コンテナを待たずに起動した結果

<InlineSvg src="chart-nowait.svg" label="全部のコンテナを待つと、Discord botは読み上げのヘルスチェック合格まで30.0秒待ってから起動して約66秒。Discord botだけ待つと約36秒" class="mx-auto" style="width: 720px" />

<div class="text-center text-lg">全部のコンテナを待つと約66秒、Discord botだけなら<strong>約36秒</strong></div>

---

## まとめ

<div class="text-2xl mt-6 text-center">起動が<strong>100秒以上から約10秒</strong>になりました</div>

<br>

- 使えるコンテナは1つだけなので、3つを1つにまとめた
  - <Kogoe>スナップショットは起動した状態で撮るので、起動は遅くならない</Kogoe>
- UDPはVPC_EGRESSにすれば通る
- ただ、NAT Gatewayが高くて、コストで悩んでいる

---
hide: true
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

