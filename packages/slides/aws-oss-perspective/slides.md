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

<div class="h-full flex flex-col justify-center">
  <p style="font-size:1.2rem; color:rgba(255,255,255,0.8); margin:0 0 1rem 0;">
    JAWS-UG 茨城 #13 祝・新CBs誕生！AWS Community Builders LT大会
  </p>
  <h1>AWSはOSSをどのように<br>考えているのか？</h1>
  <div style="margin-top:2rem;">
    <div style="font-size:1.3rem; color:rgba(255,255,255,0.8); margin-bottom:0.4rem;">2026.5.13</div>
    <div style="font-size:1.5rem; font-weight:600; color:white;">池田 晃尚（@akikii__）</div>
  </div>
</div>

<div style="position:absolute; right:3rem; bottom:2.5rem;">
  <img src="/images/aboutme/eye-catch.png" class="h-48" />
</div>

---
layout: profile
transition: view-transition
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
---

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK" >



- AWS CDKへのコントリビュート 8件
- JAWS-UG CDK支部運営

</ProfileItem>

::footer::

<img src="/images/aboutme/jawsug-cdk-logo.png" />
<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---

<h2 class="slide-title">2026 AWS <span class="accent">Community Builders</span> になりました！</h2>

<BottomLinks>
  <BottomLink href="https://builder.aws.com/community/@akikii?tab=badges" label="builder.aws.com/community/@akikii" />
</BottomLinks>

<div style="display:flex; flex-direction:column; gap:1rem;">
  <img src="/images/cbs-devtools.png" style="width:100%; max-height:200px; object-fit:contain; object-position:left; border-radius:8px;" />

  <div v-click>
    <p style="font-size:1.05rem; font-weight:700; margin:0 0 0.2rem; color:var(--brand-deep);">Dev Tools とは？</p>
    <p style="margin:0 0 0.15rem; font-size:1rem;">ソフトウェア開発をより<Hl>迅速かつ効率的</Hl>にするテクノロジー</p>
    <p style="font-size:0.85rem; color:var(--ink-soft); margin:0 0 0.8rem;">IaC / CI/CD / IDE / テスト / 静的解析 など</p>
    <div style="display:flex; gap:1.5rem;">
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/cdk.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">AWS CDK</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/cloudformation.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">CloudFormation</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/sdk.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">AWS SDK</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/amplify.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">AWS Amplify</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/codepipeline.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">CodePipeline</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/codebuild.svg" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">CodeBuild</span>
      </div>
      <div style="display:flex; flex-direction:column; align-items:center; gap:0.4rem;">
        <img src="/images/aws-icons/kiro.png" style="width:40px; height:40px;" />
        <span style="font-size:0.7rem; color:var(--ink-soft);">Kiro</span>
      </div>
    </div>
  </div>
</div>

---
layout: center
class: text-left
transition: fade
---

## AWS Community Buildersプログラムメンバーに<br>なるための条件は何ですか？

---

<div style="height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1rem;">
  <div style="position:relative; display:inline-block;">
    <img src="/images/cbs-boshu-youkou.png" style="height:440px; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.12);" />
    <div style="position:absolute; top:53%; left:3%; width:42%; height:6%; background:rgba(255,220,0,0.5); border-radius:2px; pointer-events:none;"></div>
  </div>
  <BottomLinks>
    <BottomLink
      href="https://builder.aws.com/community/community-builders"
      title="引用元"
      label="AWS Community Builders — よくある質問（FAQ）"
    />
  </BottomLinks>
</div>

---

<div style="height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:1rem;">
  <div style="position:relative; display:inline-block;">
    <img src="/images/cbs-boshu-youkou.png" style="height:440px; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,0.12);" />
    <div style="position:absolute; top:53%; left:3%; width:42%; height:6%; background:rgba(255,220,0,0.5); border-radius:2px; pointer-events:none;"></div>
  </div>
  <BottomLinks>
    <BottomLink
      href="https://builder.aws.com/community/community-builders"
      title="引用元"
      label="AWS Community Builders — よくある質問（FAQ）"
    />
  </BottomLinks>
</div>
<div style="position:absolute; inset:0; background:rgba(255,255,255,0.6); z-index:99;"></div>
<Overlay position="center" fontSize="1.5rem">
  AWSはCommunity Buildersの評価基準にするほど<br>OSSを大事にしている
</Overlay>

---

<Eyebrow text="OSSとは" />
<h2 class="slide-title">OSSとは</h2>

<PlainList>
    <li>OSS = オープンソースソフトウェア</li>
    <li><Hl>ソースコードが公開</Hl>されていて、誰でも<Hl>閲覧・利用・改変・再配布</Hl>できるライセンスのもとで提供されているソフトウェア</li>
</PlainList>

<br>

<div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
  <Tag>Linux</Tag><Tag>Python</Tag><Tag>Node.js</Tag><Tag>Go</Tag><Tag>Rust</Tag><Tag>Ruby</Tag><Tag>PHP</Tag><Tag>TypeScript</Tag><Tag>OpenJDK</Tag><Tag>Kotlin</Tag>
  <Tag>Swift</Tag><Tag>Scala</Tag><Tag>Elixir</Tag><Tag>LLVM / Clang</Tag>
  <Tag>React</Tag><Tag>Vue.js</Tag><Tag>Angular</Tag><Tag>Next.js</Tag><Tag>Svelte</Tag><Tag>Vite</Tag><Tag>webpack</Tag><Tag>Tailwind CSS</Tag>
  <Tag>Django</Tag><Tag>Flask</Tag><Tag>FastAPI</Tag><Tag>Ruby on Rails</Tag><Tag>Spring Boot</Tag><Tag>Laravel</Tag><Tag>Express.js</Tag><Tag>NestJS</Tag>
  <Tag>MySQL</Tag><Tag>PostgreSQL</Tag><Tag>MongoDB</Tag><Tag>Redis</Tag><Tag>SQLite</Tag><Tag>MariaDB</Tag><Tag>Elasticsearch</Tag><Tag>ClickHouse</Tag><Tag>Cassandra</Tag>
  <Tag>Docker</Tag><Tag>Kubernetes</Tag><Tag>Terraform</Tag><Tag>Ansible</Tag><Tag>Helm</Tag><Tag>Argo CD</Tag>
  <Tag>Prometheus</Tag><Tag>Grafana</Tag><Tag>OpenTelemetry</Tag><Tag>Jaeger</Tag>
  <Tag>Nginx</Tag><Tag>HAProxy</Tag><Tag>Envoy</Tag><Tag>Istio</Tag><Tag>Traefik</Tag>
  <Tag>Apache Kafka</Tag><Tag>RabbitMQ</Tag><Tag>NATS</Tag>
  <Tag>TensorFlow</Tag><Tag>PyTorch</Tag><Tag>scikit-learn</Tag><Tag>Apache Spark</Tag><Tag>Apache Airflow</Tag><Tag>dbt</Tag>
  <Tag>Git</Tag><Tag>VS Code</Tag><Tag>Vim / Neovim</Tag><Tag>curl</Tag><Tag>OpenSSL</Tag><Tag>gRPC</Tag>
  <Tag>WordPress</Tag><Tag>Keycloak</Tag><Tag>Valkey</Tag><Tag>Cilium</Tag><Tag>Flux</Tag><Tag>CockroachDB</Tag><Tag>FreeBSD</Tag>
  <Tag>Zsh</Tag><Tag>tmux</Tag><Tag>GCC</Tag><Tag>GNU Make</Tag>
  <Tag>Pandas</Tag><Tag>NumPy</Tag><Tag>Jupyter</Tag><Tag>Matplotlib</Tag><Tag>Hugging Face</Tag><Tag>LangChain</Tag><Tag>ONNX</Tag>
  <Tag>Apache Flink</Tag><Tag>Trino</Tag><Tag>Apache Superset</Tag>
  <Tag>Loki</Tag><Tag>Fluentd</Tag><Tag>Fluent Bit</Tag><Tag>Logstash</Tag>
  <Tag>etcd</Tag><Tag>Consul</Tag><Tag>Vault</Tag><Tag>MinIO</Tag><Tag>containerd</Tag><Tag>Podman</Tag>
  <Tag>Trivy</Tag><Tag>Falco</Tag><Tag>OPA</Tag><Tag>Velero</Tag><Tag>K3s</Tag><Tag>Rancher</Tag>
  <Tag>Gitea</Tag><Tag>GitLab</Tag><Tag>Playwright</Tag><Tag>Selenium</Tag><Tag>Jest</Tag><Tag>pytest</Tag>
  <Tag>GraphQL</Tag><Tag>OpenAPI</Tag><Tag>Protocol Buffers</Tag>
  <Tag>FFmpeg</Tag><Tag>ImageMagick</Tag><Tag>Caddy</Tag><Tag>Apache Pulsar</Tag>
  <Tag>Nuxt.js</Tag><Tag>Astro</Tag><Tag>Remix</Tag><Tag>Prisma</Tag><Tag>SQLAlchemy</Tag><Tag>Hibernate</Tag>
  <Tag>Dagster</Tag><Tag>Prefect</Tag><Tag>Linkerd</Tag><Tag>Kyverno</Tag><Tag>cert-manager</Tag><Tag>Longhorn</Tag><Tag>Rook / Ceph</Tag><Tag>Crossplane</Tag>
</div>

---
clicks: 4
---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSとOSS" />
<h2 class="slide-title">AWSとOSSの<span class="accent">関わり方</span></h2>
<p style="margin:0 0 0.6rem;">AWS はオープンソースソフトウェアにどのように貢献していますか?</p>
<blockquote style="font-size:1.1rem; line-height:1.8; padding:0.7rem 0 0.7rem 1.5rem; margin:0 0 1.5rem;">
AWS は、オープンソースは <Hl>すべての人にとって良いもの</Hl> であると信じています。<br>私たちは、<Hl>オープンソースの価値をお客様に提供</Hl>し、AWSの運用上の優秀性をオープンソースコミュニティにもたらすことに取り組んでいます。
</blockquote>
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; flex:1; min-height:0; padding-bottom:2.5rem;">
  <Pillar v-click="1" title="OSSへの貢献">
    <ul>
      <li>AWSからOSSへの寄付</li>
      <li>AWSメンバーからのOSSコントリビュート</li>
    </ul>
  </Pillar>
  <Pillar v-click="2" title="OSSの公開">AWSの知見や技術をOSSとして公開</Pillar>
  <Pillar v-click="3" title="OSSを活用した<br>価値提供" :clickAt="4">
    <ul>
      <li>ユーザーのビジネスを最大化</li>
      <li>AWSの基盤を支える</li>
      <li>AWS活用を支援する</li>
    </ul>
  </Pillar>
</div>
<BottomLinks>
  <BottomLink href="https://aws.amazon.com/jp/what-is/open-source/" title="引用元" label="AWS — オープンソースとは？" />
</BottomLinks>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">ユーザービジネスを <span class="accent">最大化</span> させるOSS</h2>

<SlideDesc>
ユーザーが<Hl>undifferentiated heavy lifting</Hl>（差別化に繋がらない手間のかかる作業）にコストをかけるのをやめるために、AWSはOSSを<Hl>扱いやすくするサービスとして提供</Hl>
</SlideDesc>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:0.6rem; flex:1; min-height:0; align-content:start; margin:0 -2rem;">
  <OssCard color="#3334B9" icon="R" iconUrl="https://labs.mysql.com/common/logos/mysql-logo.svg" name="MySQL" desc="広く利用されているRDBのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/rds.svg" name="RDS / Aurora" /></template>
  </OssCard>
  <OssCard color="#E7157B" icon="K" iconUrl="https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.svg" name="Kubernetes" desc="コンテナ化されたアプリを管理するためのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="Amazon EKS" /></template>
  </OssCard>
  <OssCard color="#C7252A" icon="M" iconUrl="https://kafka.apache.org/logos/kafka-logo-tall.png" name="Apache Kafka" desc="大量データをリアルタイムに処理するストリーミング基盤OSS">
    <template #arrow><AwsService icon="/images/aws-icons/msk.svg" name="Amazon MSK" /></template>
  </OssCard>
  <OssCard color="#F46800" icon="G" iconUrl="https://raw.githubusercontent.com/grafana/grafana/main/public/img/grafana_icon.svg" name="Grafana" desc="メトリクスやログを可視化するためのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/managed-grafana.svg" name="Managed Grafana" /></template>
  </OssCard>
  <OssCard color="#C7252A" icon="V" iconUrl="https://raw.githubusercontent.com/valkey-io/valkey-io.github.io/main/static/img/Valkey-logo.svg" name="Valkey" desc="Redis互換のインメモリデータストアOSS">
    <template #arrow><AwsService icon="/images/aws-icons/elasticache.svg" name="ElastiCache" /></template>
  </OssCard>
</div>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWSの <span class="accent">基盤を支える</span> OSS</h2>

<SlideDesc>
    <PlainList>
        <li>AWS基盤にOSSを利用することで、 AWSも<Hl>undifferentiated heavy lifting</Hl>をやめることを実現</li>
        <li>AWSがフィードバックやコントリビュートすることで<Hl>OSSエコシステムの改善ループ</Hl>を回している</li>
    </PlainList>
</SlideDesc>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:0.6rem; flex:1; min-height:0; align-content:start; margin:0 -2rem;">
  <OssCard color="#4a5560" icon="L" iconUrl="https://raw.githubusercontent.com/torvalds/linux/master/Documentation/images/logo.svg" name="Linux" desc="多くのサーバーやクラウド基盤で利用されているOSのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/ec2.svg" name="AWS services 全般" /></template>
  </OssCard>
  <OssCard color="#1d3a82" icon="c" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/containerd/icon/color/containerd-icon-color.svg" name="containerd" desc="コンテナの実行を担うContainer RuntimeのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="EKS" /><AwsService icon="/images/aws-icons/fargate.svg" name="Fargate" /></template>
  </OssCard>
  <OssCard color="#F46800" icon="F" iconUrl="https://firecracker-microvm.github.io/img/logo-icon@3x.png" :isAws="true" name="Firecracker" desc="軽量VM(MicroVM)を実現するOSS">
    <template #arrow><AwsService icon="/images/aws-icons/lambda.svg" name="Lambda" /><AwsService icon="/images/aws-icons/fargate.svg" name="Fargate" /></template>
  </OssCard>
  <OssCard color="#2c7a3f" icon="B" iconUrl="/images/aws-icons/bottlerocket.svg" :isAws="true" name="Bottlerocket" desc="コンテナ実行に特化したLinuxベースのOSS">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="EKS" /><AwsService icon="/images/aws-icons/ecs.svg" name="ECS" /></template>
  </OssCard>
  <OssCard color="#425CC7" icon="OT" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/opentelemetry/icon/color/opentelemetry-icon-color.svg" name="OpenTelemetry" desc="テレメトリデータを管理するためのオブザーバビリティフレームワークOSS">
    <template #arrow><AwsService icon="/images/aws-icons/xray.svg" name="X-Ray" /><AwsService icon="/images/aws-icons/cloudwatch.svg" name="Application Signals" /></template>
  </OssCard>
</div>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWS利用を <span class="accent">支援</span> するOSS</h2>

<SlideDesc>
    <PlainList>
        <li>AWSの<Hl>セキュリティや運用、開発体験を向上</Hl>させるために様々なOSSが提供されている</li>
        <li>ユーザーのフィードバックやコントリビュートを受け入れ、<Hl>AWSエコシステムの改善ループ</Hl>を回している</li>
    </PlainList>
</SlideDesc>

<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:0.6rem; flex:1; min-height:0; align-content:start; margin:0 -2rem;">
  <OssCard color="#232F3E" icon="SDK" iconUrl="/images/aws-icons/sdk.svg" :isAws="true" :dense="true" name="AWS SDK" desc="各言語からAWSを操作するSDK" />
  <OssCard color="#232F3E" icon="$_" iconUrl="/images/aws-icons/cli.svg" :isAws="true" :dense="true" name="AWS CLI" desc="AWSを操作するCLIツール" />
  <OssCard color="#C7252A" icon="C" iconUrl="/images/aws-icons/cdk.svg" :isAws="true" :dense="true" name="AWS CDK" desc="プログラミング言語でAWSを定義するIaCツール" />
  <OssCard color="#E7157B" icon="A" iconUrl="/images/aws-icons/amplify.svg" :isAws="true" :dense="true" name="AWS Amplify" desc="Web / モバイル開発を支援するツール" />
  <OssCard color="#7d3cf0" icon="S" iconUrl="https://strandsagents.com/latest/assets/logo-github.svg" :isAws="true" :dense="true" name="Strands Agents" desc="AI Agent開発を支援するツール" />
  <OssCard color="#F46800" icon="λ" iconUrl="/images/aws-icons/lambda.svg" :isAws="true" :dense="true" name="Powertools" desc="Lambdaのベストプラクティスを手軽に扱えるツール" />
  <OssCard color="#7B42BC" icon="T" iconUrl="https://raw.githubusercontent.com/devicons/devicon/master/icons/terraform/terraform-original.svg" :dense="true" name="Terraform" desc="マルチクラウドのIaCツール" />
  <OssCard color="#0c1a24" icon="M" iconUrl="https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/mcp.png" :dense="true" name="MCP Servers" desc="AI Agentが連携するためのプロトコル" />
  <OssCard color="#1d3a82" icon="Tv" iconUrl="https://raw.githubusercontent.com/aquasecurity/trivy/main/docs/imgs/logo.png" :dense="true" name="Trivy" desc="アプリの脆弱性を検出するツール" />
  <OssCard color="#EF7B4D" icon="Ar" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/argo/icon/color/argo-icon-color.svg" :dense="true" name="Argo CD" desc="KubernetesのGitOps CD" />
</div>
</div>

---

<Eyebrow text="おわりに" />
<h2 class="slide-title">Summary</h2>

<ol style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:0;">
  <SummaryItem num="00" sub="OSSへの貢献 / OSSの公開 / OSSを活用した価値提供">
    AWSはOSSを <strong>「すべての人にとって良いもの」</strong> と考え、積極的に関わる
  </SummaryItem>
  <SummaryItem num="01" sub="MySQL · Kubernetis · Apache Kafka · Grafana · Valkey...">
      ユーザーが<strong>ビジネス価値の提供に注力</strong>できるよう、OSSをマネージドサービスとして提供
  </SummaryItem>
  <SummaryItem num="02" sub="Linux · containerd · Firecracker · Bottlerocket · OpenTelemetry...">
    <strong>AWSの基盤を支える</strong>ためにOSSを活用し、OSSエコシステムの改善ループを回している
  </SummaryItem>
  <SummaryItem num="03" sub="CDK · SDK · CLI · Amplify · Powertools · Argo CD ...">
    <strong>AWS利用を支援</strong>するOSSを公開し、AWSエコシステムの改善ループを回している
  </SummaryItem>
</ol>

---
layout: center
class: text-center
transition: fade
---

## 宣伝

---

<div style="position:absolute; inset:32px; display:flex; align-items:center; justify-content:center;">
  <div style="display:flex; flex-direction:column; gap:1.4rem;">
    <div>
      <h2 class="slide-title" style="margin-bottom:0;"><span class="accent">AWS CDK Conference</span> Japan 2026</h2>
    </div>
    <div style="display:flex; align-items:center; gap:2.5rem;">
      <img src="/images/cdk-conference.png" style="width:480px; border-radius:12px; box-shadow:0 4px 24px rgba(0,0,0,0.12); clip-path:inset(0 0 0 3px round 12px);" />
      <div>
        <div style="font-size:3.2rem; font-weight:900; color:var(--brand-deep); font-family:'JetBrains Mono',monospace; line-height:1.1;">7.18<span style="font-size:2rem; font-family:'Noto Sans JP',sans-serif;">（土）</span></div>
        <div style="font-size:2rem; font-weight:700; color:var(--brand-deep); margin-bottom:0.8rem;">開催決定！</div>
        <p style="font-size:1.2rem; color:var(--ink-soft); margin:0 0 1.2rem; line-height:1.8;">
          JAWS-UG CDK支部 主催<br>詳細は近日公開予定
        </p>
        <div style="display:flex; align-items:center; gap:1rem; padding:0.8rem 1rem; border-radius:0.75rem; border:2px solid var(--accent-warm); background:rgba(233,132,75,0.06);">
          <img src="/images/cfp-qr.png" style="width:72px; height:72px; flex-shrink:0;" />
          <div>
            <div style="font-size:1.1rem; font-weight:800; color:var(--accent-warm);">Call for Proposal</div>
            <div style="font-size:0.9rem; color:var(--ink-soft); line-height:1.5;">登壇者募集中！<br>（5/31 23:59まで）</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

---
layout: none
---

<div style="position:absolute; inset:0; display:flex; flex-direction:column;">
  <div style="flex:0 0 53%; overflow:hidden;">
    <img src="/images/mates-hero.png" style="width:100%; height:100%; object-fit:cover; object-position:left top;" />
  </div>
  <div style="flex:1; background:white; padding:1.4rem 3rem; display:flex; align-items:center; justify-content:center;">
    <div style="flex:0 0 auto; margin-right:48px;">
      <p style="color:#888; font-size:0.95rem; margin:0 0 0.3rem;">リードエンジニア（バックエンド/フロントエンド/SRE)</p>
      <p style="font-size:3rem; font-weight:900; margin:0 0 1rem; line-height:1.1;">
        <span style="color:#0283B2;">積極</span><span style="color:#1a1a1a;">採用中</span>
      </p>
      <div style="display:flex; align-items:center; gap:0.8rem;">
        <img src="/images/aboutme/mates-logo.png" style="height:40px;" />
        <div>
          <div style="font-size:0.95rem; font-weight:600; color:#333;">株式会社メイツ</div>
          <div style="font-size:0.85rem; color:#888;">Mates Inc.</div>
        </div>
      </div>
    </div>
    <div style="flex:0 0 auto; display:flex; flex-direction:column; align-items:center; gap:0.5rem;">
      <img src="/images/mates-pitta-qr-code.png" style="width:120px; height:120px; display:block;" />
      <p style="font-size:0.8rem; color:#888; margin:0;">カジュアル面談はこちら</p>
    </div>
  </div>
</div>

---
class: cover
---

<div style="position:absolute; left:10rem; top:50%; transform:translateY(-55%);">
    
  <h1 style="font-size:2.8rem; font-weight:900; color:white; line-height:1.25; margin:0 0 1rem; letter-spacing:-0.01em;">
      Thank You!
  </h1>
</div>

<div style="position:absolute; right:3rem; bottom:1.5rem; text-align:center;">
  <p style="color:white; font-size:1.15rem; margin:0 0 0.5rem; font-weight:500;">
    ＼ ご清聴ありがとうございました！ ／
  </p>
  <img src="/images/aboutme/eye-catch.png" style="height:190px;" />
</div>
