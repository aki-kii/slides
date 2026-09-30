---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>ファイルを編集するよ〜</ChatMessage>

<PipelineStage stage="edit">

**ファイル編集後**に検証する仕組み

- Linter
  - ソースコードを静的解析して、プログラミング言語やCDKのルール違反を検証
- 型チェッカー
  - ソースコードで定義している型に矛盾がないかを検証

</PipelineStage>

<!--
1. Claudeが機能を実装しています
2. 一番下の層、ファイルを編集するたびにhookで鳴るセンサーはこの2つです
3. 型チェックが見るのは型の矛盾だけ。これが後で効いてきます
-->

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>Lintエラーが出ちゃった</ChatMessage>

<PipelineStage stage="edit" status="failed">

```bash [Lint結果]
$ pnpm lint

  × awscdk/pascal-case-construct-id
    Construct IDはPascalCaseで指定してください

Found 0 warnings and 1 error.
```

- awscdk-lint<Kogoe> (eslint-plugin-awscdk/oxlint-plugin-awscdk)</Kogoe>
  - CDKのセオリーに基づくコーディング規約を提供するLintプラグイン

</PipelineStage>

<BottomLink href="https://awscdk-lint.dev/" label="awscdk-lint Lint plugins for AWS CDK" />

---
transition: fade
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading :texts="['修正するよ', '修正したよ']" />

<PipelineStage stage="edit" :status="$clicks < 1 ? 'running' : 'done'">

````md magic-move [ソースコード] {duration: 300}
```ts
const bucket = new s3.Bucket(this, 'log-bucket', {
  //                               ^^^^^^^^^^^^
  // ❌ Construct IDがPascalCaseになっていない
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
```

```ts
// ✅ Construct IDをPascalCaseに修正
const bucket = new s3.Bucket(this, 'LogBucket', {
  removalPolicy: cdk.RemovalPolicy.RETAIN,
});
```
````

</PipelineStage>

<!--
6. Construct IDはPascalCaseで書くのがCDKの流儀。エージェントはケバブケースで書いていました
7. Lintは違反したルール名と、コードの場所まで教えてくれます。
   なのでエージェントはそれを読んで自分で直せます。ここで人間は何もしていません
-->

---
transition: slide-left
---

<ChapterLabel label="エージェントの動きをトレースしてみよう"/>

<ChatMessage from="agent" heading>Lintエラーなくなった！</ChatMessage>

<PipelineStage stage="edit" status="done">

```bash [Lint結果]
$ pnpm lint

Found 0 warnings and 0 errors.
```

</PipelineStage>

<!--
8. 直りました。ここで押さえておきたいのは、
   このコードは型チェックも通るし、この後に出てくる synth も diff も通るということです
9. 編集のたびに鳴るので、書いている最中にエージェントが直せました。
   一番回数の多い層を、待ち時間ゼロで潰せます
-->
