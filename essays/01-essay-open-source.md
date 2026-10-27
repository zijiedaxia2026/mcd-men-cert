# 【征文】我用 WorkBuddy 30 分钟从 0 到 1 发布了一个 GitHub 开源项目（附真实踩坑）

> 作者：晓雪（球球）· 首发：腾讯频道 WorkBuddy 频道「实用文章」板块 · 2026-10-27
> 本篇为 WorkBuddy 频道首届征文参赛作品（投稿期 2026-10-12 ～ 11-02）

先说结果：从空白目录到公开仓库 github.com/zijiedaxia2026/mcd-men-cert（9 个文件：可运行源码 + 完整文档 + 示例证书 + MIT 许可证），全程约 30 分钟，中间还踩掉一个 Windows 经典大坑。

原来这活要半天：手动建仓、手写 README/声明/集成说明、配 SSH、调试、push。这次全交给 WorkBuddy 拆步执行：

1. 生成完整项目：Python 证书生成器 + 官方要求的 5 个文件一次成型；
2. 联网核实：调 GitHub 公开 API 核对赛事规则与榜单格式，不凭记忆；
3. 配 SSH：写入 ed25519 私钥与 ~/.ssh/config；
4. 后台 git push，不耽误另一台设备的 GitHub 工作。

## 真实踩坑（很多人会遇）

ssh -T 报 "error in libcrypto: unsupported"。不是密钥坏了——WorkBuddy 读文件头 hex 发现每行结尾是 0d0a（CRLF）：Windows 下 Python 文本模式把 \n 写成了 \r\n，OpenSSL 拒认。改用二进制模式 open(path,"wb") 重写后，ssh-keygen -y 正常还原公钥，ssh -T 返回 Hi！推送成功。

## 可复用方法

1. 把"建仓 → 写文件 → 配密钥 → 排障 → 推送"拆成小步喂给 WorkBuddy；
2. 遇到底层报错让它读原始字节定位根因，别盲试；
3. 多设备共用账号用 SSH 密钥，互不干扰。

（内容为真实操作记录，已脱敏。）
