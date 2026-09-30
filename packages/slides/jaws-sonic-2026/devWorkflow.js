/**
 * コーディングエージェントの開発フローの層。
 * 下の層 (実行頻度が高く、1サイクルが速いもの) から順に並べる。
 *
 * ここが唯一の定義。dev-workflow / cdk-sensors のスライドと、
 * 4章トレースのレール (components/PipelineStage.vue) がこれを読む。
 * 層を足したり名前を変えたりするときは、このファイルだけ直せばよい。
 *
 * key    : PipelineStage の stage に渡す短縮名
 * label  : 図に出す層の名前
 * desc   : 「開発フロー」のスライドで pill の右に出す説明
 * sensor : 「開発フローごとのCDKセンサー」で pill の右に出す検証
 */
export const DEV_WORKFLOW_STEPS = [
  {
    key: 'edit',
    label: 'ファイル編集',
    desc: '実装のためにファイルを編集する',
    sensor: 'Linter / 型チェッカー',
  },
  {
    key: 'commit',
    label: 'git commit',
    desc: '編集したファイルをまとめてコミットする',
    sensor: '単体テスト / cdk synth',
  },
  {
    key: 'push',
    label: 'git push',
    desc: 'コミットをまとめてリモートブランチにプッシュする',
    sensor: 'cdk diff',
  },
  {
    key: 'pr',
    label: 'PR作成',
    desc: 'プルリクエストを作成するとCIで検証が走る',
    sensor: 'CI (cdk validate / cdk drift / Linter / 単体テスト / 型チェッカー)',
  },
  {
    key: 'deploy',
    label: 'cdk deploy',
    desc: 'PRをマージするとCDから実環境にデプロイされる',
    sensor: 'CD (cdk deploy) / cdk diagnose',
  },
];

/** ラベルだけ要る側 (PipelinePyramid) 向け */
export const DEV_WORKFLOW_LABELS = DEV_WORKFLOW_STEPS.map((step) => step.label);
