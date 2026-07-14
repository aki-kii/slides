---
layoutClass: gap-8
transition: slide-left
---

## アーキテクチャの比較

<img src="/images/logs-architecture.dio.svg" />

<v-click>
  <Annotation x="71%" y="78%" width="88px">
    書き込み料金<br>Down
  </Annotation>
  <Annotation x="57%" y="50%" width="48px">
    vCPU料金<br>Up
  </Annotation>
  <Annotation x="71%" y="52%" width="88px">
    書き込み料金<br>Up
  </Annotation>

</v-click>

<BottomLinks>
  <BottomLink href="https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/userguide/using_firelens.html" title="Amazon ECS ログを AWS サービスまたは AWS Partner に送信する (FireLens)" />
  <BottomLink href="https://aws.amazon.com/jp/firehose/pricing/" title="Amazon Data Firehose 料金" />
</BottomLinks>

<!--

■ 現状の構成

- アプリはECSでホスティングし、すべてのログをCloudWatch Logsに送信している
- 【図1: 構成図（現状）】① ECS（Fargate / アプリコンテナ）→ CloudWatch Logs
- そこで、アプリログをS3へ配信する方法に変更することを検討
- S3へ配信できればCWLの高いログ取り込み料金がかからないのでコスト削減になりそう

■ 変更案のアーキテクチャ

- FireLensコンテナを利用してアプリログをS3バケットに配信する方法を検討
- 【図2: 構成図（変更案）】
  ② ECS（Fargate / アプリコンテナ + FireLensコンテナ）
    → Data Firehose → S3（アプリログ）
    → CloudWatch Logs（エラーログ）
- FireLensコンテナ: 他コンテナのログをルーティングする役割。アプリログを後続のData Firehoseへストリーミング出力（図3→FireLensコンテナ）
- Data Firehose: ストリーミング出力されたアプリログを受け付け、一定量たまったらまとめてS3に保存（図3→Data Firehose-S3）
- エラーログ: メトリクスフィルターでAlarmを作っているため、そのままCloudWatch Logsに出力（図3→FireLens-CWL）

■ コスト発生源の比較

【CWL（現状）】
① CloudWatch Logs
  取り込み料金、保存料金

【S3 + CWL（変更案）】
① FireLensコンテナ
  ECSタスクに割り当てるvCPUの増加分
② Data Firehose
  取り込み料金（取り込んだデータ量に応じて課金）
③ S3バケット
  取り込みは実質無料（PUTリクエスト料金のみ。Firehoseがまとめて書き込むので僅少）、保存料金、取得（GETリクエスト）料金
④ CloudWatch Logs
  取り込み料金、保存料金、クエリ料金

→ エラーログはリクエストのたびに発生するものではなく、微々たる量なのでコスト計算からは除外

-->
