FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /opt/app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends  \
    ffmpeg \
    net-tools \
    vim \
    mc \
    libcom-err2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

COPY --from=builder /opt/app/.venv .venv
COPY . .

ENV PATH="/opt/app/.venv/bin:$PATH"
ENV PYTHONPATH="/opt/app/src"
ENV TZ="Asia/Yekaterinburg"

ENTRYPOINT ["python", "src/main.py"]
CMD ["--bind", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker"]