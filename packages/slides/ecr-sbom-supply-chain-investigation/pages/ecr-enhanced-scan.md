---
layout: center
transition: view-transition
---


<div style="view-transition-name: ecr-enhanced-scan">
    <h2>ECR拡張スキャン？</h2>
</div>

---
transition: slide-left
---

<div style="view-transition-name: ecr-enhanced-scan">
    <h2>ECRイメージスキャン（拡張スキャン）とは？</h2>
</div> 

ECRリポジトリに登録された<strong>コンテナイメージをセキュリティスキャン</strong>するAmazon Inspectorの機能（ECRに統合されている）

<v-click>

- OS・パッケージ/ライブラリの脆弱性を検出
- 脆弱性DBにCVEが追加されるとスキャン（継続スキャンの場合）
- コンテナイメージの **SBOM をエクスポート**できる

<Kogoe>※ ECRベーシックスキャン、プッシュスキャンはSBOMエクスポート非対応</Kogoe>

</v-click>
