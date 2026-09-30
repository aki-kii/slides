---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>プルリクエスト作ったよ</ChatMessage>

<PipelineStage stage="pr">

**プルリクエスト作成後**の検証（CI）
- cdk validate
  - オフライン：ルールセットに照らして検証
  - オンライン：AWSの状態を見てデプロイ可能か検証
- cdk drift
  - デプロイ済みのリソースに手で変更された形跡がないかを検証
- Lint / 型チェック / 単体テスト

</PipelineStage>

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['`cdk validate`が失敗してる']" />

<PipelineStage stage="pr" status="failed">

```bash [cdk validate結果]
$ cdk validate BotStack --unstable=validate

FATAL Resource of type 'AWS::S3::Bucket'
  with identifier 'akikii-conversation-log'
  already exists.
# AWSに同名のS3バケットが既に存在していた
```

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
const bucket = new s3.Bucket(this, 'LogBucket', {
  bucketName: 'akikii-conversation-log',
//            ^^^^^^^^^^^^^^^^^^^^^^^^^
//         AWSに同名のS3バケットが既に存在していた
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
```

```ts
const bucket = new s3.Bucket(this, 'LogBucket', {
  // ✅ bucketNameは指定せず、CDKに一意な名前を付けさせる
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
```
````

</PipelineStage>

---
transition: slide-left
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['`cdk validate` 通った！CIも成功したよ']" />

<PipelineStage stage="pr" status="done">

```bash [cdk validate結果]
$ cdk validate BotStack --unstable=validate

✨  Validation passed (1 stack)
```

</PipelineStage>

<!--
10. デプロイの数分を待たずに、AWS本体に聞けました
11. 失敗してロールバックしてから気づく必要がありません
-->
