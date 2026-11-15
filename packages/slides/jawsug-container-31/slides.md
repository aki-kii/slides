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

# <span style="font-size: 0.95em; line-height: 1.4; display: inline-block"><span style="color:#ffd54f">SOCIインデックス</span>で<br>コンテナの起動を早くしてみた</span>

<div class="opacity-70">

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
  今日は
  <h2><strong>コンテナアプリの起動</strong>を<br>早くする話</h2>
  <div class="text-xl mt-6">起動に時間がかかって<strong>困っていた</strong>ので、改善してみた</div>
</div>

---

<div class="kari">仮：使う場面の言い方は未定</div>

## 自作のDiscord音声botとは？

<div class="text-lg mt-2">DiscordのボイスチャンネルでClaude Codeと<strong>通話する仕組み</strong>を作りました</div>

<InlineSvg src="bot-overview.svg" label="Discordのボイスチャンネルで話した声を音声botが文字起こししてテキストチャンネルに書き、Claude Code botの返事を音声botが読み上げる。音声botはECS Fargate、Claude Codeは手元のPCで動く" class="mx-auto mt-2" style="width: 600px" />

<div class="text-xl mt-2" v-click>→ 話した声を<strong>文字起こし</strong>してClaude Codeに渡し、返事は<strong>読み上げ</strong>で聞く</div>
<div class="text-xl mt-1" v-click>→ 画面を見なくても、<strong>声だけで</strong>Claude Codeとやりとりできる</div>

<!--
仮の札: 「声だけでClaude Codeとやりとりする」は、既存のスライドの「Claude Codeと通話する仕組み」と life の構成まとめ（読み上げ・文字起こし・bot）から書いた。どんな場面で使っているか（画面を見なくても、の部分）は本人の言葉が記録にないため。
-->

---

<div class="kari">仮：特性の言い方は未定</div>

## 自作のDiscord音声bot

<div class="text-lg mt-2">読み上げ・文字起こし・botの<strong>3つのコンテナ</strong>を1つのECSタスクで動かす</div>

<InlineSvg src="bot-task.svg" label="ECSタスク（Fargate）の中に、Discord bot、読み上げ（VOICEVOX）、文字起こしの3つのコンテナがある" class="mx-auto mt-4" style="width: 700px" />

<div class="text-xl mt-4" v-click>→ コストを抑えるため、<strong>使うときだけ</strong>ECSタスクを起動する</div>
<div class="text-xl mt-1" v-click>→ 起動が遅いと、そのぶん<strong>話せるまで待たされる</strong>ので、起動を早くしたい</div>

<!--
仮の札: 構成まとめでは「アプリの説明→特性→その特性を元に改善したかった」の流れだけが決まっていて、特性の言い方は本人の言葉がないため。
-->

---
chapter: 起動にかかる時間を見る
---

<ChapterLabel />

<div class="text-sm opacity-70">まず</div>

## 起動にかかる時間の内訳

<InlineSvg src="chart-breakdown.svg" label="改善前の起動を1本のタイムラインで表した図。全体約106秒のうち、タスクの準備のあとにイメージの取得37.5秒、その他を挟んで読み上げの起動0.8秒、ヘルスチェック待ちを挟んでbotの起動1.5秒" class="mx-auto mt-4" style="width: 780px" />

<div class="text-xl mt-4" v-click>→ <strong>イメージの取得</strong>が大きな塊</div>
<div class="text-lg mt-1 pl-8" v-click>読み上げ（VOICEVOX）のイメージが<strong>約1.9GB</strong>と大きいから <Kogoe>削りようがない</Kogoe></div>

<!--
タイムラインの順番と「その他」の長さは、LT #40 の記録（2026-10-14 23:14 の回）の流れに合わせた: 準備 約25秒 → 取得 37.5秒 → 取得後 8.0秒 → 読み上げ起動 0.8秒 → 待ち 29.2秒 → bot起動 1.5秒 → VCへ接続 0.9秒。全体が約106秒になるよう、準備を約28秒で描いている。
図の表記（2026-11-15 本人コメント対応）: 準備は「タスクの準備」、待ち 29.2秒は「ヘルスチェック待ち」と表記した。待ちの中身は、botが読み上げ（VOICEVOX）のヘルスチェック完了を待つ時間（依存条件 HEALTHY の待ち）。取得後 8.0秒は小さいので「その他」のまま。
-->

---
layout: center
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div>
  イメージの取得が大きな塊なので
  <h2><strong>SOCIインデックス</strong>で<br>プル時間を短くする</h2>
</div>

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<div class="text-lg mt-3">コンテナイメージを<strong>遅延読み込み</strong>できる仕組み<Kogoe>（AWSが作ったOSS）</Kogoe></div>

<InlineSvg src="soci-flow.svg" label="いつもの起動はプルでイメージを全部取得してから起動する。SOCIインデックスではプルは最小限なので速くなるが、起動時に足りないファイルを取るので起動は長くなる" class="mx-auto mt-6" style="width: 720px" />

<div class="text-xl mt-6" v-click>→ <strong>プルは速くなる</strong>けど、<strong>起動はいつもより時間がかかる</strong></div>

<BottomLink href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html" title="Fargate tasks and services - Lazy loading container images using Seekable OCI" />

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">仕組みの前に</div>

## イメージレイヤー・span・zTOCとは？

<InlineSvg src="soci-terms.svg" label="コンテナイメージはレイヤーを重ねたもの。大きいレイヤーはspanという単位に区切られ、zTOCというレイヤーの目次で、どのファイルがどのspanにあるかが分かる" class="mx-auto mt-2" style="width: 640px" />

<div class="text-lg mt-3"><strong>イメージレイヤー</strong>：イメージを作っている層。ふだんのプルでは丸ごと取得する</div>
<div class="text-lg mt-1"><strong>span</strong>：レイヤーを区切った、取得の単位</div>
<div class="text-lg mt-1"><strong>zTOC</strong>：レイヤーごとの目次。どのファイルがどのspanにあるかが分かる</div>

<!--
事実は research_notes の soci-pull-mechanism レポートによる。zTOC はファイルの情報（TOC）と、圧縮の途中から展開するためのチェックポイント（zInfo）の2つでできている。gzip は途中から展開できないので、このチェックポイントが要る。span は既定で4MiB（展開後のサイズ）。zTOC は既定で10MiB以上のレイヤーにだけ作られる。
-->

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="flex items-center gap-4">
  <img src="/images/aws/ecr.svg" class="h-12" />
  <h2 class="!m-0">SOCIインデックスとは？</h2>
</div>

<div class="text-lg mt-3">プルのときは、イメージから<strong>最小限のファイル</strong>しか取得しない</div>

<InlineSvg src="soci-mechanism.svg" label="プル時はSOCIインデックスとzTOC、小さいレイヤーだけを取得する。起動時に足りないファイルは、zTOCを使ってspanごとに区切られたイメージレイヤーから探して取得する" class="mx-auto mt-3" style="width: 700px" />

<div class="text-lg mt-3" v-click>→ 起動時に足りないファイルを、<strong>zTOC</strong>を使って<strong>spanごと</strong>に区切られたレイヤーから探して取得する</div>

<!--
プル時に取るのは、manifest/config・SOCIインデックス・全レイヤーのzTOC（イメージの約1〜3%）と、zTOCが作られない小さいレイヤー（既定10MiB未満）の全量。
大きなレイヤーの中身は取らずに起動する。起動後のバックグラウンド取得も既定で走る。
-->

---
chapter: イメージの取得を速くする
---

<ChapterLabel />

<div class="text-sm opacity-70">入れてみると</div>

## SOCIインデックスを入れた結果

<InlineSvg src="chart-soci.svg" label="改善前とSOCIインデックスありの比較。全体は約106秒から48.6秒、イメージの取得は37.5秒から3.3秒に短縮。読み上げの起動は0.8秒から9.1秒、botの起動は1.5秒から4.7秒に延びた" class="mx-auto mt-1" style="width: 720px" />

<div class="text-lg mt-2" v-click>→ プルは<strong>37.5秒 → 3.3秒</strong>。その代わり、コンテナの<strong>起動は延びた</strong></div>

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

<div class="text-sm opacity-70">次に</div>

## botは読み上げの準備を待っていた

<br>

- botは、読み上げ（VOICEVOX）の<strong>読み込みが終わるのを待ってから</strong>起動していた
- SOCIインデックスで、読み上げの起動が<strong>0.8秒 → 9.1秒</strong>に延びた

<div class="text-xl mt-8" v-click>→ でも、botがボイスチャンネルに入るだけなら、読み上げは<strong>まだいらない</strong></div>

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

<div class="kari">仮：言い方は未定</div>

## botは待たずに起動する

<br>

- 読み上げの準備を待たずに、botが先にボイスチャンネルに入る
- 準備ができていなくても、<strong>声や文章はためておいて</strong>、準備ができたら流す

<!--
仮の札: 構成まとめ（2026-11-15）で「待たずに起動する（言い方の詳細は後で詰める）」となっているため。
-->

---
chapter: ほかのコンテナを待たない
---

<ChapterLabel />

## 待たずに起動した結果

<InlineSvg src="chart-total.svg" label="全体の起動時間は、改善前の約106秒から、SOCIインデックスで48.6秒、さらに待たずに起動して32.7秒" class="mx-auto mt-8" style="width: 760px" />

<div class="text-center text-2xl mt-10" v-click><strong>100秒以上</strong> → <strong>約30秒台</strong>に！</div>

---

<div class="kari">仮：一文の言い回しは未定</div>

## まとめ

<div class="summary mt-16">
  SOCIインデックスを使うと<br><strong>イメージのプル時間が速くなる</strong>から<br>起動を短くできた！！！
</div>

<style>
.summary { font-size: 2rem; font-weight: 700; line-height: 1.6; text-align: center; }
</style>

<!--
仮の札: 構成まとめ（2026-11-15）では「という雰囲気の一文」とされていて、言い回しが決まっていないため。
-->

---

<div class="text-sm opacity-70">補足</div>

## 調べてるうちに見つけたCDKの便利な部品

<br>

- `NatInstanceProviderV2`
  - <Kogoe>NATインスタンスを作れる</Kogoe>
- `SociIndexV2Build`
  - <Kogoe>SOCIインデックスを作れる（@cdklabs/deploy-time-build）</Kogoe>

<!--
時間があれば話す。無ければ飛ばす。
-->

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
