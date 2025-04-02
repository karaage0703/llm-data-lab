# LLM Data Lab

LLM（大規模言語モデル）を活用したデータ分析のためのリポジトリです。

## 概要

このリポジトリは、データサイエンティストがLLMの力を活用してデータ分析を効率的に行うための環境とツールを提供します。基本的なデータ分析から高度な可視化、LLMを使った洞察の抽出まで、データ分析のワークフローをサポートします。

## 機能

- 基本的なデータ分析ツール（統計情報、欠損値分析など）
- データ可視化ツール（ヒストグラム、散布図、相関ヒートマップなど）
- LLMを活用したデータ分析（準備中）
- Jupyter Notebookによる対話的な分析環境
- uvによる依存関係管理

## 環境のセットアップ

### 前提条件

- Python 3.10以上
- [uv](https://github.com/astral-sh/uv)（高速なPythonパッケージマネージャー）

### セットアップ手順

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/llm-data-lab.git
cd llm-data-lab
```

2. セットアップスクリプトを実行

```bash
./setup_env.sh
```

このスクリプトは以下の処理を行います：
- uvがインストールされていない場合はインストール
- 仮想環境の作成
- 依存パッケージのインストール

3. 仮想環境をアクティベート

```bash
source .venv/bin/activate
```

## 使い方

### 基本的なデータ分析

`tools/basic_analysis.py`を使用して、データの基本的な分析を行います。

```bash
python tools/basic_analysis.py データファイルのパス
```

オプション：
- `--output`, `-o`: 分析結果を保存するファイルのパス
- `--head`, `-n`: 表示する先頭行数（デフォルト: 5）

例：
```bash
python tools/basic_analysis.py data/sample.csv --output analysis_report.txt
```

### データの可視化

`tools/visualization.py`を使用して、データの可視化を行います。

```bash
python tools/visualization.py データファイルのパス --type 可視化の種類 [オプション]
```

可視化の種類：
- `hist`: ヒストグラム（`--column`オプションが必要）
- `box`: 箱ひげ図（`--column`オプションが必要）
- `scatter`: 散布図（`--x`と`--y`オプションが必要）
- `corr`: 相関ヒートマップ
- `pair`: ペアプロット
- `count`: カテゴリ列の度数分布
- `time`: 時系列データの折れ線グラフ（`--date`と`--column`オプションが必要）

例：
```bash
# ヒストグラムの描画
python tools/visualization.py data/sample.csv --type hist --column 価格 --output hist.png

# 散布図の描画
python tools/visualization.py data/sample.csv --type scatter --x 身長 --y 体重 --hue 性別 --output scatter.png

# 相関ヒートマップの描画
python tools/visualization.py data/sample.csv --type corr --output corr.png
```

### Jupyter Notebookの使用

対話的なデータ分析を行うには、Jupyter Notebookを使用します。

```bash
jupyter notebook
```

`notebooks`ディレクトリに新しいノートブックを作成し、分析を始めることができます。

## データ分析のワークフロー

1. **データの準備**: データファイルを`data`ディレクトリに配置します。
2. **基本分析**: `tools/basic_analysis.py`を使用して、データの基本的な特性を把握します。
3. **可視化**: `tools/visualization.py`を使用して、データの視覚的な分析を行います。
4. **詳細分析**: Jupyter Notebookを使用して、より詳細な分析を行います。
5. **LLM活用**: LLMを使用して、データからより深い洞察を得ます（準備中）。

## 注意事項

- 巨大なデータを扱う場合は、直接プロンプトに読み込まず、まずツールを使用して基本的な分析を行ってください。
- データの特性（サイズ、形式、欠損値の有無など）を把握してから、適切な分析手法を選択してください。
- 大規模なデータセットの場合は、サンプリングやチャンク処理を検討してください。

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
