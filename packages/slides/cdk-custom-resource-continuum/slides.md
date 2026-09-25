---
background: '#0283B2'
class: 'cover'
drawings:
  persist: false
transition: slide-left
title: CDKのカスタムリソースのお話し
mdc: true
addons:
  - '@slides/ui'
fonts:
  sans: 'Noto Sans JP'
  serif: 'Noto Sans JP'
  mono: 'Fira Code'
---

**JAWS-UG 茨城 #17 秋の推しAWSサービスLTまつり！**

# CFn未対応でも諦めない！<br>CDKのカスタムリソースのお話し

2026.9.30（水）\
池田 晃尚（[@akikii\_\_](https://x.com/akikii__)）

<div class="absolute right-8 bottom-8">
  <img src="/public/images/aboutme/eye-catch.png" class="h-36" />
</div>

<!--
1. よろしくお願いします
2. CDKのカスタムリソースのお話しをします
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
layout: center
transition: view-transition
---

<div style="view-transition-name: cfn-unsupported">
  みなさんは
  <h2>新しいサービスをCDKで作ろうとしたら<br>CloudFormation未対応だった</h2>
  ことはありませんか？
</div>

<!--
1. みなさんは、新しいサービスをCDKで作ろうとしたら、CloudFormationに対応していなかった、ということはありませんか？
-->

---
layout: center
transition: view-transition
---

<div style="view-transition-name: cfn-unsupported">
  <Kogoe>ぼくはありました...</Kogoe>
  <h2>Continuum のコードレビューを作ろうとしたら<br>CloudFormation未対応で困った！</h2>
  <Kogoe>Continuum（旧 AWS Security Agent）</Kogoe>
</div>

<Overlay>
  <strong>カスタムリソース</strong>を使ってCDKで管理しました！
</Overlay>

<!--
1. ぼくはありました
2. Continuum、旧 Security Agent のコードレビューを作ろうとしたとき、CloudFormationに対応していなくて困りました
3. （クリック）なので、カスタムリソースを使ってCDKで管理しました、というお話しです
-->

---
layout: center
class: text-center
transition: fade
---

## ① Continuum のコードレビューを導入したい

---
chapter: ① Continuum のコードレビューを導入したい
---

<ChapterLabel />

## GitLab のリポジトリを AI でレビューしたい

<br>

コードレビューに必要な最小構成は<strong>3つ</strong>

<PlainList>
  <li>🔗 Integration<Kogoe class="ml-3">GitLab との連携</Kogoe></li>
  <li>🧑‍💻 Agent Space<Kogoe class="ml-3">Continuum のエージェントの作業場所</Kogoe></li>
  <li>🔍 Code Review<Kogoe class="ml-3">どのリポジトリをどうレビューするかの設定</Kogoe></li>
</PlainList>

<Kogoe>Continuum はあくまで題材です</Kogoe>

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/userguide/connect-gitlab.html" title="Connect AWS Security Agent to GitLab repositories" />

<!--
1. GitLab のリポジトリに対して、AI でコードレビューをしたいと思いました
2. 必要なリソースは、Integration、Agent Space、Code Review の3つです
3. Continuum はあくまで題材で、今日の本題はカスタムリソースです
-->

---
chapter: ① Continuum のコードレビューを導入したい
---

<ChapterLabel />

<div>
  <Tag name="CloudFormation未対応" color="red" />
  <h2>Agent Space しか CloudFormation に対応していない...</h2>
</div>

<br>

<PlainList>
  <li>⭕️ Agent Space<Kogoe class="ml-3">L1 Construct がある</Kogoe></li>
  <li>❌ Integration</li>
  <li>❌ Code Review</li>
</PlainList>

<Overlay>
  このままだと<strong>CDKで書けない</strong>...！
</Overlay>

<!--
1. この3つのうち、CloudFormation に対応しているのは Agent Space だけでした
2. Integration と Code Review は対応していないので、このままだと CDK で書くことができません
-->

---
layout: center
class: text-center
transition: fade
---

## ② それでもCDKで書きたい

---
chapter: ② それでもCDKで書きたい
---

<ChapterLabel />

<div>
  <Kogoe>マネコンから作ればいいのでは？</Kogoe>
  <h2>それでもCDKで書きたい理由があります</h2>
</div>

<br>

<PlainList>
  <li>💡 リポジトリを見れば構成が分かる</li>
  <li>💡 既存のインフラと同じ場所で管理できる</li>
  <li>💡 Code Review を作りやすく消しやすい</li>
  <li>💡 L1 Construct が来ても無駄にならない</li>
</PlainList>

<Overlay>
  <strong>なんでこの設定にしたんだっけ</strong>を<br>設定にいちばん近いところに残せる！
</Overlay>

<!--
1. マネコンから作ればいいのでは、と思うかもしれません
2. でも、それでも CDK で書きたい理由があります
3. リポジトリを見れば構成が分かる、既存のインフラと同じ場所で管理できる、作りやすく消しやすい、L1 が来ても無駄にならない
4. （クリック）一番大きいのは、なんでこの設定にしたんだっけ、を設定にいちばん近いところに残せることだと思っています
5. マネコンから作ると、どんな設定でやっているかを探すのも大変になっちゃいます
-->

---
layout: center
class: text-center
transition: fade
---

## ③ カスタムリソースとは

---
chapter: ③ カスタムリソースとは
---

<ChapterLabel />

<TitledSection title="カスタムリソース" description="デプロイ時に呼ばれて、リソースを管理する処理を自分で書ける仕組み" />

<div class="flex gap-4 items-center justify-center mt-4">

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/cfn-icon.dio.png" class="h-24"/>
  <span class="text-gray-400 w-40 text-center text-sm">CloudFormation</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2 text-center">
  <strong>Create / Update / Delete</strong>
  <span class="text-gray-400 text-sm">3種類のイベントが届く</span>
</div>

<span class="text-3xl">→</span>

<div class="flex flex-col items-center gap-2">
  <img src="/public/images/icons8-aws-240.png" class="h-24"/>
  <span class="text-gray-400 w-40 text-center text-sm">Lambda / SNS トピック<br>（自分で書いた処理）</span>
</div>

</div>

<Overlay>
  <PlainList>
    <li>💡 1つの処理の中でイベントごとに分岐する</li>
    <li>💡 渡したプロパティはテンプレートにそのまま載る</li>
  </PlainList>
</Overlay>

<BottomLink href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/template-custom-resources.html" title="カスタムリソースを使用してカスタムプロビジョニングロジックを作成する" />

<!--
1. カスタムリソースは、デプロイのときに呼ばれて、リソースを管理する処理を自分で書ける仕組みです
2. 呼び出し先は Lambda か SNS トピックで、Create、Update、Delete の3種類のイベントが届きます
3. （クリック）1つの処理の中で分岐して、渡したプロパティはテンプレートにそのまま載ります
-->

---
chapter: ③ カスタムリソースとは
---

<ChapterLabel />

## CDK ではカスタムリソースの書き方が2つあります

<br>

<TitledSection title="AwsCustomResource" description="呼び出す AWS SDK の操作を指定するだけ。Lambda を書かなくていい" />

<br>

<TitledSection title="Provider Framework" description="自分で書いた Lambda で処理する。CloudFormation とのやりとりは肩代わりしてくれる" />

<Overlay>
  Code Review と Integration で<strong>使い分けました</strong>
</Overlay>

<!--
1. CDK では、カスタムリソースの書き方が2つあります
2. AwsCustomResource は、呼び出す SDK の操作を指定するだけで、めっちゃ楽です
3. Provider Framework は、自分で Lambda を書く代わりに、細かいことまでできます
4. （クリック）今回は Code Review と Integration で使い分けました
-->

---
layout: center
class: text-center
transition: fade
---

## ④ Code Review は AwsCustomResource で

---
chapter: ④ Code Review は AwsCustomResource で
---

<ChapterLabel />

<div>
  <Kogoe>Code Review は</Kogoe>
  <h2>各イベントが API 1回で済むので素直に書ける！</h2>
</div>

<PlainList>
  <li>Create → <code>CreateCodeReview</code></li>
  <li>Update → <code>UpdateCodeReview</code></li>
  <li>Delete → <code>BatchDeleteCodeReviews</code></li>
</PlainList>

<Overlay>
  呼ぶ SDK を<strong>指定するだけ</strong>で作れます
</Overlay>

<BottomLink href="https://docs.aws.amazon.com/securityagent/latest/APIReference/API_Operations.html" title="AWS Security Agent API Reference - Actions" />

<!--
1. Code Review のほうは、SDK に Create、Update、Delete がそのまま揃っています
2. プロパティも普通に指定するだけなので、素直に書けます
-->

---
chapter: ④ Code Review は AwsCustomResource で
---

<ChapterLabel />

```ts {all|2-6|7-11|12-16}
new AwsCustomResource(this, "CodeReview", {
  onCreate: {
    service: "SecurityAgent", action: "CreateCodeReview",
    parameters: { agentSpaceId, title, assets },
    physicalResourceId: PhysicalResourceId.fromResponse("codeReviewId"),
  },
  onUpdate: {
    service: "SecurityAgent", action: "UpdateCodeReview",
    parameters: { agentSpaceId, codeReviewId: idRef, assets },
    physicalResourceId: PhysicalResourceId.fromResponse("codeReviewId"),
  },
  onDelete: {
    service: "SecurityAgent", action: "BatchDeleteCodeReviews",
    parameters: { agentSpaceId, codeReviewIds: [idRef] },
  },
  policy: AwsCustomResourcePolicy.fromSdkCalls({ resources: ANY_RESOURCE }),
});
```

<Overlay>
  <PlainList>
    <li>💡 Construct でラップすれば、リポジトリの配列から量産できる</li>
  </PlainList>
</Overlay>

<!--
1. AwsCustomResource だと、こんな感じで書けます
2. Create、Update、Delete それぞれに、呼ぶ SDK の操作を割り当てるだけです
3. （クリック）Construct でラップすれば、リポジトリの配列から量産もできます
-->

---
layout: center
class: text-center
transition: fade
---

## ⑤ Integration は Provider Framework で

---
chapter: ⑤ Integration は Provider Framework で
---

<ChapterLabel />

<div>
  <Tag name="シークレット" color="orange" />
  <h2>Integration の作成には<br>GitLab のアクセストークンが必要</h2>
</div>

```json
{
  "provider": "GITLAB",
  "input": {
    "gitlab": { "accessToken": "glpat-xxxx...", "tokenType": "GROUP" }
  }
}
```

<Overlay>
  AwsCustomResource だと、トークンが<br><strong>テンプレートやログに平文で残ってしまう</strong>...！
</Overlay>

<!--
1. 問題は Integration のほうです
2. Create のときに、GitLab のパーソナルアクセストークンやグループアクセストークンを、引数でそのまま渡します
3. （クリック）AwsCustomResource だと、渡したパラメータがテンプレートに載るし、ログにも出たりするので、色々まずいです
-->

---
chapter: ⑤ Integration は Provider Framework で
---

<ChapterLabel />

## トークンは Lambda の中で<br>Secrets Manager から読む

<Kogoe>テンプレートには ARN だけ渡す</Kogoe>

<PlainList>
  <li>① Secrets Manager からトークンを取得</li>
  <li>② 取得したトークンで <code>CreateIntegration</code> を呼ぶ</li>
</PlainList>

<Overlay>
  API 呼び出しが<strong>2回</strong>になるので<br>AwsCustomResource では書けない
</Overlay>

<!--
1. なので、テンプレートには Secrets Manager の ARN だけを渡して、Lambda の中でトークンを読むようにしました
2. （クリック）こうすると API の呼び出しが2回になるので、AwsCustomResource では書けません
3. そこで Provider Framework の出番です
-->

---
chapter: ⑤ Integration は Provider Framework で
---

<ChapterLabel />

```ts {all|2-9|10-14}
export const handler = async (event: CdkCustomResourceEvent) => {
  if (event.RequestType === "Create") {
    const accessToken = await getToken(event.ResourceProperties.TokenSecretArn);
    const res = await client.send(new CreateIntegrationCommand({
      provider: "GITLAB", integrationDisplayName,
      input: { gitlab: { accessToken, tokenType: "GROUP", groupId } },
    }));
    return { PhysicalResourceId: res.integrationId };
  }
  if (event.RequestType === "Delete") {
    await client.send(new DeleteIntegrationCommand({
      integrationId: event.PhysicalResourceId,
    }));
  }
};
```

<Overlay>
  Provider を使えば、自分で書くのは<strong>onEvent ハンドラだけ</strong>
</Overlay>

<!--
1. Provider Framework を使うと、自分で書くのは onEvent ハンドラだけで済みます
2. Create のときに Secrets Manager からトークンを読んで、CreateIntegration を呼んでいます
3. TODO: Update の扱い（Integration には Update の API がない）
-->

---
chapter: ⑤ Integration は Provider Framework で
---

<ChapterLabel />

<div>
  <Kogoe>素のカスタムリソースだと...</Kogoe>
  <h2>Lambda が落ちると、CloudFormation が<br>作成中のまま1時間待たされる</h2>
</div>

<Overlay>
  Provider Framework なら、プロバイダーの Lambda が<br><strong>受け止めて終わらせてくれる！</strong>
</Overlay>

<!--
1. Provider Framework には、すごく嬉しいところもあります
2. 素のカスタムリソースだと、Lambda の中で分岐やエラー処理をちゃんと書かないといけません
3. Lambda が急に落ちると、CloudFormation は作成中のまま、デフォルトで1時間待つようになっています
4. （クリック）Provider Framework なら、プロバイダーの Lambda が受け止めて終了してくれるので、その1時間待ちをスキップできます
-->

---
layout: center
class: text-center
transition: fade
---

## ⑥ カスタムリソースの使い分け

---
chapter: ⑥ カスタムリソースの使い分け
---

<ChapterLabel />

## AwsCustomResource が使えるのは

<PlainList>
  <li>✅ SDK の呼び出しが1回で済む</li>
  <li>✅ レスポンスが 4096 バイト以内</li>
  <li>✅ 完了を待たなくていい</li>
</PlainList>

<Overlay>
  外れたら <strong>Provider Framework</strong> を使いましょう！
</Overlay>

<!--
1. AwsCustomResource が使えるのは、SDK の呼び出しが1回で済む、レスポンスが4096バイト以内、完了を待たなくていい、のときです
2. （クリック）どれかから外れたら、Provider Framework を使いましょう
-->

---
layout: center
---

<div>
  <Kogoe>まとめ</Kogoe>
  <h2>API さえあれば<br>CFn未対応でもCDKに載せられる！</h2>
</div>

<br>

<PlainList>
  <li>💡 L1 は API のパラメータとほぼ1対1なので、あとで置き換えるのも機械的</li>
  <li>💡 簡単なら AwsCustomResource、シークレットを扱うなら Provider Framework</li>
</PlainList>

<!--
1. まとめです
2. API さえあれば、CloudFormation に対応していなくても CDK に載せられます
3. L1 は API のパラメータとほぼ1対1なので、あとで L1 に置き換えるのも機械的にできそうです
-->

---
layout: center
class: cover
style: 'background-color: #0283B2;'
---

<div>
  みなさんも
  <h2>「CFn未対応だから」で諦める前に<br>API があるか見てみてください！</h2>
</div>

<br><br>

<div class="absolute right-8 bottom-8 flex flex-col items-center print:hidden" style="color: #e0e0e0; gap: 0;">
  ＼ ご静聴ありがとうございました！ ／
  <img src="/public/images/aboutme/eye-catch.png" class="h-32" />
</div>

<!--
1. みなさんも「CloudFormation に対応していないから」で諦める前に、API があるかを見てみてください
2. ご静聴ありがとうございました
-->
