# CLAUDE.md

## プロジェクト概要

Slidev プレゼンテーション用の pnpm モノレポ。各スライドデッキは独立したパッケージとして管理する。

## 技術スタック

- **ランタイム**: Node.js 24 (mise で管理)
- **パッケージマネージャ**: pnpm (ワークスペース)
- **スライドフレームワーク**: [Slidev](https://sli.dev/)

## ディレクトリ構成

```
slides/
├── .claude/           # Claude Code 設定
├── packages/
│   └── slides/        # 各スライドデッキ (pnpm ワークスペース)
│       └── <name>/    # 個別のスライドプロジェクト
├── package.json       # ルート package.json (private)
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── mise.toml          # ツールバージョン管理
├── .npmrc
└── .gitignore
```

## よく使うコマンド

```bash
# セットアップ
mise install
pnpm install

# スライドの開発サーバー起動 (各パッケージディレクトリで)
pnpm dev

# スライドのビルド (各パッケージディレクトリで)
pnpm build

# スライドのエクスポート (各パッケージディレクトリで)
pnpm export

# 新しいスライドデッキの作成 (ルートディレクトリで)
pnpm new-slide <name>
```

## 新しいスライドデッキの作成手順

`pnpm new-slide <name>` を実行すると、以下が自動で行われる:

1. `packages/slides/<name>/` ディレクトリを作成
2. `package.json` (Slidev 依存関係付き) と `slides.md` (テンプレート) を生成

作成後は以下を実行:

```bash
pnpm install
cd packages/slides/<name> && pnpm dev
```

## コーディング規約

- コミットメッセージは日本語または英語の prefix 付き (例: `feat:`, `fix:`, `docs:`)
- スライドの内容は日本語で記述

## 環境

- pnpm は mise で管理されている
- Bash ツールで pnpm を使うには `eval "$(mise activate bash)"` を先に実行する必要がある
  - 例: `eval "$(mise activate bash)" && pnpm new-slide my-talk`
