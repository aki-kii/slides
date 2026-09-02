---
transition: fade
---

<ChapterLabel label="ドリフトの修正"/>

## ② ドリフトを**正**としてCDKに反映する

<img src="/images/drift-correction-refactor.dio.svg"/>

<br>

- `cdkrd check --pre-deploy`: ドリフトを検出しながら、コーディングエージェントでドリフトが無くなるまで修正する
  - `--pre-deploy`オプションをつけると合成したテンプレートとAWSリソースの差分を比較する
- ドリフトが無くなったらCDKデプロイする

---
transition: fade
---

<ChapterLabel label="ドリフトの修正：Step2. refactorフェーズ"/>

コーディングエージェントで差分をCDKソースに反映


```sh
/goal 以下の手順で、CDKソースと実環境のリソース状態を一致させてください。

1. `cdkrd check` を実行し、全ドリフト（declared + undeclared + added）を把握する
2. undeclared ドリフトがあれば、該当プロパティをライブ値でCDKコードに明示的に定義する
3. added out-of-band resourcesがあればCDKコードに定義を追加し、`cdk import` で取り込む
4. `cdkrd check --pre-deploy` を実行し、残りの declared ドリフトをCDKソースに取り込む
5. 差分が無くなるまで 2〜4 を繰り返す
```

→ ドリフトが発生してないことを確認してデプロイ！

<Kogoe>※ ここではリソースの変更が発生しません。</Kogoe>

<Overlay>これにてドリフトの修正は完了です！</Overlay>
