---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>実装するよー</AgentTitle>

<PipelineStage rail="1-file-edit">

ファイルを編集した後のhookで、次のセンサーが動作します

- **Linter**
  - ソースコードを静的解析して、プログラミング言語やCDKのルール違反を検証
- **型チェック**
  - 定義されている型に矛盾がないかを検証

</PipelineStage>

<!--
1. Claudeが機能を実装しています
2. 一番下の層、ファイルを編集するたびにhookで鳴るセンサーはこの2つです
3. 型チェックが見るのは型の矛盾だけ。これが後で効いてきます
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>Lintエラーが出ちゃった</AgentTitle>

<PipelineStage rail="1-file-edit-failed">

```ts [ソースコード]
export interface ConversationLogProps {
  readonly taskRole: iam.Role;
  /**                    ^^^^
  * oxlint-plugin-awscdk/no-construct-in-interface
  * InterfaceのPropsにはInterface型の指定を推奨
  */
}
```

</PipelineStage>

<br>

- **awscdk-lint**
  - CDKのルールを扱うLintプラグイン（ESLint/Oxlint）
  - CDKにおけるセオリーをコーディング規則として取り入れられる

<BottomLink href="https://awscdk-lint.dev/" label="awscdk-lint Lint plugins for AWS CDK" />

<br>

<!--
4. 会話ログの置き場をConstructに切り出して、書き込む相手のタスクロールを外から受け取る形にしました
5. ここでLinterがエラーを出しました。引っかかったのはCDKのルール違反です
6. Role は「CDKがこれから作るロール」、IRole は「ロールならなんでも」。
   Role で受けると、別のスタックで作ったロールやインポートしたロールを渡せなくなります
-->

---
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['修正したよ！', 'Lintエラー消えた！']" />

<PipelineStage :rail="$clicks < 1 ? '1-file-edit' : '1-file-edit-done'">

```ts [ソースコード]
export interface ConversationLogProps {
  readonly taskRole: iam.IRole;
  // ✅ インタフェース型(IRole)を渡すように修正
}
```

<div v-click>

<br>

```bash [Lint結果]
$ pnpm lint

Found 0 warnings and 0 errors.
```

</div>

</PipelineStage>

<!--
7. 直りました。ここで押さえておきたいのは、
   このコードは型チェックも通るし、この後に出てくる synth も diff も通るということです
8. 編集のたびに鳴るので、書いている最中にエージェントが直せました。
   一番回数の多い層を、待ち時間ゼロで潰せます
-->
