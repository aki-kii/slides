/**
 * #93 の図（public/images/*.svg）の定義。組み立ては @slides/tools に任せる。
 *
 *   pnpm diagrams --icons <アイコン置き場>   # または環境変数 AWS_ICONS
 *
 * AWS のアイコンは AWS Architecture Icons 2026-07-31 版（Icon-package_07312026）。
 */
import { defineDiagrams, palette, type DiagramKit } from '@slides/tools';

const { INK, SUB, LINE, GREEN, GREEN_BG, RED, RED_BG, GRAY } = palette;
const CONSOLE_BLUE = '#0972d3';

// 実際の IP セット（partner-allowed-ips）と同じ並び。A社は 203.0.113.12、B社は 203.0.113.128/28
const ROWS = [
  '198.51.100.7/32',
  '203.0.113.80/32',
  '192.0.2.24/32',
  '192.0.2.10/32',
  '203.0.113.12/32',
  '198.51.100.45/32',
  '203.0.113.128/28',
];
const A_NEW = '198.51.100.200/32';
// A社（203.0.113.12）と見間違えてB社の行（203.0.113.128/28）を消し、A社の新しい値を足した後の一覧
const AFTER: (string | null)[] = [...ROWS.slice(0, 6), null, A_NEW];

type Row = readonly [string, string];

const ALB_CODE: Row[] = [
  [INK, "const alb = new ApplicationLoadBalancer(this, 'Alb', {"],
  [INK, '  vpc,'],
  [INK, '  internetFacing: true,'],
  [INK, '});'],
  [INK, ''],
  [GREEN, '// 取引先のシステムがHTTPでしか連携できないため、HTTPを許可する'],
  [INK, "alb.addListener('Http', {"],
  [INK, '  port: 80,'],
  [INK, '  protocol: ApplicationProtocol.HTTP,'],
  [INK, '});'],
];

const SG_CODE: Row[] = [
  [INK, "const sg = new ec2.SecurityGroup(this, 'BastionSg', {"],
  [INK, '  vpc,'],
  [INK, '  allowAllOutbound: true,'],
  [INK, '});'],
  [INK, ''],
  [RED, 'sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22));'],
];

/** 見ると不安になるので、第2・第3オクテットを伏せる（第1・第4オクテットとプレフィックスは残す） */
function maskIp(ip: string): string {
  const [a, , , ...rest] = ip.split('.');
  return `${a}.■.■.${rest.join('.')}`;
}

/** 行頭の空白の数 */
const indentOf = (line: string) => line.length - line.trimStart().length;

function diagrams(kit: DiagramKit): Record<string, string> {
  const { icon: inner, text: t, arrow, service, svg } = kit;

  // ---------------------------------------------------------------- 共通の部品
  function pane(
    x: number,
    y: number,
    w: number,
    h: number,
    title: string,
    key: string,
  ) {
    return [
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
      `<line x1="${x}" y1="${y + 46}" x2="${x + w}" y2="${y + 46}" stroke="${LINE}" stroke-width="2"/>`,
      inner(key, x + 14, y + 8, 30),
      t(x + 54, y + 30, title, { size: 17, weight: 'bold', anchor: 'start' }),
    ];
  }

  /**
   * 7枚目の実スクショ（IP セットを編集）と同じ形：入力欄＋「削除」ボタン、下に「IP アドレスの追加」。
   * rows の null は消えた行（赤い点線の空欄）。marks は {行番号: [印, 色]} で、行の右に添える。
   */
  function editRows(
    x: number,
    y: number,
    rows: (string | null)[],
    step = 34,
    marks: Record<number, [string, string]> = {},
  ) {
    const o = [
      t(x, y + 16, 'IP アドレス (CIDR 表記)', {
        size: 14,
        weight: 'bold',
        anchor: 'start',
      }),
    ];
    rows.forEach((ip, i) => {
      const yy = y + 28 + i * step;
      if (ip === null) {
        o.push(
          `<rect x="${x}" y="${yy}" width="478" height="26" rx="6" fill="${RED_BG}" stroke="${RED}" stroke-width="2" stroke-dasharray="6 4"/>`,
        );
      } else {
        o.push(
          `<rect x="${x}" y="${yy}" width="400" height="26" rx="6" fill="#ffffff" stroke="${GRAY}" stroke-width="1.5"/>`,
        );
        o.push(t(x + 12, yy + 18, maskIp(ip), { size: 15, anchor: 'start' }));
        o.push(
          `<rect x="${x + 414}" y="${yy}" width="64" height="26" rx="13" fill="#ffffff" stroke="${CONSOLE_BLUE}" stroke-width="2"/>`,
        );
        o.push(
          t(x + 446, yy + 18, '削除', {
            size: 13,
            weight: 'bold',
            color: CONSOLE_BLUE,
          }),
        );
      }
      if (marks[i]) {
        const [label, color] = marks[i];
        o.push(
          t(x + 488, yy + 18, label, {
            size: 14,
            weight: 'bold',
            color,
            anchor: 'start',
          }),
        );
      }
    });
    const yy = y + 28 + rows.length * step + 2;
    o.push(
      `<rect x="${x}" y="${yy}" width="150" height="26" rx="13" fill="#ffffff" stroke="${CONSOLE_BLUE}" stroke-width="2"/>`,
    );
    o.push(
      t(x + 75, yy + 18, 'IP アドレスの追加', {
        size: 13,
        weight: 'bold',
        color: CONSOLE_BLUE,
      }),
    );
    return o;
  }

  /** AI（コーディングエージェントなど）。特定の製品に寄せないよう、文字だけの印にする */
  function aiBadge(cx: number, cy: number, size = 56) {
    const h = Math.floor(size / 2);
    return [
      `<rect x="${cx - h}" y="${cy - h}" width="${size}" height="${size}" rx="14" fill="${INK}"/>`,
      t(cx, cy + 9, 'AI', { size: 24, weight: 'bold', color: '#ffffff' }),
    ];
  }

  /** CDK のコード。日本語のコメントは等幅フォントだと字形が崩れるので、本文のフォントで描く */
  function cdkCode(
    x: number,
    y: number,
    w: number,
    rows: Row[],
    title = 'コード（AWS CDK）',
  ) {
    const h = 76 + rows.length * 19.5;
    const o = [
      `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
      inner('code', x + 14, y + 12, 36),
      t(x + 60, y + 38, title, { size: 18, weight: 'bold', anchor: 'start' }),
    ];
    let yy = y + 80;
    for (const [c, line] of rows) {
      if (c === GREEN) {
        o.push(
          t(x + 16, yy, line.trim(), { size: 13, color: c, anchor: 'start' }),
        );
      } else if (line) {
        o.push(
          t(x + 16, yy, line.replaceAll(' ', '&#160;'), {
            size: 13,
            color: c,
            anchor: 'start',
            mono: true,
          }),
        );
      }
      yy += 19.5;
    }
    return o;
  }

  function chain(keys: string[], x: number, y: number, size = 32, gap = 58) {
    const o: string[] = [];
    keys.forEach((k, i) => {
      o.push(inner(k, x + i * gap, y, size));
      if (i < keys.length - 1) {
        const mid = y + Math.floor(size / 2);
        o.push(
          arrow(
            `M${x + i * gap + size + 3},${mid} L${x + (i + 1) * gap - 4},${mid}`,
          ),
        );
      }
    });
    return o;
  }

  const res: [string, string][] = [
    ['waf', 'AWS WAF'],
    ['elb', 'ALB'],
    ['ecs', 'Amazon ECS'],
  ];
  const out: Record<string, string> = {};

  // ---------------------------------------------------------------- 導入: 構成
  {
    const b: string[] = [];
    ['A社', 'B社', 'C社'].forEach((name, i) => {
      const y = 50 + i * 80;
      b.push(inner('office', 30, y, 48));
      b.push(
        t(92, y + 32, name, { size: 18, weight: 'bold', anchor: 'start' }),
      );
    });
    b.push(t(70, 304, 'お客さんの会社', { size: 15, color: SUB }));
    b.push(
      '<rect x="200" y="10" width="790" height="320" rx="14" fill="none" stroke="#232F3E" stroke-width="2"/>',
    );
    b.push(inner('cloud', 200, 10, 30));
    b.push(
      t(238, 31, 'AWS Cloud', {
        size: 17,
        weight: 'bold',
        color: '#232F3E',
        anchor: 'start',
      }),
    );
    b.push(...service('waf', 330, 100, 'WAF', { sub: 'IPセット' }));
    b.push(...service('elb', 610, 100, 'ALB'));
    b.push(...service('ecs', 880, 100, '業務システム', { sub: '(ECS)' }));
    b.push(arrow('M144,140 L292,108'));
    b.push(t(214, 104, 'アクセスする', { size: 16 }));
    b.push(arrow('M366,100 L572,100'));
    b.push(t(470, 88, '許可した会社だけ通す', { size: 16 }));
    b.push(arrow('M646,100 L842,100'));
    b.push(t(744, 88, 'リクエストを渡す', { size: 16 }));
    const [x0, y0] = [226, 196];
    b.push(
      `<rect x="${x0}" y="${y0}" width="300" height="118" rx="10" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
    );
    b.push(
      t(x0 + 14, y0 + 24, 'IPセット', {
        size: 14,
        weight: 'bold',
        color: SUB,
        anchor: 'start',
      }),
    );
    [
      ['A社', '203.0.113.12/32'],
      ['B社', '203.0.113.128/28'],
      ['C社', '192.0.2.10/32'],
    ].forEach(([who, ip], i) => {
      const yy = y0 + 52 + i * 24;
      b.push(t(x0 + 22, yy, who, { size: 16, anchor: 'start' }));
      b.push(
        t(x0 + 80, yy, maskIp(ip), { size: 16, mono: true, anchor: 'start' }),
      );
    });
    b.push(
      `<rect x="${x0 + 10}" y="${y0 + 33}" width="280" height="25" rx="6" fill="none" stroke="${RED}" stroke-width="2.5"/>`,
    );
    b.push(
      t(x0 + 316, y0 + 52, 'A社のIPアドレスを変更する', {
        size: 17,
        weight: 'bold',
        color: RED,
        anchor: 'start',
      }),
    );
    out['story-architecture.svg'] = svg(
      1000,
      340,
      b,
      '取引先からのアクセスをWAFのIPセットで許可している構成',
    );
  }

  // ---------------------------------------------------------------- 導入: 画面
  {
    // ⑤ 事件
    const b = pane(
      20,
      6,
      600,
      350,
      'マネジメントコンソール　IP セットを編集',
      'console',
    );
    b.push(
      ...editRows(
        48,
        58,
        AFTER.filter((ip) => ip),
      ),
    );
    [
      ['A社', '接続できるようになりました！', GREEN, GREEN_BG],
      ['B社', '急に接続できなくなった！', RED, RED_BG],
    ].forEach(([who, msg, c, bg], i) => {
      const y = 40 + i * 120;
      b.push(inner('office', 670, y + 6, 40));
      b.push(t(690, y + 66, who, { size: 13, weight: 'bold' }));
      b.push(
        `<rect x="724" y="${y}" width="256" height="52" rx="14" fill="${bg}" stroke="${c}" stroke-width="2"/>`,
      );
      b.push(t(852, y + 33, msg, { size: 16, weight: 'bold', color: c }));
    });
    out['story-incident.svg'] = svg(
      1000,
      360,
      b,
      'IPセットの編集画面。B社の行が消えて、A社の新しい値が入っている。A社は接続でき、B社は接続できない',
    );
  }
  {
    // ⑥ 元の値が分からない。A社の旧と新が両方残り、B社の行が消えている
    const b = pane(
      20,
      6,
      600,
      350,
      'マネジメントコンソール　IP セットを編集',
      'console',
    );
    b.push(
      ...editRows(48, 52, AFTER, 31, {
        4: ['A社（旧）', INK],
        6: ['B社（削除）', RED],
        7: ['A社（新）', INK],
      }),
    );
    out['story-lost.svg'] = svg(
      640,
      360,
      b,
      'IPセットの編集画面。A社の旧と新のIPアドレスが両方残り、B社の行が消えている',
    );
  }

  // ---------------------------------------------------------------- 1部: デプロイの仕組み（差分）
  {
    const b: string[] = [];
    const row = (
      x: number,
      y: number,
      items: [string, string][],
      empty?: string,
      hl?: string,
    ) => {
      const o: string[] = [];
      items.forEach(([k, n], i) => {
        const xx = x + i * 72;
        if (k === empty) {
          // 差分になるところ。足りない枠を緑の破線で見せる
          o.push(
            `<rect x="${xx}" y="${y}" width="48" height="48" rx="8" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2.5" stroke-dasharray="6 4"/>`,
          );
        } else {
          o.push(inner(k, xx, y, 48));
          if (k === hl) {
            o.push(
              `<rect x="${xx - 6}" y="${y - 6}" width="60" height="60" rx="10" fill="none" stroke="${GREEN}" stroke-width="3"/>`,
            );
          }
        }
        const on = k === empty || k === hl;
        o.push(
          t(xx + 24, y + 68, n, {
            size: 13,
            weight: on ? 'bold' : 'normal',
            color: on ? GREEN : INK,
          }),
        );
      });
      return o;
    };
    // コード（あるべき姿）
    b.push(
      `<rect x="20" y="20" width="250" height="140" rx="12" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
    );
    b.push(inner('code', 32, 30, 28));
    b.push(
      t(66, 50, 'コード（あるべき姿）', {
        size: 16,
        weight: 'bold',
        anchor: 'start',
      }),
    );
    b.push(...row(44, 68, res, undefined, 'ecs'));
    // 現在の状態
    b.push(
      `<rect x="20" y="210" width="250" height="140" rx="12" fill="#f5f7f9" stroke="${LINE}" stroke-width="2"/>`,
    );
    b.push(inner('cloud', 32, 220, 28));
    b.push(
      t(66, 240, '現在の状態', { size: 16, weight: 'bold', anchor: 'start' }),
    );
    b.push(...row(44, 258, res, 'ecs'));
    // IaCのツールで比較
    b.push(inner('toolkit', 376, 146, 64));
    b.push(t(408, 232, 'IaCのツール', { size: 16, weight: 'bold' }));
    b.push(arrow('M276,90 L330,90 L330,166 L370,166'));
    b.push(arrow('M276,280 L330,280 L330,196 L370,196'));
    b.push(t(316, 186, '比較', { size: 15, anchor: 'end' }));
    // 差分（ここだけを大きく見せる）
    b.push(arrow('M446,178 L520,178', { color: GREEN }));
    b.push(
      `<rect x="528" y="104" width="148" height="150" rx="12" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="3" stroke-dasharray="7 5"/>`,
    );
    b.push(t(602, 134, '差分', { size: 20, weight: 'bold', color: GREEN }));
    b.push(inner('ecs', 566, 148, 72));
    b.push(
      `<rect x="${566 - 6}" y="${148 - 6}" width="84" height="84" rx="12" fill="none" stroke="${GREEN}" stroke-width="3"/>`,
    );
    b.push(
      t(602, 244, 'Amazon ECS', { size: 14, weight: 'bold', color: GREEN }),
    );
    // デプロイ → 実リソース
    b.push(arrow('M682,178 L736,178', { color: GREEN }));
    b.push(t(709, 166, 'デプロイ', { size: 14, weight: 'bold', color: GREEN }));
    b.push(
      '<rect x="742" y="110" width="244" height="140" rx="12" fill="#ffffff" stroke="#232F3E" stroke-width="2"/>',
    );
    b.push(inner('cloud', 742, 110, 28));
    b.push(
      t(778, 130, '実リソース', {
        size: 16,
        weight: 'bold',
        color: '#232F3E',
        anchor: 'start',
      }),
    );
    b.push(...row(764, 156, res, undefined, 'ecs'));
    out['iac-diff.svg'] = svg(
      1000,
      366,
      b,
      'IaCのツールが、コードのあるべき姿と現在の状態を比較し、その差分だけを実リソースへデプロイする',
    );
  }

  // ---------------------------------------------------------------- 2部: アップデート
  {
    // 上から古い順。cdk diagnose はスライドのカードで取り上げるので強調する
    const items = [
      ['2025-11', 'CloudFormation 早期バリデーション'],
      ['2025-11', 'CloudFormation Language Server'],
      ['2025-11', 'AWS IaC MCP Server'],
      ['2026-04', 'cdk diagnose（プレビュー）'],
      ['2026-06', 'cdk validate（プレビュー）'],
      ['2026-06', 'Terraform MCP Server GA'],
      ['2026-07', 'cdk lsp（プレビュー）'],
    ];
    const pick = 'cdk diagnose（プレビュー）';
    const b: string[] = [];
    const [step, y0, lx] = [46, 30, 104];
    b.push(
      `<line x1="${lx}" y1="${y0 - 14}" x2="${lx}" y2="${y0 + step * (items.length - 1) + 14}" stroke="${LINE}" stroke-width="3"/>`,
    );
    items.forEach(([ym, name], i) => {
      const y = y0 + i * step;
      const hot = name === pick;
      if (hot) {
        b.push(
          `<rect x="${lx + 14}" y="${y - 18}" width="330" height="36" rx="8" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2"/>`,
        );
      }
      b.push(
        t(10, y + 6, ym, {
          size: 16,
          weight: 'bold',
          color: SUB,
          anchor: 'start',
          mono: true,
        }),
      );
      b.push(
        `<circle cx="${lx}" cy="${y}" r="8" fill="${hot ? GREEN : '#ffffff'}" stroke="${GREEN}" stroke-width="3"/>`,
      );
      b.push(
        t(lx + 26, y + 6, name, {
          size: 17,
          weight: hot ? 'bold' : 'normal',
          color: hot ? GREEN : INK,
          anchor: 'start',
        }),
      );
    });
    out['ai-updates.svg'] = svg(
      460,
      y0 + step * (items.length - 1) + 30,
      b,
      'IaCのツールのアップデートを古い順に並べた年表。cdk diagnose（プレビュー）を強調している',
    );
  }

  // ---------------------------------------------------------------- 3部: 学び方
  {
    // 「AIに聞く」⇄「自分で触る（設定・操作）」のループ。手順やコマンドは書かない
    const b: string[] = [];
    b.push(...aiBadge(120, 100, 64));
    b.push(t(120, 166, 'AIに聞く', { size: 18, weight: 'bold' }));
    b.push(inner('user', 408, 68, 64));
    b.push(
      t(440, 166, '自分で触る（設定・操作）', { size: 18, weight: 'bold' }),
    );
    b.push(arrow('M162,86 L396,86', { color: GREEN, width: 3 }));
    b.push(arrow('M396,114 L162,114', { color: GREEN, width: 3 }));
    out['learning-loop.svg'] = svg(
      560,
      186,
      b,
      'AIに聞くことと、自分で設定や操作を触ることをくり返す',
    );
  }
  {
    // 作る範囲を少しずつ広げる（Lambda → ＋API Gateway → ＋DynamoDB）を小さく1行で。作った部分だけ色を付ける
    const b = [
      '<defs><filter id="gs"><feColorMatrix type="saturate" values="0"/></filter></defs>',
    ];
    b.push(
      t(200, 20, '作る範囲を少しずつ広げる', { size: 17, weight: 'bold' }),
    );
    const stages: [string[], string][] = [
      [['lambda'], 'Lambda'],
      [['apigw', 'lambda'], '＋API Gateway'],
      [['apigw', 'lambda', 'dynamodb'], '＋DynamoDB'],
    ];
    const [size, gap, step] = [30, 6, 136];
    stages.forEach(([built, name], i) => {
      const x0 = 14 + i * step;
      ['apigw', 'lambda', 'dynamodb'].forEach((key, j) => {
        const ic = inner(key, x0 + j * (size + gap), 46, size);
        b.push(
          built.includes(key)
            ? ic
            : `<g filter="url(#gs)" opacity="0.3">${ic}</g>`,
        );
      });
      b.push(t(x0 + 51, 104, name, { size: 14, weight: 'bold' }));
      if (i < stages.length - 1)
        b.push(arrow(`M${x0 + 108},61 L${x0 + step - 6},61`, { color: GREEN }));
    });
    out['learning-progress.svg'] = svg(
      400,
      116,
      b,
      'Lambdaだけを作り、API Gateway、DynamoDBと、作る範囲を少しずつ広げる',
    );
  }

  // ---------------------------------------------------------------- 1部: 特徴
  {
    const b: string[] = [];
    // マネコン（手作業）：作業者ごとにマネコンで操作するので、結果がばらつく（下の IaC と同じ並びで比べる）
    b.push(
      `<rect x="10" y="10" width="580" height="190" rx="14" fill="#ffffff" stroke="${GRAY}" stroke-width="2" stroke-dasharray="7 5"/>`,
    );
    b.push(
      t(28, 40, 'マネコン（手作業）', {
        size: 20,
        weight: 'bold',
        anchor: 'start',
      }),
    );
    ['新人', 'ベテラン'].forEach((n, i) => {
      const y = 82 + i * 74;
      b.push(inner('user', 34, y - 22, 44));
      b.push(t(92, y + 6, n, { size: 16, weight: 'bold', anchor: 'start' }));
      b.push(arrow(`M166,${y} L222,${108 + (i * 2 - 1) * 6}`));
    });
    b.push(
      ...service('console', 258, 108, 'マネコンで操作', { size: 48, fs: 16 }),
    );
    b.push(arrow('M292,108 L352,108'));
    for (let r = 0; r < 2; r++) {
      const y = 50 + r * 58;
      res.forEach(([k], j) => b.push(inner(k, 370 + j * 48, y, 38)));
    }
    b.push(
      `<rect x="414" y="104" width="46" height="46" rx="8" fill="none" stroke="${RED}" stroke-width="3"/>`,
    );
    b.push(
      t(441, 186, '結果がばらつく', { size: 17, weight: 'bold', color: RED }),
    );
    // IaC
    b.push(
      `<rect x="10" y="210" width="580" height="190" rx="14" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2"/>`,
    );
    b.push(
      t(28, 240, 'IaC', {
        size: 20,
        weight: 'bold',
        color: GREEN,
        anchor: 'start',
      }),
    );
    ['新人', 'ベテラン'].forEach((n, i) => {
      const y = 282 + i * 74;
      b.push(inner('user', 34, y - 22, 44));
      b.push(t(92, y + 6, n, { size: 16, weight: 'bold', anchor: 'start' }));
      b.push(
        arrow(`M166,${y} L222,${308 + (i * 2 - 1) * 6}`, { color: GREEN }),
      );
    });
    b.push(...service('code', 258, 308, '同じコード', { size: 48, fs: 16 }));
    b.push(arrow('M292,308 L352,308', { color: GREEN }));
    for (let r = 0; r < 2; r++) {
      const y = 250 + r * 58;
      res.forEach(([k], j) => b.push(inner(k, 370 + j * 48, y, 38)));
    }
    b.push(t(441, 392, '同じ結果', { size: 17, weight: 'bold', color: GREEN }));
    out['feature-reproducibility.svg'] = svg(
      600,
      410,
      b,
      'マネコンの手作業では作業者ごとに結果がばらつくが、IaCは同じコードから誰がやっても同じ結果になる',
    );
  }
  {
    const resourcesRow = (x: number, y: number) =>
      chain(['waf', 'elb', 'ecs'], x, y, 36, 58);
    // 左：レビューしたソースコードをデプロイ（見出しはスライド側）
    let b: string[] = [];
    b.push(...service('user', 60, 56, 'レビュー', { size: 44, fs: 15 }));
    b.push(arrow('M92,56 L166,56', { color: GREEN }));
    b.push(...service('code', 210, 56, 'ソースコード', { size: 48, fs: 15 }));
    b.push(arrow('M210,112 L210,176', { color: GREEN }));
    b.push(
      t(222, 150, 'デプロイ', {
        size: 15,
        weight: 'bold',
        color: GREEN,
        anchor: 'start',
      }),
    );
    b.push(...resourcesRow(134, 186));
    out['feature-cm-deploy.svg'] = svg(
      330,
      232,
      b,
      'レビューしたソースコードを、WAF・ALB・ECSへデプロイする',
    );

    // 右：戻すときは、前のコミットに戻して再度デプロイ
    b = [];
    const y = 60;
    b.push(inner('git', 10, y - 24, 48));
    b.push(
      `<line x1="96" y1="${y}" x2="236" y2="${y}" stroke="${INK}" stroke-width="2.5"/>`,
    );
    b.push(
      `<circle cx="96" cy="${y}" r="11" fill="#ffffff" stroke="${GREEN}" stroke-width="3"/>`,
    );
    b.push(
      `<circle cx="236" cy="${y}" r="11" fill="#ffffff" stroke="${GRAY}" stroke-width="3"/>`,
    );
    b.push(
      t(96, y + 34, '前のコミット', { size: 15, weight: 'bold', color: GREEN }),
    );
    b.push(t(236, y + 34, '今のコミット', { size: 15, color: GRAY }));
    b.push(
      arrow(`M236,${y - 16} C220,${y - 42} 112,${y - 42} 98,${y - 18}`, {
        color: GRAY,
      }),
    );
    b.push(t(166, y - 40, '戻す', { size: 15, color: SUB }));
    b.push(arrow(`M96,${y + 44} L96,204 L126,204`, { color: GREEN }));
    b.push(
      t(108, 150, '再度デプロイ', {
        size: 15,
        weight: 'bold',
        color: GREEN,
        anchor: 'start',
      }),
    );
    b.push(...resourcesRow(134, 186));
    out['feature-cm-rollback.svg'] = svg(
      330,
      232,
      b,
      '戻すときは、前のコミットに戻して、WAF・ALB・ECSへ再度デプロイする',
    );
  }
  {
    const b: string[] = [];
    // リソースの関連（左・メイン）
    b.push(
      t(8, 30, 'リソース同士の関連を追える', { size: 16, anchor: 'start' }),
    );
    res.forEach(([k, n], i) => {
      const y = 62 + i * 118;
      b.push(inner(k, 24, y, 56));
      b.push(t(94, y + 34, n, { size: 17, weight: 'bold', anchor: 'start' }));
      if (i < 2) b.push(arrow(`M52,${y + 60} L52,${y + 114}`));
    });
    // コード（右・CDK）
    b.push(arrow('M214,210 L198,210'));
    b.push(
      `<rect x="220" y="40" width="600" height="360" rx="12" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
    );
    b.push(inner('code', 234, 52, 36));
    b.push(
      t(280, 78, 'コード（AWS CDK）', {
        size: 18,
        weight: 'bold',
        anchor: 'start',
      }),
    );
    let y = 128;
    for (const [c, line] of ALB_CODE) {
      if (c === GREEN) {
        // 日本語のコメントは等幅フォントだと字形が崩れるので、本文のフォントで描く（字下げぶんだけずらす）
        b.push(
          t(238 + indentOf(line) * 10.2, y, line.trim(), {
            size: 17,
            color: c,
            anchor: 'start',
          }),
        );
      } else if (line) {
        b.push(
          t(238, y, line.replaceAll(' ', '&#160;'), {
            size: 17,
            color: c,
            anchor: 'start',
            mono: true,
          }),
        );
      }
      y += 25.5;
    }
    out['feature-structure.svg'] = svg(
      830,
      410,
      b,
      'WAF・ALB・ECSの関連が分かる構成と、ALBを定義したAWS CDKのコード。あえてHTTPを許可する設定に、その意図をコメントで残している',
    );
  }
  {
    // 右：同じコードのまま、別の環境にもデプロイ（見出しはスライド側）
    let b: string[] = [];
    b.push(...service('code', 40, 136, '同じコード', { size: 48, fs: 14 }));
    ['開発環境', '本番環境'].forEach((env, i) => {
      const y = 34 + i * 112;
      b.push(
        `<rect x="112" y="${y}" width="210" height="84" rx="12" fill="#ffffff" stroke="#232F3E" stroke-width="2"/>`,
      );
      b.push(inner('cloud', 112, y, 24));
      b.push(
        t(144, y + 18, env, {
          size: 14,
          weight: 'bold',
          color: '#232F3E',
          anchor: 'start',
        }),
      );
      b.push(...chain(['waf', 'elb', 'ecs'], 140, y + 38));
      b.push(arrow(`M68,136 L86,136 L104,${y + 50}`, { color: GREEN }));
    });
    out['feature-reuse-envs.svg'] = svg(
      330,
      240,
      b,
      '同じコードのまま、WAF・ALB・ECSの構成を開発環境と本番環境にデプロイする',
    );

    // 左：共通する部分を切り出して、他の構成に組み込む（スライドのリード「インフラの共通部分を切り出して再利用できる」の図）
    b = [];
    b.push(
      `<rect x="90" y="6" width="150" height="88" rx="12" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2"/>`,
    );
    b.push(
      t(165, 30, '共通する部分', { size: 15, weight: 'bold', color: GREEN }),
    );
    b.push(...chain(['elb', 'ecs'], 119, 46, 36, 56));
    b.push(arrow('M165,98 L165,128', { color: GREEN }));
    b.push(
      t(177, 118, '組み込む', {
        size: 15,
        weight: 'bold',
        color: GREEN,
        anchor: 'start',
      }),
    );
    b.push(
      `<rect x="14" y="134" width="302" height="106" rx="12" fill="#ffffff" stroke="${LINE}" stroke-width="2"/>`,
    );
    b.push(
      t(30, 158, '他の構成', { size: 15, weight: 'bold', anchor: 'start' }),
    );
    b.push(
      `<rect x="28" y="168" width="132" height="60" rx="10" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2" stroke-dasharray="7 5"/>`,
    );
    b.push(...chain(['elb', 'ecs'], 42, 180, 36, 58));
    b.push(arrow('M160,198 L204,198'));
    b.push(inner('dynamodb', 212, 176, 40));
    b.push(t(232, 232, 'Amazon DynamoDB', { size: 11, color: SUB }));
    out['feature-reuse-parts.svg'] = svg(
      330,
      248,
      b,
      'ALBとECSの共通する部分を切り出して、DynamoDBを使う他の構成に組み込む',
    );
  }

  // ---------------------------------------------------------------- 2部: AI に向いている理由
  {
    const b = cdkCode(10, 20, 470, ALB_CODE);
    b.push(...aiBadge(620, 140));
    b.push(arrow('M488,140 L584,140', { color: GREEN }));
    b.push(t(536, 126, 'コードを渡す', { size: 15, color: GREEN }));
    b.push(
      t(620, 200, '現状と意図が伝わる', {
        size: 15,
        weight: 'bold',
        color: GREEN,
      }),
    );
    // AWS を読みに行く（時間とトークンがかかる）
    b.push(inner('cloud', 836, 116, 48));
    b.push(t(860, 188, 'AWSのリソース', { size: 15, weight: 'bold' }));
    b.push(arrow('M656,140 L826,140', { color: GRAY, dash: '7 5' }));
    b.push(
      `<circle cx="741" cy="140" r="16" fill="#ffffff" stroke="${RED}" stroke-width="3"/>`,
    );
    b.push(
      `<path d="M734,133 L748,147 M748,133 L734,147" stroke="${RED}" stroke-width="3" stroke-linecap="round"/>`,
    );
    b.push(t(741, 98, 'MCPやCLIでAWSを読み取ると', { size: 14, color: SUB }));
    b.push(t(741, 118, '時間もトークンもかかる', { size: 14, color: SUB }));
    out['ai-context.svg'] = svg(
      940,
      300,
      b,
      'CDKのコードにはアーキテクチャ全体と設定の意図が書いてあり、AIにはコードを渡せば伝わる。AWSをMCPやCLIで読みに行くと時間もトークンもかかる',
    );
  }
  {
    const b: string[] = [];
    // 自己フィードバックのハーネス
    b.push(
      `<rect x="10" y="20" width="420" height="270" rx="16" fill="none" stroke="${GREEN}" stroke-width="2" stroke-dasharray="8 6"/>`,
    );
    b.push(
      t(30, 48, '自己フィードバックするハーネス', {
        size: 16,
        weight: 'bold',
        color: GREEN,
        anchor: 'start',
      }),
    );
    b.push(...aiBadge(70, 130));
    b.push(arrow('M102,130 L164,130'));
    b.push(t(133, 116, '実装', { size: 15 }));
    b.push(inner('code', 170, 102, 56));
    b.push(t(198, 186, 'コード', { size: 16, weight: 'bold' }));
    b.push(arrow('M232,130 L294,130'));
    b.push(inner('toolkit', 300, 102, 56));
    b.push(t(328, 186, '検証', { size: 16, weight: 'bold' }));
    b.push(t(328, 208, 'lint・validateなど', { size: 13, color: SUB }));
    // エラーを返して AI が直す
    b.push(arrow('M328,222 L328,256 L70,256 L70,166', { color: RED }));
    b.push(
      t(199, 246, 'エラー → AIが自分で直す', {
        size: 15,
        weight: 'bold',
        color: RED,
      }),
    );
    // 通ったら、人間が差分を見る
    b.push(arrow('M362,130 L582,130'));
    b.push(t(472, 116, '検証を通過', { size: 15 }));
    b.push(inner('user', 590, 102, 56));
    b.push(t(618, 186, '人間', { size: 16, weight: 'bold' }));
    b.push(t(618, 208, 'デプロイ前に差分を見る', { size: 13, color: SUB }));
    b.push(arrow('M652,130 L766,130', { color: GREEN }));
    b.push(t(709, 116, 'デプロイ', { size: 15, weight: 'bold', color: GREEN }));
    b.push(inner('cloud', 774, 102, 56));
    b.push(t(802, 186, 'AWS', { size: 16, weight: 'bold' }));
    b.push(t(802, 208, '壊れたものが届かない', { size: 13, color: SUB }));
    out['ai-validation.svg'] = svg(
      880,
      300,
      b,
      'AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする',
    );
  }
  {
    const b: string[] = [];
    // 危うい行の下地（コードより先に描いて、文字の下に敷く）
    b.push(
      `<rect x="22" y="${20 + 80 + 5 * 19.5 - 15}" width="526" height="22" rx="4" fill="${RED_BG}"/>`,
    );
    b.push(...cdkCode(10, 20, 550, SG_CODE));
    const hl = 20 + 80 + 5 * 19.5 - 4;
    // スキャン結果の吹き出し
    b.push(
      `<path d="M560,${hl} L592,${hl - 14} L592,${hl + 14} z" fill="${RED_BG}" stroke="${RED}" stroke-width="2" stroke-linejoin="round"/>`,
    );
    b.push(
      `<rect x="590" y="${hl - 40}" width="340" height="80" rx="14" fill="${RED_BG}" stroke="${RED}" stroke-width="2"/>`,
    );
    b.push(
      `<rect x="588" y="${hl - 12}" width="6" height="24" fill="${RED_BG}"/>`,
    );
    b.push(
      t(760, hl - 6, '全世界からのSSHを許可しています', {
        size: 18,
        weight: 'bold',
        color: RED,
      }),
    );
    b.push(
      t(760, hl + 22, '受信元 0.0.0.0/0 → TCP 22', {
        size: 13,
        color: RED,
        mono: true,
      }),
    );
    // 同じコードを、2つのタイミングでスキャンする
    for (const [x, when, how, tool] of [
      [60, '実装中', 'cdk synth のときにルールでチェック', 'cdk-nag'],
      [
        320,
        'セキュリティスキャン',
        'リポジトリ全体をまとめてスキャン',
        'Continuumコードレビューなど',
      ],
    ] as const) {
      b.push(arrow(`M${x + 110},244 L${x + 110},220`, { color: GREEN }));
      b.push(
        `<rect x="${x}" y="248" width="220" height="70" rx="12" fill="${GREEN_BG}" stroke="${GREEN}" stroke-width="2"/>`,
      );
      b.push(t(x + 110, 271, when, { size: 16, weight: 'bold', color: GREEN }));
      b.push(t(x + 110, 290, how, { size: 12, color: INK }));
      b.push(t(x + 110, 308, tool, { size: 12, color: SUB }));
    }
    out['ai-safety.svg'] = svg(
      940,
      324,
      b,
      'セキュリティグループで22番ポートを0.0.0.0/0に開けているCDKのコードを、実装中はcdk-nag、セキュリティスキャンではContinuumコードレビューなどでスキャンし、全世界からのSSHを許可していると指摘される',
    );
  }
  {
    const b: string[] = [];
    b.push(...aiBadge(50, 70));
    b.push(arrow('M82,70 L170,70'));
    b.push(t(126, 56, '実装', { size: 15 }));
    b.push(inner('code', 176, 42, 56));
    b.push(t(204, 126, 'コード', { size: 16, weight: 'bold' }));
    b.push(arrow('M238,70 L326,70'));
    b.push(inner('git', 332, 42, 56));
    b.push(t(360, 126, 'リポジトリ', { size: 16, weight: 'bold' }));
    b.push(arrow('M394,70 L482,70'));
    b.push(inner('toolkit', 488, 42, 56));
    b.push(t(516, 126, 'CI/CD', { size: 16, weight: 'bold' }));
    b.push(arrow('M550,70 L670,70', { color: GREEN }));
    b.push(t(610, 56, 'デプロイ', { size: 15, weight: 'bold', color: GREEN }));
    b.push(inner('cloud', 676, 42, 56));
    b.push(t(704, 126, 'AWS', { size: 16, weight: 'bold' }));
    // AI から AWS へ：読み取り権限は渡す（緑・実線）
    b.push(arrow('M56,102 L56,168 L698,168 L698,142', { color: GREEN }));
    b.push(
      `<circle cx="377" cy="168" r="17" fill="#ffffff" stroke="${GREEN}" stroke-width="3"/>`,
    );
    b.push(
      `<path d="M369,168 L375,175 L386,161" fill="none" stroke="${GREEN}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>`,
    );
    b.push(
      t(377, 206, '読み取り権限は渡す', {
        size: 16,
        weight: 'bold',
        color: GREEN,
      }),
    );
    // 書き込み・デプロイ権限は渡さない（赤・点線）
    b.push(
      arrow('M44,102 L44,236 L710,236 L710,142', { color: RED, dash: '7 5' }),
    );
    b.push(
      `<circle cx="377" cy="236" r="17" fill="#ffffff" stroke="${RED}" stroke-width="3"/>`,
    );
    b.push(
      `<path d="M369,228 L385,244 M385,228 L369,244" stroke="${RED}" stroke-width="3" stroke-linecap="round"/>`,
    );
    b.push(
      t(377, 274, '書き込み・デプロイ権限は渡さない', {
        size: 16,
        weight: 'bold',
        color: RED,
      }),
    );
    out['ai-permission.svg'] = svg(
      760,
      284,
      b,
      'AIはコードを実装するだけで、デプロイはCI/CDが行う。AIにはAWSの読み取り権限は渡すが、書き込み・デプロイ権限は渡さない',
    );
  }

  return out;
}

export default defineDiagrams({
  note: 'AWS Architecture Icons 2026-07-31 版（Icon-package_07312026）',
  icons: {
    waf: 'Arch_AWS-WAF_64.svg',
    elb: 'Arch_Elastic-Load-Balancing_64.svg',
    ecs: 'Arch_Amazon-Elastic-Container-Service_64.svg',
    console: 'Arch_AWS-Management-Console_64.svg',
    lambda: 'Arch_AWS-Lambda_64.svg',
    apigw: 'Arch_Amazon-API-Gateway_64.svg',
    dynamodb: 'Arch_Amazon-DynamoDB_64.svg',
    cloud: 'AWS-Cloud-logo_32.svg',
    office: 'Res_Office-building_48_Light.svg',
    user: 'Res_User_48_Light.svg',
    code: 'Res_Source-Code_48_Light.svg',
    toolkit: 'Res_Toolkit_48_Light.svg',
    git: 'Res_Git-Repository_48_Light.svg',
  },
  build: diagrams,
});
