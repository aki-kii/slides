---
layout: center
transition: view-transition
---

<div>
  <div>そうなった時は</div>
  <h2>アプリログはLogsに書き出し続けるべき...？</h2>
</div>

<Overlay>
  いいえ、まだ希望があります！！！！
</Overlay>

---
transition: slide-left
---

<div>
  <h2>ECS Managed Instanceという選択肢</h2>
  <Kogoe>（まだ試せてないので違ったらすみません）</Kogoe>
</div>

<img src="/images/ecs-managed.png" class="h-36 mx-auto my-4" />

- EC2インスタンスでホストされるものの、管理はAWSに任せられる
- インスタンス単位でvCPUを決められるため、タスクに割り当てるvCPUを明示的に指定しなくてよい

<Overlay>

→ FireLensコンテナを追加してもvCPUが極端に増えない！

</Overlay>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/ManagedInstances.html" title="Amazon ECS Managed Instances (AWS ドキュメント)" />

---
transition: slide-left
---

<div>
  <h2>Managed Daemon(ECS Managed Instance)</h2>
</div>

<img src="/images/managed-daemon.dio.svg" class="h-44 mx-auto my-4" />

- **インスタンスごとに1つだけ**デーモンタスクを起動できる
- FargateのようにタスクごとにFireLensコンテナを割り当てる必要がないので、**vCPUを節約できる**

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/managed-daemons.html" title="Amazon ECS マネージドデーモン (AWS ドキュメント)" />

<!--
画像: なし

■ 今後の展望：ECS Managed Instances + Managed Daemons

- 今回のコスト増の根本原因は、Fargateがタスク単位の離散的なvCPUで課金されるため、FireLensサイドカーの追加で1vCPU→2vCPUに跳ね上がった点
- 解消手段として ECS Managed Instances への移行が考えられる
  - 課金がタスク単位ではなくEC2インスタンス単位になるため、Fargate特有のvCPUジャンプによるコスト増が発生しない
- さらに、2026年4月に登場した Managed Daemons を使えば、ログルーター（Fluent Bit）をインスタンスごとに1つだけ常駐させられる
  - タスクごとにFireLensサイドカーを積む必要がなくなるため、そもそもFireLensコンテナ自体が不要になる
- → Managed Instances + Managed Daemons（Fluent Bit）で、サイドカーなしでログをルーティングできる
-->
