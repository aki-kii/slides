---
transition: fade
---

## ドリフトとは？

CDKの差分は2種類ある

- ≠ cdk diff：テンプレートとスタックの差分を検出する
- = cdk drift：スタックとAWSリソースの差分を検出する


<img src="/images/cdk-diff-drift.dio.svg" class="mt-2 w-full max-h-[50%] object-contain mx-auto">

---
transition: fade
---

## ドリフトとは？

スタックの定義とAWSリソースの設定値の差異をドリフトと呼ぶ

<img src="/images/cdk-drift.dio.svg" class="mt-2 w-full max-h-[70%] object-contain mx-auto">

---
transition: fade
---

## ドリフトがなぜ問題になるの？

IaCでは管理下のリソースをIaC以外の方法で変更しないことが鉄則

- IaCでの一元管理が成り立たなくなり見通しが悪くなる
- デプロイ時に設定が競合して消えてしまう可能性がある
- デプロイ時にエラーが発生する場合がある

<BottomLink label="CloudFormation ベストプラクティス - CloudFormation ですべてのスタックリソースを管理する" href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/best-practices.html#donttouch" />

<Overlay>CDK・CloudFormationのドリフトには問題点がある...！</Overlay>

---
layout: center
transition: fade
---

<div>
  <div>CDK・CloudFormationのドリフトの問題点</div>
　　<h2>全てのプロパティのドリフトを<br>検出できない！！！</h2>
</div>

---
transition: slide-left
---

## CDKドリフトでは検出できない差分

<br>

<img src="/images/no-drift-detect.dio.svg">

<Overlay>
そんな中、希望の光が...！
</Overlay>
