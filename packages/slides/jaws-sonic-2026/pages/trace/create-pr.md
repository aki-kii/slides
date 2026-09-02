---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>PullRequest作ったよ</AgentTitle>

<PipelineStage rail="4-create-pr">

PullRequest作成後のCIで、次のセンサーが動作します

- **`cdk validate`**
  - <Kogoe>CloudFormationの事前検証で、AWS本体と矛盾しないかを検証</Kogoe>
- **`cdk drift`**
  - <Kogoe>デプロイ済みのリソースに手で変更された形跡がないかを検証</Kogoe>
- **Linter / 型チェック / 単体テスト**
  - <Kogoe>ここまでで回したものを、クリーンな環境で回し直す</Kogoe>

</PipelineStage>

<!--
1. PullRequestを作成しました
2. PR作成時に起動するGitHub ActionsでCIが回ります
3. cdk validate は synth してチェンジセットを作り、
   CloudFormationのサーバー側の事前検証を叩きます。ここで初めてAWS本体に問い合わせます
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['CIの`cdk validate`が失敗してる']" />

<PipelineStage rail="4-create-pr-failed">

```ts [ソースコード]
const bucket = new s3.Bucket(this, 'Bucket', {
  bucketName: 'akikii-conversation-log',
//            ^^^^^^^^^^^^^^^^^^^^^^^^^
//            同名のS3バケットが既に存在していた
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
});
```

```text [cdk validate結果]
$ cdk validate BotStack --unstable=validate

FATAL Resource of type 'AWS::S3::Bucket'
  with identifier 'akikii-conversation-log'
  already exists.
```

</PipelineStage>

<!--
4. バケット名は他から参照できるように固定してありました
5. その名前はもう使われている、と言われました。
   前に手で作って試したバケットが残っていたんです
6. どのconstructが問題かまで返るので、エージェントはそのまま直せます
7. 同じコードで cdk diff を回しても、バケットが増えるとしか言いません。
   diff が見ているのは自分のスタックの中身だけで、アカウントに他に何があるかは見ていない
8. ここが5つの層のなかで一番大きな分かれ目です。
   従来ならデプロイして数分待って、失敗してロールバックして初めて分かる類の失敗でした
-->

---
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['修正したよ！', '`cdk validate`通った！CIも成功したよ']" />

<PipelineStage :rail="$clicks < 1 ? '4-create-pr' : '4-create-pr-done'">

```ts [ソースコード]
const bucket = new s3.Bucket(this, 'Bucket', {
  // bucketNameは指定せず、CDKに一意な名前を付けさせる
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
});
```

<div v-click>

```text [cdk validateの出力]
$ cdk validate BotStack --unstable=validate

✨  Validation passed (1 stack)
```

</div>

</PipelineStage>

<!--
10. デプロイの数分を待たずに、AWS本体に聞けました
11. 失敗してロールバックしてから気づく必要がありません
-->
