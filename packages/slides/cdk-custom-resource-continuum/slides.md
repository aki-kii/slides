---
layout: title
drawings:
  persist: false
transition: slide-left
title: CDK のカスタムリソースで Continuum（旧 Security Agent）を定義した話
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

**JAWS-UG 茨城 #17 秋の推しAWSサービスLTまつり！**

<div class="text-xl font-bold opacity-90 mt-6">CloudFormation 未対応でも諦めない！</div>

# <span style="font-size: 0.72em; line-height: 1.4; display: inline-block">CDK のカスタムリソースで<br>Continuum（旧 Security Agent）を定義した話</span>

2026.9.30（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/public/images/aboutme/eye-catch.png" class="h-36" />
</div>

<!--
1. よろしくお願いします
2. CDK のカスタムリソースで Continuum（旧 Security Agent）を定義した話をします
-->

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

<img src="/images/aboutme/jawsug-cdk-logo.png" />
<img src="/images/aboutme/aws-community-builders-logo.png" />
<AwsCertBadges dir="/images/aboutme/awscerts/enabled" :per-row="8" :gap="0" class="h-full" />

---
transition: view-transition
---

<div style="view-transition-name: cdk-icon" class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？</h2>
</div>

**プログラミング言語**で**AWS リソース**を定義する IaC フレームワーク

<div class="flex gap-4 items-center justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">プログラミング言語で<br>AWSリソースを定義</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-28"/>
  <span class="text-gray-400 w-44 text-center text-sm">前回との差分を<br>デプロイ</span>
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

<!--
1. 推しサービスは AWS CDK です
2. プログラミング言語で AWS リソースを定義して、CloudFormation を通してデプロイするサービスです
3. 裏側では CloudFormation が動いているので、CloudFormation が対応していないリソースは基本的に書けません
-->

---
layout: center
---

<div>
  プロジェクトで
  <h2><strong>Continuum コードスキャニング</strong>を<br>導入したときの話をします</h2>
</div>

<!--
1. 今日は、プロジェクトで Continuum コードスキャニングを導入したときの話をします
-->

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuum コードスキャニングとは？</h2>
</div>

<div class="mt-3" style="font-size: 1.2rem; line-height: 1.7">
  <div>Continuum（Security Agent が改名）の機能の1つ</div>
  <div><strong>AI エージェント</strong>がソースコードをスキャンして脆弱性を検出する機能</div>
  <div class="mt-3">フルリポジトリスキャン</div>
</div>

<InlineSvg src="code-scanning.svg" label="Continuum コードスキャニングがリポジトリ全体を読み、見つかった脆弱性と修正案をスキャン結果として出す図" class="mx-auto mt-1" style="width: 620px" />


<BottomLinks>
  <BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/05/aws-security-agent-full-repository-code-review/" title="AWS Security Agent now supports full repository code reviews" />
  <BottomLink href="https://aws.amazon.com/about-aws/whats-new/2026/06/aws-continuum/" title="Introducing AWS Continuum for security at machine speed" />
</BottomLinks>

<!--
1. Continuum コードスキャニングは、AI エージェントがソースコードをスキャンして、脆弱性を検出する機能です
2. 今回使ったのはフルリポジトリスキャンで、GitHub や GitLab などのリポジトリ全体を読んで解析します
3. スキャン結果には、見つかった脆弱性の重要度と場所が出て、ファイルと行を指定した修正案も出してくれます
4. ちなみに Continuum は、AWS Security Agent の新しい名前です
-->

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Continuum コードスキャニングとは？</h2>
</div>

<div class="text-lg mt-2">リソース構成</div>

<InlineSvg src="continuum-code-review.svg" label="Integration が GitLab のアクセストークンで GitLab と接続し、Agent Space の中の CodeReview が GitLab のリポジトリをスキャンする構成図。Agent Space は CloudFormation 対応、Integration と CodeReview は CloudFormation 未対応" class="mx-auto mt-6" style="width: 800px" />

<!--
1. Continuum コードスキャニングを使うときは、こんな構成になります
2. Integration は、GitLab のアクセストークンを使って GitLab と接続します
3. Agent Space は、Continuum が管理するアプリの単位です。この中に CodeReview を作ると、CodeReview が対象のリポジトリをスキャンします
4. このうち CloudFormation に対応しているのは Agent Space だけで、Integration と CodeReview は、2026年9月27日時点では CloudFormation で作れません
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AWS CDK とは？（再）</h2>
</div>

CDK は CloudFormation テンプレートを生成してデプロイする

<div class="flex gap-4 items-center justify-center mt-6">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/typescript-logo.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">CDK のコード</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">CloudFormation<br>テンプレート</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-24"/>
  <span class="text-gray-400 w-44 text-center text-sm">AWS リソース</span>
</div>

</div>

<div class="text-center text-xl mt-10">
  CloudFormation が対応していないリソースは<br><strong>CDK でも標準の方法では定義できない</strong>
</div>

<!--
1. CDK は、コードから CloudFormation テンプレートを生成して、リソースをデプロイします
2. そのため、CloudFormation が対応していないリソースは、CDK でも標準の方法では定義できません
3. Integration と CodeReview も、このままだと CDK で書けません
-->

---
layout: center
transition: view-transition
---

<div style="view-transition-name: cfn-unsupported">
  Continuum コードスキャニングを CDK で管理するため
  <h2><strong>カスタムリソース</strong>で定義しました！</h2>
</div>

<!--
1. そこで、Continuum コードスキャニングを CDK で管理するため、カスタムリソースで定義しました
2. 今日はそのお話しをします
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg">CloudFormation のライフサイクルに合わせて<strong>カスタムの処理を実行する</strong>仕組み</div>

<InlineSvg src="custom-resource-lifecycle.svg" label="Stack や Construct の作成・プロパティ変更・削除に応じて、カスタムリソースの中で CloudFormation のリソースから Lambda 関数へ Create・Update・Delete のイベントが届き、Lambda 関数が API を呼んで実行結果を S3 オブジェクトに書き込み、CloudFormation がその応答を待ち受ける図" class="mx-auto mt-2" style="width: 700px" />

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/template-custom-resources.html" title="カスタムリソースを使用してカスタムプロビジョニングロジックを作成する" />

<!--
1. カスタムリソースは、CloudFormation のライフサイクルに合わせて、カスタムの処理を実行する仕組みです
2. カスタムリソースは、CloudFormation のリソースと、処理を担当する Lambda 関数でできています
3. Stack や Construct を作成すると Create、Construct のプロパティを変更すると Update、Stack や Construct を削除すると Delete のイベントが、Lambda 関数に届きます
4. Lambda 関数は、AWS や外部の API を呼んで処理します
5. Lambda 関数は実行結果を S3 オブジェクトに書き込みます。CloudFormation はその応答を待ち受けていて、届いたら次へ進みます
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg mt-4">e.g. DynamoDB にマスターデータを投入するカスタムリソース</div>

<InlineSvg src="custom-resource-dynamodb.svg" label="カスタムリソースの Lambda 関数が、Create で DynamoDB テーブルにマスターデータを投入し、Update で変更されたレコードを更新し、Delete で投入したデータを削除する図" class="mx-auto mt-4" style="width: 780px" />

<!--
1. 例として、DynamoDB でマスターデータを管理するために、カスタムリソースでデータを投入するケースを考えてみます
2. Create のイベントでは、Lambda 関数が DynamoDB にマスターデータを投入します
3. Update のイベントでは、変更されたプロパティをもとに、Lambda 関数がレコードを更新します
4. Delete のイベントでは、Lambda 関数が投入したデータを削除します
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/cfn-icon.dio.png" class="h-12" />
  <h2 class="!m-0">カスタムリソースとは？</h2>
</div>

<div class="text-lg mt-4">e.g. S3 バケットを空にするカスタムリソース（autoDeleteObjects）</div>

<InlineSvg src="custom-resource-s3.svg" label="カスタムリソースの Lambda 関数が、Create と Update では何もせず、Delete で S3 バケットのオブジェクトを全て削除する図" class="mx-auto mt-4" style="width: 780px" />

<!--
1. もう1つ例を出すと、CDK の S3 バケットの autoDeleteObjects もカスタムリソースです
2. CloudFormation は、中にオブジェクトが残っているバケットを削除できません
3. そこで、Create と Update のイベントでは何もせず、Delete のイベントで Lambda 関数がバケットのオブジェクトを全て削除します
4. 実際には、新しいオブジェクトが置かれないようにバケットポリシーで拒否してから、全バージョンのオブジェクトを消しています
5. 補足: バケット名が変わるときは、Update で PhysicalResourceId が新しいバケット名に変わるので、CloudFormation が古いほうに Delete を送り、そこで古いバケットの中身が消えます（aws-cdk-lib 2.268.0 のハンドラで確認）
-->

---

## 何故そこまでして CDK で定義したかったの？

<br>

- CloudFormation のライフサイクルで管理できる
- 定義したリソースを複製しやすい
  - e.g. リポジトリごとに CodeReview を作れる
- 設定を設計意図と一緒にソースコードに残せる
  - マネコンで作ると設計意図は別途ドキュメントが必要

<div class="mt-8 opacity-70">
  <div style="font-size: 1rem">ほかにも</div>
  <ul class="!mt-1">
    <li style="font-size: 1.05rem">他のリソースと合わせて CDK で統一できる</li>
    <li style="font-size: 1.05rem">CloudFormation が対応したら L1 Construct に取り込みやすい</li>
  </ul>
</div>

<!--
1. 何故そこまでして CDK で定義したかったのか、という話です
2. まず、CloudFormation のライフサイクルで管理できます
3. 次に、定義したリソースを複製しやすいです。たとえば、リポジトリごとに CodeReview を作れます
4. そして、なんでこの設定にしたんだっけ、という設計意図と一緒に、設定をソースコードに残せます。マネコンから作成すると、設計意図は別途ドキュメントがないと残せません
5. ほかにも、他のリソースと合わせて CDK で統一できるし、CloudFormation が対応したら L1 Construct に取り込みやすい、というのもあります
-->

---
layout: center
---

<div>
  <h2>Continuum コードスキャニングを<br>カスタムリソースを使って CDK で定義します</h2>
</div>

<!--
1. ここからは、Continuum コードスキャニングを、カスタムリソースを使って CDK で定義していきます
-->

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0"><span style="font-size: 0.85em">Continuum コードスキャニングのリソース構成</span></h2>
</div>

<InlineSvg src="continuum-code-review.svg" label="Integration が GitLab のアクセストークンで GitLab と接続し、Agent Space の中の CodeReview が GitLab のリポジトリをスキャンする構成図。Agent Space は CloudFormation 対応、Integration と CodeReview は CloudFormation 未対応" class="mx-auto mt-6" style="width: 800px" />

<!--
1. もう一度、Continuum コードスキャニングのリソース構成です
2. このうち CloudFormation に対応していない Integration と CodeReview を、カスタムリソースで定義していきます
-->

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">CodeReview のポイント</h2>
</div>

<br>

- 連携したリポジトリをコードスキャンするためのリソース
- CloudFormation のイベントに対応した API が揃っている
  - Create: `CreateCodeReview`
  - Update: `UpdateCodeReview`
  - Delete: `BatchDeleteCodeReviews`

<div v-click class="mt-8 text-xl">
  → <strong>AwsCustomResource</strong> を利用する
</div>

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/APIReference/API_Operations.html" title="AWS Security Agent API Reference - Actions" />

<!--
1. まずは CodeReview のポイントです
2. CodeReview は、連携したリポジトリをコードスキャンするためのリソースです
3. CloudFormation のイベントに対応した API が揃っています。Create には CreateCodeReview、Update には UpdateCodeReview、Delete には BatchDeleteCodeReviews です
4. （クリック）なので、AwsCustomResource を利用します
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">AwsCustomResource とは？</h2>
</div>

<br>

- CloudFormation イベントごとに AWS SDK を1つだけ呼べる
- 処理を書かずに、プロパティを渡すだけで済む
- 呼び出す AWS SDK から IAM ポリシーを自動で作れる

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html" title="class AwsCustomResource (construct) · AWS CDK" />

<!--
1. AwsCustomResource は、CDK が用意しているカスタムリソースの書き方です
2. CloudFormation のイベントごとに、AWS SDK の呼び出しを1つだけ設定できます
3. カスタムリソースを扱うための処理は書かずに、プロパティを渡すだけで済みます
4. 権限も、AwsCustomResourcePolicy.fromSdkCalls を使えば、呼び出す AWS SDK から必要な IAM ポリシーを自動で作ってくれます
-->

---

## CodeReview のための AwsCustomResource

<InlineSvg src="awscr-codereview.svg" label="AwsCustomResource のカスタムリソースで、Create に CreateCodeReview、Update に UpdateCodeReview、Delete に BatchDeleteCodeReviews を割り当て、CDK が自動で作る Lambda 関数が CodeReview を操作する図" class="mx-auto mt-4" style="width: 840px" />

<!--
1. CodeReview のための AwsCustomResource は、こんなイメージです
2. Create のイベントには CreateCodeReview、Update には UpdateCodeReview、Delete には BatchDeleteCodeReviews を割り当てます
3. 呼び出しを担当する Lambda 関数は、CDK が自動で作ってくれます
-->

---

<div class="flex items-center gap-4">
  <img src="/images/aws/security-agent.svg" class="h-12" />
  <h2 class="!m-0">Integration のポイント</h2>
</div>

<br>

- GitLab のアクセストークンと Continuum を連携するリソース
- プロパティにアクセストークンを渡す必要がある
  - テンプレートやログにアクセストークンが流出してしまう
- Secrets Manager の ARN だけ渡し、処理の中でトークンを取得する
  - API 呼び出しが2回必要

<div v-click class="mt-6 text-xl">
  → <strong>カスタムリソースプロバイダーフレームワーク</strong>を利用する
</div>

<!--
1. 次は Integration のポイントです
2. Integration は、GitLab のアクセストークンと Continuum コードスキャニングを連携するリソースです
3. 作成するときに、プロパティにアクセストークンを渡す必要があります
4. AwsCustomResource だと、渡したプロパティが CloudFormation テンプレートやログに残ってしまい、アクセストークンが流出してしまいます
5. そこで、プロパティには Secrets Manager の ARN だけを渡して、処理の中でトークンを取得します。こうすると API の呼び出しが2回必要になるので、AwsCustomResource では書けません
6. （クリック）なので、カスタムリソースプロバイダーフレームワークを利用します
-->

---

<div class="flex items-center gap-4">
  <img src="/public/images/aboutme/awscdk.dio.png" class="h-12" />
  <h2 class="!m-0">プロバイダーフレームワークとは？</h2>
</div>

<div class="text-sm opacity-70 mt-1">カスタムリソースプロバイダーフレームワーク</div>

- CloudFormation イベントに合わせた処理を Lambda 関数で書ける
- 処理はソースコードで書くので、複雑な処理も任せられる
- カスタムリソースに必要な機能を簡単に使える
  - CloudFormation への応答
  - エラーハンドリング
  - 非同期処理のポーリング
- 呼び出す処理に必要な権限は自分で付与する必要がある

<BottomLink href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html#provider-framework" title="Provider Framework · AWS CDK" />

<!--
1. カスタムリソースプロバイダーフレームワークは、CloudFormation のイベントに合わせた処理を、Lambda 関数で実装できる仕組みです
2. 処理はソースコードで書くので、複雑な処理も任せられます
3. カスタムリソースに必要な機能も、簡単に使えます。CloudFormation への応答、エラーハンドリング、非同期処理のポーリングです
4. ただし、処理用の Lambda 関数が Secrets Manager を読んだり API を呼んだりする権限は、grantRead などで自分で付けます
5. 素のカスタムリソースだと、Lambda が急に落ちると CloudFormation は応答を待って、デフォルトで1時間待たされます。プロバイダーフレームワークなら、そこを受け止めて失敗として返してくれます
-->

---

<h2><span style="font-size: 0.85em">Integration のためのプロバイダーフレームワーク</span></h2>

<div class="text-sm opacity-70 mt-1">※ 省略のため Create イベントのみ記載</div>

<InlineSvg src="provider-integration.svg" label="プロバイダーフレームワークのカスタムリソースが、プロパティで Secrets Manager の ARN を受け取り、CDK が作るフレームワーク用の Lambda 関数から自前の処理用 Lambda 関数に Create を渡し、Secrets Manager からアクセストークンを取得して CreateIntegration を呼び出す図" class="mx-auto mt-4" style="width: 840px" />

<!--
1. Integration のためのプロバイダーフレームワークは、こんなイメージです
2. プロパティとしては、アクセストークンそのものではなく、Secrets Manager の ARN を受け取ります
3. プロバイダーフレームワークでは、フレームワーク用の Lambda 関数を CDK が自動で作ってくれます。イベントはそこから、自前で書いた処理用の Lambda 関数に渡されます
4. 処理用の Lambda 関数の中で、Secrets Manager からアクセストークンを取得します
5. そのアクセストークンをプロパティに指定して、CreateIntegration を呼び出します
6. これで、アクセストークンが CloudFormation テンプレートやログに残りません
-->

---

<h2>AwsCustomResource と<br>プロバイダーフレームワークの使い分け</h2>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="rounded-xl border-2 border-gray-300 p-5">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-9" />
      <span class="font-bold" style="font-size: 1.2rem; white-space: nowrap">AwsCustomResource</span>
    </div>
    <ul>
      <li style="font-size: 1.1rem">AWS SDK の呼び出し1回で済む</li>
      <li style="font-size: 1.1rem">機密情報を扱わない</li>
      <li style="font-size: 1.1rem">処理の完了を待たなくていい</li>
    </ul>
  </div>
  <div class="rounded-xl border-2 border-gray-300 p-5">
    <div class="flex items-center gap-3 mb-2">
      <img src="/public/images/aboutme/awscdk.dio.png" class="h-9" />
      <span class="font-bold" style="font-size: 1.2rem; white-space: nowrap">プロバイダーフレームワーク</span>
    </div>
    <ul>
      <li style="font-size: 1.1rem">複数の処理が必要</li>
      <li style="font-size: 1.1rem">機密情報を扱う</li>
      <li style="font-size: 1.1rem">処理の完了を待ちたい</li>
      <li style="font-size: 1.1rem">AWS 以外の API を呼びたい</li>
    </ul>
  </div>
</div>

<!--
1. 最後に、AwsCustomResource とプロバイダーフレームワークの使い分けです
2. AwsCustomResource は、各イベントが AWS SDK の呼び出し1回で済んで、機密情報を扱わず、処理の完了を待たなくていいときに使います。CodeReview がこれでした
3. プロバイダーフレームワークは、複数の処理が必要なとき、機密情報を扱うとき、時間のかかる処理の完了を待ちたいとき、AWS 以外の API を呼びたいときに使います。Integration がこれでした
-->

---
layout: center
---

<div>
  <Kogoe>おわりに</Kogoe>
  <h2><span style="font-size: 0.82em">カスタムリソースを使えば<br>CloudFormation 未対応のサービスも<br>CDK で管理できる！</span></h2>
</div>

<br>

<div class="text-lg">その他カスタムリソースを使いたくなるタイミング</div>

- CloudFormation で定義できないものを管理したい
- デプロイしたリソースにデータを投入したい
- デプロイフローに処理を差し込みたい
- デプロイ時に外部から情報を取得したい

<!--
1. おわりにです
2. カスタムリソースを使えば、CloudFormation に対応していないサービスも、CDK で管理できます
3. その他、カスタムリソースを使いたくなるタイミングを4つ挙げます
4. CloudFormation で定義できないものを管理したいとき。未対応の AWS リソースや、AWS 外のサービスの設定などです
5. デプロイしたリソースにデータを投入したいとき。初期データの投入や、ファイルの配置などです
6. デプロイフローに処理を差し込みたいとき。作成後の一度きりの処理や、削除前の後片付けなどです
7. デプロイ時に外部から情報を取得したいとき。別のリージョンやアカウントにある値の参照などです
-->

---
layout: center
class: text-center
transition: fade
---

## 宣伝

---
src: ./pages/pr/mates/index.md
---

---
layout: ending
---

# Thank You!

<div class="absolute right-8 bottom-8 flex flex-col items-center gap-2">
  <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0;">＼ ご清聴ありがとうございました！ ／</p>
  <img src="/images/aboutme/eye-catch.png" class="h-36" />
</div>

<!--
1. ご清聴ありがとうございました
-->
