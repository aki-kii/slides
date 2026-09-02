---
layout: center
transition: fade
---

## ②ドリフトの予防

---
transition: slide-left
---

<ChapterLabel label="ドリフトのない運用：②予防"/>

## リソースを変更する権限を絞る

リソースの変更をCI/CDに限定し、ドリフトを未然に防ぐ

- 開発者のIAMポリシーからリソースの変更権限を除外する
- hotfixなど直接変更が必要な場合は、一時的な権限昇格の仕組みを検討する
  - e.g. TEAM（Temporary elevated access management）<GitHubCard repo="aws-samples/iam-identity-center-team" width="280px" />
