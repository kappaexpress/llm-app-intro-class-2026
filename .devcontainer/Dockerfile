FROM mcr.microsoft.com/devcontainers/typescript-node
# FROM mcr.microsoft.com/devcontainers/python

# 対話的なプロンプトをスキップするための設定
ENV DEBIAN_FRONTEND=noninteractive

# パッケージリストの更新とChromium、日本語フォントのインストール
RUN apt-get update && apt-get install -y \
    iputils-ping \
    dnsutils \
    sqlite3 \
    chromium \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*