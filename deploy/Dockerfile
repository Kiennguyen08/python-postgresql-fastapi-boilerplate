# pull official base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# set work directory
WORKDIR /opt

# set static environment variables
ENV UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy

RUN apt-get update && \
  apt-get install -y ffmpeg libjemalloc2 && \
  rm -rf /var/lib/apt/lists/*

# install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-dev

# copy project
COPY app/ app/
COPY config/ config/

ENV PATH="/opt/.venv/bin:$PATH" \
  OTEL_SERVICE_NAME="voice-biometric-service" \
  OTEL_METRICS_EXPORTER="" \
  LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libjemalloc.so.2" \
  MALLOC_CONF="background_thread:true,metadata_thp:auto,dirty_decay_ms:5000,muzzy_decay_ms:5000"

# command: use exec-format over shell-format
ENTRYPOINT ["opentelemetry-instrument", "uvicorn", "--factory", "app:create_app"]
CMD ["--host=0.0.0.0", "--port=80", "--workers=1", "--log-config=config/log-config.yml"]