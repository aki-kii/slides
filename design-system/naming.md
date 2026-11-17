# デッキの名前（提案）

`packages/slides/<名前>/` のフォルダ名の付け方の提案。名前はそのまま、パッケージ名（`@slides/<名前>`）と公開の URL（`https://aki-kii.github.io/slides/<名前>/`）になる。

状態: 提案。本人は決めていない。既存のデッキの名前は変えない（URL が変わり、共有したリンクが切れるため）。

## 今の名前（2026-11-18）

`slides.md` がリポジトリに入った日の順。

| 入った日 | 名前 | 付け方 | 登壇した場 |
|---|---|---|---|
| 2026-03-06 | `cdk-day1-experiment` | 話題 | — |
| 2026-03-18 | `cdk-3min-cooking` | 話題 | — |
| 2026-05-12 | `aws-oss-perspective` | 話題 | — |
| 2026-07-14 | `ecr-sbom-supply-chain-investigation` | 話題 | — |
| 2026-07-14 | `failed-ecs-log-cost-reduction` | 話題 | — |
| 2026-09-02 | `zero-drift-cdk-ops` | 話題 | — |
| 2026-10-01 | `cdk-custom-resource-continuum` | 話題 | JAWS-UG 茨城 #17 |
| 2026-10-01 | `jaws-sonic-2026` | 場＋年 | JawsSonic 2026 |
| 2026-10-22 | `jawsug-tokyo-lunch-lt-40` | 場＋回 | JAWS-UG 東京 ランチタイム LT #40 |
| 2026-10-29 | `jawsug-bgnr-93` | 場＋回 | JAWS-UG 初心者支部 #93 |
| 2026-11-05 | `jawsug-cdk-tokyo-cdkd-talk` | 場＋話題 | JAWS-UG CDK 支部×東京支部 |
| 2026-11-11 | `jiyugaoka-any-1` | 場＋回 | 自由が丘.any #1 |
| 2026-11-12 | `jawsug-container-31` | 場＋回 | JAWS-UG コンテナ支部 #31 |
| — | `whats-cloud-assembly` | 話題 | `slides.md` がない |

（「—」は名前から場が読み取れないもの。ここでは調べていない）

分かること:

- 2つの付け方がある。**話題で付ける**（2026-09 まで）と、**登壇した場と回で付ける**（2026-10 から）
- 2026-10-22 以降の5つはすべて場から始まっている。今はこちらに移っている
- どれも英小文字・数字・ハイフンだけ。`pnpm new-slide` は名前の形を確かめていない

## 提案する決まり

1. **登壇した場がある発表は `<場>-<回>`**。e.g. `jawsug-bgnr-93`、`jiyugaoka-any-1`
   - JAWS-UG は `jawsug-<支部>-<回>`。支部は短い英語（`bgnr`、`container`、`tokyo-lunch-lt`）
   - 回の番号が無い場は年を付ける。e.g. `jaws-sonic-2026`
2. **同じ場で2本話す、または回の番号が無く年でも分けられないときは、最後に話題を足す**。e.g. `jawsug-cdk-tokyo-cdkd-talk`
3. **場の無いもの（ブログ用、社内、場が決まる前に作り始めたもの）は話題で付ける**。2〜4語、英小文字。e.g. `zero-drift-cdk-ops`
4. 使う文字は英小文字・数字・ハイフンだけ。日本語やアンダースコアは使わない
5. 場が決まる前に話題で作り始めたデッキは、場が決まっても名前を変えない（URL を変えないため）

## この提案にしない場合の候補

- 日付を前に付ける（`2026-11-jawsug-container-31`）。life の `tasks/speaking/` のフォルダ名（`2026-11-jawsug-container-31`）とそろい、並びが日付順になる。ただし今の名前とは形が大きく変わる
