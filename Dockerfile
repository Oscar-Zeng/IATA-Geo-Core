# 使用 Python 3.11 镜像
FROM python:3.11-slim-bookworm

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行服务 (使用 python 运行 mcp_server.py)
ENTRYPOINT ["python", "mcp_server.py"]