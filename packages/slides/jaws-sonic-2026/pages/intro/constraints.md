---
layout: default
title: constraints
transition: fade
clicks: 1
---

<!--
  走りながら音声でやり取りしていると何が起きるかを、2 かたまりで言い切るページ。
  本文はイントロと同じ「小さい前置き → 大きい言い切り」で組み、左端は見出しごとそろえる。
-->
<div class="constraint-page">
  <h2 class="constraint-title">音声でやりとりする制約</h2>
  <StatementList gap="wide">
    <Statement
      lead-size="md"
      note="ランニング中はソースコードを読めないので"
      lead="限りなく要約してもらったものをレビューしている"
    />
    <Statement
      v-click
      lead-size="md"
      note="実装に不具合があった場合"
      lead="何回もデプロイし直すことになり時間がかかってしまう"
    />
  </StatementList>
</div>

<!--
1. 音声でやり取りするうえでの制約の話です
2. ランニング中はソースコードを読めないので、限りなく要約してもらったものをレビューしています
3. （クリック）実装に不具合があった場合、何回もデプロイし直すことになり時間がかかってしまいます
-->
