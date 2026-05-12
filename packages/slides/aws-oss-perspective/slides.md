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

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ（2025.9〜）">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK" />

::footer::

<img src="/images/aboutme/jawsug-cdk-logo.png" />
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

<p style="font-size:1.1rem; line-height:1.5; margin-bottom:1rem;">
<strong style="color:var(--brand-deep);">オープンソースソフトウェア（OSS）</strong> — ソースコードが公開され、誰でも <strong>閲覧・利用・改変・再配布</strong> できるソフトウェア。身近なところに溢れている。
</p>

<div style="display:flex; flex-wrap:wrap; gap:0.35rem; align-content:flex-start;">
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Linux</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Python</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Node.js</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Go</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Rust</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Ruby</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">PHP</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">TypeScript</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">OpenJDK</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Kotlin</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Swift</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Scala</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Elixir</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">LLVM / Clang</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">React</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Vue.js</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Angular</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Next.js</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Svelte</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Vite</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">webpack</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Tailwind CSS</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Django</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Flask</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">FastAPI</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Ruby on Rails</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Spring Boot</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Laravel</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Express.js</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">NestJS</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">MySQL</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">PostgreSQL</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">MongoDB</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Redis</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">SQLite</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">MariaDB</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Elasticsearch</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">ClickHouse</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Cassandra</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Docker</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Kubernetes</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Terraform</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Ansible</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Helm</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Argo CD</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Prometheus</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Grafana</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">OpenTelemetry</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Jaeger</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Nginx</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">HAProxy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Envoy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Istio</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Traefik</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Kafka</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">RabbitMQ</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">NATS</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">TensorFlow</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">PyTorch</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">scikit-learn</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Spark</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Airflow</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">dbt</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Git</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">VS Code</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Vim / Neovim</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">curl</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">OpenSSL</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">gRPC</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">WordPress</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Keycloak</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Valkey</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Cilium</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Flux</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">CockroachDB</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">FreeBSD</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Zsh</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">tmux</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">GCC</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">GNU Make</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Pandas</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">NumPy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Jupyter</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Matplotlib</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Hugging Face</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">LangChain</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">ONNX</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Flink</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Trino</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Superset</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Loki</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Fluentd</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Fluent Bit</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Logstash</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">etcd</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Consul</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Vault</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">MinIO</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">containerd</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Podman</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Trivy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Falco</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">OPA</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Velero</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">K3s</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Rancher</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Gitea</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">GitLab</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Playwright</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Selenium</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Jest</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">pytest</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">GraphQL</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">OpenAPI</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Protocol Buffers</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">FFmpeg</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">ImageMagick</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Caddy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Apache Pulsar</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Nuxt.js</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Astro</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Remix</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Prisma</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">SQLAlchemy</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Hibernate</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Dagster</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Prefect</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Linkerd</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Kyverno</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">cert-manager</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Longhorn</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Rook / Ceph</span>
  <span style="border:1.5px solid var(--line); border-radius:999px; padding:0.25rem 0.7rem; font-size:0.82rem; font-weight:600; color:var(--ink); white-space:nowrap;">Crossplane</span>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSとOSS" />
<h2 class="slide-title">AWSとOSSの<span class="accent">関わり方</span></h2>
<blockquote style="font-size:1.1rem; line-height:1.5; padding:0.7rem 0 0.7rem 1.5rem;">
AWS は、オープンソースは <em>すべての人にとって良いもの</em> であると信じています。<br>私たちは、オープンソースの価値をお客様に提供し、AWSの運用上の優秀性をオープンソースコミュニティにもたらすことに取り組んでいます。
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

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">ユーザービジネスを <span class="accent">最大化</span> させるOSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1rem;">
<span style="background:var(--brand-tint); color:var(--brand-deep); padding:0.2rem 0.6rem; border-radius:4px; font-weight:700;">差別化につながらない作業に手をかけない</span>
— OSSを <strong>マネージドサービス</strong> として提供。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); grid-template-rows:1fr; gap:0.6rem; flex:1; min-height:0; padding-bottom:2rem; margin:0 -2rem;">
  <OssCard color="#3334B9" icon="R" iconUrl="https://labs.mysql.com/common/logos/mysql-logo.svg" name="MySQL" desc="広く使われるRDB。運用負荷を肩代わり。">
    <template #arrow><AwsService icon="/images/aws-icons/rds.svg" name="RDS / Aurora" /></template>
  </OssCard>
  <OssCard color="#E7157B" icon="K" iconUrl="https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.svg" name="Kubernetes" desc="コンテナオーケストレーション。">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="Amazon EKS" /></template>
  </OssCard>
  <OssCard color="#C7252A" icon="M" iconUrl="https://kafka.apache.org/logos/kafka-logo-tall.png" name="Apache Kafka" desc="ストリーミング基盤。">
    <template #arrow><AwsService icon="/images/aws-icons/msk.svg" name="Amazon MSK" /></template>
  </OssCard>
  <OssCard color="#F46800" icon="G" iconUrl="https://raw.githubusercontent.com/grafana/grafana/main/public/img/grafana_icon.svg" name="Grafana" desc="メトリクス・ログ可視化。">
    <template #arrow><AwsService icon="/images/aws-icons/managed-grafana.svg" name="Managed Grafana" /></template>
  </OssCard>
  <OssCard color="#C7252A" icon="V" iconUrl="https://raw.githubusercontent.com/valkey-io/valkey-io.github.io/main/static/img/Valkey-logo.svg" name="Valkey" desc="Redis互換のインメモリストア。">
    <template #arrow><AwsService icon="/images/aws-icons/elasticache.svg" name="ElastiCache" /></template>
  </OssCard>
</div>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWSの <span class="accent">基盤を支える</span> OSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1rem;">
AWS自身もOSSを使い、<strong>フィードバック</strong> と <strong>コントリビュート</strong> で改善ループを回している。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); grid-template-rows:1fr; gap:0.6rem; flex:1; min-height:0; padding-bottom:2rem; margin:0 -2rem;">
  <OssCard color="#4a5560" icon="L" iconUrl="https://raw.githubusercontent.com/torvalds/linux/master/Documentation/images/logo.svg" name="Linux" desc="サービス基盤の多くで稼働。Kernelにも貢献。">
    <template #arrow><AwsService icon="/images/aws-icons/ec2.svg" name="AWS services 全般" /></template>
  </OssCard>
  <OssCard color="#1d3a82" icon="c" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/containerd/icon/color/containerd-icon-color.svg" name="containerd" desc="Container Runtime。コミュニティへ貢献。">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="EKS" /><AwsService icon="/images/aws-icons/fargate.svg" name="Fargate" /></template>
  </OssCard>
  <OssCard color="#F46800" icon="F" iconUrl="https://firecracker-microvm.github.io/img/logo-icon@3x.png" :isAws="true" name="Firecracker" desc="軽量MicroVM。AWSが公開。">
    <template #arrow><AwsService icon="/images/aws-icons/lambda.svg" name="Lambda" /><AwsService icon="/images/aws-icons/fargate.svg" name="Fargate" /></template>
  </OssCard>
  <OssCard color="#2c7a3f" icon="B" iconUrl="/images/aws-icons/bottlerocket.svg" :isAws="true" name="Bottlerocket" desc="コンテナ特化Linux。AWSが公開。">
    <template #arrow><AwsService icon="/images/aws-icons/eks.svg" name="EKS" /><AwsService icon="/images/aws-icons/ecs.svg" name="ECS" /></template>
  </OssCard>
  <OssCard color="#425CC7" icon="OT" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/opentelemetry/icon/color/opentelemetry-icon-color.svg" name="OpenTelemetry" desc="可観測性の標準仕様。AWSもコントリビュート。">
    <template #arrow><AwsService icon="/images/aws-icons/xray.svg" name="X-Ray" /><AwsService icon="/images/aws-icons/cloudwatch.svg" name="App Signals" /></template>
  </OssCard>
</div>
</div>

---

<div style="display:flex; flex-direction:column; height:100%;">
<Eyebrow text="AWSを活量した価値提供" />
<h2 class="slide-title">AWS利用を <span class="accent">支援</span> するOSS</h2>

<p style="font-size:1.1rem; color:var(--ink-soft); margin:-0.5rem 0 1rem;">
セキュリティ・運用・開発体験を上げるためのOSSを公開・活用。エコシステム全体で改善ループを回す。
</p>

<div style="display:grid; grid-template-columns:repeat(5,1fr); grid-template-rows:1fr; gap:0.6rem; flex:1; min-height:0; padding-bottom:2rem; margin:0 -2rem;">
  <OssCard color="#C7252A" icon="C" iconUrl="/images/aws-icons/cdk.svg" :isAws="true" :dense="true" name="AWS CDK" desc="言語でAWSを記述するIaC。" />
  <OssCard color="#232F3E" icon="SDK" iconUrl="/images/aws-icons/sdk.svg" :isAws="true" :dense="true" name="AWS SDK" desc="各言語からAWSを操作するSDK。" />
  <OssCard color="#232F3E" icon="$_" iconUrl="/images/aws-icons/cli.svg" :isAws="true" :dense="true" name="AWS CLI" desc="AWS操作と自動化のCLI。" />
  <OssCard color="#E7157B" icon="A" iconUrl="/images/aws-icons/amplify.svg" :isAws="true" :dense="true" name="AWS Amplify" desc="Web / モバイル開発支援。" />
  <OssCard color="#7d3cf0" icon="S" iconUrl="https://strandsagents.com/latest/assets/logo-github.svg" :isAws="true" :dense="true" name="Strands Agents" desc="AI Agent開発支援。" />
  <OssCard color="#F46800" icon="λ" iconUrl="/images/aws-icons/lambda.svg" :isAws="true" :dense="true" name="Powertools" desc="Lambdaのベストプラクティス。" />
  <OssCard color="#7B42BC" icon="T" iconUrl="https://raw.githubusercontent.com/devicons/devicon/master/icons/terraform/terraform-original.svg" :dense="true" name="Terraform" desc="マルチクラウドIaC。" />
  <OssCard color="#0c1a24" icon="M" iconUrl="https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/docs/mcp.png" :dense="true" name="MCP Servers" desc="AIエージェント連携。" />
  <OssCard color="#1d3a82" icon="Tv" iconUrl="https://raw.githubusercontent.com/aquasecurity/trivy/main/docs/imgs/logo.png" :dense="true" name="Trivy" desc="脆弱性スキャナ。" />
  <OssCard color="#EF7B4D" icon="Ar" iconUrl="https://raw.githubusercontent.com/cncf/artwork/main/projects/argo/icon/color/argo-icon-color.svg" :dense="true" name="Argo CD" desc="KubernetesのGitOps CD。EKSと相性抜群。" />
</div>
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
  <SummaryItem num="02" sub="Linux · containerd · Firecracker · Bottlerocket · OpenTelemetry">
    <strong>AWSの基盤を支える</strong> — OSSを活用しフィードバックで改善。
  </SummaryItem>
  <SummaryItem num="03" sub="CDK · SDK · CLI · Amplify · Powertools · Argo CD …">
    <strong>AWS利用を支援</strong> — OSSを公開しコミュニティと共に発展。
  </SummaryItem>
  <SummaryItem num="→" sub="Contribute back, and join the loop.">
    だから <strong>OSSへの貢献はCBs選考基準にも含まれる</strong>。
  </SummaryItem>
</ol>

---

<div style="position:absolute; inset:32px; display:flex; align-items:center; justify-content:center;">
  <div style="display:flex; flex-direction:column; gap:1.4rem;">
    <div>
      <Eyebrow text="告知" />
      <h2 class="slide-title" style="margin-bottom:0;"><span class="accent">AWS CDK Conference</span> Japan 2026</h2>
    </div>
    <div style="display:flex; align-items:center; gap:2.5rem;">
      <img src="/images/cdk-conference.png" style="width:480px; border-radius:12px; box-shadow:0 4px 24px rgba(0,0,0,0.12); clip-path:inset(0 0 0 3px round 12px);" />
      <div>
        <div style="font-size:3.2rem; font-weight:900; color:var(--brand-deep); font-family:'JetBrains Mono',monospace; line-height:1.1;">7.18<span style="font-size:2rem; font-family:'Noto Sans JP',sans-serif;">（土）</span></div>
        <div style="font-size:2rem; font-weight:700; color:var(--brand-deep); margin-bottom:0.8rem;">開催決定！</div>
        <p style="font-size:1.2rem; color:var(--ink-soft); margin:0; line-height:1.8;">
          JAWS-UG CDK支部 主催<br>詳細は近日公開予定
        </p>
      </div>
    </div>
  </div>
</div>

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
