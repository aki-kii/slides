---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>実装できたしpushするね</AgentTitle>

<PipelineStage rail="3-git-push">

pushする前のhookで、次のセンサーが動作します

- **`cdk diff`**
  - <Kogoe>いまデプロイされているスタックと、これから出すテンプレートを見比べて差分を検証</Kogoe>
  - <Kogoe>見ているのは自分のスタックの中身だけ</Kogoe>

</PipelineStage>

<!--
1. 実装を終えて、リモートブランチにpushしようとしています
2. push前に cdk diff を回しています。
   いまAWSにデプロイされているものと、これから出すものを見比べるコマンドです
3. ここ、あとで効いてきます。diff が見ているのは自分のスタックの中身だけです
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['`cdk diff`で想定外の差分が出てる']" />

<PipelineStage rail="3-git-push-failed">

```ts [ソースコード]
new ecs.FargateService(this, 'BotService', {
  cluster,
  taskDefinition,
  serviceName: 'discord-bot',
//             ^^^^^^^^^^^^^ ECSサービス名を明示した
});
```

<br>
    
```text [cdk diff結果]
Resources
[~] AWS::ECS::Service BotService/Service replace
 └─ [~] ServiceName (requires replacement)
     └─ [+] discord-bot
[+] AWS::S3::Bucket ConversationLog/Bucket
```

</PipelineStage>

<!--
4. エージェントは会話ログの実装のついでに、気になったところを直していました。
   ECSサービス名が指定されていなかったので、明示するようにした
5. 正しい方向の修正に見えますが、diff はこう言いました。replace、作り直しです
6. しかもCloudFormationは新しいサービスを作ってから古いのを消すので、
   その間、同じDiscordトークンでbotが2つ立ち上がります
-->

---
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['修正したよ！', '差分が想定通りになったからpushしたよ']" />

<PipelineStage :rail="$clicks < 1 ? '3-git-push' : '3-git-push-done'">

```ts [ソースコード]
new ecs.FargateService(this, 'BotService', {
  cluster,
  taskDefinition,
  // ✅ リソースが置き換わるプロパティ変更は取りやめ
});
```

<div v-click>

<br>

```text [cdk diff結果]
Resources
[+] AWS::S3::Bucket ConversationLog/Bucket
```

</div>

</PipelineStage>

<!--
7. サービス名を渡すのをやめて、差分が想定通りになりました
8. 型もLintもsynthも通る修正でした。プロパティを1つ足しただけで、書き方としては正しいので
9. 実環境を壊す前に止まりました。壊さないと分かっているから、任せたまま進められます
-->
