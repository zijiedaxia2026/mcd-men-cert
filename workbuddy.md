# WorkBuddy 开发对话上下文（workbuddy.md）

> 本文件用于核验本项目系使用 WorkBuddy 开发，符合 M-CODE 联动奖励条件。

## 开发背景
用户希望在 1024 程序员节「麦当劳程序员创意开发大赛」中用 WorkBuddy 做一个**能晒、能涨星**的麦当劳 MCP 作品。需求要点：
- 必须基于麦当劳 MCP 能力；
- 要让人愿意 Star（即可分享、有传播性）；
- 合规只读、Token 不外泄。

## 关键决策（WorkBuddy 内完成）
1. **选题**：放弃已严重内卷的「省钱 / 优惠券」方向，改做「麦门认证证书」——把订单史变成可晒卡片，靠社交传播涨星。
2. **架构**：WorkBuddy 负责编排麦当劳 MCP 只读接口 → 结构化数据 → `generate_certificate.py` 生成自包含 HTML 证书。
3. **合规**：仅用 `order-list` / `query-my-account` 等只读 Tool；Token 仅存在于连接器配置，不入仓。
4. **可离线**：证书生成器不依赖 MCP 也能用（内置示例数据），便于评审复现。

## 验证
- 用内置示例数据运行 `generate_certificate.py` → 成功产出 `sample.html`（自包含，无外部依赖）。
- 输入字段缺省时自动占位，不影响出图。

## 提交物
- `README.md` / `CONTEST_DECLARATION.md` / `MCP_INTEGRATION.md` / `SKILL.md` / `generate_certificate.py` / `sample.html` / `workbuddy.md`
