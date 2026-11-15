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
  <h2>コンテナアプリの起動を<br>早くする話</h2>
  <div class="text-xl mt-6">起動に時間がかかって困っていたので、改善してみた</div>
</div>

---

<!-- slide-id: s-c09c833bf636d5b9 -->
<div class="kari">仮：定義の言い方は未定</div>

<div class="flex items-center gap-4">
  <img src="/images/discord.svg" class="h-12" />
  <h2 class="!m-0">自作のDiscord音声botとは？</h2>
</div>

<div class="text-lg mt-3">Discordのボイスチャンネルで<strong>読み上げと文字起こし</strong>をするbot</div>

<InlineSvg src="bot-task.svg" label="1つのECSタスク（Fargate）の中に、bot、読み上げ（VOICEVOX）、文字起こしの3つのコンテナがある" class="mx-auto mt-8" style="width: 760px" />

<div class="text-xl mt-6">→ 3つのコンテナを1つのECSタスクにまとめて動かしている</div>

<!--
仮の札: 構成まとめ（2026-11-15）には「Discord音声bot（読み上げ＝VOICEVOX、文字起こし、botの3コンテナを1タスクにまとめた構成）」とだけあり、botを一言で言う定義の文は本人の言葉がないため。
-->

---
layout: center
---

<!-- slide-id: s-87cada606e6f210e -->
<div class="kari">仮：アプリの特性の言い方は未定</div>

<div>
  このbotは、話したいときだけECSタスクを起動するので
  <h2>起動が遅いと、<br>話し始めるまで待たされる</h2>
</div>

<!--
仮の札: 構成まとめでは「アプリの説明→特性→その特性を元に改善したかった」の流れだけが決まっていて、特性の中身と言い方は本人の言葉がないため。「使うときだけ起動する」は、前のデッキに置いてあった仮の中身から取った。
-->

---
chapter: 起動にかかる時間を見る
---

<!-- slide-id: s-e1e48e9fc8821ccd -->
<ChapterLabel />

<div class="text-sm opacity-70">まず</div>

## 起動にかかる時間の内訳

<InlineSvg src="chart-breakdown.svg" label="改善前の起動を1本のタイムラインで表した図。全体約106秒のうち、タスクの準備のあとにイメージのプル37.5秒、読み上げの起動0.8秒、ヘルスチェック待ちを挟んでbotの起動1.5秒" class="mx-auto mt-4" style="width: 800px" />

<div class="text-xl mt-4" v-click>→ イメージのプルが大きな塊</div>
<div class="text-xl mt-2" v-click>→ 読み上げ（VOICEVOX）のコンテナイメージが約1.9GBと大きいから</div>

<!--
タイムラインの順番と「その他」の長さは、LT #40 の記録の流れに合わせた: 準備 → プル 37.5秒 → プル後 8.0秒 → 読み上げ起動 0.8秒 → 待ち 29.2秒 → bot起動 1.5秒 → VCへ接続 0.9秒。全体が約106秒になるよう、準備の長さを残りで決めている。
-->

---
layout: center
chapter: イメージのプルを速くする
---

<!-- slide-id: s-9969bbcc92d8cef5 -->
<ChapterLabel />

<div>
  イメージのプルが大きな塊なので
  <h2>SOCIインデックスで<br>プル時間を短くする</h2>
</div>

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

<InlineSvg src="soci-lifecycle.svg" label="コンテナが動くまでの流れ pull → create → start。pull ではECRリポジトリのSOCIインデックスなど最低限だけ読み込み、start のときにコンテナイメージから必要なファイルを読み取る" class="mx-auto mt-2" style="width: 600px" />

<div class="soci-points">

- コンテナイメージのレイヤーに対してインデックスを作成することで、<br>コンテナ起動時に必要なファイルだけ読み取って起動する
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

<!-- slide-id: s-7c809e7e8d360db8 -->
<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg mt-3">いつもの起動と比べると、<br>イメージのプルは速くなるが、コンテナの起動にはいつもより時間がかかる</div>

<InlineSvg src="soci-compare.svg" label="いつもの起動はpullでイメージを全部取得するので長い。SOCIインデックスを使うとpullは短くなるが、startが長くなる" class="mx-auto mt-10" style="width: 760px" />

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-7067122156c4c57a -->
<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスの仕組み</h2>
</div>

<div class="text-lg mt-3">プルのときは、イメージから最小限のファイルしか取得しない</div>

<InlineSvg src="soci-mechanism.svg" label="pullのときは、ECRリポジトリからSOCIインデックス（レイヤーの目次であるzTOC）と小さいレイヤーだけを取得する。startのときに足りないファイルは、zTOCで探して、スパンごとに区切られた大きいレイヤーから取得する" class="mx-auto mt-3" style="width: 680px" />

<div class="text-lg mt-3" v-click>→ 起動時に足りないファイルを、zTOCを使ってスパンごとに区切られたイメージレイヤーから探して取得する</div>

<!--
プル時に取るのは、manifest/config・SOCIインデックス・全レイヤーのzTOC（イメージの約1〜3%）と、zTOCが作られない小さいレイヤー（既定10MiB未満）の全量。
大きなレイヤーの中身は取らずに起動する。起動後のバックグラウンド取得も既定で走る。
-->

---
chapter: イメージのプルを速くする
---

<!-- slide-id: s-67d1a97a584737a0 -->
<ChapterLabel />

<div class="text-sm opacity-70">入れてみると</div>

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="改善前とSOCIインデックスを使った起動の比較。全体は約106秒から48.6秒、イメージのプルは37.5秒から3.3秒に短縮。読み上げの起動は0.8秒から9.1秒、botの起動は1.5秒から4.7秒に伸びた" class="mx-auto mt-2" style="width: 760px" />

<div class="text-xl mt-2" v-click>→ プルは37.5秒 → 3.3秒。その代わり、コンテナの起動は伸びた</div>

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

<InlineSvg src="chart-total.svg" label="全体の起動時間は、改善前の約106秒から、SOCIインデックスで48.6秒、さらに待たずに起動して32.7秒" class="mx-auto mt-10" style="width: 760px" />

<div class="text-center text-2xl mt-10" v-click>100秒以上 → 約30秒台に！</div>

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
