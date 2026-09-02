---
transition: slide-left
---

# ログ書き込み料金の削減効果が薄い

<img src="/images/cost-calculate.dio.svg" class="mt-2 w-full max-h-[60%] object-contain mx-auto" />

<Kogoe>※ 一部計算式を簡略化しています。</Kogoe>

<br>

<v-click>
  → ログ量が少なく「削減できる料金」を<strong>「増加する料金」が上回って</strong>しまいました...
</v-click>

<!--
画像: /images/cost-calculate.dio.svg（削減できる料金 vs 増加する料金 の内訳）

■ 理由②：ログ量がそんなに多くなかった

- 削減できる料金 = ログの量 ×（Logs書き込み単価 − Firehose書き込み単価）
                  ＋ 保存期間分のログの量 ×（Logs保存単価 − S3保存単価）
- 増加する料金 = vCPU単価 × 1タスクのvCPU × 総稼働時間（＝Fargate料金の差分）
- ポイント: 削減側は「ログの量」に比例。増加側（vCPU）はログ量に依存しない
- 今回はログ量が小さく、削減できる料金が増加する料金に届かなかった → ペイできなかった
-->
