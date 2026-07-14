---
transition: fade
---


<div class="mt-6 flex flex-col gap-3">
  <div v-for="item in [
    { date: '2026/3/19', name: 'Trivy' },
    { date: '2026/3/23', name: 'Checkmarx KICS' },
    { date: '2026/3/24', name: 'LiteLLM / Telnyx' },
    { date: '2026/3/31', name: 'axios' },
    { date: '2026/4/22', name: 'Bitwarden CLI' },
    { date: '2026/5/11', name: 'TanStack / Mistral AI / UiPath' },
  ]" :key="item.date" class="flex items-center gap-4 border-l-4 border-blue-500 pl-4 py-1">
    <span class="font-mono text-sm text-gray-400 w-28 shrink-0">{{ item.date }}</span>
    <span class="font-mono text-base font-semibold">{{ item.name }}</span>
  </div>
</div>
<br>
<v-click>
→ たくさんのツールが<strong>サプライチェーン攻撃による侵害</strong>を受けています！
</v-click>

---
transition: slide-left
---

<div style="view-transition-name: software-sapply-chain-attack">
    <h2>ソフトウェアサプライチェーン攻撃とは</h2>
</div> 

ソフトウェアが依存するライブラリやツールに<strong>悪意あるコードを混入</strong>し、取り込んだプロダクトを<strong>間接的に侵害</strong>する攻撃手法

<v-click>

<Card title="2026/3/31 - npmパッケージ「axios」の侵害" variant="info">

<PlainList>
<li>メンテナーアカウントの乗っ取りにより悪意あるバージョンが公開されました。</li>
<li>インストールするだけでRATが展開、<strong>ローカルのクレデンシャル・APIキーが外部に送信</strong>されました。</li>
</PlainList>

</Card>

</v-click>

<v-click>
→ <strong>プロダクトに影響がないか</strong>迅速に調査する必要がある
</v-click>

<Overlay position="center" clickStart="3">
    <strong>SBOM</strong>を利用してコンテナイメージへの影響範囲を<br>一瞬で特定する方法を紹介します！
</Overlay>
