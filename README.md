# Discourse 已读计数验证

本 fork 使用 GitHub Actions 启动临时 Discourse 2026.7.5。进入 **Actions → Test forum read receipt → Run workflow** 可以执行一次。论坛只监听 runner 的回环接口，测试凭据在运行时生成。

工作流创建一个普通读者账号和两个各含一帖的公开话题。Chrome 使用标准自动化模式登录，打开目标话题，由 Discourse 自己的前端提交阅读状态。测试在浏览前后独立查询 PostgreSQL 的账号已读帖数和两个话题的阅读记录。成功条件为账号已读帖数增加 1、目标帖新增一条阅读记录、未打开的对照帖仍为 0。运行摘要给出前值、后值和差值。

浏览器入口为 `linux_do_headless.py`。数据库查询见 `ci/read_counts.sql`。工作流结束后删除测试容器。

[上游项目](https://github.com/icysaintdx/linuxdosss)
