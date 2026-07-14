---
layout: two-cols-header
layoutClass: gap-8
transition: slide-left
---

## コストの比較

::left::

awslogs パターン

<img src="/images/logs-architecture.dio.png" />


::right::

awsfirelens パターン

<img src="/images/firelens-architecture.dio.png" />

<Overlay>
    FireLensパターンの検討を行います
</Overlay>

<!--
画像: なし

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
