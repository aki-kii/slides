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
- CDK Contributer (6 & 1 merged)

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

<img src="/public/images/typescript-logo.png" class="h-36"/>
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

<!-- TODO: コードブロックをダークテーマにしたい -->

---

<div>
  ただし...
  <h2>CDKで検証したくない理由もありそうです...</h2>
</div>
<PlainList>
  <v-click><li>❌ アジリティが低下しそう</li></v-click>
  <!-- NOTE: 
    - リポジトリを作成してリソースを作り始めるまでに時間がかかる
    - プロパティを試行錯誤するのにいちいちデプロイの手間がかかる
  -->
  <v-click><li>❌ 技術的な制約がある</li></v-click>
  <!-- NOTE:
    - 最新のリソース・プロパティに対応していない
  -->
  <v-click><li>❌ IaC管理は過剰ではないか</li></v-click>
  <!-- NOTE:
    - 検証で使い捨てるリソースをわざわざIaCにしてなくてもいいのでは？
  -->
  <div style="view-transition-name: cdk-low-experience">
    <v-click><li>❌ 学習コストがかかってしまう</li></v-click>
    <!-- NOTE:
      - 初学者にはコストが高い
      - 慣れててもプロパティの設定を調べる手間がかかる
    -->
  </div>
</PlainList>
<br>
<v-click>
  <h3>→ CDKで検証したくなる<strong>５つのプラクティス</strong>を紹介します！</h3>
</v-click>

---
layout: center
---

## CDKで技術検証するためのプラクティス

<PlainList>
  <li>① 専用のリポジトリを作成するべし</li>
  <li>② ハイブリッドで検証するべし</li>
  <li>③ CDKの便利機能を活用するべし</li>
  <li>④ Custom Construct を育てるべし</li>
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
---

<div>
  <Tag name="アジリティの低下" color="orange" />
  <h2>CDKで検証するとき、初期構築に手間取るため面倒くさくて諦めてしまう</h2>
</div>

---
transition: view-transition
layout: center
class: text-left
---

## 検証用のサンドボックスリポジトリをあらかじめ用意することで、技術検証の初動を早められます！

<Kogoe>リポジトリのテンプレートを作ってもよいです</Kogoe>

<br>

<v-click>
  <span style="view-transition-name: recommended-customize">
    → おすすめのカスタマイズを紹介します
  </span>
  <Kogoe>(TypeScript限定)</Kogoe>
</v-click>

---
transition: view-transition
---

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ
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
---

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ
  <TitledSection title="Oxfmt" description="コードを解析してルールに従って成形するツール" />
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

<div style="view-transition-name: recommended-customize">
  おすすめカスタマイズ
  <TitledSection title="Snapshot Test" description="CDKから生成するテンプレートの差分を検証する" />
</div>

```diff
FAIL test/cdk-sandbox.test.ts > Snapshot test
Error: Snapshot `Snapshot test 1` mismatched
...
"Properties": {
-   "VisibilityTimeout": 30,
+   "VisibilityTimeout": 60,
},
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
---

<div>
  <Tag name="アジリティの低下" color="orange" />
  <h2>リソースの設定を試行錯誤しているとき、<br>CDKでプロパティの設定変更するのは大変...</h2>
</div>

<div>
  <Tag name="技術的な制約" color="blue" />
  <h2>最新の機能にCDKの実装が追いついていない</h2>
</div>

---

## CDKでデプロイしたリソースをマネコンから変更することで、慣れているマネコンから試行錯誤できます！

<img src="/public/images/hybrid.dio.png" class="h-40"/>

<Overlay position="center" clickStart="2">

<PlainList>
  <li>💡 確定したタイミングでCDKを書き直せばセーブポイントになる</li>
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
---

<div>
  <Tag name="アジリティの低下" color="orange" />
  <h2>マネコンからリソースを作る方が簡単に作れるのではないか？</h2>
</div>

---
layout: center
transition: view-transition
---

## CDKはAWSの設定を抽象化して直感的に扱いやすいようにする機能をたくさん持っています

<div style="view-transition-name: convinient-feature">
  <v-click>
    → CDKの便利機能を紹介します！
  </v-click>
</div>

<!-- TODO:
  - 表現を変更する
 -->


---
transition: view-transition
---

<div style="view-transition-name: convinient-feature">
  CDKの便利機能
  <TitledSection title="L2 Construct" description="プロパティを扱いやすいように抽象化したコンポーネント" />
</div>

```ts
new Vpc(this, 'Vpc', { maxAzs: 2 });
```

  <BottomLink href="https://aws.amazon.com/jp/blogs/news/leverage-l2-constructs-to-reduce-the-complexity-of-your-aws-cdk-application/" title="CDK アプリケーションの複雑さを軽減する L2 Construct の活用" />
<!-- TODO: アーキテクチャ図を作成 参考 https://speakerdeck.com/akihisaikeda/aws-cdknotui-sipointo-cloudformationtobi-jiao-sitemita?slide=17 -->

---
transition: view-transition
---

<div style="view-transition-name: convinient-feature">
  CDKの便利機能
  <TitledSection title="Grants" description="リソース間のIAMロールの設定を直感的かつ簡単に設定できる" />
</div>

```ts
// DynamoDBテーブル
const table = new Table(this, "Table", {
  partitionKey: { name: "id", type: AttributeType.STRING },
});
// Lambda関数
const func = new NodejsFunction(this, "Function", {
  entry: path.join(__dirname, "../../src/lambda/index.ts"),
});
// Lambda関数がDynamoDBに対して読み書きできる権限を付与
table.grants.readWriteData(func);
```

  <BottomLink href="https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/define-iam-l2.html" title="AWS CDK を使用して L2 コンストラクトのアクセス許可を定義する" />

---

<div style="view-transition-name: convinient-feature">
  CDKの便利機能
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

## ④ Custom Construct を育てるべし

---
layout: center
transition: view-transition
---

<div>
  <Tag name="IaCの必要性" color="red" />
  <h2>検証で使い捨てるリソースをわざわざ<br>IaCにしてなくてもいいのでは？</h2>
</div>

---

## Custom Construct？

<PlainList>
  <li>AWSリソースをレゴブロックのように組み合わせられるコンポーネント</li>
</PlainList>

→ 繰り返し使う構成や、理解しやすい構成でコンポーネント化して自分だけのConstructを作ろう！

<Overlay>
  💡 技術検証する時に<strong>よく使う構成</strong>を育てることで<br>素早く検証できるようになる
</Overlay>

---

<div>
  最近作ったCustom Construct ①<br>
  <Kogoe>アラームを継続的に発生させたかったので作りました</Kogoe>
  <h2>数分おきにCloudWatchアラームを発生させるConstruct</h2>
</div>

- Lambda関数を3分おきに実行 → Lambda関数の呼び出し回数が1回以上の場合アラーム状態とする

---

<div>
  最近作ったCustom Construct ②<br>
  <Kogoe>構成要素が多くて面倒だったので作りました</Kogoe>
  <h2>SNSトピックからStep Functionsを実行するConstruct</h2>
</div>

- SNSトピック → SQSキュー → EventBridgeパイプス → Step Functions

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
---

<div>
  <Tag name="アジリティの低下" color="orange" />
  <h2>デプロイ失敗時のトライ＆エラーに骨が折れる</h2>
</div>

<div>
  <Tag name="アジリティの低下" color="orange" />
  <h2>プロパティを変更するためにドキュメントを<br>調べるのは大変</h2>
</div>

<div>
  <Tag name="学習コスト" color="green" />
  <h2>初心者が理解するために手間がかかってしまう</h2>
</div>

---

## ⑤ コーディングエージェントに頼るべし

コーディングエージェントはCDKのソースコードをコンテキストとして扱えるため相性がいい！

<!-- TODO: コメントを含めたいい感じの意図が伝わるソースコード -->

---

## AWS Infrastructure as Code MCP Server

- CDK ドキュメントの検索
- 複雑な処理をとりあえず書いてもらえる（Step Functionsのワークフローとか）
- CDK のベストプラクティスに沿った
- ベストプラクティス

<!-- NOTE:
CDKはソースコードで全てを語るのでエージェントとの相性がいい

- 変数やコメントで意図をコンテキストに含めやすい
- ドキュメントを見てもわからないプロパティの設定方法を聞ける
- 複雑な処理をとりあえず書いてもらえる（Step Functionsのワークフローとか）
- サンプルコードをインプットとして渡すのもよい
- MCPサーバーもある
-->

<BottomLink href="https://awslabs.github.io/mcp/servers/aws-iac-mcp-server" title="AWS IaC MCP Server"/>


---

## CDKで検証しない理由は解消できそう？

<PlainList>
  <li>❌ 検証のスピードが下がってしまいそう</li>
  <li>❌ 新しく追加されたサービス・機能は使えないじゃん</li>
  <li>❌ 検証するためだけなのにIaC管理する必要ないよね？</li>
  <li>❌ CDK書くのに慣れてない.....</li>
</PlainList>

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

<div class="absolute right-8 bottom-8 flex flex-col items-center" style="color: #e0e0e0; gap: 0;">
  <v-click>＼ ご静聴ありがとうございました！ ／</v-click>
  <img src="/public/images/aboutme/eye-catch.png" class="h-32" />
</div>