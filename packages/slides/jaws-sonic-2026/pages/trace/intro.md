---
layout: section
transition: slide-left
---

## エージェントの動きをトレースしてみよう

---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

## 音声botに機能追加

> 走行中の会話ログをS3に保存して、あとで振り返れるようにして

<img src="/images/voiceio/architecture-aws-after.svg" class="mt-4 w-full max-h-[62%] object-contain mx-auto">

<!--
1. 1章で作ったDiscord bot基盤に、機能をひとつ足します
2. 依頼はこれだけ。「会話ログをS3に保存して、あとで振り返れるようにして」
3. 3つのコンテナが1つのECSタスクで動いているので、タスクロールも1つ。
   あとでここにS3への権限を足すことになります
4. ここから先はエージェントに任せて、開発フローを下から上へ登っていきます。
   縛りをひとつ置きます。人間はコードを1行も読みません
-->
