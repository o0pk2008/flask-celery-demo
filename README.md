# Flask + Celery 异步任务处理原型系统

## 项目简介
本项目基于 Flask + Celery + Redis 实现异步任务处理，支持任务添加、状态查询，并集成 Flower 监控。

## 环境准备（推荐使用 Anaconda）
1. 创建并激活名为 Celery 的 Anaconda 环境：
   ```bash
   conda create -n Celery python=3.9 -y
   activate Celery
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## Redis 启动
请确保本地已安装 Redis 并启动，或使用 Docker 快速启动：
```bash
docker run -d -p 6379:6379 redis
```
## PostgreSQL Docker 启动（持久化挂载）
用户名：celeryuser
密码：123456
数据库名：celerydb
本地数据目录：D:/AILAB/postgres_data

```bash
docker run -d --name pg-celery-demo -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=celeryuser -e POSTGRES_DB=celerydb -p 5432:5432 -v D:/AILAB/Celery/postgres_data:/var/lib/postgresql/data postgres:14
```
| 参数部分                                                     | 作用说明                                                         |
| ----------------------------------------------------------- | ---------------------------------------------------------------  |
| `docker run`                                                | 运行一个新的容器                                                  |
| `-d`                                                        | 后台运行（detached mode）                                         |
| `--name pg-celery-demo`                                     | 给这个容器取个名字，方便后续管理（如停止、查看日志）                  |
| `-e POSTGRES_PASSWORD=123456`                               | 设置数据库超级用户（默认是 postgres）的密码                         |
| `-e POSTGRES_USER=celeryuser`                               | 创建一个新的数据库用户 `celeryuser`                                |
| `-e POSTGRES_DB=celerydb`                                   | 创建一个新数据库 `celerydb`，属于上面的用户                         |
| `-p 5432:5432`                                              | 宿主机的 5432 端口映射到容器的 5432 端口（PostgreSQL 默认端口）      |
| `-v D:/AILAB/Celery/postgres_data:/var/lib/postgresql/data` | 将宿主机目录挂载为容器的数据存储目录，实现数据库**持久化**            |
| `postgres:14`                                               | 使用的镜像，`postgres` 是官方镜像，`14` 是版本号                    |


## 用 Docker 启动 pgAdmin
```bash
docker run -d --name pgadmin4 -p 9080:80 -e PGADMIN_DEFAULT_EMAIL=admin@qq.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4
```
| 参数                       | 含义                                         |
| -------------------------- | ------------------------------------------- |
| `-p 9080:80`               | 把容器的 80 端口映射到本机的 9080，用浏览器访问 |
| `PGADMIN_DEFAULT_EMAIL`    | 登陆邮箱（自定义）                            |
| `PGADMIN_DEFAULT_PASSWORD` | 登陆密码（自定义）                            |
| `dpage/pgadmin4`           | 官方 pgAdmin 镜像                            |


## 启动 Flask API
```bash
python run.py
```

## 启动 Celery Worker
```bash
celery -A tasks.celery worker --loglevel=info --pool=threads --hostname=myworker1@%h
```
| 参数 | 含义 |
|--------------------------------------|----------------------------------------------------------------------|
| celery | Celery 命令行工具 |
| -A tasks.celery | 指定 Celery 应用（即 tasks/celery.py 里的 celery 实例） |
| worker | 启动 worker 进程，负责执行任务 |
| --loglevel=info | 日志级别为 info，显示详细运行信息 |
| --pool=threads | 使用线程池模式（适合 Windows，避免多进程兼容性问题） |
| --hostname=myworker1@%h | 设置 worker 名称为 myworker1@主机名（%h 会自动替换为主机名） |

## 启动 Flower 监控
```bash
celery -A tasks.celery flower --address=0.0.0.0 --port=5555
```
| 参数 | 含义 |
|--------------------------------------|----------------------------------------------------------------------|
| celery | Celery 命令行工具 |
| -A tasks.celery | 指定 Celery 应用（即 tasks/celery.py 里的 celery 实例） |
| flower | 启动 Flower 监控服务 |
| --address=0.0.0.0 | 监听所有网卡（允许外部访问 Flower 面板） |
| --port=5555 | Flower 监听的端口号为 5555 |

访问方式：
启动后，在浏览器访问 http://localhost:5555（本机）或 http://<你的主机IP>:5555（局域网其他机器）。
