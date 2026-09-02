---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>一区切りついたしcommitするね</AgentTitle>

<PipelineStage rail="2-git-commit">

commitする前のhookで、次のセンサーが動作します

- **`cdk synth`**
  - <Kogoe>CDKのコードからCloudFormationテンプレートを組み立てて、設定の組み合わせが成立するかを検証</Kogoe>
- **ユニットテスト / Snapshot**
  - <Kogoe>組み上がったテンプレートが意図どおりかを検証</Kogoe>

</PipelineStage>

<!--
1. ファイルの編集が終わって、commitしようとしています
2. commit前のフックで cdk synth を回しています。
   CDKのコードからCloudFormationのテンプレートを組み立てるコマンドで、デプロイはしません
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>commit前のSynthesizeが失敗した</AgentTitle>

<PipelineStage rail="2-git-commit-failed">

```ts [ソースコード]
const bucket = new s3.Bucket(this, 'Bucket', {
  autoDeleteObjects: true,
//^^^^^^^^^^^^^^^^^
// removalPolicy に RemovalPolicy.DESTROY が必要
});
```

</PipelineStage>

<!--
3. 中身を消す設定はあるのに、バケット自体を消す設定がありません
4. プロパティ1つ1つは正しいので、型検査は通ります。
   組み合わせが成立しているかは、組み立ててみるまで分かりません
5. エラーコードと、ソースの何行目か、それから construct のツリーまで返ります
-->

---
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['修正したよ！', 'Synthesize通ったからcommitしたよ']" />

<PipelineStage :rail="$clicks < 1 ? '2-git-commit' : '2-git-commit-done'">

```ts [ソースコード]
const bucket = new s3.Bucket(this, 'Bucket', {
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
  // ✅ 相互依存するプロパティをどちらも設定
});
```

<br>

<div v-click>

```text [cdk synthの出力]
$ pnpm cdk synth

Successfully synthesized to /path/to/cdk.out
Supply a stack id to display its template.
```

</div>

</PipelineStage>

<!--
6. エージェントはエラーをそのまま読んで直しました
7. AWSに触らずに数秒で終わります。何度失敗しても、コストもゴミも残りません
-->
