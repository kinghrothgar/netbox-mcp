FROM python:3.12-slim

# `docker` CLI so test fixtures can spawn the netbox-mcp container
# under test (via the host's docker socket bind-mounted at run time).
# Using docker-cli rather than docker.io to avoid pulling the daemon
# (we never run dockerd inside the test container).
RUN apt-get update \
    && apt-get install -y --no-install-recommends docker-cli \
    && rm -rf /var/lib/apt/lists/*

# Versions of httpx and fastmcp pinned to match the production
# Dockerfile so the in-test fastmcp.Client speaks the same wire format
# as the netbox-mcp server it talks to.
RUN pip install --no-cache-dir \
    pytest==8.3.4 \
    pytest-asyncio==0.24.0 \
    pytest-timeout==2.3.1 \
    httpx==0.28.1 \
    fastmcp==3.3.1

# The repo is bind-mounted at /work at run time; source changes don't
# require rebuilding this image.
WORKDIR /work

CMD ["pytest", "-v", "tests/"]
