#!/bin/bash

# uvを使用して仮想環境をセットアップするスクリプト

# エラーが発生したら停止
set -e

echo "LLM Data Lab 環境セットアップを開始します..."

# uvがインストールされているか確認
if ! command -v uv &> /dev/null; then
    echo "uvがインストールされていません。インストールします..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # PATHを更新
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 仮想環境が存在するか確認
if [ ! -d ".venv" ]; then
    echo "仮想環境を作成しています..."
    uv venv
else
    echo "既存の仮想環境を使用します..."
fi

# 仮想環境をアクティベート
source .venv/bin/activate

# 依存関係をインストール
echo "依存関係をインストールしています..."
uv pip install -e ".[dev]"

# pre-commitフックをインストール（オプション）
if [ -f ".pre-commit-config.yaml" ]; then
    echo "pre-commitフックをインストールしています..."
    pre-commit install
fi

echo "環境セットアップが完了しました！"
echo "仮想環境をアクティベートするには以下のコマンドを実行してください："
echo "source .venv/bin/activate"