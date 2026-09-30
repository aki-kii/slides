---
layout: center
transition: slide-left
clicks: 2
---

<StatementList>
  <Statement note="半年くらい前から">
    <span style="view-transition-name: running-text">ランニングを始めました</span>
  </Statement>
  <div class="intro-stats">
    <span class="intro-note" v-click="1">最初は</span>
    <span class="intro-figure" v-click="1">3〜4km</span>
    <span class="intro-note" v-click="1">くらい走るのがやっとでしたが…</span>
    <span class="intro-note" v-click="2">いまは</span>
    <span class="intro-figure" v-click="2"><strong>10km</strong></span>
    <span class="intro-note" v-click="2">くらい走っています！</span>
  </div>
</StatementList>

---
layout: center
transition: slide-left
---

<StatementList>
  <div class="intro-qa">
    <span class="intro-mark intro-lead">Q.</span>
    <Statement lead="なぜ走る距離が伸びたの？" :notes="['気合い？根性？執念？']" />
  </div>
  <div class="intro-qa" v-click>
    <span class="intro-mark intro-lead"><strong>A.</strong></span>
    <Statement
      :notes="['走りながら音声入力で指示しています！', 'CDKでAWSリソースもデプロイできちゃいます！！！']"
    >
      <strong>走りながらコーディングエージェントを動かしている</strong>ので暇じゃなくなったから
    </Statement>
  </div>
</StatementList>

---
src: ./voiceio.md
---

---
src: ./constraints.md
---
