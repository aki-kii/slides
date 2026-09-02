---
layout: center
transition: fade
---

## ③ドリフトの検知

---
transition: fade
---

<ChapterLabel label="ドリフトのない運用：③検知"/>

## デプロイゲートで検知する

CIに`cdkrd check --fail`を組み込み、ドリフトしていればデプロイを停止

- ドリフトがある状態でデプロイすると、設定を意図せず上書きしてしまう可能性がある
- デプロイ前にドリフトを検知すれば安全にブロックできる

<Overlay>このタイミングでドリフトに気づくとデプロイが遅れてしまう...！</Overlay>

---
transition: slide-left
---

<ChapterLabel label="ドリフトのない運用：③検知"/>

## ドリフト検知ジョブをスケジュール実行する

`cdkrd check --fail`を定期実行し、ドリフト発生時に通知する

- GitHub Actionsなどでスケジュール実行する
- デプロイを待たずに早期検知できる
- 期間を短くすれば発生してすぐに気づけるため原因の特定がしやすい
