---
id: theme-verification
name: 検証してみた系
---

何かを実際に試して、測った結果や分かったことを見せる話

## 見本

<!-- shots:theme-verification -->

failed-ecs の p.3 言い切り → p.5 図 → p.6 Overlay → p.7 図 → p.13 まとめ

## 中身

- **デッキ**: container-31（「SOCIインデックスでコンテナの起動を速くしてみた」）、failed-ecs（「ECSアプリログをFireLensでコスト削減しようとしたけど諦めた話」）、cdk-day1（「最初からAWS CDKで技術検証してもいいんじゃない？」）、ecr-sbom（「ECR拡張スキャンでSBOMを収集してサプライチェーン攻撃の影響調査を爆速で終わらせてみた」）
- **背骨**: [分析 → 改善 → 振り返り](@flow-analyze-improve-review)。導入では困りごとを言い切る（failed-ecs「CloudWatch Logsの書き込み料金が高い！！！」）
- **主役のページ**: 困りごとの [言い切り](@page-kamishibai)、使うものの [「〜とは？」](@page-what-is-list)、構成や測った結果の [図＋結論](@page-figure-conclusion)、締めの [まとめ（言い切り）](@page-summary-statement)

## 気を付けること

- 悪くなった所も見せる（コンテナ支部、2026-11-15）。諦めた話も結果として見せてよい（failed-ecs）
