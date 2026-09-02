---
layout: two-cols-header
layoutClass: gap-8
transition: slide-left
---

# FireLens導入でvCPUのコストが大幅増

::left::

<StackedBar
  class="mt-6"
  unit="vCPU"
  :height="320"
  :segments="[
    { label: 'App', value: 1, color: '#ED7100' },
    { label: 'FireLens', value: .25, color: '#1BA1A8' },
    { label: '空き', value: .75, color: '#cbd5e1', dashed: true },
  ]"
/>

::right::

- FireLensコンテナは 0.25vCPUほどの余力が必要
- FargateのvCPUは.25, .5, 1, 2, ..., 32と、2の冪乗になっている
- アプリコンテナが1vCPUを下回りたくないなら2vCPUを割り当てる必要がある

<Overlay>2倍のvCPU料金がかかってしまうこととなった...！</Overlay>

<BottomLink href="https://aws.amazon.com/jp/fargate/pricing/" title="AWS Fargate 料金" />


<!--
画像: scalling-mini-tasks.dio.png（小さいタスクを大量スケーリングしている図）

■ 理由①：FireLens追加でvCPUが2倍になる（vCPU肥大）

1. （前提のおさらい）1vCPUの小さいタスクを大量に並べて捌いている
2. ここにFireLensコンテナを足したい。FireLensは0.25vCPU程の余力が必要
   - アプリと同じタスクに足すこともできるが、スケールアウトに時間がかかるためアプリの余力は削りたくない
3. しかしFargateは1vCPUの次が2vCPU。1.25vCPUは選べず、2vCPUを割り当てる必要がある！
4. → ECSタスクの料金が単純に2倍に。しかも小さいタスクを大量に並べているので、その2倍が全タスクに波及する
5. （回収）前述のNode.js特性で、増えた2vCPU目も使い切れない＝まるまる損

使用画像候補: scalling-mini-tasks.dio.png / scalling-mini-tasks.drawio.svg

-->
