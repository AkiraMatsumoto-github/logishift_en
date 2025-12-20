# 自作テーマの本番環境デプロイガイド

LogiShiftテーマをローカル環境から本番サーバーのWordPressに反映させる方法を説明します。

## 📋 概要

**GitHub Actionsによる完全自動デプロイ**を採用しています。
初回デプロイも日常の更新も、すべてGitHubへのプッシュ（または手動トリガー）のみで完結します。サーバー上での複雑なコマンド操作は不要です。

---

## 🚀 デプロイフロー（GitHub Actions）

### 1. 仕組み
`.github/workflows/deploy-theme.yml` が、`themes/logishift/` ディレクトリ内の変更を検知し、自動的に本番サーバーへファイルを転送（rsync）します。

### 2. 実行タイミング
- **自動実行**: `main` ブランチへ `themes/logishift/**` の変更をプッシュした時。
- **手動実行**: GitHub上で "Run workflow" ボタンを押した時（再デプロイ時など）。

### 3. 初回セットアップ手順

#### Step 1: GitHub Secretsの設定
リポジトリの **Settings** → **Secrets and variables** → **Actions** に以下の環境変数を設定してください。

| Name | Value | 説明 |
|------|-------|------|
| `SERVER_HOST` | `sv15718.xserver.jp` (例) | サーバーのホスト名 |
| `SERVER_USER` | `xs937213` (例) | SSHユーザー名 |
| `SSH_PRIVATE_KEY` | `-----BEGIN...` | SSH秘密鍵の内容 |
| `SSH_PORT` | `10022` | SSHポート番号 (Xserverは通常10022) |

#### Step 2: デプロイ実行
コードを `main` ブランチにプッシュするだけで、初回デプロイ完了です。

```bash
git add themes/logishift
git commit -m "Initial theme deploy"
git push origin main
```

#### Step 3: テーマの有効化
デプロイが完了したら、WordPress管理画面にアクセスし、テーマを有効化します。

1. https://(your-domain)/wp-admin/ にアクセス
2. **外観** → **テーマ** をクリック
3. **LogiShift** テーマの「有効化」をクリック

---

## �️ ワークフローファイルの構成

参考：`.github/workflows/deploy-theme.yml`

```yaml
name: Deploy Theme
on:
  push:
    paths: ['themes/logishift/**']
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy theme files
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: ${{ secrets.SSH_PORT }}
          source: "themes/logishift/*"
          target: "~/logishift.net/public_html/(domain)/wp-content/themes/"
          strip_components: 1
          rm: true
```

※ `target` パスはリポジトリ（JP/EN）によって異なります。

---

## 🚨 緊急時: 手動デプロイ（Git Archive）

GitHub Actionsが利用できない場合や、即座にサーバーにバグ修正を適用したい場合のバックアップ手段です。

```bash
# ローカルでアーカイブ作成して転送
cd project_root
git archive --format=tar.gz --prefix=logishift/ HEAD:themes/logishift > theme.tar.gz
scp theme.tar.gz user@host:~/

# サーバーで適用
ssh user@host
cd ~/
tar -xzf theme.tar.gz
rsync -av --delete logishift/ ~/path/to/wp-content/themes/logishift/
rm -rf logishift theme.tar.gz
```

---

## ✅ デプロイ後の確認リスト

- [ ] GitHub Actionsの実行ログがすべて緑色（Success）になっているか
- [ ] WordPress管理画面でテーマが認識されているか
- [ ] サイトの表示（トップページ、記事ページ）が崩れていないか
- [ ] CSS/JSが正しく読み込まれているか（キャッシュクリアが必要な場合あり）

## ⚠️ トラブルシューティング

**Q. パーミッションエラーが出る**
A. ワークフロー内で `chmod` を実行していますが、失敗する場合はサーバーにSSH接続し、手動で権限を修正してください。
`chmod -R 755 .../wp-content/themes/logishift`

**Q. 変更が反映されない**
A. WordPressのキャッシュ、ブラウザのキャッシュ、サーバー（Nginx/Apache）のキャッシュをクリアしてください。
