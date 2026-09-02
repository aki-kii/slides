---
layout: center
transition: fade
---

## ④ドリフト対応の自動化

---
layout: center
transition: fade
---

<div>
    <div>ドリフト発生を検知した時</div>
    <h2>自動で対応できれば運用の負荷が下がります</h2><br>
    <strong>※ 自動化にはリスクもあるため、組織の運用方針に合わせて検討してください。</strong>
</div>

---
transition: fade
---

<ChapterLabel label="ドリフトのない運用：④自動化"/>

## ドリフトを全て破棄する

ドリフト検知ジョブで`cdkrd revert`を実行し、ドリフトを自動で破棄する

- ドリフトを絶対に許さない組織に向いている
- `--remove-unrecorded`で、追加された子リソースも削除できる

---
transition: slide-left
---

<ChapterLabel label="ドリフトのない運用：④自動化"/>

## ドリフトを全て記録する

検知ジョブで`cdkrd record`を実行し、ドリフトをベースラインに記録してPR（Pull Request）を作成する

- hotfixなどで直接変更が発生する運用に向いている
- 不要な記録はPR上で修正すればOK
- さらにドリフト修正手順をSkill化してAIエージェントに載せれば、CDKソースへの自動反映も自動化できる...！？
