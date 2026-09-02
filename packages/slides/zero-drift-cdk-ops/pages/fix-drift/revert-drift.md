---
transition: fade
---

<ChapterLabel label="ドリフトの修正"/>

## ① ドリフトを**誤**として破棄する

<br>

<img src="/images/drift-correction-revert.dio.svg"/>

<br>

- `cdkrd revert`：破棄したいドリフトを選択してスタックに定義されている値もしくはデフォルト値に戻す

<Kogoe>※ 子リソースを破棄するには`--remove-unrecorded`オプションが必要</Kogoe>

---
transition: slide-left
---

<ChapterLabel label="ドリフトの修正：Step1. revertフェーズ"/>

対象のドリフトを選択して破棄する

```sh
❯ pnpm exec cdkrd revert
● CdkrdVerify-main (ap-northeast-1): reading live AWS state & computing drift…
  space = toggle · → = all · ← = none · enter = confirm
  # ■ 選択済み：revert する
  ■ Description -> deployed-template value
  ■ MemorySize  -> remove (undeclared, not in baseline)
  # □ 未選択：ドリフト状態のままにする
  □ Timeout     -> remove (undeclared, not in baseline)
  □ AWS_IAM ... -> DELETE out-of-band AWS::Lambda::Url
  2 selected
◆ Apply 2 revert op(s) to CdkrdVerify-main? This WRITES to AWS.  ● Yes
CdkrdVerify-main: CLEAN after revert.
```

<Kogoe>※ 出力は一部省略しています</Kogoe>
