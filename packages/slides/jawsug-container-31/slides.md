---
layout: title
drawings:
  persist: false
transition: fade
title: SOCIインデックスでコンテナの起動を早くしてみた
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<!-- slide-id: s-2e49c3400c263186 -->
# <span style="font-size: 0.95em; line-height: 1.4; display: inline-block"><span style="color:#ffd54f">SOCIインデックス</span>で<br>コンテナの起動を早くしてみた</span>

<div style="color: #fff; opacity: 1">

2026.11.16（月）\
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

<!-- slide-id: s-3ff98294b8253ca6 -->
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

<!-- slide-id: s-8902058138e3d09a -->
<div>
  今日は
  <h2>ECSにホストしたコンテナアプリの<br>起動を早くする話</h2>
  <div class="text-xl mt-6">起動時間が遅くて困っていたため、改善を図りました</div>
</div>

---

<!-- slide-id: s-c09c833bf636d5b9 -->
<div class="flex items-center gap-4">
  <img src="/images/discord.svg" class="h-12" />
  <h2 class="!m-0">自作のDiscord音声botとは？</h2>
</div>

<div class="text-lg mt-2"><strong>Claude Codeと通話できる</strong>Discord bot</div>

<InlineSvg src="bot-overview.svg" label="ユーザーがボイスチャンネルで話すと、botが文字起こししてテキストチャンネルに投稿する。Claude CodeはChannelsでテキストチャンネルに接続していて、返事をテキストチャンネルに返す。botがその返事をボイスチャンネルで読み上げる" class="mx-auto mt-2" style="width: 600px" />

---

<!-- slide-id: s-5b1e7c0a94d2f683 -->
<div class="flex items-center gap-4">
  <img src="/images/discord.svg" class="h-12" />
  <h2 class="!m-0">自作のDiscord音声botとは？</h2>
</div>

<div class="text-lg mt-3">3つのコンテナを<strong>1つのECSタスク</strong>としてFargate上に動かしています</div>

<InlineSvg src="bot-task.svg" label="1つのECSタスク（Fargate）の中に、bot、読み上げ（VOICEVOX）、文字起こし（Transcribe Streaming）の3つのコンテナがある" class="mx-auto mt-8" style="width: 760px" />

---
layout: center
---

<!-- slide-id: s-87cada606e6f210e -->
<div>
  費用を抑えるために、使いたい時にタスクを起動して使い終わったら止めている
  <h2>毎回の起動に<br>約77秒かかっていた</h2>
  <div class="text-xl mt-6">起動時間が長いと音声会話のハードルが高くなり、<br>使いたい時も面倒くさくて使わなかったことがある</div>
</div>

---
chapter: 起動にかかる時間を見る
---

<!-- slide-id: s-e1e48e9fc8821ccd -->
<ChapterLabel />

<div class="text-sm opacity-70">まず</div>

## 改善前の起動時間の内訳

<InlineSvg src="chart-breakdown.svg" label="改善前の起動を1本のタイムラインで表した図。全体約77秒のうち、イメージのプル37.5秒、読み上げの起動0.8秒、botの起動1.5秒。残りはその他の起動処理" class="mx-auto mt-4" style="width: 800px" />

<div class="text-xl mt-4" v-click>→ 一番大きいのはイメージの取得（プル）。VOICEVOXのコンテナイメージが約1.9GBと、かなり大きいから</div>
<div class="text-xl mt-2" v-click>→ まずはこのプルの時間を短くするところから改善していきます</div>

<!--
タイムラインの順番と「その他」の長さは、LT #40 の記録の流れに合わせた: その他 → プル 37.5秒 → プル後 8.0秒 → 読み上げ起動 0.8秒 → bot起動 1.5秒 → VCへ接続 0.9秒。
全体はヘルスチェックを改善した後の約77秒（2026-11-16 本人の決定。ヘルスチェックの説明は話に入れないので、待ちの区切りは図から外した）。最初の「その他」の長さを残りで決めている。
-->

---
layout: center
chapter: イメージのプルを速くする
---

<!-- slide-id: s-9969bbcc92d8cef5 -->
<ChapterLabel />

<div>
  さっきの内訳で一番大きかったのは
  <h2>コンテナイメージのプル</h2>
  <div class="text-xl mt-6">読み上げコンテナに使っているVOICEVOXのイメージが約1.9GBと大きい</div>
  <div class="text-lg mt-4 opacity-80">通常、ECSタスクを起動する時は全てのイメージをプルしてからコンテナの起動が始まるため、コンテナのイメージサイズが起動時間に直結する</div>
</div>

---
chapter: イメージのプルを速くする
---

<ChapterLabel />

## コンテナイメージのプルを速くするためには

<div class="means mt-8">
  <div class="mean ng">
    <div class="mark">×</div>
    <div class="name">イメージの軽量化</div>
    <div class="why">VOICEVOXはOSSとして提供されているものをそのまま使うため、できない</div>
  </div>
  <div class="mean ng">
    <div class="mark">×</div>
    <div class="name">イメージのキャッシュ</div>
    <div class="why">FargateはECSタスクごとに環境が独立しているため、できない</div>
  </div>
  <div class="mean ok">
    <div class="mark">○</div>
    <div class="name">イメージの遅延読み込み</div>
    <div class="why">SOCI Snapshotterによって実現する</div>
  </div>
</div>

<div class="text-xl mt-8" v-click>→ イメージの遅延読み込みをSOCI Snapshotterによって実現していく</div>

<style>
.means { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; }
.mean { border: 2px solid #c9d0d9; border-radius: 12px; padding: 1rem 1.1rem; background: #fff; }
.mean .mark { font-size: 1.6rem; font-weight: 700; color: #6b7684; line-height: 1.2; }
.mean .name { font-size: 1.25rem; font-weight: 700; margin-top: 0.3rem; }
.mean .why { font-size: 0.95rem; color: #6b7684; margin-top: 0.6rem; line-height: 1.5; }
.mean.ok { border-color: #0E8A6E; background: #e9f5f1; }
.mean.ok .mark, .mean.ok .name { color: #0E8A6E; }
</style>

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-156016a127432fe1 -->
<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCI（Seekable OCI）とは？</h2>
</div>

<div class="text-lg mt-2">コンテナイメージを<strong>遅延読み込み</strong>することでコンテナの起動を早くするための技術</div>

<InlineSvg src="soci-lifecycle.svg" label="コンテナが動くまでの流れ pull → create → start。pull ではECRリポジトリのSOCIインデックスなど最低限だけ読み込み、start のときにコンテナイメージから必要なファイルを読み取る" class="mx-auto mt-2" style="width: 560px" />

<div class="soci-points">

- イメージをプルする時に必要最低限のファイルのみ取得してコンテナを起動し、<br>他のファイルはアプリの実行中に必要になった時に取得する
- コンテナイメージのレイヤーに対してインデックスを作成することで実現している
- インデックスはコンテナイメージを作り直さずに後付けできる

</div>

<style>
.soci-points { margin-top: 0.2rem; }
.soci-points ul { margin: 0; }
.soci-points li { font-size: 1rem !important; line-height: 1.45 !important; margin-bottom: 0 !important; }
</style>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---
chapter: イメージのプルを速くする
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg mt-2">仕組みは、レイヤー・span・zTOCという3つの言葉で説明できる</div>

<InlineSvg src="soci-terms.svg" label="コンテナイメージはレイヤーを重ねたもの。レイヤーはTARアーカイブを圧縮したもので、zTOCがspanという単位に区切っている。zTOCはレイヤーのインデックスで、どのファイルがレイヤーの中のどこにあるかが書いてある" class="mx-auto mt-1" style="width: 540px" />

<div class="text-base mt-2"><strong class="term">レイヤー</strong>：イメージを構成する層。Dockerfileに書いてある区切りごとにTARアーカイブを圧縮したもの</div>
<div class="text-base mt-1"><strong class="term">zTOC</strong>：レイヤーのインデックス。どのファイルが、圧縮されたレイヤーの中のどこにあるかが書いてある</div>
<div class="text-base mt-1"><strong class="term">span</strong>：zTOCがレイヤーを区切った単位。ファイルを取りに行くときは、このspan単位で取得する</div>

<style>
.term { color: var(--ink) !important; }
</style>

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-7c809e7e8d360db8 -->
<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg mt-3">コンテナの起動は、イメージのプル（pull）→ コンテナの作成（create）→<br>コンテナの起動（start）という順に進む</div>

<InlineSvg src="soci-compare.svg" label="遅延読み込みなしは、pullでイメージ全体を取得してレイヤーを全部展開し、ファイルが全部そろってからコンテナを作成する。SOCIは、pullでイメージ全体は取得せず、全てのレイヤーを取得していない状態でコンテナを作成する" class="mx-auto mt-10" style="width: 760px" />

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-7067122156c4c57a -->
<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg mt-3">プルで取得するのは、SOCIインデックスとzTOC、<br>10MiB未満の小さいレイヤーだけ</div>

<InlineSvg src="soci-mechanism.svg" label="pullのときは、ECRリポジトリからSOCIインデックス（レイヤーのインデックスであるzTOC）と10MiB未満の小さいレイヤーだけを取得する。startのときに足りないものは、zTOCから探して、span単位でレイヤーから取得する" class="mx-auto mt-1" style="width: 500px" />

<div class="text-lg mt-2" v-click>→ 起動時、アプリがファイルを読むたびに足りないものをzTOCから探して、span単位で取得する</div>
<div class="text-lg mt-1" v-click>→ 必要になった分から読み込むため、遅延読み込みと呼ばれている</div>

<!--
プル時に取るのは、manifest/config・SOCIインデックス・全レイヤーのzTOC（イメージの約1〜3%）と、zTOCが作られない小さいレイヤー（既定10MiB未満）の全量。
大きなレイヤーの中身は取らずに起動する。起動後のバックグラウンド取得も既定で走る。
-->

---
chapter: イメージのプルを速くする
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスを適用する</h2>
</div>

<div class="text-lg mt-3">遅延読み込みが効果を発揮しやすいのは、圧縮後のサイズが<strong>250MiB</strong>を超えるコンテナイメージ</div>

<div class="apply mt-8">
  <div class="target">
    <img src="/images/aws/ecs-container.svg" class="h-14" />
    <div class="name">Discord botコンテナ</div>
  </div>
  <div class="target">
    <img src="/images/aws/ecs-container.svg" class="h-14" />
    <div class="name">読み上げコンテナ<br><span class="sub">VOICEVOX</span></div>
  </div>
</div>

<div class="text-lg mt-8">→ この2つにSOCIインデックスを適用する</div>
<div class="text-base mt-3 opacity-80">適用には、SOCI Index Builder や SOCI CLI が一般的だが、<br>CDKの deploy-time-build Construct がSOCIインデックスの構築に対応していたので、こちらを利用した</div>

<style>
.apply { display: flex; justify-content: center; gap: 2rem; }
.apply .target { display: flex; align-items: center; gap: 1rem; border: 2px solid #c9d0d9; border-radius: 12px; padding: 0.8rem 1.6rem; min-width: 300px; }
.apply .name { font-size: 1.25rem; font-weight: 700; line-height: 1.3; }
.apply .sub { font-size: 0.9rem; font-weight: 400; color: #6b7684; }
</style>

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-67d1a97a584737a0 -->
<ChapterLabel />

<div class="text-sm opacity-70">入れてみると</div>

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="改善前とSOCIインデックスを使った起動の比較。全体は約77秒から約49秒、イメージのプルは37.5秒から3.3秒に短縮。読み上げの起動は0.8秒から9.1秒、botの起動は1.5秒から4.7秒に伸びた" class="mx-auto mt-0" style="width: 580px" />

<div class="text-base mt-1" v-click>→ イメージのプルは圧倒的に速くなったが、<br>その代わりにコンテナの起動時間が伸びた<br><span class="text-sm opacity-80">（最小限のファイルしか取らなかったため、起動時に足りないファイルがあるたびに取りに行く）</span></div>
<div class="text-2xl font-bold mt-2" v-click>全体で約29秒も短縮できました！</div>

---
chapter: ほかのコンテナを待たない
---

<!-- slide-id: s-a4dcee05fcc576d6 -->
<ChapterLabel />

<div class="text-sm opacity-70">次に</div>

## botは読み上げの読み込みを待っていた

<div class="text-lg mt-2">botは、読み上げ（VOICEVOX）の読み込みが終わるのを待ってから起動していた</div>

<InlineSvg src="wait-before.svg" label="読み上げのコンテナが読み込みを終えるまで、botのコンテナは待ち、読み込みが完了してから起動してボイスチャンネル（VC）に入る" class="mx-auto mt-8" style="width: 760px" />

---
chapter: ほかのコンテナを待たない
---

<!-- slide-id: s-150b4c72a8603b32 -->
<ChapterLabel />

<div class="kari">仮：言い方は未定</div>

## botは待たずに起動する

<div class="text-lg mt-2">botは読み上げの読み込みを待たずに起動して、先にボイスチャンネルに入る</div>

<InlineSvg src="wait-after.svg" label="botのコンテナは読み上げの読み込みを待たずに起動してボイスチャンネル（VC）に入り、声や文章をためておき、読み上げの準備ができたら流す" class="mx-auto mt-8" style="width: 760px" />

<!--
仮の札: 構成まとめ（2026-11-15）で「待たずに起動する（言い方の詳細は後で詰める）」となっているため。図の「声や文章をためる」「準備ができたら流す」は構成まとめの「声や文章はためておいて、準備ができたら流す」から。
-->

---
chapter: ほかのコンテナを待たない
---

<!-- slide-id: s-4a40864a983f1fa8 -->
<ChapterLabel />

## 待たずに起動した結果

<InlineSvg src="chart-total.svg" label="全体の起動時間は、改善前の約77秒から、SOCIインデックスで約49秒、さらに待たずに起動して32.7秒" class="mx-auto mt-10" style="width: 760px" />

<div class="text-center text-2xl mt-10" v-click>約77秒 → 約30秒台に！</div>

---
layout: center
---

<!-- slide-id: s-03a0a2c107c9bb52 -->
<div class="kari">仮：一文の言い回しは未定</div>

<div class="text-sm opacity-70">まとめ</div>

<div class="summary mt-6">
  SOCIインデックスを使うと<br><strong>イメージのプル時間が速くなる</strong>から<br>起動を短くできた！！！
</div>

<style>
.summary { font-size: 2rem; font-weight: 700; line-height: 1.6; text-align: center; }
</style>

<!--
仮の札: 構成まとめ（2026-11-15）では「という雰囲気の一文」とされていて、言い回しが決まっていないため。
-->

---

<!-- slide-id: s-8bcd6cdc6f796018 -->
<div class="kari">仮：載せる部品は未定</div>

<div class="text-sm opacity-70">補足</div>

## 調べてるうちに見つけたCDKの便利な部品

<br>

- `NatInstanceProviderV2`
  - <Kogoe>NATインスタンスを作れる</Kogoe>
- `SociIndexV2Build`
  - <Kogoe>SOCIインデックスを作れる（@cdklabs/deploy-time-build）</Kogoe>

<!--
時間があれば話す。無ければ飛ばす（構成まとめ 2026-11-15）。
仮の札: 余談を入れることは決まっているが、どの部品を載せるかは本人の言葉が記録にないため。前のデッキに置いてあった中身をそのまま残した。
-->

---
layout: ending
---

<!-- slide-id: s-bd274433b54aefeb -->
# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
