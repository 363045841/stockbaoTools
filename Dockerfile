FROM python:3.12-slim

WORKDIR /app

# 配置 pip 镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.trusted-host mirrors.aliyun.com

# 安装 uv
RUN pip install uv

# 设置 uv 镜像源
ENV UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 使用 uv 安装依赖
RUN uv sync --frozen --no-dev

# 复制源代码
COPY *.py ./

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["uv", "run", "python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]