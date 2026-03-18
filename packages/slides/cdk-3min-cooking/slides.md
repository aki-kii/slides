---
background: '#0283B2'
class: 'cover'
drawings:
  persist: false
transition: slide-left
title: AWS CDK 3分クッキング
mdc: true
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
  custom: 'Yomogi'
---

**クラウド食堂 #7 ~1周年をふりかえってみよう会~**

# AWS CDK 3分クッキング

2026.3.18（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
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

<div style="view-transition-name: cdk-icon">
  <ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK" />
</div>

::footer::

<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />


---
transition: view-transition
---

<div style="view-transition-name: cdk-icon" class="flex items-center gap-4">
  <img src="/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？</h2>
</div>

**プログラミング言語**を利用して**AWSリソース**を構築するサービス

<div class="flex gap-4 items-center justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">プログラミング言語で<br>AWSリソースを定義</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">AWSリソースの状態を見て<br>差分をデプロイ</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">AWSリソース</span>
</div>

</div>

<div class="absolute left-14 bottom-3" style="font-size: 0.7rem; color: #333333; line-height: 1; white-space: nowrap;">
  Special Thanks! Shota Kawasaki (<a href="https://x.com/kawaaaas" target="_blank" rel="noopener noreferrer" style="color: deepskyblue; text-decoration: none;">@kawaaaas</a>)
</div>

---
layout: center
class: text-left
---

## AWS CDKでAPIを実装するデモをやります

---

<div>
  今回作るのは
  <h2>クラウド食堂のイベント一覧を表示するAPI</h2>
</div>

<br>

<img src="/images/app-server-error.png" />

<Underline x="686px" y="418px" width="155px" color="#ef4444" :stroke-width="3" />

<Overlay>
  /api/events へのGETリクエストが失敗している<br>
  (500 Internal Server Error)
</Overlay>

---
clicks: 1
---

## アーキテクチャ

<br>

<img v-if="$clicks < 1" src="/images/architecture.dio.png" />
<img v-if="$clicks >= 1" src="/images/architecture-target.dio.png" />

---
layout: demo
qrUrl: https://d1raisruj23ivg.cloudfront.net/index.html
qrLabel: "デモアプリはこちら"
---

<script setup>
const steps = [
  { 
    label: 'スナップショットテストを実行',
    desc: 'terminal',
    image: '/images/owl-asset/owl-smile.png',
    tips: "スナップショットテストのTIPS",
    code: 'pnpm test'
  },
  {
    label: 'Lxambda関数を実装',
    desc: 'lib/usecases/api.ts',
    image: '/images/owl-asset/owl-smile.png',
    tips: 'NodejsFunctionコンストラクトはTypeScriptのソースコードをビルドなしにLambda関数へデプロイできちゃう優れもの！',
    code: [
      'const listEventFunction = new NodejsFunction(this, "ListEventsFunction", {', 
      '  entry: path.join(__dirname, "../../src/lambda/list-events.ts"),', 
      '  environment: {', 
      '    TABLE_NAME: props.eventsTable.tableName,', 
      '  },', 
      '});'
    ]
  },
  { 
    label: 'Lambda関数に権限を付与',
    desc: 'lib/usecases/api.ts',
    image: '/images/owl-asset/owl-inspiration.png',
    tips: 'Grantsメソッドは、複雑なIAM Policyの権限付与を1行で書けてとても便利です',
    code: 'props.eventsTable.grants.readData(listEventFunction);'
  },
  { 
    label: 'API Gatewayにメソッドを登録',
    desc: 'lib/usecases/api.ts',
    image: '/images/owl-asset/owl-cry.png',
    tips: '本当はCloudFrontディストリビューションにAPI Gatewayのビヘイビアを追加するところから始めたかった…けどデプロイに時間がかかりすぎるので泣く泣く省略しました',
    code: [
      'const events = api.addResource("events");',
      'events.addMethod("GET", new LambdaIntegration(listEventFunction));'
    ]
  },
  {
    label: 'AWSにログイン',
    desc: 'terminal',
    image: '/images/owl-asset/owl-smile.png',
    tips: 'ローカルに長期クレデンシャルを持たなくてよくなって最高ですね！',
    code: 'aws login'
  },
  {
    label: 'デプロイ',
    desc: 'terminal',
    image: '/images/owl-asset/owl-smile.png',
    tips: 'cdk deployのTIPS',
    code: 'pnpm cdk deploy --yes'
  },
]
</script>

::screen::

<ScreenShare />

::notes::

<DemoSteps :steps="steps" />

<Overlay clickStart=7>
  デプロイしたものがこちらです👨‍🍳
</Overlay>

::tips::

<DemoTips :steps="steps" initialTips="デモを始めるよ！" initialImage="/images/owl-asset/owl-speak.png" />


---
layout: full
---

<LazyIframe url="https://dk5jnepkz2uee.cloudfront.net/index.html" />

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
