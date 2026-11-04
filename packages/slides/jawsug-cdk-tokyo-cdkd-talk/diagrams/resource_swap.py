"""図の AWS リソースの組を、AWS WAF / ALB / Amazon ECS から API Gateway / Lambda / DynamoDB に置き換える。

iac-diff.svg（初心者支部で登壇したスライドから持ってきた図）の部品を使う図は、書き出す前にこれを通す（2026-11-04 本人）。
"""
import os
import re

ICONS = os.environ["AWS_ICONS"].rstrip("/") + "/"
NEW = {
    "waf": ("Arch_Amazon-API-Gateway_64.svg", "API Gateway"),
    "elb": ("Arch_AWS-Lambda_64.svg", "Lambda"),
    "ecs": ("Arch_Amazon-DynamoDB_64.svg", "DynamoDB"),
}
OLD_LABEL = {"waf": "AWS WAF", "elb": "ALB", "ecs": "Amazon ECS"}
_n = [0]


def _icon(name, x, y, size):
    _n[0] += 1
    prefix = f"rs{_n[0]}-"
    s = open(ICONS + name).read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


ICON_RE = re.compile(r'<svg x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="[\d.]+" viewBox="0 0 80 80">'
                     r'<g id="(waf|elb|ecs)\d+-Icon-Architecture/64/Arch_[^"]+".*?</svg>', re.S)


def swap(svg):
    svg = ICON_RE.sub(lambda m: _icon(NEW[m.group(4)][0], m.group(1), m.group(2), m.group(3)), svg)
    for key, old in OLD_LABEL.items():
        svg = svg.replace(f">{old}<", f">{NEW[key][1]}<")
    return svg
