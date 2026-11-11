---
routerMode: hash
layout: title
drawings:
  persist: false
transition: fade
title: MuseをAI秘書にして健康管理を任せてみた
mdc: true
htmlAttrs:
  lang: ja
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

<div class="text-2xl font-normal opacity-90">自由が丘.any #1</div>

# MuseをAI秘書にして<br>健康管理を任せてみた

<div class="title-meta">

2026.11.11（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

</div>

<div class="absolute right-8 bottom-8">
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

---
layout: profile
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
transition: slide-left
---

- 普段はAWSコミュニティ（JAWS-UG）によくいます
- コーヒーが好き
- ランニングしながらAI（Grok Bot）と会話して開発してます

---
layout: center
transition: fade
clicks: 1
---

<StatementList>
  <Statement
    lead="健康になりたい！！！！"
    :notes="['30歳を超えてからそう思うことが増えました']"
  />
  <Statement
    v-click="1"
    note="しかし、"
    lead="健康になるためには"
    :notes="['ハードルがたくさんあります']"
  />
</StatementList>

---
layout: center
transition: fade
clicks: 1
---

<StatementList>
  <Statement
    lead="健康な生活は、食事と運動から"
    lead-size="md"
    :notes="['料理も、体を動かすのも、やること自体は好きです', 'でも、その前後で「考えること」がとにかく多いんです']"
  />
  <Statement
    v-click="1"
    note="健康には考えることがたっっっくさんあって大変ですね！"
    lead="ということで健康管理をAIに全部任せちゃいました！"
    lead-size="md"
  />
</StatementList>

---
layout: center
chapter: 説明
clicks: 1
---

<ChapterLabel />

<StatementList>
  <Statement>
    <span class="u-click u-agent" :class="{ 'is-on': $clicks >= 1 }">パーソナルAIエージェント</span> <span class="u-click u-muse" :class="{ 'is-on': $clicks >= 1 }">Muse</span>を<br><span class="u-click u-minorun" :class="{ 'is-on': $clicks >= 1 }">『みのるん式』</span>によってAI秘書にしてます
  </Statement>
</StatementList>

<style>
.u-click { text-decoration: underline; text-decoration-color: transparent; text-decoration-thickness: 3px; text-underline-offset: 0.25em; transition: text-decoration-color 0.3s; }
.u-agent.is-on { text-decoration-color: #2F6FB3; }
.u-muse.is-on { text-decoration-color: #E67E22; }
.u-minorun.is-on { text-decoration-color: #27AE60; }
</style>

---
chapter: 説明
---

<ChapterLabel />

# <span class="title-u title-u-agent">パーソナルAIエージェント</span>とは？

<div class="muse-feature-text">質問に答えるだけでなくあなたの代わりにアクションを実行して物事を片付けるAI</div>
<div class="definition-source">Meta社の公式FAQより意訳</div>

<div class="kari-row">
  <div class="kari">仮：説明は書き味をそろえた仮置き</div>
</div>

<div class="agent-split">
<div class="agent-grid">
  <div class="agent-item"><img class="agent-icon" src="/images/muse/muse-app-icon.svg" alt="Museのアプリアイコン" /><span>Muse</span></div>
  <div class="agent-item"><img class="agent-icon" src="/images/agents/grok-bot.png" alt="Grok Botのアプリアイコン" /><span>Grok Bot</span></div>
  <div class="agent-item"><img class="agent-icon" src="/images/agents/dots.png" alt="Dotsのキャラクター（Felipe）" /><span>Dots</span></div>
  <div class="agent-item"><img class="agent-icon" src="/images/agents/claude-duet.png" alt="Claude Duetのアプリアイコン" /><span>Claude Duet</span></div>
</div>
<ul class="agent-points">
  <li>ユーザーごとに独立したクラウド環境で動く</li>
  <li>ユーザーの代わりにブラウザの操作やコマンドラインの実行などコンピューターの操作をお願いできる</li>
  <li>様々なアプリやサービスと連携できる</li>
  <li>与えたタスクを非同期で自律的に実行できる</li>
</ul>
</div>

<!--
仮：説明の箇条書きは、これまでの4項目（ユーザーごとに独立したクラウド環境で動く／ユーザーの代わりにブラウザの操作やコマンドラインの実行などコンピューターの操作をお願いできる／様々なアプリやサービスと連携できる／与えたタスクを非同期で自律的に実行できる）を書き味をそろえて並べた仮置き。本人の言葉で直す前提。
Dots は ChatGPT の中の機能で単体の公式アイコンが無いため、OpenAI 公式の dots 紹介ページに出ている青い雲のキャラクター Felipe（フェリペ）の画像を使っている（本人が送った公式ページのスクリーンショットから切り取ったもの）。Claude Duet のアイコンは App Store（US）の公式アプリアイコン。
-->

---
chapter: 説明
class: muse-feature-page
---

<ChapterLabel />

# <span class="title-u title-u-muse">Muse</span>とは？

<div class="kari-row">
  <div class="kari">仮：箇条書きの文は書き味をそろえた仮置き</div>
</div>

<div class="muse-feature-text">あなたの指示に応じてアクションを実行して作業をこなすパーソナルAIエージェントであり、他のアプリやサービスと接続することができます</div>

<div class="muse-feature-grid">
<div class="avatar-compose">
  <img class="avatar-big" src="/images/muse/jolly.png" alt="Museの公式のエージェントのキャラクター（Jolly）" />
  <div class="avatar-custom">
    <svg class="avatar-arrow" viewBox="0 0 260 280" aria-hidden="true">
      <defs><marker id="avatar-arrowhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3498db" /></marker></defs>
      <path d="M 44 152 C 34 200, 96 222, 146 196" fill="none" stroke="#3498db" stroke-width="2.5" stroke-linecap="round" marker-end="url(#avatar-arrowhead)" />
    </svg>
    <img class="avatar-small" src="/images/muse/mamedaifuku.png" alt="本人のMuseのアバター（まめだいふく）" />
    <div class="avatar-caption">エージェントの見た目も<br>パーソナライズできてかわいい！</div>
  </div>
</div>
<ul class="muse-features">
  <li>無料から使い始められて気軽に試せる</li>
  <li>利用量が寛大でたくさん使える</li>
  <li>スマホから気軽に呼び出せる</li>
  <li>豊富なアプリやサービスとコネクタで接続できる
    <div class="connector-icons">
      <img src="/images/connectors/google.png" alt="Google" />
      <img src="/images/apps/health.png" alt="ヘルスケア" />
      <img src="/images/connectors/moneyforward.png" alt="マネーフォワード ME" />
      <img src="/images/connectors/1password.png" alt="1Password" />
      <img src="/images/connectors/facebook.png" alt="Facebook" />
      <img src="/images/connectors/instagram.png" alt="Instagram" />
      <img src="/images/connectors/threads.png" alt="Threads" />
    </div>
  </li>
  <li>スペースで自分専用のアプリを作れる</li>
  <li><s>倫理観がない</s></li>
</ul>
</div>

<!--
仮：箇条書きのうち「豊富なアプリやサービスとコネクタで接続できる」と「スマホから気軽に呼び出せる」は本人の言葉。「無料から使い始められて気軽に試せる」「利用量が寛大でたくさん使える」は、その書き味にそろえた仮置き。「スペースで自分専用のアプリを作れる」は本人の言葉（2026-11-11）。
-->

---
chapter: 説明
---

<ChapterLabel />

# <span class="title-u title-u-minorun">みのるん式</span>とは？

<div class="quote-slide">
  <img src="/images/minorun-slide-4.jpg" alt="みのるんさんのスライド「みのるん式とは？」のページ" />
</div>

<BottomLink href="https://speakerdeck.com/minorun365/kiro-crew-de-minoru-nshiki-shigotojutsu-ya-te-mita" title="出典：Kiro Crewで「みのるん式」仕事術やってみた" />

---
chapter: 説明
clicks: 1
---

<ChapterLabel />

# みのるん式とは？

<div class="kari-row">
  <div class="kari">仮：図の中の依頼と情報の例は仮置き</div>
</div>

<p class="monorepo-lead">『みのるん式』メソッドを活用して、僕のプライベートな情報を詰め込んだモノレポ（1つのGitリポジトリ）をAIに渡して秘書にしています</p>

<MonorepoSecretaryFigure
  label="僕がAI秘書（Muse）に睡眠や体重の記録、スライドや献立の作成などを細かく依頼し、AI秘書がGitリポジトリで情報やスキルを確認する図"
  class="monorepo-figure"
/>

<Overlay :click-start="1" position="center" font-size="1.8rem">

このAI秘書に健康管理を任せました

</Overlay>

<!--
仮：図の中の依頼のうち、本人の言葉は「睡眠の記録」「体重の記録」「スライド作成の依頼」「献立作成の依頼」。ほかの4つ（筋トレの記録／買い物リスト作成／食事の栄養チェック／筋トレメニューの相談）と、Gitリポジトリの中の情報・スキルの例（睡眠・体重・食事の記録／これまでに決めたこと／記録の付け方／献立やスライドの作り方）は、実際に任せていることから埋めた仮置き。本人の言葉で直す前提。
-->

---
layout: center
transition: fade
---

<div class="kari">仮：文言は本人の言葉で直す前の仮置き</div>

<StatementList>
  <Statement note="健康管理をしてもらうために、AI秘書には" lead-size="md">
    <span>記録と提案をしてもらっています</span>
  </Statement>
</StatementList>

<!--
仮：本人の「健康管理してもらうために、記録と提案をしてもらってる」を組み立てた仮置き。本人の言葉で直す前提。
-->

---
chapter: 記録
---

# 記録

<p class="record-lead">記録するためにMuseに様々な情報を連携します</p>

<div class="record-list">
  <div class="record-item">
    <img class="record-icon" src="/images/apps/health.png" alt="ヘルスケア" />
    <div class="record-text">
      <div class="record-name">ヘルスケア</div>
      <div class="record-src">Museのコネクタで連携。体重・体脂肪率（オムロンコネクト）、睡眠・歩数、ランニングの記録（Apple Watch）</div>
    </div>
  </div>
  <div class="record-item">
    <img class="record-icon" src="/images/apps/asken.png" alt="あすけん" />
    <div class="record-text">
      <div class="record-name">あすけん</div>
      <div class="record-src">アプリからスクショで連携。一日分のカロリー・PFC（タンパク質・脂質・炭水化物）バランス・栄養素</div>
    </div>
  </div>
  <div class="record-item">
    <div class="record-icon record-icon--none" aria-hidden="true"></div>
    <div class="record-text">
      <div class="record-name">筋トレアプリ</div>
      <div class="record-src">Museのスペースで自作。トレーニングメニュー・重量の記録</div>
    </div>
  </div>
</div>

---
layout: center
class: text-center
---

## 提案

---
chapter: 提案
---

<ChapterLabel />

# 献立

<div class="with-visual">
<div>

- 栄養素とPFC、カロリーを考えつつ、余り物少なく考えてくれる
- 好きなものの好みも覚えてくれる

</div>
<img class="visual-space" src="/images/spaces/menu-oyakodon.png" alt="夕食メニューのスペース（親子丼の日）" />
</div>

---
chapter: 提案
---

<ChapterLabel />

# 筋トレメニュー

<div class="with-visual">
<div>

- 僕ができるトレーニングメニューを考えてくれる
- わからない種目を減らすためにたまに新しい種目を教えてくれる
- 器具の状況によって柔軟にメニューを変えれる
- 成長によって重量を増やしてくれる
- スペースのアプリでメニューを入力しておける

</div>
<img class="visual-space" src="/images/spaces/training-app.jpg" alt="筋トレ記録のスペース（今日のメニューの画面）" />
</div>

---
layout: center
chapter: まとめ
---

<ChapterLabel />

<div class="with-visual">
<StatementList>
  <Statement
    note="MuseをAI秘書にして健康管理してもらうことで"
    lead="僕のことをよく理解して最適な食事やトレーニングのメニューを考えてくれるようになりました"
    lead-size="md"
  />
</StatementList>
<img class="muse-icon" src="/images/muse/muse-app-icon.svg" alt="Museの公式アイコン" />
</div>

---
layout: ending
---

# Thank You!

ご清聴ありがとうございました

<div class="absolute right-8 bottom-8">
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>
