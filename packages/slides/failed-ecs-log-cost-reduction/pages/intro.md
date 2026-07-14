---
layout: center
transition: view-transition
---

<div>
  <h2>CloudWatch Logsの書き込み料金が<br>高い！！！</h2>
</div>

---
layout: two-cols-header
layoutClass: gap-8
transition: slide-left
---

ログ 100GB / 月あたりの書き込み料金

::left::

<div class="h-full flex flex-col justify-center items-center">

<BarChart
  unit="USD"
  :height="200"
  :bars="[
    { label: 'CloudWatch Logs', value: 76, color: '#E7157B', valueLabel: '76USD' },
    { label: 'S3 Bucket', value: 1, color: '#7AA116', valueLabel: '0.01USD 未満' },
  ]"
/>

<Kogoe>※ S3への書き込みは単純比較できないため概算</Kogoe>

</div>

::right::

<div class="h-full flex flex-col justify-center space-y-6">

<div>
  <div class="flex items-center gap-2 font-bold text-lg">
    <img src="/public/images/awsicons/cloudwatch.dio.png" class="h-12" />
    <span>CloudWatch Logs</span>
  </div>
  <div>0.76 USD / GB</div>
</div>

<div>
  <div class="flex items-center gap-2 font-bold text-lg">
    <img src="/public/images/awsicons/s3.dio.png" class="h-12" />
    <span>S3 Bucket（PUT）</span>
  </div>
  <div>0.0047 USD / 1,000 PUT</div>
</div>

</div>

<Overlay>
    コスト削減のためS3にログを書き出したい！
</Overlay>

<BottomLinks>
  <BottomLink href="https://aws.amazon.com/jp/cloudwatch/pricing/" title="Amazon CloudWatch 料金" />
  <BottomLink href="https://aws.amazon.com/jp/s3/pricing/" title="Amazon S3 料金" />
</BottomLinks>


<!--
画像: なし（左=BarChartで可視化 / 右=計算の内訳）

イントロ
とにかくCloudWatch Logsの書き込み料金が高いんです！

- CWL取り込み: $0.76 / GB → 100GB/月で $76（100 × 0.76）
- S3書き込み(PUT): $0.0047 / 1,000 PUT → 同条件で $0.01 未満（800 / 1000 × 0.0047）
  ※ Firehoseが128MB単位でまとめ書きするのでPUT回数は約800回（100GB ÷ 128MB）。詳細は後述
- → CWLは桁違いに高い。だからアプリログをS3に書き込む方式を検討した

後出し: Firehose取り込み料金・vCPU増はこの後のスライドで明かす
-->
