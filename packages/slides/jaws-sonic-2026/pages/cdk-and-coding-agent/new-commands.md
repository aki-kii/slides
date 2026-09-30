---
layout: default
title: new-commands-cards
transition: fade
---

<script setup>
/**
 * new-commands.md の横並び版 (案)。中身は同じで、縦積みではなく
 * 3つのカードを横に並べる。3つが対等な選択肢に見える代わりに、
 * 1枚あたりの幅が狭くなるので説明は折り返す前提で組む。
 */
const COMMANDS = [
  {
    date: '2026/04',
    preview: true,
    name: 'cdk diagnose',
    lines: [
      'デプロイに失敗した原因を調査するコマンド',
      'デプロイログやCloudTrail、作成したリソースのログなどを見て判断する',
    ],
  },
  {
    date: '2026/06',
    preview: true,
    name: 'cdk validate',
    lines: [
      'デプロイに失敗しないか検証するコマンド',
      '<strong>オフラインバリデーション</strong><br>→ルールセットに照らして検証</ul>',
      '<strong>オンラインバリデーション</strong><br>→AWSアカウントの実際の状態に合わせて、デプロイ可能か検証する',
    ],
  },
  {
    date: '2026/07',
    preview: true,
    name: 'cdk lsp',
    lines: [
      'コードを書いている最中に、CDK特有のエラーや警告を教えてくれる<strong>Language Server</strong>を立てるコマンド',
      '保存時にSynthesizeを実行して、エラー箇所をソースコードとマッピングして返す',
    ],
  },
];
</script>

<ChapterLabel label="CDK × コーディングエージェント"/>

## CDKの最近の動向

CDKの実装が正しいか**検証できるコマンド**が続々追加されている
<div class="cards">
  <div class="card" v-for="c in COMMANDS" :key="c.name">
    <div class="card-head">
      <span class="card-date">{{ c.date }}</span>
      <span class="card-preview" v-if="c.preview">プレビュー</span>
    </div>
    <div class="card-name">
      <code>{{ c.name }}</code>
    </div>
    <div class="card-lines">
      <div v-for="(line, i) in c.lines" :key="i" v-html="line" />
    </div>
  </div>
</div>

<style>
/*
 * 3列を等分する。1fr にしておくと、説明の長さが違っても幅がそろい、
 * カードの頭 (日付 / コマンド名) が3枚で横一直線になる。
 */
.cards {
  margin-top: 1.4rem;
  display: grid;
  /* minmax(0, 1fr) にしないと、折り返さない語 (バリデーション) を持つカードだけ広がる */
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.9rem;
  align-items: stretch;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.9rem 1rem;
  border: 2px solid rgba(20, 36, 58, 0.2);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.6);
}

/* 日付と「いつから使えるか」を1行に並べる。狭いカードなので折り返しは許す */
.card-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  column-gap: 0.5rem;
  row-gap: 0.1rem;
}

.card-date {
  font-family: var(--slidev-code-font-family, monospace);
  font-size: 0.85rem;
  color: rgba(20, 36, 58, 0.55);
}

.card-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* カード幅が狭いので、コマンド名は折り返させず幅の基準にする */
.card-name code {
  font-size: 1rem;
  white-space: nowrap;
}

/* まだプレビュー段階であることの但し書き。強調ではないので彩度は抑える */
.card-preview {
  padding: 0.05em 0.5em;
  border: 1px solid rgba(190, 120, 20, 0.45);
  border-radius: 4px;
  color: #a4661a;
  font-size: 0.65rem;
  font-weight: 700;
  white-space: nowrap;
}

.card-lines {
  margin-top: 0.35rem;
  padding-top: 0.55rem;
  border-top: 1px solid rgba(20, 36, 58, 0.15);
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  font-size: 0.8rem;
  line-height: 1.55;
  color: #3a3941;
}

/* 「オンラインバリデーション」が途中で割れて「ン」だけ残るので、語で折らせる */
.card-lines :deep(strong) {
  white-space: nowrap;
}

.cards-summary {
  margin-top: 1.4rem;
}

.cards-point {
  font-size: 1.3rem;
  font-weight: 700;
  line-height: 1.4;
}
</style>
