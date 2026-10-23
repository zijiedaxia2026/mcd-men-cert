#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦门认证证书生成器 (mcd-men-cert)
=================================
把麦当劳 MCP 的只读接口数据（order-list / query-my-account 等）变成一张
自包含、可直接截图分享的「麦门认证证书」+ 一页式生涯报告。

用法：
    python generate_certificate.py data.json > cert.html
    python generate_certificate.py            # 用内置示例数据生成 sample.html

输入 JSON 结构（字段均可缺省，缺失时用占位值，不影响出图）：
{
  "user_id": "138****1234",
  "orders": [
    {"date":"2026-01-02", "amount": 38.5, "items":[{"name":"薯条","qty":1},{"name":"麦辣鸡腿堡","qty":2}]}
  ],
  "points": 12800
}
"""
import json
import sys
import html
import datetime
import hashlib

# 段位阈值（按累计订单数）
def rank_title(total_orders: int) -> str:
    if total_orders >= 200:
        return "钻石麦门 · 传说信徒"
    if total_orders >= 100:
        return "铂金麦门 · 资深门徒"
    if total_orders >= 50:
        return "黄金麦门 · 认证弟子"
    if total_orders >= 20:
        return "白银麦门 · 入门信徒"
    return "青铜麦门 · 见习生"

def nickname(top_item: str) -> str:
    table = {
        "薯条": "薯条护卫长",
        "麦辣鸡腿堡": "辣堡品鉴官",
        "巨无霸": "巨无霸主教",
        "麦旋风": "旋风甜心",
        "麦辣鸡翅": "鸡翅指挥官",
        "可乐": "快乐水大使",
        "板烧鸡腿堡": "板烧宗师",
        "派": "派の守护",
    }
    return table.get(top_item, f"首席{top_item}鉴赏家")

def analyze(data: dict) -> dict:
    orders = data.get("orders", []) or []
    total = len(orders)
    spent = round(sum(float(o.get("amount", 0) or 0) for o in orders), 1)
    avg = round(spent / total, 1) if total else 0.0

    cat = {}
    for o in orders:
        for it in o.get("items", []) or []:
            name = it.get("name", "未知单品")
            cat[name] = cat.get(name, 0) + int(it.get("qty", 1) or 1)
    top3 = sorted(cat.items(), key=lambda x: -x[1])[:3]
    top_item = top3[0][0] if top3 else "麦门秘宝"
    top_str = "、".join(f"{n}×{c}" for n, c in top3) if top3 else "暂无记录"

    uid = str(data.get("user_id", "anonymous"))
    cert_no = "MC-" + hashlib.md5(uid.encode("utf-8")).hexdigest()[:8].upper()
    today = datetime.date.today().isoformat()

    return {
        "user_id": uid,
        "total": total,
        "spent": spent,
        "avg": avg,
        "top_item": top_item,
        "top_str": top_str,
        "points": int(data.get("points", 0) or 0),
        "title": rank_title(total),
        "nick": nickname(top_item),
        "cert_no": cert_no,
        "date": today,
    }

CARD = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>麦门认证证书</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#1a1206;display:flex;justify-content:center;align-items:center;min-height:100vh;
        font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;padding:24px}}
  .cert{{width:680px;max-width:100%;background:linear-gradient(160deg,#fff7e6,#ffe8b0);
        border:3px solid #c9962b;border-radius:22px;padding:42px 38px;position:relative;
        box-shadow:0 24px 60px rgba(0,0,0,.45)}}
  .seal{{position:absolute;right:34px;top:34px;width:96px;height:96px;border-radius:50%;
        border:3px solid #c0392b;color:#c0392b;display:flex;flex-direction:column;
        align-items:center;justify-content:center;transform:rotate(-12deg);font-weight:800;
        font-size:13px;text-align:center;line-height:1.3;opacity:.92}}
  .brand{{text-align:center;color:#a8761b;letter-spacing:6px;font-size:14px;font-weight:700}}
  h1{{text-align:center;color:#7a4d0a;font-size:30px;margin:6px 0 2px;letter-spacing:2px}}
  .sub{{text-align:center;color:#9b7320;font-size:13px;margin-bottom:22px}}
  .line{{height:2px;background:linear-gradient(90deg,transparent,#c9962b,transparent);margin:14px 0}}
  .row{{display:flex;justify-content:space-between;padding:9px 4px;border-bottom:1px dashed #e3c478;font-size:15px}}
  .row .k{{color:#8a6516}} .row .v{{color:#5a3d08;font-weight:700}}
  .title-badge{{text-align:center;margin:22px 0 8px;font-size:24px;font-weight:800;color:#b8860b}}
  .nick{{text-align:center;color:#7a4d0a;font-size:16px;margin-bottom:6px}}
  .foot{{display:flex;justify-content:space-between;margin-top:22px;color:#8a6516;font-size:12px}}
  .qr-hint{{text-align:center;color:#a8761b;font-size:12px;margin-top:10px}}
</style></head>
<body><div class="cert">
  <div class="seal">麦门<br>认证<br>MAIMEN<br>CERT</div>
  <div class="brand">M A I M E N · C E R T I F I C A T I O N</div>
  <h1>麦 门 认 证 证 书</h1>
  <div class="sub">Certificate of McDonald's Devotion · 1024 程序员节限定</div>
  <div class="line"></div>
  <div class="row"><span class="k">持证人</span><span class="v">{user_id}</span></div>
  <div class="row"><span class="k">累计订单</span><span class="v">{total} 单</span></div>
  <div class="row"><span class="k">累计花费</span><span class="v">¥{spent}</span></div>
  <div class="row"><span class="k">平均客单</span><span class="v">¥{avg}</span></div>
  <div class="row"><span class="k">最爱单品</span><span class="v">{top_str}</span></div>
  <div class="row"><span class="k">剩余积分</span><span class="v">{points}</span></div>
  <div class="title-badge">{title}</div>
  <div class="nick">荣誉称号：{nick}</div>
  <div class="foot"><span>认证编号：{cert_no}</span><span>签发日期：{date}</span></div>
  <div class="qr-hint">由 WorkBuddy × 麦当劳 MCP 自动生成 · 扫码晒出你的麦门身份</div>
</div></body></html>"""

def render(s: dict) -> str:
    return CARD.format(**s)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "user_id": "138****1024",
            "points": 12800,
            "orders": [
                {"date": "2026-01-02", "amount": 38.5, "items": [{"name": "薯条", "qty": 1}, {"name": "麦辣鸡腿堡", "qty": 2}]},
                {"date": "2026-02-14", "amount": 52.0, "items": [{"name": "巨无霸", "qty": 1}, {"name": "薯条", "qty": 2}, {"name": "可乐", "qty": 1}]},
                {"date": "2026-03-08", "amount": 29.0, "items": [{"name": "麦辣鸡腿堡", "qty": 1}, {"name": "薯条", "qty": 1}]},
                {"date": "2026-05-20", "amount": 66.0, "items": [{"name": "巨无霸", "qty": 2}, {"name": "麦旋风", "qty": 1}]},
                {"date": "2026-07-01", "amount": 41.5, "items": [{"name": "板烧鸡腿堡", "qty": 1}, {"name": "薯条", "qty": 1}, {"name": "可乐", "qty": 1}]},
                {"date": "2026-09-09", "amount": 88.0, "items": [{"name": "麦辣鸡翅", "qty": 3}, {"name": "薯条", "qty": 2}]},
            ],
        }
    s = analyze(data)
    out = render(s)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

if __name__ == "__main__":
    main()
