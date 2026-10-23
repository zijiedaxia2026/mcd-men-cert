# MCP 接入说明 (MCP_INTEGRATION.md)

本项目基于 **麦当劳中国 MCP Server**（`https://mcp.mcd.cn`，远程托管）构建，全部使用**只读**工具，不涉及下单、支付等写操作。

## 1. 接入方式

在 MCP Client（如 WorkBuddy 的「自定义连接器 → 配置 MCP」）中填入：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

> Token 通过麦当劳开放平台（open.mcd.cn/mcp）用手机号登录后申请，仅作为环境变量 / 连接器配置传入，**不写入任何仓库文件**。

## 2. 实际使用的 Tool

| Tool | 用途 | 是否只读 |
|---|---|---|
| `order-list` | 拉取历史订单（日期、金额、明细） | ✅ 只读 |
| `query-my-account` | 查询积分、会员等级等账户信息 | ✅ 只读 |
| `query-my-coupons` | 查询可用券（仅用于丰富报告，可选） | ✅ 只读 |

## 3. 调用流程

```
用户发起「生成麦门认证证书」
   ↓
WorkBuddy 调用 order-list（分页拉取历史订单）
   ↓
（可选）调用 query-my-account 获取积分
   ↓
把结构化结果映射为 data.json（见 README 输入格式）
   ↓
generate_certificate.py 分析 → 计算段位 / 称号 / 认证编号
   ↓
输出自包含 HTML 证书（cert.html），用户截图分享
```

## 4. 业务价值

- **把冷数据变成社交货币**：订单史本是私密消费记录，本项目将其转化为一张可晒的「认证证书」，显著降低分享心理门槛，自带传播性。
- **零门槛体验 MCP**：用户无需理解任何接口，一句话即可看到自己与麦当劳的「关系证明」，是麦当劳 MCP 能力最直观的 Demo 之一。
- **合规优先**：仅只读、Token 不外泄、输出不含真实凭证，符合《参赛声明》与活动规则。
