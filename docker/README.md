# 旧版 Docker 工具

本目录保留旧版工具，目标地址为容器自身的回环接口。要运行带独立 Discourse 和 PostgreSQL 核验的端到端测试，请使用[主文档](../README.md)中的工作流。

## 飞牛NAS / 任意 Docker 环境部署

### 快速开始

```bash
# 1. 进入 docker 目录
cd docker

# 2. 复制配置文件，填入账号密码
cp .env.example .env
nano .env

# 3. 启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f
```

### 配置说明

编辑 `.env` 文件：

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `LINUXDO_USERNAME` | ✅ | - | 测试论坛用户名 |
| `LINUXDO_PASSWORD` | ✅ | - | 测试论坛密码 |
| `RUNS_PER_DAY` | ❌ | 2 | 每天运行次数 |
| `TOPICS_MIN` | ❌ | 15 | 每次最少浏览帖子数 |
| `TOPICS_MAX` | ❌ | 40 | 每次最多浏览帖子数 |
| `LIKE_RATE` | ❌ | 30 | 点赞概率 (0-100) |
| `RUN_ON_START` | ❌ | true | 启动时是否立即运行一次 |

### 运行机制

- 启动后立即执行一次浏览任务
- 之后的任务从 07:00 起，在 16 小时内按固定间隔运行
- 浏览数量和点赞概率由配置控制
- 浏览器数据持久化，登录状态会保持

### 常用命令

```bash
# 启动
docker-compose up -d

# 停止
docker-compose down

# 查看日志
docker-compose logs -f

# 重启
docker-compose restart

# 重新构建（更新代码后）
docker-compose up -d --build

# 只运行一次（不启动调度器）
docker-compose run --rm linuxdo --once
```

### 资源占用

- 内存限制: 1GB
- CPU 限制: 1 核
- 磁盘: Chrome 数据约 200MB
