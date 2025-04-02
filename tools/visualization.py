#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
データの可視化を行うスクリプト。

このスクリプトは、CSVやExcelなどの形式のデータファイルを読み込み、
様々な種類のグラフや可視化を生成します。
"""

import argparse
import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(file_path: str) -> pd.DataFrame:
    """データファイルを読み込みます。

    Args:
        file_path: データファイルのパス。

    Returns:
        読み込んだデータフレーム。

    Raises:
        FileNotFoundError: ファイルが見つからない場合。
        ValueError: サポートされていないファイル形式の場合。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".csv":
        # CSVファイルの読み込み
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"CSVファイルの読み込みに失敗しました: {e}")
            print("エンコーディングを指定して再試行します...")
            return pd.read_csv(file_path, encoding="shift-jis")

    elif file_ext in [".xlsx", ".xls"]:
        # Excelファイルの読み込み
        return pd.read_excel(file_path)

    elif file_ext == ".json":
        # JSONファイルの読み込み
        return pd.read_json(file_path)

    elif file_ext == ".parquet":
        # Parquetファイルの読み込み
        return pd.read_parquet(file_path)

    else:
        raise ValueError(f"サポートされていないファイル形式です: {file_ext}")


def setup_plot_style() -> None:
    """プロットのスタイルを設定します。"""
    # Seabornのスタイル設定
    sns.set_style("whitegrid")

    # フォントの設定
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Hiragino Sans", "Yu Gothic", "Meiryo", "Arial", "DejaVu Sans"]

    # 日本語の文字化け防止
    plt.rcParams["axes.unicode_minus"] = False


def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30, output_path: Optional[str] = None) -> None:
    """指定した列のヒストグラムを描画します。

    Args:
        df: データフレーム。
        column: ヒストグラムを描画する列名。
        bins: ビンの数。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' はデータフレームに存在しません。")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"列 '{column}' は数値型ではありません。")

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=column, bins=bins, kde=True)
    plt.title(f"{column} の分布")
    plt.xlabel(column)
    plt.ylabel("頻度")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"ヒストグラムを保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_boxplot(df: pd.DataFrame, column: str, by: Optional[str] = None, output_path: Optional[str] = None) -> None:
    """指定した列の箱ひげ図を描画します。

    Args:
        df: データフレーム。
        column: 箱ひげ図を描画する列名。
        by: グループ化する列名。Noneの場合はグループ化しない。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' はデータフレームに存在しません。")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"列 '{column}' は数値型ではありません。")

    if by is not None and by not in df.columns:
        raise ValueError(f"列 '{by}' はデータフレームに存在しません。")

    plt.figure(figsize=(12, 6))

    if by is None:
        sns.boxplot(x=df[column])
        plt.title(f"{column} の箱ひげ図")
    else:
        sns.boxplot(x=by, y=column, data=df)
        plt.title(f"{by} ごとの {column} の箱ひげ図")

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"箱ひげ図を保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: Optional[str] = None, output_path: Optional[str] = None) -> None:
    """散布図を描画します。

    Args:
        df: データフレーム。
        x: X軸の列名。
        y: Y軸の列名。
        hue: 色分けする列名。Noneの場合は色分けしない。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    if x not in df.columns:
        raise ValueError(f"列 '{x}' はデータフレームに存在しません。")

    if y not in df.columns:
        raise ValueError(f"列 '{y}' はデータフレームに存在しません。")

    if not pd.api.types.is_numeric_dtype(df[x]):
        raise ValueError(f"列 '{x}' は数値型ではありません。")

    if not pd.api.types.is_numeric_dtype(df[y]):
        raise ValueError(f"列 '{y}' は数値型ではありません。")

    if hue is not None and hue not in df.columns:
        raise ValueError(f"列 '{hue}' はデータフレームに存在しません。")

    plt.figure(figsize=(10, 8))

    if hue is None:
        sns.scatterplot(x=x, y=y, data=df)
    else:
        sns.scatterplot(x=x, y=y, hue=hue, data=df)

    plt.title(f"{x} と {y} の散布図")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"散布図を保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_correlation_heatmap(df: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """相関係数のヒートマップを描画します。

    Args:
        df: データフレーム。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    # 数値列のみを選択
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        print("数値列が2つ未満のため、相関ヒートマップを描画できません。")
        return

    # 相関係数の計算
    corr_matrix = numeric_df.corr()

    # ヒートマップの描画
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(
        corr_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0, annot=True, fmt=".2f", square=True, linewidths=0.5
    )

    plt.title("相関係数ヒートマップ")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"相関ヒートマップを保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_pairplot(
    df: pd.DataFrame, columns: Optional[List[str]] = None, hue: Optional[str] = None, output_path: Optional[str] = None
) -> None:
    """ペアプロットを描画します。

    Args:
        df: データフレーム。
        columns: 描画する列のリスト。Noneの場合は数値列すべて。
        hue: 色分けする列名。Noneの場合は色分けしない。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    # 描画する列の選択
    if columns is None:
        # 数値列のみを選択
        plot_df = df.select_dtypes(include=["number"])
        if plot_df.shape[1] < 2:
            print("数値列が2つ未満のため、ペアプロットを描画できません。")
            return
    else:
        # 指定された列が存在するか確認
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"列 '{col}' はデータフレームに存在しません。")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise ValueError(f"列 '{col}' は数値型ではありません。")

        plot_df = df[columns]

    # hueの確認
    if hue is not None:
        if hue not in df.columns:
            raise ValueError(f"列 '{hue}' はデータフレームに存在しません。")

        # hue列を追加
        plot_df = pd.concat([plot_df, df[hue]], axis=1)

    # ペアプロットの描画
    g = sns.pairplot(plot_df, hue=hue, diag_kind="kde")
    g.fig.suptitle("ペアプロット", y=1.02)

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"ペアプロットを保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_count(df: pd.DataFrame, column: str, output_path: Optional[str] = None) -> None:
    """カテゴリ列の度数を棒グラフで描画します。

    Args:
        df: データフレーム。
        column: 描画する列名。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    if column not in df.columns:
        raise ValueError(f"列 '{column}' はデータフレームに存在しません。")

    plt.figure(figsize=(12, 6))

    # 値の数をカウント
    value_counts = df[column].value_counts()

    # 値の数が多すぎる場合は上位10個のみ表示
    if len(value_counts) > 10:
        print(f"列 '{column}' の値が10個以上あるため、上位10個のみ表示します。")
        value_counts = value_counts.head(10)

    # 棒グラフの描画
    sns.barplot(x=value_counts.index, y=value_counts.values)

    plt.title(f"{column} の度数分布")
    plt.xlabel(column)
    plt.ylabel("度数")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"度数分布グラフを保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def plot_time_series(
    df: pd.DataFrame, date_column: str, value_column: str, freq: Optional[str] = None, output_path: Optional[str] = None
) -> None:
    """時系列データを折れ線グラフで描画します。

    Args:
        df: データフレーム。
        date_column: 日付列の名前。
        value_column: 値列の名前。
        freq: リサンプリングの頻度（例: 'D', 'W', 'M'）。Noneの場合はリサンプリングしない。
        output_path: 出力ファイルのパス。Noneの場合は表示のみ。
    """
    if date_column not in df.columns:
        raise ValueError(f"列 '{date_column}' はデータフレームに存在しません。")

    if value_column not in df.columns:
        raise ValueError(f"列 '{value_column}' はデータフレームに存在しません。")

    if not pd.api.types.is_numeric_dtype(df[value_column]):
        raise ValueError(f"列 '{value_column}' は数値型ではありません。")

    # 日付列をdatetime型に変換
    try:
        df[date_column] = pd.to_datetime(df[date_column])
    except Exception as e:
        raise ValueError(f"列 '{date_column}' を日付型に変換できません: {e}")

    # データをソート
    df = df.sort_values(by=date_column)

    # リサンプリング
    if freq is not None:
        df_resampled = df.set_index(date_column).resample(freq)[value_column].mean().reset_index()
        x = df_resampled[date_column]
        y = df_resampled[value_column]
    else:
        x = df[date_column]
        y = df[value_column]

    # 折れ線グラフの描画
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker="o", linestyle="-", markersize=4)

    plt.title(f"{value_column} の時系列変化")
    plt.xlabel(date_column)
    plt.ylabel(value_column)
    plt.grid(True)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"時系列グラフを保存しました: {output_path}")
    else:
        plt.show()

    plt.close()


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(description="データの可視化を行います。")
    parser.add_argument("file_path", help="可視化するデータファイルのパス")
    parser.add_argument(
        "--type",
        "-t",
        choices=["hist", "box", "scatter", "corr", "pair", "count", "time"],
        default="hist",
        help="可視化の種類",
    )
    parser.add_argument("--column", "-c", help="可視化する列名")
    parser.add_argument("--x", help="散布図のX軸の列名")
    parser.add_argument("--y", help="散布図のY軸の列名")
    parser.add_argument("--by", help="グループ化する列名")
    parser.add_argument("--hue", help="色分けする列名")
    parser.add_argument("--date", help="時系列グラフの日付列名")
    parser.add_argument("--freq", help="時系列データのリサンプリング頻度（例: 'D', 'W', 'M'）")
    parser.add_argument("--output", "-o", help="出力ファイルのパス")

    args = parser.parse_args()

    try:
        # データの読み込み
        df = load_data(args.file_path)

        # プロットスタイルの設定
        setup_plot_style()

        # 可視化の種類に応じた処理
        if args.type == "hist":
            if args.column is None:
                raise ValueError("ヒストグラムには --column オプションが必要です。")
            plot_histogram(df, args.column, output_path=args.output)

        elif args.type == "box":
            if args.column is None:
                raise ValueError("箱ひげ図には --column オプションが必要です。")
            plot_boxplot(df, args.column, by=args.by, output_path=args.output)

        elif args.type == "scatter":
            if args.x is None or args.y is None:
                raise ValueError("散布図には --x と --y オプションが必要です。")
            plot_scatter(df, args.x, args.y, hue=args.hue, output_path=args.output)

        elif args.type == "corr":
            plot_correlation_heatmap(df, output_path=args.output)

        elif args.type == "pair":
            columns = args.column.split(",") if args.column else None
            plot_pairplot(df, columns=columns, hue=args.hue, output_path=args.output)

        elif args.type == "count":
            if args.column is None:
                raise ValueError("度数分布図には --column オプションが必要です。")
            plot_count(df, args.column, output_path=args.output)

        elif args.type == "time":
            if args.date is None or args.column is None:
                raise ValueError("時系列グラフには --date と --column オプションが必要です。")
            plot_time_series(df, args.date, args.column, freq=args.freq, output_path=args.output)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
