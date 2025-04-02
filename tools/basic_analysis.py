#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基本的なデータ分析を行うスクリプト。

このスクリプトは、CSVやExcelなどの形式のデータファイルを読み込み、
基本的な統計情報や欠損値の確認などの分析を行います。
"""

import argparse
import os
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd


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


def basic_statistics(df: pd.DataFrame) -> None:
    """データフレームの基本的な統計情報を表示します。

    Args:
        df: 分析対象のデータフレーム。
    """
    print("\n=== 基本情報 ===")
    print(f"行数: {df.shape[0]}")
    print(f"列数: {df.shape[1]}")

    print("\n=== データ型 ===")
    print(df.dtypes)

    print("\n=== 欠損値の数 ===")
    print(df.isnull().sum())

    print("\n=== 数値列の基本統計量 ===")
    print(df.describe())

    # カテゴリ列の基本統計量
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(categorical_cols) > 0:
        print("\n=== カテゴリ列の基本統計量 ===")
        print(df[categorical_cols].describe())


def check_duplicates(df: pd.DataFrame) -> None:
    """データフレームの重複行を確認します。

    Args:
        df: 分析対象のデータフレーム。
    """
    dup_count = df.duplicated().sum()
    print(f"\n=== 重複行の数: {dup_count} ===")
    if dup_count > 0:
        print("重複行の例:")
        print(df[df.duplicated(keep="first")].head())


def analyze_correlations(df: pd.DataFrame, threshold: float = 0.7) -> None:
    """数値列間の相関関係を分析します。

    Args:
        df: 分析対象のデータフレーム。
        threshold: 表示する相関係数の閾値。
    """
    # 数値列のみを選択
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        print("\n=== 相関分析 ===")
        print("数値列が2つ未満のため、相関分析を行えません。")
        return

    # 相関係数の計算
    corr_matrix = numeric_df.corr()

    # 閾値以上の相関係数を持つ列のペアを表示
    print(f"\n=== 相関係数（絶対値が{threshold}以上のもの）===")
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) >= threshold:
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                corr_val = corr_matrix.iloc[i, j]
                print(f"{col1} - {col2}: {corr_val:.4f}")


def save_analysis_report(df: pd.DataFrame, output_path: Optional[str] = None) -> None:
    """分析結果をファイルに保存します。

    Args:
        df: 分析対象のデータフレーム。
        output_path: 出力ファイルのパス。Noneの場合は保存しません。
    """
    if output_path is None:
        return

    with open(output_path, "w", encoding="utf-8") as f:
        # 基本情報
        f.write("=== 基本情報 ===\n")
        f.write(f"行数: {df.shape[0]}\n")
        f.write(f"列数: {df.shape[1]}\n\n")

        # データ型
        f.write("=== データ型 ===\n")
        f.write(str(df.dtypes) + "\n\n")

        # 欠損値
        f.write("=== 欠損値の数 ===\n")
        f.write(str(df.isnull().sum()) + "\n\n")

        # 基本統計量
        f.write("=== 数値列の基本統計量 ===\n")
        f.write(str(df.describe()) + "\n\n")

        # カテゴリ列の基本統計量
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        if len(categorical_cols) > 0:
            f.write("=== カテゴリ列の基本統計量 ===\n")
            f.write(str(df[categorical_cols].describe()) + "\n\n")

        # 重複行
        dup_count = df.duplicated().sum()
        f.write(f"=== 重複行の数: {dup_count} ===\n\n")

        # 相関分析
        numeric_df = df.select_dtypes(include=["number"])
        if numeric_df.shape[1] >= 2:
            f.write("=== 相関係数（絶対値が0.7以上のもの）===\n")
            corr_matrix = numeric_df.corr()
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if abs(corr_matrix.iloc[i, j]) >= 0.7:
                        col1 = corr_matrix.columns[i]
                        col2 = corr_matrix.columns[j]
                        corr_val = corr_matrix.iloc[i, j]
                        f.write(f"{col1} - {col2}: {corr_val:.4f}\n")

    print(f"分析レポートを保存しました: {output_path}")


def main() -> None:
    """メイン関数。"""
    parser = argparse.ArgumentParser(description="データファイルの基本的な分析を行います。")
    parser.add_argument("file_path", help="分析するデータファイルのパス")
    parser.add_argument("--output", "-o", help="分析結果を保存するファイルのパス")
    parser.add_argument("--head", "-n", type=int, default=5, help="表示する先頭行数")

    args = parser.parse_args()

    try:
        # データの読み込み
        df = load_data(args.file_path)

        # データの先頭を表示
        print(f"\n=== データの先頭 {args.head} 行 ===")
        print(df.head(args.head))

        # 基本的な統計情報
        basic_statistics(df)

        # 重複行の確認
        check_duplicates(df)

        # 相関分析
        analyze_correlations(df)

        # 分析結果の保存
        if args.output:
            save_analysis_report(df, args.output)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
