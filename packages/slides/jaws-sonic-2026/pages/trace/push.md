---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>一通り実装できたしpushするよ</ChatMessage>

<PipelineStage stage="push">

**push前**に検証する仕組み

- **`cdk diff`**
  - デプロイ済みのCFnテンプレートと合成した<br>CFnテンプレートを見比べて差分を検証
  - AWSへアクセスして確認する

</PipelineStage>

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['想定外の差分があったみたい']" />

<PipelineStage stage="push" status="failed">

```bash [cdk diff結果]{2-3}
Resources
[~] AWS::ECS::Service BotService/Service replace
 └─ [~] ServiceName (requires replacement)
     └─ [+] discord-bot
[+] AWS::S3::Bucket ConversationLog/Bucket
```

- requires replacement
  - リソースが新しく作り直される
  - ステートフルなリソースを置き換えると<br>データが消えてしまって大惨事に...

</PipelineStage>

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['修正するよ', '修正したよ']" />

<PipelineStage stage="edit" :status="$clicks < 1 ? 'running' : 'done'">

<!-- 既定 (500ms) だと変形が間延びするので短めにする -->
````md magic-move [ソースコード] {duration: 300}
```ts
new ecs.FargateService(this, 'BotService', {
  cluster,
  taskDefinition,
  serviceName: 'discord-bot',
//             ^^^^^^^^^^^^^ ECSサービス名を明示した
});
```

```ts
new ecs.FargateService(this, 'BotService', {
  cluster,
  taskDefinition,
  // ✅ リソースが置き換わるプロパティ変更は取りやめ
});
```
````

</PipelineStage>

<!--
7. サービス名を渡すのをやめました
8. 型もLintもsynthも通る修正でした。プロパティを1つ足しただけで、書き方としては正しいので
-->

---
transition: slide-left
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>差分が想定通りになったからpushしたよ</ChatMessage>

<PipelineStage stage="push" status="done">

```bash [cdk diff結果]
Resources
[+] AWS::S3::Bucket ConversationLog/Bucket
```

</PipelineStage>

<!--
9. 差分が想定通りになりました
10. 実環境を壊す前に止まりました。壊さないと分かっているから、任せたまま進められます
-->
