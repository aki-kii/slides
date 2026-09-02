---
layout: center
transition: view-transition
---

<div>
  <div>検討の結果...</div>
  <v-click>
  <h2>FireLensパターンは<strong>不採用！！！</strong></h2>
  </v-click>
</div>

<v-click>
　　→　導入すると逆に<strong>コスト増</strong>になってしまった
</v-click>

<Overlay>
    FireLensはコスト削減で<br>よく利用されているパターンなのに？？？  
</Overlay>

<!--
画像: なし

■ 結論：S3移行を断念

- 弊社ではアプリログのS3移行を断念した
- CloudWatch Logsだけにログを出力していたパターンに比べて、約3倍もコストがかかる計算結果になったため
- コスト増の主な原因は、FireLensコンテナを追加したことによるECSタスクのvCPU増加
- FireLensを利用するパターンはよくあるコスト削減パターン。なぜ弊社のアーキテクチャではコスト増となったかを次から解説
-->
