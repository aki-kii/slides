---
background: '#0283B2'
class: 'cover'
drawings:
  persist: false
transition: slide-left
title: スライドタイトル
mdc: true
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

**イベント名**

# スライドタイトル

2026.X.X（X）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

---
layout: profile
image: /images/aboutme/me.jpeg
name: アキキー | 池田 晃尚
---

<ProfileItem icon="/images/aboutme/mates-logo.png" name="株式会社メイツ（2025.9〜）">

- バックエンドエンジニア / SRE

</ProfileItem>

<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK">

- CDK Conference 2025 Speaker
- CDK Contributor (7PRs merged)

</ProfileItem>

::footer::

<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---
layout: demo
clicks: 3
---

<script setup>
const steps = [
  { label: 'AWS コンソールにログイン',    tips: 'シークレットウィンドウで開くと複数アカウントを同時に使えます' },
  { label: 'Cloud9 環境を起動',           tips: 'インスタンスタイプは t3.small 以上を推奨。起動まで1〜2分かかります' },
  { label: 'CDK プロジェクトを初期化',    tips: 'cdk init app --language typescript を実行。node_modules のインストールが自動で走ります' },
  { label: 'cdk deploy を実行',           tips: 'デプロイ前に cdk diff で差分を確認しておくと安心です' },
]
</script>

::screen::

<ScreenShare />

::notes::

<DemoSteps :steps="steps" />

::tips::

<DemoTips :steps="steps" />

---
layout: center
class: cover
style: 'background-color: #0283B2;'
---

<div>
  <h2>ご清聴ありがとうございました！</h2>
</div>

<div class="absolute right-8 bottom-8 flex flex-col items-center print:hidden" style="color: #e0e0e0; gap: 0;">
  <img src="/images/aboutme/eye-catch.png" class="h-32" />
</div>
