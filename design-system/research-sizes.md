# サイズの調査メモ

[土台のサイズ](foundation.md#base-size) を決めたときの調べものと考えたこと。調べたのは 2026-11-18。

## 問い

ページの形式（Slidev の 16:9、会場のスクリーンに映す登壇資料）で、人がスライドを見たときに読みやすい文字・アイコン・余白の大きさはどれくらいか。今のデッキに合わせるのではなく、規範として決める。

## 1. 画面の大きさ（Slidev の既定）

- Slidev の既定は `canvasWidth: 980`、`aspectRatio: 16/9`。リポジトリの `@slidev/parser` 52.11.5 の `dist/core.mjs` で確かめた。高さは 980 ÷ 16 × 9 ≒ 552px
- 既定のページの余白は `.slidev-layout { @apply px-14 py-10 }`（`@slidev/client` の `styles/layouts-base.css`）。本人のデッキは全部 `:root { font-size: 20px }` にしているので、左右 3.5rem ＝ 70px、上下 2.5rem ＝ 50px
- 既定の文字は `text-[1.1rem]`（本人のデッキでは 22px）、見出し h1 は `text-4xl`（`@slidev/theme-default` の `styles/layouts.css`）
- PowerPoint のワイド画面は 13.333 × 7.5 インチ ＝ 960 × 540pt。Slidev の 980 × 552px とほぼ同じなので、pt で書かれた推奨値は px に読み替えられる（1pt ≒ 1.02px）

## 2. 文字の大きさの推奨（スライドのアクセシビリティの指針）

| 出典 | 本文 | 見出し | 確かめ方 |
|---|---|---|---|
| ニューヨーク市 障害者局 Accessible Slidedecks Guide | 24pt 以上。ビデオ会議だけで見るなら、少しの文字は 18pt でよい | — | ページを開いて確かめた |
| UC Merced Accessibility | 24pt 以上 | 36pt 以上 | 検索結果で確かめた（ページは 403 で開けなかった） |
| University of Georgia（DASH） | — | タイトル 44pt 以上 | 検索結果で確かめた |
| University of Illinois Springfield | 18 以上 | — | 検索結果で確かめた |
| Guy Kawasaki の 10/20/30 ルール | 30pt 以上 | — | よく知られた経験則。LT のように枚数の少ない発表の目安 |

いちばん多い推奨は「本文 24pt 以上」。見出しは 36pt 以上（UC Merced）。どれも「会場が広ければ大きく」と添えている。

→ 本文の下限を 24px、見出しを 36px、表紙のタイトルを 40〜48px（UGA の 44pt を中に入れる）にした。補足は NYC の「少しの文字は 18pt」を下限にした。LT は文字を減らして 28px 以上（Kawasaki の 30pt に近づける）を目指す。

## 3. 見る距離と文字の高さ（AVIXA DISCAS）

AV 機器の業界団体 AVIXA の規格 ANSI/INFOCOMM V202.01（DISCAS）は、画面のいちばん小さい大事な要素（英小文字など）の高さが画面の高さの何%か（%Element Height）で、読める距離を決める。基本の読み取り（BDM）の係数は 200。見る距離 ÷ 画面の高さ（Viewing Ratio）ごとの下限は次の通り（AVIXA の説明ページの表から抜粋）。

| 見る距離 ÷ 画面の高さ | 要素の高さの下限 |
|---|---|
| 3〜4 | 2.0% |
| 4〜5 | 2.5% |
| 5〜6 | 3.0% |
| 6〜7 | 3.5% |
| 8〜9 | 4.5% |

Slidev の画面の高さ 552px に当てはめると:

- 補足 18px ＝ 3.3%。画面の高さの約6倍の距離まで
- 本文 24px ＝ 4.3%。約8倍の距離まで
- 出典のリンク 12px ＝ 2.2%。約4倍の距離まで。会場の後ろからは読めない前提なので「読ませない文字」の例外にした

日本語の字は字面が em の枠いっぱいに近い（英小文字の x の高さは em の半分ほど）。ここでは文字の大きさ（px）÷ 画面の高さをそのまま %Element Height として扱った。日本語は画数が多いので、英語より有利とは考えず、同じ下限を使う（判断）。

## 4. コントラスト

- WCAG 2.2 の 1.4.3（最低限）は文字 4.5:1、大きい文字（18pt 以上、または 14pt 以上の太字）は 3:1。1.4.6（高度）は 7:1、大きい文字は 4.5:1
- NYC のガイドはスライドに 7:1 以上を求めている
- 会場のプロジェクターは画面より色が薄く出るので、本文・見出しは 7:1、補足は 4.5:1、24px 以上の太字の強調は 3:1 を下限にした
- 今のデッキの値は [土台の色](foundation.md#base-color) の表に計算して載せた。小声（約 2.7:1）、章ラベル（約 1.8:1）、出典の題名（約 2.6:1）が足りない

## 5. 行の間・行の数

- WCAG 2.2 の 1.4.12（文字の間隔）は行の高さを文字の 1.5 倍まで広げても崩れないことを求めている。本文の行の間を 1.5 倍にした
- NYC のガイドの「1行8語、1枚8行」から、1枚の本文を8行までにした。日本語は語で数えにくいので、行の長さは本人の決まり「文字は1行に収める」に任せた

## 6. 出典がなく、判断で決めたこと

- アイコンの大きさ（見出しの横 36〜40px、図の主役 48px 以上、グループ枠 24px 以上）。見出しの文字の高さと、diagram-style.md の大きさ（箱のアイコン 48〜64、グループ枠 28〜32）を画面の大きさに直した値から決めた
- 図の中の文字を viewBox の単位で 22 以上にすること。図が 1000 の幅で描かれ、画面では 840px（左右の余白 70px を引いた幅）に縮むので、補足の下限 18px を逆算した
- 日本語の文字の高さの扱い（3. の最後）

## 出典

- Slidev（`@slidev/parser`、`@slidev/client`、`@slidev/theme-default` 52.11.5 のソース、リポジトリの `node_modules`）。説明は https://sli.dev/features/canvas-size
- NYC Mayor's Office for People with Disabilities「Accessible Slidedecks Guide」 https://www.nyc.gov/site/mopd/publications/guides/accessible-slidedecks-guide.page
- UC Merced Accessibility「General Guidelines」 https://accessibility.ucmerced.edu/node/321
- University of Georgia DASH「Slides」 https://dash.uga.edu/create-accessible-content/slides/
- University of Illinois Springfield「Microsoft PowerPoint Accessibility」 https://www.uis.edu/resource/accessibility/microsoft-powerpoint-accessibility
- Guy Kawasaki の 10/20/30 ルール（著書『The Art of the Start』、2005 年のブログ）。まとめ: https://ahaslides.com/blog/10-20-30-rule-presentations
- AVIXA「Display Image Size for 2D Content in Audiovisual Systems（ANSI/INFOCOMM V202.01）」 https://www.avixa.org/standards/discas-calculators/discas/learn-more-about-display-size
- W3C「WCAG 2.2」1.4.3 https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html 、1.4.6 https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html 、1.4.12 https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
