# 使用 Python 3.11 镜像
FROM python:3.11-slim-bookworm

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 增加 -u 参数，禁用 Python 的输出缓冲
ENTRYPOINT ["python", "-u", "mcp_server.py"]