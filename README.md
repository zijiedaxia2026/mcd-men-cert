# 麦门认证 · mcd-men-cert

> 把你的麦当劳订单史，变成一张能晒的「麦门认证证书」+ 一页式生涯报告。
> 基于 **麦当劳 MCP** 只读接口自动生成，由 **WorkBuddy** 驱动。

[![M-CODE](https://img.shields.io/badge/M--CODE-1024程序员节-orange)](https://github.com/M-China/mcd-developer-innovation-challenge)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ 它能做什么

- 🪪 **一键出证**：读取你的累计订单、花费、最爱单品、剩余积分，自动生成「麦门认证证书」（含段位、荣誉称号、认证编号）。
- 📊 **生涯报告**：一页式统计你的麦门消费画像。
- 🖼️ **可分享**：证书是**自包含 HTML**，截图即发朋友圈 / 小红书 / 群聊，天然带传播——这也是它最容易涨 Star 的原因。
- 🔒 **只读合规**：只用麦当劳 MCP 的只读接口，不碰下单、支付，Token 仅走环境变量。

## 🎯 目标用户

- 想看看自己「麦门段位」的吃货
- 爱晒消费画像的社交玩家
- 想用最省事的方式体验麦当劳 MCP 的开发者

## 🚀 快速开始

### 方式一：在 WorkBuddy 里一句话生成（推荐）

1. 在 WorkBuddy 左侧【专家 · 技能 · 连接器】启用「麦当劳 MCP」并填入你的 Token。
2. 直接对话：「用 mcd-men-cert 给我生成麦门认证证书」。
3. WorkBuddy 会自动调用只读接口 → 统计 → 产出证书 HTML。

### 方式二：本地运行

```bash
# 准备数据（来自麦当劳 MCP 的 order-list / query-my-account 只读结果）
python generate_certificate.py data.json > cert.html

# 或用内置示例数据先看效果
python generate_certificate.py > sample.html
```

打开 `cert.html` 即可看到你的麦门认证证书，截图分享。

## 📦 输入数据格式

```json
{
  "user_id": "138****1024",
  "points": 12800,
  "orders": [
    {"date":"2026-01-02","amount":38.5,"items":[{"name":"薯条","qty":1},{"name":"麦辣鸡腿堡","qty":2}]}
  ]
}
```

字段均可缺省，缺失时自动用占位值，不影响出图。

## 🧩 段位规则（按累计订单数）

| 订单数 | 段位 |
|---|---|
| ≥200 | 钻石麦门 · 传说信徒 |
| ≥100 | 铂金麦门 · 资深门徒 |
| ≥50 | 黄金麦门 · 认证弟子 |
| ≥20 | 白银麦门 · 入门信徒 |
| <20 | 青铜麦门 · 见习生 |

## 📁 仓库结构

| 文件 | 说明 |
|---|---|
| `README.md` | 项目介绍与使用 |
| `CONTEST_DECLARATION.md` | 参赛声明（官方模板，内容不可改） |
| `MCP_INTEGRATION.md` | 麦当劳 MCP 接入与工具调用说明 |
| `SKILL.md` | WorkBuddy Skill 定义 |
| `generate_certificate.py` | 证书生成源码（自包含，可离线运行） |
| `sample.html` | 示例证书（内置数据生成） |
| `workbuddy.md` | WorkBuddy 开发对话上下文（联动奖励核验） |

## 🏆 参赛

本项目参加 **麦当劳程序员节创意开发大赛（M-CODE / 1024）**。
官方仓库：<https://github.com/M-China/mcd-developer-innovation-challenge>

---

*非麦当劳官方产品，仅供娱乐与学习。数据以麦当劳官方实时结果为准。*
