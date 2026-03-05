---
background: '#0283B2'
class: 'cover'
drawings:
  persist: false
transition: slide-left
title: 最初からAWS CDKで技術検証してもいいんじゃない？
mdc: true
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

# 最初からAWS CDKで技術検証しても<br>いいんじゃない？

**JAWS-UG 茨城 #12 春の推しAWSサービスLTまつり！**

<br>

2026.3.11（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/public/images/aboutme/eye-catch.png" class="h-36" />
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
<ProfileItem title="推しサービス" icon="/images/aboutme/awscdk.dio.png" name="AWS CDK">

- CDK Conference 2025 Speaker
- CDK Contributer

</ProfileItem>

</div>

::footer::

<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="4" class="h-full" />

---

<div style="view-transition-name: cdk-icon" class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？</h2>
</div>

プログラミング言語でAWSリソースを構築するIaCサービス

<img src="/public/images/icons8-aws-240.png" class="h-36"/>

---
layout: center
transition: view-transition
---

<div style="view-transition-name: tech-experiment">
  みなさんは
  <h2>AWSで技術検証してますか？</h2>
</div>

<!--
CDK推しの自分ですがこれまでは技術検証をマネコンから行ってました。先日思い立ってCDKで検証を始めたところ、CDKで技術検証を初めてもいいんじゃない！？と思えたので、そのメリットやプラクティスを紹介させていただきます。
-->

---
transition: view-transition
---

<div style="view-transition-name: tech-experiment">
  ここでいう
  <h2>AWSでの技術検証とは？</h2>
</div>

特定の目的のためにAWSサービスを**実際に触って**検証すること

<v-click>

- プロダクトの技術課題が解消可能か
- 新しいサービスが公開された
- 興味のあるサービスを理解するため

などなど...

</v-click>

<Overlay position="center" clickStart="2">

そこで提案したいことがあります

</Overlay>
  

---
layout: center
class: text-left
---

<div style="view-transition-name: tech-experiment">
  <h2>最初からAWS CDKで技術検証しても<br>いいんじゃない？</h2>
</div>

---

## 大体の方はマネコンから検証してますよね

<img src="/images/management-console.png" class="h-72">

<Overlay position="center" clickStart="1">

⭕️ 初学者から上級者まで親しみやすい<br>
⭕️ 試行錯誤しやすい<br>
⭕️ リリース当日から試せる

</Overlay>

---

## CDKから検証するといいこともあります

```ts {all}{ maxHeight:'360px' }
import path from "node:path";

import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { LambdaRestApi } from "aws-cdk-lib/aws-apigateway";
import { AttributeType, Table } from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";

export class MyConstruct extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // DynamoDB Table
    const table = new Table(this, "Table", {
      partitionKey: { name: "id", type: AttributeType.STRING },
    });
    // Lambda Function
    const func = new NodejsFunction(this, "Function", {
      entry: path.join(__dirname, "../../src/lambda/index.ts"),
    });
    table.grants.readWriteData(func);

    // API Gateway
    new LambdaRestApi(this, "Api", { handler: func });
  }
}
```

<Overlay position="center" clickStart="1">

⭕️ 設定内容がコードとして残るので再現性が高い<br>
⭕️ 本番のワークロードに昇華しやすい<br>
⭕️ リソースの消し忘れが少なくなる

</Overlay>


---
transition: view-transition
---

<div>
  ただし...
  <h2>CDKで検証したくない理由もありそうです...</h2>
</div>

<PlainList>
  <li>❌ 検証のスピードが下がってしまいそう</li>
  <li>❌ 新しく追加されたサービス・機能は使えないじゃん</li>
  <li>❌ 検証するためだけなのにIaC管理する必要ないよね？</li>
  <div style="view-transition-name: cdk-low-experience">
    <li>❌ CDK書くのに慣れてない.....</li>
  </div>
</PlainList>
<br>
<v-click>
  <h3>→ これらのポイントを解消するお話をさせていただきます！</h3>
</v-click>
<v-click>
...が、1つ謝らせてください
</v-click>

---

<div style="view-transition-name: cdk-low-experience">
  <h2>❌ CDK書くのに慣れてない...</h2>
</div>

<v-click>
  <h3>A: CDKの実装経験を積みましょう...！</h3>
</v-click>

<v-click>
身も蓋も無い話ですみません。。。<br><br>
基礎さえ抑えていれば、CDKで技術検証していくうちに着実に力がつきます！！<br>
<Kogoe>（むしろチャンス！）</Kogoe><br>
開発するフェーズで学び始めるよりはスムーズなのでは？と思ったりもしてます
</v-click>

<Overlay position="center" clickStart="3">

それでは

</Overlay>

---
layout: center
class: text-center
---

## CDKで技術検証したくなる<br>**５つのプラクティス**を伝授します！

---

## 1. ハイブリッドで検証するべし

<!-- NOTE:
- 全てをCDKで定義しなくていいんです！
- 設定を試行錯誤するのはマネコンからのほうが早い
- 設定が確定した部分をCDKで定義 → **セーブポイント**になる
- `cdk drift` で変更したプロパティを検出できる
  - CFn対象外のプロパティは検出できないので過信しないこと
- テンプレートの状態にリセットする方法もある
-->

---

## 2. 専用のリポジトリを作成するべし

<!-- NOTE:
- CDKで一番面倒なのはリポジトリの初期構築！？
- `cdk init`で手軽に作れるが、必要なツールを入れていると面倒
- **あらかじめサンドボックス用リポジトリを用意**しておく

最低限入れとくといいもの:

- リンター、フォーマッター
- スナップショットテスト
- `eslint-plugin-awscdk`
-->

---

## 3. L2 Construct を活用するべし

<!-- NOTE:
リソースを抽象化して扱える L2 Construct で素早く検証できる

```ts
// 数行でVPC、サブネット、ルートテーブルなど一括作成
const vpc = new Vpc(this, 'Vpc', { maxAzs: 2 });
```

Grants で簡単に権限付与

```ts
table.grantReadWriteData(func);
```

fromLookup で既存リソースも参照可能

```ts
const existingVpc = Vpc.fromLookup(this, 'ExistingVpc', {
  vpcId: 'vpc-1234567890abcdef0',
});
```
-->

---

## 4. Custom Construct を育てるべし

<!-- NOTE:
Constructはレゴブロックのように組み合わせられ、自分でも作れる

- 繰り返し利用するコンポーネントをカスタムConstructとして定義
- 例: 最近作ったカスタムConstruct
  - 数分おきにCloudWatchアラームを発生させるConstruct
  - SNSトピック → SQSキュー → EventBridgeパイプス → Step Functions
- Constructを作るのにスニペットはおすすめ
- **Construct Hub** には人が作ったカスタムConstructがたくさん
-->

---

## 5. Coding Agent に頼るべし

<!-- NOTE:
CDKはソースコードで全てを語るのでエージェントとの相性がいい

- 変数やコメントで意図をコンテキストに含めやすい
- ドキュメントを見てもわからないプロパティの設定方法を聞ける
- 複雑な処理をとりあえず書いてもらえる（Step Functionsのワークフローとか）
- サンプルコードをインプットとして渡すのもよい
- MCPサーバーもある
-->

---

## CDKで検証しない理由は解消できそう？

- ❌ 検証のスピードが下がってしまいそう<br>
- ❌ 新しく追加されたサービス・機能は使えないじゃん<br>
- ❌ 検証するためだけなのにIaC管理する必要ないよね？<br>
- ❌ CDK書くのに慣れてない.....

---
layout: center
class: cover
style: 'background-color: #0283B2;'
---

# 最初からAWS CDKで技術検証<br>してもいいんじゃない？

<br><br>

<div class="absolute right-8 bottom-8 flex flex-col items-center" style="color: #e0e0e0; gap: 0;">
  ＼ ご静聴ありがとうございました！ ／
  <img src="/public/images/aboutme/eye-catch.png" class="h-32" />
</div>