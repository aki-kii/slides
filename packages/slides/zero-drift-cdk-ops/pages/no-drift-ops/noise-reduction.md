---
layout: center
transition: fade
---

## ①ドリフトの誤検知を除外する

---
transition: fade
---

<ChapterLabel label="ドリフトのない運用：①誤検知の除外"/>

## ベースラインに記録する

`cdkrd record`<br>
CDKで定義していないプロパティの期待値をベースラインに記録する。<br>
記録した値と実環境が異なれば、ドリフトとして検出できる

- CDK以外の仕組みで管理されているプロパティ
  - e.g. AWS Config自動修復
- CloudFormation未定義のプロパティ

---
transition: slide-left
---

<ChapterLabel label="ドリフトのない運用：①誤検知の除外"/>

## 変化する値をドリフト対象外にする

`cdkrd ignore`<br>
値が外部の影響で変化するプロパティはドリフトの検知から除外する

- ECS AutoScalingでECSタスクの必要タスク数が増減する
- Parameter Storeの値を書き換える
