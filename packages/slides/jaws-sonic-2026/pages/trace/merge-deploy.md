---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>実装したよ！ニンゲン、これでいい？</AgentTitle>

<PipelineStage rail="5-merge-pr">

<div class="chat">

<div class="bubble bubble--agent">

- 会話ログ用のS3バケットを追加
- タスクロールに書き込み権限を付与

</div>

<div class="turn-human">

<div class="turn-human-row">

<div class="bubble bubble--human">おk、マージしといて</div>

<img class="human-icon" src="/images/aboutme/me-icon.png" />

</div>

</div>

</div>

<div v-click>

PRをマージするとCI/CDからデプロイされます

```bash
$ cdk deploy --no-rollback
```

</div>

</PipelineStage>

<br>

- `--no-rollback`オプション
  - デプロイに失敗してもリソースを削除しない

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bubble {
  position: relative;
  width: fit-content;
  max-width: 92%;
  padding: 0.4rem 0.9rem;
  border-radius: 0.6rem;
}

.bubble ul {
  margin: 0;
}

/* エージェント側。タイトルの吹き出しと揃える */
.bubble--agent {
  background: rgba(217, 119, 87, 0.14);
}

/* ニンゲン側。右のアイコンから吹き出しが生えて、ひと言だけ返ってくる */
.turn-human {
  align-self: flex-end;
  text-align: right;
}

.turn-human-row {
  display: flex;
  align-items: center;
  /* しっぽ (0.5rem) がアイコンに刺さらないだけの間隔をとる */
  gap: 1.1rem;
}

.bubble--human {
  background: rgba(31, 117, 203, 0.12);
  font-size: 1.6rem;
  font-weight: 600;
  padding: 0.3rem 1.4rem;
}

/* 吹き出しのしっぽ。アイコンの方 (右) を向かせる */
.bubble--human::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  border: 0.5rem solid transparent;
  border-left-color: rgba(31, 117, 203, 0.12);
}

.human-icon {
  flex: none;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 1px 6px rgba(20, 30, 60, 0.18);
}

.who {
  margin-top: 0.2rem;
  margin-right: 3.7rem;
  font-size: 0.85rem;
  opacity: 0.55;
}
</style>

<!--
1. ここで初めて人間が出てきます
2. エージェントが「こんな方向性で実装した」と要約を出してきて、
   人間はノータイムで「おk」と返しただけです
3. 見ているのは「要件と合っているか」だけ。
   壊れていないかは、ここまでの4つの層が既に言ってくれています
4. マージすると開発環境にデプロイされます。--no-rollback を付けているのがポイントです
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle>デプロイが失敗しちゃった...</AgentTitle>

<PipelineStage rail="5-merge-pr-failed">

```bash [デプロイログ]
BotStack | UPDATE_FAILED | AWS::ECS::Service
Resource handler returned message:
'ECS Deployment Circuit Breaker was triggered'
# タスクが起動できずデプロイ失敗
```

コンテナの起動に失敗した理由が残っていない

</PipelineStage>

<!--
4. エージェントは最小権限にしようとして、L2の grant を使わず自分でポリシーを書いていました
5. デプロイが落ちました。返ってくるのは、暗号みたいな名前と素っ気ない一文だけです
6. これを見ても根本原因は分かりません。しかもCIのログはもう手元にありません
-->

---
transition: fade
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['`cdk diagnose`で原因を調べるね']" />

<PipelineStage rail="5-merge-pr-failed">

```bash [cdk diagnoseの出力]
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

</PipelineStage>

- cdk diagnoseコマンドはロググループも見てくれる

<!--
7. 失敗したデプロイの記録をCloudFormationから引き直して、
   暗号みたいな名前を、自分が書いたコードの場所に翻訳してくれます
8. さらにECSの停止したタスクとコンテナのログまで辿って、真の原因を出しました
9. バケット本体と、中に入っているものは別の名前で指します。
   書き込む先は中身なのに、バケット本体のARNに権限を付けていました
-->

---
transition: slide-left
---

<ChapterLabel label="4章 トレース"/>

<AgentTitle :texts="['修正して再デプロイするね', 'デプロイ成功した！']" />

<PipelineStage :rail="$clicks < 1 ? '5-merge-pr' : '6-all-done'">

```ts [ソースコード]
// S3バケットへ書き込み権限を付与
conversationLog.grants.write(taskRole);
```

<div v-click>

```text [デプロイログ]
BotStack | UPDATE_COMPLETE | AWS::CloudFormation::Stack

 ✅  BotStack

Deployment time: 274.4s
```

</div>

</PipelineStage>

<!--
10. 自前のポリシーを grants.write の1行に置き換えました。
    L2 の grant を使えば、バケット本体と中身の両方に正しく権限が付きます
11. --no-rollback にしていたので、失敗した所から再開できました
12. 一番高い層の失敗が、エージェントの読める形で返ってきました。
    人間が原因を探す時間が乗りません
-->
