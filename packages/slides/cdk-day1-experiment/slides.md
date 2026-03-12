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
え
**JAWS-UG 茨城 #12 春の推しAWSサービスLTまつり！**

# 最初からAWS CDKで技術検証しても<br>いいんじゃない？


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
- CDK Contributor (7PRs merged)

</ProfileItem>
</div>

::footer::

<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---

<div style="view-transition-name: cdk-icon" class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
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
transition: view-transition
---

<div style="view-transition-name: tech-experiment">
  みなさんは
  <h2>AWSで技術検証してますか？</h2>
</div>

---
transition: view-transition
---

<div style="view-transition-name: tech-experiment">
  ここでいう
  <h2>AWSでの技術検証とは？</h2>
</div>

<div>
  <div>特定の目的のためにAWSサービスを<strong>実際に触って</strong>検証すること</div>
  <Kogoe>とします</Kogoe>
</div>

<br>

<v-click>

- プロダクトの技術課題が解消可能か
- 新しいサービスが公開された
- 興味のあるサービスを理解するため

<Kogoe>などなど...</Kogoe>

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

<PlainList>
  <li>⭕️ 初学者から上級者まで親しみやすい</li>
  <li>⭕️ 試行錯誤しやすい</li>
  <li>⭕️ リリース当日から試せる</li>
</PlainList>

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

<PlainList>
  <li>⭕️ 設定内容がコードとして残るので再現性が高い</li>
  <li>⭕️ 本番のワークロードに昇華しやすい</li>
  <li>⭕️ リソースの消し忘れが少なくなる</li>
  <li>⭕️ 簡単に作り直せるので使わない間はリソースを削除できる</li>
</PlainList>

</Overlay>

---

<div>
  ただし...
  <h2>CDKで検証したくない理由もありそうです...</h2>
</div>

<br>

<PlainList>
  <li>❌ 検証スピードが落ちそう</li>
  <li>❌ 最新機能に追いついていない</li>
  <li>❌ IaC管理は過剰ではないか</li>
  <li>❌ 学習コストがかかってしまう</li>
</PlainList>

<br>

<Overlay>
  CDKで検証したくなる<strong>５つのプラクティス</strong>を紹介します！
</Overlay>

---
layout: center
---

## CDKで技術検証するためのプラクティス

<PlainList>
  <li>① 専用のリポジトリを作成するべし</li>
  <li>② ハイブリッドで検証するべし</li>
  <li>③ CDKの便利機能を活用するべし</li>
  <li>④ 検証用 Custom Construct を育てるべし</li>
  <li>⑤ コーディングエージェントに頼るべし</li>
</PlainList>

---
layout: center
class: text-center
transition: view-transition
---

## ① 専用のリポジトリを作成するべし

---
layout: center
transition: view-transition
chapter: ① 専用のリポジトリを作成するべし
---

<ChapterLabel />

<div>
  <Tag name="検証スピードの低下" color="orange" />
  <h2>CDKで検証するとき、初期構築に手間取るため面倒くさくて諦めてしまう</h2>
</div>
<Kogoe>というお悩みを解決します</Kogoe>

---
transition: view-transition
layout: center
class: text-left
chapter: ① 専用のリポジトリを作成するべし
---

<ChapterLabel />

## 検証用のリポジトリを事前に用意することで<br>技術検証の初動を早められます！

<Kogoe>リポジトリのテンプレートを作ってもよいです</Kogoe>

<br>

<Overlay>
  <div>おすすめのカスタマイズを<strong>3つ</strong>紹介します</div>
  <Kogoe>(TypeScript限定)</Kogoe>
</Overlay>

---
transition: view-transition
chapter: ① 専用のリポジトリを作成するべし
---

<ChapterLabel />

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ ① Linter
  <TitledSection title="ESLint" description="コードを解析してルールに従って検査するツール" />
</div>

専用プラグイン `eslint-plugin-awscdk` により、CDKのセオリー・<br>ベストプラクティスを強制できる

```ts
// Construct ID must be PascalCase. (awscdk/pascal-case-construct-id)
new Bucket(this, 'my-bucket');
```

<Overlay>
  <PlainList>
    <li>💡 構文エラーを事前に解析できる</li>
    <li>💡 CDKの落とし穴につまづきにくくなる</li>
  </PlainList>
</Overlay>

<BottomLinks>
  <BottomLink href="https://eslint.org/" title="Find and fix problmes in your JavaScript code" />
  <BottomLink href="https://eslint-plugin-awscdk.dev/ja/" title="eslint-plugin-awscdk - ESLint plugin for AWS CDK" />
</BottomLinks>

---
transition: view-transition
chapter: ① 専用のリポジトリを作成するべし
---

<ChapterLabel />

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ ② Formatter
  <TitledSection title="Oxfmt" description="コードを解析してルールに従って整形するツール" />
</div>

````md magic-move
```ts
import {NodejsFunction, Code} from "aws-cdk-lib/aws-lambda"
import {Construct} from "constructs"
export class MyConstruct extends Construct{constructor(scope:Construct,id:string){super(scope,id)
new NodejsFunction(this,"Function",{entry: path.join(__dirname, "src/handler.ts"),})}}
```
```ts
import { NodejsFunction } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export class MyConstruct extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);
    new NodejsFunction(this, "Function", {
      entry: path.join(__dirname, "src/handler.ts"),
    });
  }
}
```
````

<Overlay>
  <PlainList>
    <li>💡 コードのスタイルが統一されるので読みやすくなる</li>
  </PlainList>
</Overlay>

<BottomLink href="https://oxc.rs/docs/guide/usage/formatter.html" title="Oxfmt" />

---
chapter: ① 専用のリポジトリを作成するべし
---

<ChapterLabel />

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ ③ Test
  <TitledSection title="Snapshot Test" description="CDKから生成するテンプレートの差分を検証する" />
</div>

```diff
"Queue4A7E3555": {
  "Type": "AWS::SQS::Queue",
  "Properties": {
-   "VisibilityTimeout": 30,
+   "VisibilityTimeout": 60,
  },
  "DeletionPolicy": "Delete",
  "UpdateReplacePolicy": "Delete",
}
```

<Overlay>
  <PlainList>
    <li>💡 意図しないプロパティを設定することを防げる</li>
    <li>💡 こまめにアップデートしておけば差分が見やすい</li>
  </PlainList>
</Overlay>

<BottomLink href="https://zenn.dev/aki_kii/articles/cdk-snapshottest-practice" title="AWS CDK スナップショットテストのプラクティス集" />

---
layout: center
class: text-center
transition: fade
---

## ② ハイブリッドで検証するべし

---
layout: center
transition: fade
chapter: ② ハイブリッドで検証するべし
---

<ChapterLabel />

<div>
  <Tag name="検証スピードの低下" color="orange" />
  <h2>リソースの設定を試行錯誤しているとき、<br>CDKでプロパティの設定を変更するのは大変...</h2>
</div>

<div>
  <Tag name="最新機能に未対応" color="blue" />
  <h2>最新の機能にCDKの実装が追いついていない</h2>
</div>

<Kogoe>というお悩みを解決します</Kogoe>

---
chapter: ② ハイブリッドで検証するべし
---

<ChapterLabel />

## CDKでデプロイしたリソースを<br>慣れているマネコンから試行錯誤しましょう！

<br>

<img src="/public/images/hybrid.dio.png" class="h-50"/>

<Overlay position="center" clickStart="1">

<PlainList>
  <li>💡 確定したタイミングでCDKのコードに落とし込めばセーブポイントになる</li>
  <li>💡 新しく提供されたサービスもすぐに検証できる</li>
</PlainList>

</Overlay>

---
layout: center
class: text-center
transition: fade
---

## ③ CDKの便利機能を活用するべし

---
layout: center
transition: view-transition
chapter: ③ CDKの便利機能を活用するべし
---

<ChapterLabel />

<div>
  <Tag name="検証スピードの低下" color="orange" />
  <h2>マネコンからリソースを作る方が簡単に作れるのではないか？</h2>
</div>
<Kogoe>というお悩みを解決します</Kogoe>

---
layout: center
transition: view-transition
chapter: ③ CDKの便利機能を活用するべし
---

<ChapterLabel />

<div>
  AWS CDKは
  <h2>AWSリソースの複雑な設定を抽象化して<br>直感的に扱えるようにしてくれます！</h2>
</div>

<Overlay>
  そんなCDKの便利機能を<strong>3つ</strong>紹介します！
</Overlay>

---
transition: view-transition
chapter: ③ CDKの便利機能を活用するべし
---

<ChapterLabel />

<div style="view-transition-name: convinient-feature">
  CDKの便利機能 ①
  <TitledSection title="L2 Construct" description="プロパティを扱いやすいように抽象化したコンポーネント" />
</div>

<div class="flex gap-6 items-center">

<div>

```ts
new Vpc(this, "Vpc", {
  ipAddresses: IpAddresses.cidr("10.0.0.0/16"),
  subnetConfiguration: [
    {
      cidrMask: 24,
      name: "public",
      subnetType: SubnetType.PUBLIC,
    },
  ],
});
```

</div>

<div class="flex flex-col items-center text-sm text-gray-400 gap-1 shrink-0">
  <span class="text-2xl">→</span>
</div>

<img src="/public/images/l2-vpc.dio.png" class="h-60 shrink-0" />

</div>

  <BottomLink href="https://aws.amazon.com/jp/blogs/news/leverage-l2-constructs-to-reduce-the-complexity-of-your-aws-cdk-application/" title="CDK アプリケーションの複雑さを軽減する L2 Construct の活用" />

---
transition: view-transition
chapter: ③ CDKの便利機能を活用するべし
---

<ChapterLabel />

<div style="view-transition-name: convinient-feature">
  CDKの便利機能 ②
  <TitledSection title="Grants" description="リソース間のIAMロールの設定を直感的かつ簡単に設定できる" />
</div>

```ts
// Lambda関数
const func = new NodejsFunction(this, "Function", {
  entry: path.join(__dirname, "../../src/lambda/index.ts"),
});
// DynamoDBテーブル
const table = new Table(this, "Table", {
  partitionKey: { name: "id", type: AttributeType.STRING },
});
// Lambda関数がDynamoDBに対して読み書きできる権限を付与
table.grants.readWriteData(func);
```

  <BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/define-iam-l2.html" title="AWS CDK を使用して L2 コンストラクトのアクセス許可を定義する" />

---
chapter: ③ CDKの便利機能を活用するべし
---

<ChapterLabel />

<div style="view-transition-name: convinient-feature">
  CDKの便利機能 ③
  <TitledSection title="fromLookup" description="デプロイ済みのリソースをCDKで参照できる" />
</div>

```ts
const vpc = Vpc.fromLookup(this, "ExistingVpc", {
  // デプロイ済みのVPC
  vpcId: "vpc-1234567890abcdef0",
});

new Cluster(this, "Cluster", {
  // ECSクラスターを参照したVPCに配置
  vpc,
});
```

  <BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/resources.html" title="リソースと AWS CDK" />

---
layout: center
class: text-center
transition: fade
---

## ④ 検証用 Custom Construct を育てるべし

---
layout: center
transition: view-transition
chapter: ④ 検証用 Custom Construct を育てるべし
---

<ChapterLabel />

<div>
  <Tag name="IaCの必要性" color="red" />
  <h2>検証で使い捨てるリソースをわざわざ<br>IaCにしてなくてもいいのでは？</h2>
</div>

<Kogoe>というお悩みを解決します</Kogoe>

---
chapter: ④ 検証用 Custom Construct を育てるべし
transition: fade
---

<ChapterLabel />

## Custom Construct？

<PlainList>
  <li>AWSリソースをレゴブロックのように組み合わせられるコンポーネント</li>
</PlainList>

<img src="/public/images/custom-construct.dio.png" class="h-50 shrink-0" />

→ 繰り返し使う構成や、理解しやすい構成でコンポーネント化して<br>自分だけのConstructを作れます！

<Overlay>
  最近作った検証用Custom Constructを紹介します！
</Overlay>

---
chapter: ④ 検証用 Custom Construct を育てるべし
transition: fade
---

<ChapterLabel />

<div>
  最近作ったCustom Construct ①<br>
  <h2>数分おきにCloudWatchアラームを発生させるConstruct</h2>
  <Kogoe>アラームを継続的に発生させたかったので作りました</Kogoe>
</div>

<br>

<img src="/public/images/frequency-alarm-construct.dio.png" class="shrink-0" />

---
chapter: ④ 検証用 Custom Construct を育てるべし
transition: fade
---

<ChapterLabel />

<div>
  最近作ったCustom Construct ②<br>
  <h2>SNSトピックからStep Functionsを実行するConstruct</h2>
  <Kogoe>構成要素が多くて面倒だったので作りました</Kogoe>
</div>

<br>

<img src="/public/images/invoke-statemachine-construct.dio.png" class="shrink-0" />

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
layout: center
class: text-center
transition: fade
---

## ⑤ コーディングエージェントに頼るべし

---
layout: center
transition: view-transition
chapter: ⑤ コーディングエージェントに頼るべし
---

<ChapterLabel />

<div>
  <Tag name="検証スピードの低下" color="orange" />
  <h2>デプロイ失敗時のトライ＆エラーに骨が折れる</h2>
</div>

<div>
  <Tag name="検証スピードの低下" color="orange" />
  <h2>プロパティを変更するためにドキュメントを<br>調べるのは大変</h2>
</div>

<div>
  <Tag name="学習コスト" color="green" />
  <h2>初心者が理解するために手間がかかってしまう</h2>
</div>

<Kogoe>というお悩みを解決します</Kogoe>

---
chapter: ⑤ コーディングエージェントに頼るべし
transition: fade
---

<ChapterLabel />

<div>
  コーディングエージェントは
  <h2>ソースコードをコンテキストとして扱えるためCDKと相性がいい！</h2>
</div>

<br>

- CDK本体のコードからプロパティの実装方法がわかる
- 自分のCDKコードから作成したリソースの設定がわかる
- 変数名・コメントから設定の意図がわかる

<Overlay>
  CDKをもっと扱いやすくしてくれるMCPサーバーを紹介します！
</Overlay>

---
chapter: ⑤ コーディングエージェントに頼るべし
---

<ChapterLabel />

## AWS Infrastructure as Code MCP Server

<div>
  <div>AWS の IaC に関連する機能をたくさん提供している</div>
  <Kogoe><a href="https://awslabs.github.io/mcp/servers/cdk-mcp-server">AWS CDK MCP Server</a>は非推奨になり、こちらが推奨されています</Kogoe>
</div>

<br>

- デプロイ失敗のトラブルシューティング
- CloudFormationテンプレートの検証
- CDK ドキュメントの検索（CDK/CloudFormation/サンプルコード）
- ベストプラクティスに沿った実装
- コンプライアンスチェック（cfn-guard）
<Kogoe>...などなど</Kogoe>

<BottomLink href="https://awslabs.github.io/mcp/servers/aws-iac-mcp-server" title="AWS IaC MCP Server"/>

---
layout: center
class: cover
style: 'background-color: #0283B2;'
---

<div>
  みなさんも
  <h2>最初からAWS CDKで技術検証<br>してもいいんじゃない？</h2>
  と思えましたか？
</div>

<br><br>

<div class="absolute right-8 bottom-8 flex flex-col items-center print:hidden" style="color: #e0e0e0; gap: 0;">
  ＼ ご静聴ありがとうございました！ ／
  <img src="/public/images/aboutme/eye-catch.png" class="h-32" />
</div>