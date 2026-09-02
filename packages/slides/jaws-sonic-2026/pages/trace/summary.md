---
layout: center
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<div class="text-center">

<div class="text-xl opacity-70">人間がコードを1行も読んでいなくても</div>

<h2 class="mt-2">CDKはこの階段の<br>全段に道具を持っている</h2>

<div v-click class="mt-8 text-xl">

`cdk validate` は<strong>どのconstructが問題か</strong>を、<br>
`cdk diagnose` は<strong>自分の書いたコードの場所</strong>を指して返る

</div>

</div>

<!--
1. 人間がやったのは、依頼を1つ出したことと、PRの要約を聞いたことだけでした
2. 5つの層は、それぞれ違うものを照らしていました。下の層では原理的に出せないものだけを担当しています
3. CDKはこの階段の全段に道具を持っています。
   しかも返ってくるものが、エージェントがそのまま読んで直せる形になっている
4. だから、IaC、特にCDKは、
   コーディングエージェントでAWSインフラを構築する検証サイクルを回すのに向いています
-->
