# SNS自動投稿 API設定ガイド

このドキュメントでは、LogiShiftの自動記事生成パイプラインにおいて、記事公開時に X (旧Twitter) や Threads へ自動投稿するためのAPIキー取得手順を説明します。

## 1. X (Twitter) API

Xへの投稿を自動化するには、X Developer Portal にアクセスし、Project と App を作成する必要があります。**Free (無料)** プランで、今回の用途（記事更新の通知）には十分です。

### 事前準備
- LogiShift用（または投稿させたい）Xアカウント
- そのアカウントに紐付いた**電話番号認証**（開発者登録に必須です）

### 手順 (Step-by-Step)

1.  **Developer Portal にアクセス**
    - [developer.twitter.com](https://developer.twitter.com/en/portal/dashboard) にアクセスします。
    - まだ開発者登録をしていない場合はサインアップしてください。プラン選択画面が出た場合は「Sign up for Free access」を探して **Free** プランを選択します。
    - **注意:** Freeプランでは **月間1,500件**（1日約50件）の投稿が可能です。ツイートの読み込み（検索やタイムライン取得）はできませんが、投稿（Write）のみの今回の用途には問題ありません。

2.  **Project と App の作成**
    - ダッシュボードの **"Create Project"** をクリックします。
    - 名前を入力（例: `LogiShift Automation`）。
    - Use case（用途）を選択: **"Making a bot"** を選びます。
    - Description（説明）: 「物流ニュース記事の更新情報を自動投稿します」などと英語で入力します（例: *Posting updates about logistics news articles automatically.*）。
    - そのProject内に **App** を作成します（名前の例: `LogiShift Poster`）。

3.  **ユーザー認証設定 (User authentication settings)**
    - Appの設定画面で "User authentication settings" を探し、**"Set up"** または **"Edit"** をクリックします。
    - **App permissions (権限):** 必ず **"Read and Write"** を選択してください。（これが重要です。「Read」のみだと投稿できません）
    - **Type of App:** **"Web App, Automated App or Bot"** を選択します。
    - **App info:**
        - **Callback URI / Redirect URL:** `http://localhost` と入力してください（スクリプトからの利用なので実際には遷移しません）。
        - **Website URL:** `https://logishift.net`
    - 設定を保存します。

4.  **Keys and Tokens (キーとトークンの取得)**
    - Appの **"Keys and tokens"** タブに移動します。
    - 以下の **4つの値** を生成（Generate）し、コピーして保存してください。**重要:** 一度しか表示されないため、必ず直後にメモしてください。
    
    1.  **API Key** (Consumer Key)
    2.  **API Key Secret** (Consumer Secret)
    3.  **Access Token**
    4.  **Access Token Secret**
    
    ※もし "Read and Write" に権限変更する前に Access Token を発行していた場合は、**必ず再生成（Regenerate）** してください。権限変更は再生成しないと反映されません。

5.  **`.env` ファイルへの保存**
    - `automation` ディレクトリの `.env` ファイルに以下のように追記してください：

    ```bash
    X_API_KEY="取得したAPI Key"
    X_API_SECRET="取得したAPI Key Secret"
    X_ACCESS_TOKEN="取得したAccess Token"
    X_ACCESS_TOKEN_SECRET="取得したAccess Token Secret"
    ```

---

## 2. Threads API (Meta)

Threads APIの利用は少し複雑で、Facebook開発者アカウントとInstagramアカウント（プロアカウント）の連携が必要です。

1.  **Meta for Developers**
    - [developers.facebook.com](https://developers.facebook.com/) にアクセスします。
    - "マイアプリ" -> "アプリを作成"。
    - タイプ: **"Threads"** (またはビジネス) を選択。
2.  **設定**
    - アプリに **"Threads API"** プロダクトを追加します。
    - OAuth認証フローを通じて「長期アクセストークン」を取得する必要があります。
    - *備考:* セットアップ手順が多く、定期的なトークン更新（60日ごと）も必要になるため、まずは手軽な **Xの自動化** から先に実装することをおすすめします。
