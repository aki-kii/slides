---
background: '#015d7d'
class: 'cover'
drawings:
  persist: false
transition: slide-left
title: AWSはOSSをどのように思っているのか？
mdc: true
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'JetBrains Mono'
---

<p style="font-size:1.2rem; color:rgba(255,255,255,0.8); margin:0;">
JAWS-UG 茨城 #13 祝・新CBs誕生！AWS Community Builders LT大会
</p>
<br>

# AWSはOSSをどのように<br>考えているのか？

<div style="position:absolute; bottom:3.5rem; left:6rem;">
  <div style="font-size:1.3rem; color:rgba(255,255,255,0.8); margin-bottom:0.4rem;">2026.5.13</div>
  <div style="font-size:1.5rem; font-weight:600; color:white;">池田 晃尚（@akikii__）</div>
</div>

<div style="position:absolute; right:2rem; bottom:0.5rem;">
  <img src="/images/aboutme/eye-catch.png" class="h-48" />
</div>

---
layout: profile
transition: view-transition
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
---

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ（2025.9〜）">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK" />

::footer::

<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---

<Eyebrow text="はじめに" />
<h2 class="slide-title">このテーマを選んだ理由</h2>

AWS Community Buildersプログラムメンバーになるための条件は何ですか？
<blockquote>
ブログ記事、動画、<strong style="background:var(--brand-tint); color:var(--brand-deep); padding:2px 8px; border-radius:4px;">オープンソースへの貢献</strong>、プレゼンテーションなど、他のAWS利用者の助けとなる技術コンテンツの根拠や正確さが最も重視されます。
</blockquote>

<BottomLinks>
  <BottomLink
    href="https://builder.aws.com/community/community-builders"
    title="引用元"
    label="AWS Community Builders — よくある質問（FAQ）"
  />
</BottomLinks>

<p style="margin-top:2.5rem; font-size:1.4rem; color:var(--ink-soft); line-height:1.7;">
<span style="color:var(--brand); font-family:'JetBrains Mono',monospace; font-size:1.6rem;">→</span>
筆者は <strong>AWS CDK へのコントリビュート</strong> をCBs応募に提出。<br>
選考基準にOSSが含まれている <strong>＝ AWSはOSSをどう捉えているのか</strong> を整理したい。
</p>

---

<Eyebrow text="はじめに" />
<h2 class="slide-title">Agenda</h2>

<div style="display:flex; flex-direction:column;">
  <AgendaItem num="01" title="OSSとは" sub="用語の確認・身近な例" />
  <AgendaItem num="02" title="AWSとOSS — 3つの関わり方" sub="貢献／公開／活用した価値提供" />
  <AgendaItem num="03" title="OSSを活用した価値提供 — 3つの視点" sub="ユーザービジネス／AWS基盤／AWS利用支援" />
</div>

---

<Eyebrow text="OSSとは" />
<h2 class="slide-title">OSSとは</h2>

<p style="font-size:1.5rem; line-height:1.7;">
<strong style="color:var(--brand-deep);">オープンソースソフトウェア（Open Source Software）</strong>。<br>
ソースコードが公開され、誰でも <strong>閲覧・利用・改変・再配布</strong> できるライセンスのもとで提供されているソフトウェア。
</p>

<div style="margin-top:2.5rem; display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;">
  <span style="font-family:'JetBrains Mono',monospace; color:var(--ink-mute); letter-spacing:0.12em; margin-right:0.5rem;">EXAMPLES /</span>
  <span style="border:2px solid var(--ink); border-radius:999px; padding:0.5rem 1rem; font-weight:600; display:inline-flex; align-items:center; gap:0.5rem;"><span style="width:10px; height:10px; border-radius:50%; background:var(--brand); flex-shrink:0;"></span>Linux</span>
  <span style="border:2px solid var(--ink); border-radius:999px; padding:0.5rem 1rem; font-weight:600; display:inline-flex; align-items:center; gap:0.5rem;"><span style="width:10px; height:10px; border-radius:50%; background:var(--brand); flex-shrink:0;"></span>MySQL</span>
  <span style="border:2px solid var(--ink); border-radius:999px; padding:0.5rem 1rem; font-weight:600; display:inline-flex; align-items:center; gap:0.5rem;"><span style="width:10px; height:10px; border-radius:50%; background:var(--brand); flex-shrink:0;"></span>Kubernetes</span>
  <span style="border:2px solid var(--ink); border-radius:999px; padding:0.5rem 1rem; font-weight:600; display:inline-flex; align-items:center; gap:0.5rem;"><span style="width:10px; height:10px; border-radius:50%; background:var(--brand); flex-shrink:0;"></span>Docker</span>
  <span style="font-family:'JetBrains Mono',monospace; color:var(--ink-mute);">… 数えきれない</span>
</div>

---

<Eyebrow text="AWSとOSS" />
<h2 class="slide-title">AWSの <span class="accent">公式見解</span></h2>

<blockquote>
AWS は、オープンソースは <em>すべての人にとって良いもの</em> であると信じています。私たちは、オープンソースの価値をお客様に提供し、AWSの運用上の優秀性をオープンソースコミュニティにもたらすことに取り組んでいます。
</blockquote>

<BottomLinks>
  <BottomLink
    href="https://aws.amazon.com/jp/what-is/open-source/"
    title="引用元"
    label="AWS — オープンソースとは？"
  />
</BottomLinks>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSとOSS" />
<h2 class="slide-title">AWSのOSSへの関わり方 <span class="accent">3つ</span></h2>
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1.4rem; flex:1; min-height:0;">
  <Pillar tag="01 — CONTRIBUTE" title="OSSへの貢献">AWSメンバーによるコントリビュート。OSSプロジェクトや財団への寄付。</Pillar>
  <Pillar tag="02 — RELEASE" title="OSSの公開">AWSの社内知見・技術を、コミュニティが使える形でオープンに公開する。</Pillar>
  <Pillar tag="03 — DELIVER VALUE" title="OSSを活用した<br>価値提供" :featured="true">ユーザービジネスの最大化、AWS基盤、AWS利用支援にOSSを活かす。</Pillar>
</div>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSとOSS" />
<h2 class="slide-title">AWSとOSSの<span class="accent">関わり方</span></h2>
<blockquote style="font-size:1.1rem; line-height:1.5; padding:0.7rem 0 0.7rem 1.5rem;">
AWS は、オープンソースは <em>すべての人にとって良いもの</em> であると信じています。私たちは、オープンソースの価値をお客様に提供し、AWSの運用上の優秀性をオープンソースコミュニティにもたらすことに取り組んでいます。
</blockquote>
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; flex:1; min-height:0; margin-top:1rem; padding-bottom:2.5rem;">
  <Pillar tag="01 — CONTRIBUTE" title="OSSへの貢献">AWSメンバーによるコントリビュート。OSSプロジェクトや財団への寄付。</Pillar>
  <Pillar tag="02 — RELEASE" title="OSSの公開">AWSの社内知見・技術を、コミュニティが使える形でオープンに公開する。</Pillar>
  <Pillar tag="03 — DELIVER VALUE" title="OSSを活用した<br>価値提供" :featured="true">ユーザービジネスの最大化、AWS基盤、AWS利用支援にOSSを活かす。</Pillar>
</div>
<BottomLinks>
  <BottomLink href="https://aws.amazon.com/jp/what-is/open-source/" title="引用元" label="AWS — オープンソースとは？" />
</BottomLinks>
</div>

---

<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">ユーザービジネスを <span class="accent">最大化</span> させるOSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1.5rem;">
<span style="background:var(--brand-tint); color:var(--brand-deep); padding:0.2rem 0.6rem; border-radius:4px; font-weight:700;">差別化につながらない作業に手をかけない</span>
— OSSを <strong>マネージドサービス</strong> として提供。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:1rem;">
  <OssCard color="#3334B9" icon="R" name="MySQL / PostgreSQL" desc="広く使われるRDB。運用負荷を肩代わり。">
    <template #arrow><span class="aws-icon" style="background:#3334B9">RDS</span>RDS / Aurora</template>
  </OssCard>
  <OssCard color="#E7157B" icon="K" name="Kubernetes" desc="コンテナオーケストレーション。">
    <template #arrow><span class="aws-icon" style="background:#E7157B">EKS</span>Amazon EKS</template>
  </OssCard>
  <OssCard color="#C7252A" icon="M" name="Apache Kafka" desc="ストリーミング基盤。">
    <template #arrow><span class="aws-icon" style="background:#C7252A">MSK</span>Amazon MSK</template>
  </OssCard>
  <OssCard color="#F46800" icon="G" name="Grafana" desc="メトリクス・ログ可視化。">
    <template #arrow><span class="aws-icon" style="background:#F46800">MG</span>Managed Grafana</template>
  </OssCard>
  <OssCard color="#C7252A" icon="V" name="Valkey" desc="Redis互換のインメモリストア。">
    <template #arrow><span class="aws-icon" style="background:#C7252A">EC</span>ElastiCache</template>
  </OssCard>
</div>

---

<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWSの <span class="accent">基盤を支える</span> OSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1.5rem;">
AWS自身もOSSを使い、<strong>フィードバック</strong> と <strong>コントリビュート</strong> で改善ループを回している。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:1rem;">
  <OssCard color="#4a5560" icon="L" name="Linux" desc="サービス基盤の多くで稼働。Kernelにも貢献。">
    <template #arrow><span class="aws-icon" style="background:#4a5560">EC2</span>AWS services 全般</template>
  </OssCard>
  <OssCard color="#1d3a82" icon="c" name="containerd" desc="Container Runtime。コミュニティへ貢献。">
    <template #arrow><span class="aws-icon" style="background:#E7157B">EKS</span><span class="aws-icon" style="background:#F46800">FG</span>EKS / Fargate</template>
  </OssCard>
  <OssCard color="#F46800" icon="F" :isAws="true" name="Firecracker" desc="軽量MicroVM。AWSが公開。">
    <template #arrow><span class="aws-icon" style="background:#F46800">λ</span><span class="aws-icon" style="background:#F46800">FG</span>Lambda / Fargate</template>
  </OssCard>
  <OssCard color="#2c7a3f" icon="B" :isAws="true" name="Bottlerocket" desc="コンテナ特化Linux。AWSが公開。">
    <template #arrow><span class="aws-icon" style="background:#E7157B">EKS</span><span class="aws-icon" style="background:#F46800">ECS</span>EKS / ECS host</template>
  </OssCard>
  <OssCard color="#1a2a52" icon="C" :isAws="true" name="Corretto / OpenJDK" desc="OpenJDKベースのJava実行環境。">
    <template #arrow><span class="aws-icon" style="background:#1a2a52">JDK</span>Java runtime</template>
  </OssCard>
</div>

---

<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWS利用を <span class="accent">支援</span> するOSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1.5rem;">
セキュリティ・運用・開発体験を上げるためのOSSを公開・活用。エコシステム全体で改善ループを回す。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:0.7rem;">
  <OssCard color="#C7252A" icon="C" :isAws="true" :dense="true" name="AWS CDK" desc="言語でAWSを記述するIaC。" />
  <OssCard color="#232F3E" icon="$_" :isAws="true" :dense="true" name="AWS CLI" desc="AWS操作と自動化のCLI。" />
  <OssCard color="#E7157B" icon="A" :isAws="true" :dense="true" name="AWS Amplify" desc="Web / モバイル開発支援。" />
  <OssCard color="#7d3cf0" icon="S" :isAws="true" :dense="true" name="Strands Agents" desc="AI Agent開発支援。" />
  <OssCard color="#F46800" icon="λ" :isAws="true" :dense="true" name="Powertools" desc="Lambdaのベストプラクティス。" />
  <OssCard color="#7B42BC" icon="T" :dense="true" name="Terraform" desc="マルチクラウドIaC。" />
  <OssCard color="#0c1a24" icon="M" :dense="true" name="MCP Servers" desc="AIエージェント連携。" />
  <OssCard color="#1d3a82" icon="Tv" :dense="true" name="Trivy" desc="脆弱性スキャナ。" />
  <OssCard color="#2c7a3f" icon="e" :dense="true" name="ecspresso" desc="ECSのデプロイ支援。" />
  <OssCard color="#F46800" icon="Fn" :isAws="true" :dense="true" name="Finch" desc="ローカルコンテナ実行。" />
</div>

---

<Eyebrow text="おわりに" />
<h2 class="slide-title">Summary</h2>

<ol style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0;">
  <SummaryItem num="00" sub="Contribute / Release / Deliver Value">
    AWSはOSSを <strong>「すべての人にとって良いもの」</strong> と考え、積極的に関わる。
  </SummaryItem>
  <SummaryItem num="01" sub="RDS · EKS · MSK · Managed Grafana · ElastiCache">
    <strong>ユーザービジネスを最大化</strong> — OSSをマネージドサービスとして提供。
  </SummaryItem>
  <SummaryItem num="02" sub="Linux · containerd · Firecracker · Bottlerocket · Corretto">
    <strong>AWSの基盤を支える</strong> — OSSを活用しフィードバックで改善。
  </SummaryItem>
  <SummaryItem num="03" sub="CDK · CLI · Amplify · Powertools · Strands · Finch …">
    <strong>AWS利用を支援</strong> — OSSを公開しコミュニティと共に発展。
  </SummaryItem>
  <SummaryItem num="→" sub="Contribute back, and join the loop.">
    だから <strong>OSSへの貢献はCBs選考基準にも含まれる</strong>。
  </SummaryItem>
</ol>

---
class: cover
---

<!-- キャッチーなメッセージ（左側） -->
<div style="position:absolute; left:5rem; top:50%; transform:translateY(-55%);">
  <p style="font-size:1.3rem; color:rgba(255,255,255,0.75); margin:0 0 0.6rem; font-weight:400;">みなさんも</p>
  <h1 style="font-size:2.8rem; font-weight:900; color:white; line-height:1.25; margin:0 0 1rem; letter-spacing:-0.01em;">
    OSSへの貢献が<br>CBsへの近道かも？
  </h1>
  <p style="font-size:1.3rem; color:rgba(255,255,255,0.8);">と気づいてもらえましたか？</p>
</div>

<!-- 吹き出し＋フクロウ（右下） -->
<div style="position:absolute; right:3rem; bottom:1.5rem; text-align:center;">
  <p style="color:white; font-size:1.15rem; margin:0 0 0.5rem; font-weight:500;">
    ＼ ご清聴ありがとうございました！ ／
  </p>
  <img src="/images/aboutme/eye-catch.png" style="height:190px;" />
</div>
