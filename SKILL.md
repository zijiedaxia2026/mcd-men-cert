---
name: mcd-men-cert
title: 麦门认证证书生成器
description: 读取用户麦当劳订单史与积分（麦当劳 MCP 只读接口），生成一张可分享的「麦门认证证书」+ 一页式生涯报告。当用户想看自己的麦当劳消费画像、段位、荣誉称号，或想用麦当劳 MCP 做个能晒的趣味作品时使用。
type: tool
---

# 麦门认证证书生成器

## 触发场景
- 用户说「生成我的麦门认证证书 / 麦门段位 / 麦当劳消费报告」
- 用户想用麦当劳 MCP 做一个可分享的趣味作品

## 前置条件
- 已启用「麦当劳 MCP」连接器（Token 仅存于连接器配置，不落库）
- 仅使用只读工具：`order-list`、`query-my-account`、`query-my-coupons`

## 执行流程
1. 调用 `order-list` 拉取历史订单（按页拉全，记录 date / amount / items）。
2. （可选）调用 `query-my-account` 获取积分、会员等级。
3. 将结果整理为如下 JSON：
   ```json
   {"user_id":"138****1024","points":12800,
    "orders":[{"date":"2026-01-02","amount":38.5,"items":[{"name":"薯条","qty":1}]}]}
   ```
4. 调用本地脚本 `generate_certificate.py`：
   - 把上面 JSON 写入 `data.json`
   - 执行 `python generate_certificate.py data.json > cert.html`
5. 把 `cert.html` 路径返回给用户，提示「截图即可分享」。

## 注意事项
- 全程只读，绝不调用下单 / 支付类工具。
- 不把 Token、手机号等真实凭证写入任何文件或回复。
- 输出文案强调「仅供娱乐，数据以麦当劳官方为准」。
