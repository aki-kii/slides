---
transition: fade
---

<div class="absolute inset-8 flex items-center justify-center">
  <div class="flex flex-col gap-6">
    <h2 class="slide-title !m-0"><span class="accent">AWS CDK Conference</span> Japan 2026</h2>
    <div class="flex items-center gap-10">
      <img src="/images/cdk-conference.png" class="cdk-conf-img rounded-xl shadow-lg flex-shrink-0" />
      <div>
        <div class="cdk-conf-date font-black leading-tight mb-2">7.18<span class="cdk-conf-date-sub">（土）</span></div>
        <div class="cdk-conf-launch font-bold mb-3">開催決定！</div>
        <p class="cdk-conf-desc mb-5">JAWS-UG CDK支部 主催<br>詳細は近日公開予定</p>
        <div class="cfp-box flex items-center gap-4 p-3 rounded-xl border-2">
          <img src="/images/cfp-qr.png" class="w-16 h-16 flex-shrink-0" />
          <div>
            <div class="cfp-label font-extrabold">Call for Proposal</div>
            <div class="cfp-desc">登壇者募集中！<br>（5/31 23:59まで）</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
.cdk-conf-img { width: 480px; clip-path: inset(0 0 0 3px round 12px); }
.cdk-conf-date { font-size: 3.2rem; color: var(--brand-deep); font-family: 'JetBrains Mono', monospace; line-height: 1.1; }
.cdk-conf-date-sub { font-size: 2rem; font-family: 'Noto Sans JP', sans-serif; }
.cdk-conf-launch { font-size: 2rem; color: var(--brand-deep); }
.cdk-conf-desc { font-size: 1.2rem; color: var(--ink-soft); line-height: 1.8; }
.cfp-box { border-color: var(--accent-warm); background: rgba(231, 76, 60, 0.06); }
.cfp-label { font-size: 1.1rem; color: var(--accent-warm); }
.cfp-desc { font-size: 0.9rem; color: var(--ink-soft); line-height: 1.5; }
</style>
