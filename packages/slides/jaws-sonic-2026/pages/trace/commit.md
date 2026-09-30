---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>一区切りついたしcommitするね</ChatMessage>

<PipelineStage stage="commit">

**commit前**に検証する仕組み

- Synthesize（cdk synth）
  - CDKアプリを実行してCDKソースをCFnテンプレートに合成し、デプロイできる状態にする
- CDKの単体テスト
  - スナップショットテスト
  - Fine-grained assertionsテスト
  - バリデーションテスト

</PipelineStage>

<BottomLink href="https://aws.amazon.com/jp/builders-flash/202411/learn-cdk-unit-test/" label="AWS CDK における単体テストの使い所を学ぶ" />

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>Synthesizeが失敗した</ChatMessage>

<PipelineStage stage="commit" status="failed">

```bash [cdk synth結果]
$ pnpm cdk synth

Validation failed with the following errors:
  [BotStack/ConversationLog/Bucket]
  Cannot use 'autoDeleteObjects' property on a bucket
  without setting removal policy to 'DESTROY'.
```

- CloudFormationテンプレート合成時のバリデーションに引っかかたため失敗

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
const bucket = new s3.Bucket(this, 'Bucket', {
  autoDeleteObjects: true,
//^^^^^^^^^^^^^^^^^^^^^^^
// ❌ RemovalPolicy.DESTROYとセットで設定する必要がある
});
```

```ts
const bucket = new s3.Bucket(this, 'Bucket', {
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
  // ✅ 相互依存するプロパティをどちらも設定
});
```
````

</PipelineStage>

<!--
4. 中身を消す設定はあるのに、バケット自体を消す設定がありません
5. プロパティ1つ1つは正しいので、型検査は通ります。
   組み合わせが成立しているかは、組み立ててみるまで分かりません
6. エージェントはエラーをそのまま読んで直しました
-->

---
transition: slide-left
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>Synthesize通ったからcommitしたよ</ChatMessage>

<PipelineStage stage="commit" status="done">

```bash [cdk synth結果]
$ pnpm cdk synth

Successfully synthesized to /path/to/cdk.out
Supply a stack id to display its template.
```

</PipelineStage>

<!--
7. AWSに触らずに数秒で終わります。何度失敗しても、コストもゴミも残りません
-->
