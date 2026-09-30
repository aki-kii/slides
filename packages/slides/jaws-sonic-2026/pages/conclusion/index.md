---
layout: section
transition: slide-left
---

# まとめ

---
layout: center
transition: slide-left
clicks: 2
---

<ChapterLabel label="まとめ"/>

<StatementList>
  <Statement lead="CDKには実装したコードを検証する仕組みが揃っている" lead-size="md" />
  <Statement v-click="1" note="その仕組みを使うことで" lead="エージェントが自律的に検証して直せる" />
</StatementList>

<div class="conclusion-say" v-click="2">

<ChatMessage from="user">これでみなさんも走りながらAWSにデプロイできますね！！！</ChatMessage>

</div>

<style>
/* 言い切りの下に置く一言。吹き出しは大きいので、間だけ空けておく */
.conclusion-say {
  margin-top: 1.8rem;
}
</style>
