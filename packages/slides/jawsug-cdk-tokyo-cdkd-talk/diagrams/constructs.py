"""コンストラクトの説明の図を SVG で組む。本人の旧資料「AWS CDKの推しポイントN選」の図を作り直したもの。

  AWS_ICONS=<アイコン置き場> python3 diagrams/constructs.py

アイコンは AWS Architecture Icons 2026-07-31 版。tasks/speaking/diagram-style.md に合わせる。
コードの色はスライドのコード表示（dracula）にそろえる。
"""
import os
import re

from deploy_flow import GREEN, GREEN_BG, ICON, INK, LINE, MONO, OUT, SUB, arrow, icon, text

ICON.update({
    "cdk": "Arch_AWS-Cloud-Development-Kit_64.svg",
    "s3a": "Arch_Amazon-Simple-Storage-Service_64.svg",
    "kms": "Arch_AWS-Key-Management-Service_64.svg",
    "alb": "Arch_Elastic-Load-Balancing_64.svg",
    "ecs": "Arch_Amazon-Elastic-Container-Service_64.svg",
    "fargate": "Arch_AWS-Fargate_64.svg",
    "lambda": "Arch_AWS-Lambda_64.svg",
    "policy": "Res_AWS-Identity-Access-Management_Permissions_48.svg",
    "logs": "Res_Amazon-CloudWatch_Logs_48.svg",
})

CODE_BG, CODE_FG = "#282a36", "#f8f8f2"
TS_KEYWORD = r"\b(?:new|const|this|export|class|extends|constructor|super)\b"


def escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tokens(line, lang):
    """1 行を (文字, 色) に分ける。"""
    if line.lstrip().startswith("//"):
        return [(line, "#6272a4")]
    if lang == "yaml":
        m = re.match(r"(\s*)([\w]+)(:)(.*)$", line)
        if not m:
            return [(line, CODE_FG)]
        return [(m.group(1), CODE_FG), (m.group(2), "#8be9fd"), (m.group(3), CODE_FG), (m.group(4), "#f1fa8c")]
    out = []
    for part in re.split(rf"('[^']*'|\"[^\"]*\"|{TS_KEYWORD}|\b[A-Z]\w*\b)", line):
        if not part:
            continue
        if part[0] in "'\"":
            color = "#f1fa8c"
        elif re.fullmatch(TS_KEYWORD, part):
            color = "#ff79c6"
        elif part[0].isupper():
            color = "#50fa7b"
        else:
            color = CODE_FG
        out.append((part, color))
    return out


def code(x, y, w, lines, lang="ts", size=13, step=19, pad=10):
    h = step * len(lines) + pad * 2
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{CODE_BG}"/>']
    for i, line in enumerate(lines):
        spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in tokens(line, lang))
        out.append(f'<text x="{x + 12}" y="{y + pad + step * i + size}" font-size="{size}" font-family="{MONO}" xml:space="preserve">{spans}</text>')
    return "".join(out)


def line_y(y, i, step=19, pad=10, size=13):
    """code() の i 行目の文字の高さの中心。"""
    return y + pad + step * i + size * 0.65


def frame(x, y, w, h, name, title, sub=None):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
           icon(name, x + 28, y + 12, 28),
           text(x + 50, y + (24 if sub else 31), title, 14, INK, 700, "start")]
    if sub:
        out.append(text(x + 50, y + 40, sub, 12, SUB, None, "start", MONO))
    return "".join(out)


def green_line(d, head=True):
    m = ' marker-end="url(#mGreen)"' if head else ""
    return f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round"{m}/>'


def write(name, w, h, parts):
    defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            f'<marker id="mGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker>'
            f'<marker id="mGreenStart" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
            f'<path d="M10,0 L0,5 L10,10 z" fill="{GREEN}"/></marker></defs>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(parts) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


# ---------- 概要と L1 / L2 / L3 ----------
p = []
p.append(f'<path d="M62,44 V296" fill="none" stroke="{GREEN}" stroke-width="3" marker-start="url(#mGreenStart)" marker-end="url(#mGreen)"/>')
p += [text(38, 52, "小", 13, INK, 700), text(38, 174, "抽象度", 13, INK, 700), text(38, 298, "大", 13, INK, 700)]
p.append(f'<rect x="110" y="8" width="875" height="324" rx="14" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
p.append(icon("stack", 138, 18, 28))
p.append(text(160, 38, "CloudFormation Stack", 14, INK, 700, "start"))
rows = [
    (54, "L1 Construct", "Bucket", [("s3a", "CfnBucket")]),
    (146, "L2 Construct", "Bucket", [("s3a", None), ("kms", None)]),
    (238, "L3 Construct", "ApplicationLoadBalancedFargateService", [("alb", None), ("ecs", None), ("fargate", None)]),
]
for y, name, title, items in rows:
    p.append(f'<rect x="130" y="{y + 22}" width="130" height="38" rx="10" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>')
    p.append(text(195, y + 46, name, 13, GREEN, 700))
    p.append(arrow(f"M260,{y + 41} H340"))
    p.append(f'<rect x="340" y="{y}" width="625" height="84" rx="10" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    p.append(text(358, y + 22, title, 12, SUB, None, "start", MONO))
    x = 380
    for icon_name, label in items:
        p.append(icon(icon_name, x, y + 32, 42))
        if label:
            p.append(text(x + 34, y + 58, label, 13, INK, 700, "start"))
        x += 60
    if name.startswith("L3"):
        p.append(text(x - 14, y + 58, "…", 16, SUB))
write("construct-levels", 1000, 340, p)

# ---------- L1 ----------
YAML_S3 = ['BucketName: "akikii-sample-bucket"', "BucketEncryption:", "  ServerSideEncryptionConfiguration:", "  -", "    ServerSideEncryptionByDefault:", "      SSEAlgorithm: AES256"]
TS_L1 = ["new CfnBucket(this, 'CfnBucket', {", "  bucketName: 'akikii-sample-bucket',", "  bucketEncryption: {", "    serverSideEncryptionConfiguration: [", "      {", "        serverSideEncryptionByDefault: {", "          sseAlgorithm: 'AES256',", "        },", "      },", "    ],", "  },", "});"]
p = [frame(10, 8, 410, 330, "template", "CloudFormation Template"),
     icon("s3a", 42, 60, 30), text(66, 81, "S3 Bucket", 13, INK, 700, "start"),
     code(26, 106, 378, YAML_S3),
     frame(570, 8, 420, 330, "cdk", "CDK L1 Construct", "aws_s3.CfnBucket"),
     code(586, 62, 388, TS_L1)]
for left, right in ((0, 1), (1, 2), (2, 3), (4, 5), (5, 6)):
    p.append(green_line(f"M404,{line_y(106, left)} L586,{line_y(62, right)}"))
p.append(text(495, 88, "1:1で対応", 14, GREEN, 700))
write("construct-l1", 1000, 346, p)

# ---------- L2 ----------
YAML_KMS = ['BucketName: "akikii-sample-bucket"', "BucketEncryption:", "  ServerSideEncryptionConfiguration:", "  -", "    ServerSideEncryptionByDefault:", "      KMSMasterKeyID: !Ref KmsKey", '      SSEAlgorithm: "aws:kms"']
TS_L2 = ["new Bucket(this, 'Bucket', {", "  bucketName: 'akikii-sample-bucket',", "  encryption: BucketEncryption.KMS,", "});"]
CY, YY = 92, 92
p = [frame(10, 8, 400, 330, "cdk", "CDK L2 Construct", "aws_s3.Bucket"),
     code(26, CY, 368, TS_L2),
     frame(570, 8, 420, 330, "template", "CloudFormation Template"),
     icon("s3a", 602, 54, 28), text(626, 74, "S3 Bucket", 13, INK, 700, "start"),
     code(600, YY, 374, YAML_KMS),
     icon("kms", 626, 272, 40), text(654, 298, "KMS Key", 13, INK, 700, "start")]
y1, y2 = line_y(CY, 1), line_y(CY, 2)
ty1 = line_y(YY, 0)
top, bottom = line_y(YY, 1) - 8, line_y(YY, 6) + 8
mid = (top + bottom) / 2
p.append(green_line(f"M394,{y1} H500 L598,{ty1}"))
p.append(text(470, y1 - 8, "対応", 14, GREEN, 700))
p.append(green_line(f"M394,{y2} H500 L584,{mid}"))
p.append(text(480, y2 + 30, "抽象化", 14, GREEN, 700))
p.append(green_line(f"M596,{top} H588 V{bottom} H596", head=False))
p.append(green_line(f"M300,{CY + 96} V292 H606"))
p += [text(445, 276, "自動的に作成", 13, GREEN, 700), text(445, 310, "（指定しない場合）", 12, GREEN)]
write("construct-l2", 1000, 346, p)

# ---------- L2 の例: VPC と Lambda ----------
VPC = ["const vpc = new ec2.Vpc(this, 'SampleVpc', {", "  ipAddresses: ec2.IpAddresses.cidr('10.0.0.0/16'),", "  vpcName: 'sample-vpc',", "  subnetConfiguration: [", "    {", "      cidrMask: 24,", "      name: \"public\",", "      subnetType: ec2.SubnetType.PUBLIC,", "    },", "    {", "      cidrMask: 24,", "      name: \"private\",", "      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,", "    },", "  ]", "});"]
LAMBDA = ["new lambda.Function(this, 'SampleFunction', {", "  runtime: lambda.Runtime.NODEJS_22_X,", "  code: lambda.Code.fromAsset('lambda'),", "  handler: 'hello.handler',", "  // role: lambdaRole,", "  // logGroup: lambdaLogGroup,", "});"]
p = [text(10, 22, "直感的にわかりやすいプロパティに抽象化されている", 15, INK, 700, "start"),
     text(10, 44, "例：VPCのL2 Construct", 13, SUB, None, "start"),
     icon("cdk", 22, 56, 24), text(40, 73, "CDKソースコード（15行）", 13, INK, 700, "start"),
     code(10, 88, 372, VPC, size=11, step=15, pad=8)]
p.append(arrow("M382,216 H416"))
p.append(icon("template", 412, 58, 22))
p.append(text(426, 66, "CFnテンプレート", 11, INK, 700, "start"))
p.append(text(426, 80, "（266行）", 11, INK, 700, "start"))
p.append(f'<rect x="418" y="88" width="64" height="256" rx="6" fill="{CODE_BG}"/>')
for i in range(40):
    y = 95 + i * 6.1
    width = 16 + ((i * 17) % 34)
    color = ("#8be9fd", "#f1fa8c", "#f8f8f2")[i % 3]
    p.append(f'<line x1="{424 + (i % 4) * 3}" y1="{y}" x2="{424 + (i % 4) * 3 + width}" y2="{y}" stroke="{color}" stroke-width="1.6" opacity="0.8"/>')
X = 545
p += [text(X, 22, "関連するリソースを解釈して作成してくれる", 15, INK, 700, "start"),
      text(X, 44, "例：Lambda関数のL2 Construct", 13, SUB, None, "start"),
      icon("cdk", X + 12, 56, 24), text(X + 30, 73, "aws_lambda.Function", 12, SUB, None, "start", MONO),
      code(X, 88, 455, LAMBDA, size=12, step=17, pad=8)]
p.append(icon("lambda", X + 28, 268, 40))
p.append(text(X + 28, 326, "Lambda関数", 12, INK, 700))
p.append(arrow(f"M{X + 50},288 H{X + 78}"))
p.append(f'<rect x="{X + 80}" y="238" width="375" height="122" rx="10" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
p.append(text(X + 92, 258, "デフォルトでは自動的に作成される", 13, GREEN, 700, "start"))
p += [icon("role", X + 132, 266, 30), text(X + 132, 312, "Lambda実行ロール", 11, INK, 700)]
p += [icon("policy", X + 260, 266, 30), text(X + 260, 312, "IAM Policy", 11, INK, 700),
      text(X + 260, 325, "CreateLogGroup", 9, SUB), text(X + 260, 336, "CreateLogStream", 9, SUB), text(X + 260, 347, "PutLogEvents", 9, SUB)]
p += [icon("logs", X + 390, 266, 30), text(X + 390, 312, "CloudWatch Logs", 11, INK, 700)]
write("construct-l2-examples", 1010, 366, p)

# ---------- 自作 Construct ----------
MY = ["export class MyConstruct extends Construct {", "  constructor(scope: Construct, id: string) {", "    super(scope, id);", "", "    new Bucket(this, 'Bucket');", "    new NodejsFunction(this, 'Function', {", "      entry: path.join(__dirname, 'lambda', 'index.ts'),", "      handler: 'handler',", "      runtime: Runtime.NODEJS_22_X,", "    });", "  }", "}"]
CODE_Y = 60
p = [frame(10, 8, 590, 310, "cdk", "CDK 自作 Construct"),
     code(26, CODE_Y, 558, MY),
     frame(720, 8, 270, 310, "template", "CFn Template"),
     icon("s3a", 766, 96, 44), text(798, 124, "S3バケット", 14, INK, 700, "start"),
     icon("lambda", 766, 196, 44), text(798, 224, "Lambda関数", 14, INK, 700, "start")]
by = line_y(CODE_Y, 4)
p.append(green_line(f"M300,{by} H660 L742,118"))
f_top, f_bottom = line_y(CODE_Y, 5) - 8, line_y(CODE_Y, 9) + 8
p.append(green_line(f"M574,{f_top} H592 V{f_bottom} H574", head=False))
p.append(green_line(f"M592,{(f_top + f_bottom) / 2} H660 L742,218"))
write("construct-custom", 1000, 326, p)
