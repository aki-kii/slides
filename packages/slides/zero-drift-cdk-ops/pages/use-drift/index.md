---
layout: center
transition: fade
---

<div>
  <div>おまけ</div>
  <h2>ドリフトを利用する（？）</h2>
</div>

---
transition: fade
---

<ChapterLabel label="ドリフトを利用する"/>

## ドリフトを使い捨てる

今年に入ってからドリフトを1コマンドで元に戻せるようになりました

- `cdk deploy --revert-drift`（2026/3/9）
- `cdkrd revert`（2026/7/6）

EventBridge Schedulerのスケジュールを一度だけ実行したい時など、気軽に試せてコマンド1つで戻せるのが便利です！
