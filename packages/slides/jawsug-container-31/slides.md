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

2026.11.16（月）\
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
  <h2>ECSにホストしたコンテナアプリの<br><strong>起動を早くする</strong>話</h2>
  <div class="text-lg mt-4 opacity-70">起動時間が遅くて困っていたため、改善を図りました</div>
</div>

---

<!-- slide-id: s-c09c833bf636d5b9 -->
<h2 class="!m-0">Discord音声通話bot（自作）の仕組み</h2>

<div class="text-lg"><strong>Claude Code</strong>と通話できるDiscord bot</div>

<InlineSvg src="bot-overview.svg" label="ユーザーがボイスチャンネルで話すと、botが文字起こししてテキストチャンネルに投稿する。Claude CodeはChannelsでテキストチャンネルに接続していて、返事をテキストチャンネルに返す。botがその返事をボイスチャンネルで読み上げる" class="mx-auto mt-2" style="width: 700px" />

---

<!-- slide-id: s-5b1e7c0a94d2f683 -->
<div class="flex items-center gap-4">
  <img src="/images/discord.svg" class="h-12" />
  <h2 class="!m-0">自作のDiscord音声botとは？</h2>
</div>

<div class="text-lg">3つのコンテナを<strong>1つのECSタスク</strong>としてFargate上に動かしています</div>

<InlineSvg src="bot-task.svg" label="前のページの図を薄く敷き、音声botが動くECS Fargateの箱を開いた図。1つのECSタスク（Fargate）の中に、Discord botコンテナ、読み上げコンテナ（VOICEVOX）、文字起こしコンテナ（Transcribe Streaming）の3つがある" class="mx-auto mt-3" style="width: 760px" />

<div class="text-lg mt-3">費用を抑えるために、使いたい時にタスクを起動して使い終わったら止めている</div>

---
layout: center
---

<!-- slide-id: s-87cada606e6f210e -->
<div class="text-3xl leading-relaxed">
  <p>Discord botの起動に80秒前後かかっていました</p>
  <p>起動時間が長いと使うのも億劫になります…</p>
</div>

---

<!-- slide-id: s-e1e48e9fc8821ccd -->
<div class="flex items-center gap-4">
  <img src="/images/aws/fargate.svg" class="h-12" />
  <h2 class="!m-0">ECSタスク起動のタイムライン</h2>
</div>

<InlineSvg src="chart-breakdown.svg" label="改善前のECSタスク起動を、区間ごとに段をずらして時間順に並べたタイムライン。全体約77秒。その他の起動処理、イメージのプル37.5秒、コンテナ作成など、読み上げコンテナの起動0.8秒、Discord botコンテナの起動1.5秒、その他の起動処理の順" class="mx-auto mt-2" style="width: 740px" />

<div class="text-lg mt-4 leading-relaxed">
  <p class="!my-0"><strong>一番大きいのはイメージのプル</strong></p>
  <p class="!my-0">→ イメージのプルに時間がかかっている！</p>
  <p class="!my-0 whitespace-nowrap">→ 読み上げコンテナ（VOICEVOX）のサイズが大きい（約2GB）ため</p>
</div>

<!--
タイムラインの順番と「その他」の長さは、LT #40 の記録の流れに合わせた: その他 → プル 37.5秒 → プル後 8.0秒 → 読み上げコンテナの起動 0.8秒 → Discord botコンテナの起動 1.5秒 → VCへ接続 0.9秒。
「コンテナ作成」はプル後 8.0秒の中にある（pull → コンテナ作成 → 起動）。コンテナ作成だけの実測秒数はないので、秒数は書かずに灰色（その他の起動処理）の段として位置だけを見せている。
全体はヘルスチェックを改善した後の約77秒（2026-11-16 本人の決定。ヘルスチェックの説明は話に入れないので、待ちの区切りは図から外した）。最初の「その他」の長さを残りで決めている。
-->

---

<!-- slide-id: s-ed5f48a99294093b -->
<h2 class="!m-0"><span style="font-size: 0.85em">コンテナイメージのプルを速くするためには</span></h2>

<div class="means mt-8">

- × イメージの軽量化
  - VOICEVOXはOSSとして提供されているものをそのまま使うため、できない
- × イメージのキャッシュ
  - FargateはECSタスクごとに環境が独立しているため、できない
- ○ <strong>イメージの遅延読み込み</strong>
  - SOCIによって実現する

</div>

<div class="text-xl mt-8" v-click>→ <strong>イメージの遅延読み込み</strong>をSOCIによって実現していく</div>

<style>
.means li ul { margin-top: 0.2rem; }
.means li li { font-size: 1rem; opacity: 0.7; }
</style>

---

<!-- slide-id: s-156016a127432fe1 -->
<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCI（Seekable OCI）とは？</h2>
</div>

<div class="text-lg">コンテナイメージを<strong>遅延読み込み</strong>することでコンテナの起動を早くするための技術</div>

<div class="text-base mt-2">コンテナの起動は、イメージのプル（pull）→ コンテナの作成（create）→<br>コンテナの起動（start）という順に進む</div>

<InlineSvg src="soci-compare.svg" label="ECSタスクの中でコンテナが動くまでの流れ pull → create → start。遅延読み込みなしは、pullでイメージ全体を取得してレイヤーを全部展開し、ファイルが全部そろってからコンテナを作成する。SOCIは、pullでイメージ全体は取得せず、全てのレイヤーを取得していない状態でコンテナを作成する" class="mx-auto mt-2" style="width: 720px" />

<div class="soci-points">

- イメージをプルする時に必要最低限のファイルのみ取得してコンテナを起動し、<br>他のファイルはアプリの実行中に必要になった時に取得する
- コンテナイメージのレイヤーに対してインデックスを作成することで実現している
- インデックスはコンテナイメージを作り直さずに後付けできる

</div>

<style>
.soci-points ul { margin: 0; }
.soci-points li { font-size: 1rem !important; line-height: 1.45 !important; margin-bottom: 0 !important; }
</style>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---

<!-- slide-id: s-4ecc9db345c504e2 -->
<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg">仕組みは、レイヤー・span・zTOCという3つの言葉で説明できる</div>

<InlineSvg src="soci-terms.svg" label="コンテナイメージはレイヤーを重ねたもの。レイヤーはTARアーカイブを圧縮したもので、zTOCがspanという単位に区切っている。zTOCはレイヤーのインデックスで、どのファイルがレイヤーの中のどこにあるかが書いてある" class="mx-auto mt-1" style="width: 540px" />

<div class="terms">

- **レイヤー**：イメージを構成する層。Dockerfileに書いてある区切りごとにTARアーカイブを圧縮したもの
- **zTOC**：レイヤーのインデックス。どのファイルが、圧縮されたレイヤーの中のどこにあるかが書いてある
- **span**：zTOCがレイヤーを区切った単位。ファイルを取りに行くときは、このspan単位で取得する

</div>

<style>
.terms ul { margin: 0.25rem 0 0; }
.terms li { font-size: 1rem !important; line-height: 1.45 !important; margin-bottom: 0.1rem !important; }
</style>

---

<!-- slide-id: s-7067122156c4c57a -->
<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg">プルで取得するのは、SOCIインデックスとzTOC、<br>10MiB未満の小さいレイヤーだけ</div>

<InlineSvg src="soci-mechanism.svg" label="pullのときは、ECRリポジトリからSOCIインデックス（レイヤーのインデックスであるzTOC）と10MiB未満の小さいレイヤーだけを取得する。startのときに足りないものは、zTOCから探して、span単位でレイヤーから取得する" class="mx-auto mt-1" style="width: 500px" />

<div class="text-lg mt-2" v-click>→ 起動時、アプリがファイルを読むたびに足りないものをzTOCから探して、<strong>span単位</strong>で取得する</div>
<div class="text-lg mt-1" v-click>→ 必要になった分から読み込むため、<strong>遅延読み込み</strong>と呼ばれている</div>

<!--
プル時に取るのは、manifest/config・SOCIインデックス・全レイヤーのzTOC（イメージの約1〜3%）と、zTOCが作られない小さいレイヤー（既定10MiB未満）の全量。
大きなレイヤーの中身は取らずに起動する。起動後のバックグラウンド取得も既定で走る。
-->

---

<!-- slide-id: s-3d2ba11d928be7ba -->
<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスを適用する</h2>
</div>

<div class="text-lg">遅延読み込みが効果を発揮しやすいのは、<br>圧縮後のサイズが<strong>250MiB</strong>を超えるコンテナイメージ</div>

<div class="apply mt-6">
  <div class="target">
    <img src="/images/aws/ecs-container.svg" class="h-12" />
    <div class="name">Discord botコンテナ</div>
  </div>
  <div class="target">
    <img src="/images/aws/ecs-container.svg" class="h-12" />
    <div class="name">読み上げコンテナ<br><span class="sub">VOICEVOX</span></div>
  </div>
</div>

<div class="text-xl mt-8">→ この2つに<strong>SOCIインデックス</strong>を適用する</div>
<div class="text-sm mt-2 opacity-70">適用には、SOCI Index Builder や SOCI CLI が一般的だが、<br>CDKの deploy-time-build Construct がSOCIインデックスの構築に対応していたので、こちらを利用した</div>

<style>
.apply { display: flex; justify-content: center; gap: 1.5rem; }
.apply .target { display: flex; align-items: center; gap: 0.75rem; border: 2px solid #d1d5db; border-radius: 0.75rem; padding: 0.6rem 1.4rem; min-width: 280px; }
.apply .name { font-size: 1.1rem; font-weight: 700; line-height: 1.3; }
.apply .sub { font-size: 0.875rem; font-weight: 400; opacity: 0.7; }
</style>

---

<!-- slide-id: s-67d1a97a584737a0 -->
<div class="text-sm opacity-70">入れてみると</div>

<div class="flex items-center gap-4">
  <img src="/images/aws/fargate.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスを入れた結果</h2>
</div>

<InlineSvg src="chart-soci.svg" label="改善前とSOCIインデックスを使った起動の比較。全体は約77秒から約49秒、イメージのプルは37.5秒から3.3秒に短縮。読み上げコンテナの起動は0.8秒から9.1秒、Discord botコンテナの起動は1.5秒から4.7秒に伸びた" class="mx-auto mt-1" style="width: 560px" />

<div class="text-base mt-1" v-click>→ イメージのプルは圧倒的に速くなったが、その代わりにコンテナの起動時間が伸びた<br><span class="text-sm opacity-70">（最小限のファイルしか取らなかったため、起動時に足りないファイルがあるたびに取りに行く）</span></div>
<div class="text-xl mt-2" v-click>→ 全体で<strong>約29秒</strong>も短縮できました！</div>

---
layout: center
---

<!-- slide-id: s-03a0a2c107c9bb52 -->
<div class="kari">仮：一文の言い回しは未定</div>

<div>
  <Kogoe>まとめ</Kogoe>
  <h2>SOCIインデックスを使うと<br><strong>イメージのプル時間が速くなる</strong>から<br>起動を短くできた！！！</h2>
</div>

<!--
仮の札: 構成まとめ（2026-11-15）では「という雰囲気の一文」とされていて、言い回しが決まっていないため。
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
