---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>実装完了したよ！ニンゲン、これでいい？</ChatMessage>

<PipelineStage stage="deploy" :status="$clicks < 1 ? 'pending' : 'running'">

<ChatMessage from="agent" no-icon>

- 会話ログ用のS3バケット追加
- 会話を書込むようアプリ修正

</ChatMessage>

<ChatMessage from="user">おk、マージするね</ChatMessage>

<div v-click>

```bash [マージすると走るデプロイ]
$ cdk deploy --no-rollback
# --no-rollabackをつけるとデプロイ失敗してもリソースを切り戻さない
# 開発環境のような失敗しても問題ない環境で検証する
```

</div>

</PipelineStage>



---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>デプロイが失敗しちゃった...</ChatMessage>

<PipelineStage stage="deploy" status="failed">

```bash [デプロイログ]
BotStack | UPDATE_FAILED | AWS::ECS::Service
Resource handler returned message:
'ECS Deployment Circuit Breaker was triggered'
# タスクが起動できずデプロイ失敗
```

デプロイログからはタスク起動に失敗した理由がわからない

</PipelineStage>

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['`cdk diagnose` で原因を調べるね']" />

<PipelineStage stage="deploy" status="failed">

```bash [cdk diagnose結果]{1,7-10}
$ cdk diagnose BotStack --unstable=diagnose
Source Location:
  new ConversationLog (lib/conversation-log.ts:31:5)

  Task stopped: Essential container in task exited
  Container "discord-bot" exited with code 1
  # 作成したS3バケットへObjectを書き込む権限がなかった
  upload failed: An error occurred (AccessDenied)
  when calling the PutObject operation:
  ... is not authorized to perform: s3:PutObject
  on resource: "arn:aws:s3:::botstack-.../run.log"
```

ロールバックされずに残ったECSログから原因判明

</PipelineStage>

<!--
7. 失敗したデプロイの記録をCloudFormationから引き直して、
   暗号みたいな名前を、自分が書いたコードの場所に翻訳してくれます
8. さらにECSの停止したタスクとコンテナのログまで辿って、真の原因を出しました
9. バケットは作ったのに、タスクロールに書き込み権限を付けるのを忘れていました。
   権限が足りないことは、実際にデプロイして動かすまで誰も気付けません
-->

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['修正するよ', '修正したよ']" />

<PipelineStage stage="edit" :status="$clicks < 1 ? 'running' : 'done'">

<!-- 既定 (500ms) だと変形が間延びするので短めにする -->
````md magic-move [ソースコード] {duration: 300}
```ts
const bucket = new s3.Bucket(this, 'LogBucket', {
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
// ❌ タスクロールに書き込み権限を付与していない
```

```ts
const bucket = new s3.Bucket(this, 'LogBucket', {
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
// ✅ Grantsクラスで書き込み権限を付与
bucket.grants.write(props.taskRole);
```
````

</PipelineStage>

---
transition: slide-left
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>再デプロイしたら成功した！</ChatMessage>

<PipelineStage stage="deploy" status="done">

```bash [デプロイログ]
BotStack | UPDATE_COMPLETE | AWS::CloudFormation::Stack

 ✅  BotStack

Deployment time: 274.4s
```

</PipelineStage>
