# YouTube View Count Updater for Notion

## 概要

このプログラムは、Notionデータベースに登録されているYouTube動画のURLから動画IDを抽出し、YouTube Data APIを使って最新の再生回数を取得。
取得した再生回数をNotionの対応プロパティに自動で更新します。

---

## 機能

* Notionデータベースの指定プロパティからYouTube動画URLを読み取り
* YouTube APIを用いて動画の再生回数を取得
* 再生回数をNotionの指定プロパティに書き込み・更新
* 複数ページに対応
* ログ出力で処理状況を確認可能

---

## 使い方

### 必要なもの

* Python 3.x
* `notion_client`、`requests` モジュール（`pip install notion-client requests`）
* YouTube Data APIキー
* Notion APIトークン（内部インテグレーションのシークレット）
* NotionのデータベースID
* `config.json`（NotionのURLプロパティ名、再生回数プロパティ名を記載）

---

### 環境変数設定

以下を環境変数として設定してください（GitHub ActionsのSecretsやローカル環境にて）。

| 変数名                  | 内容                       |
| -------------------- | ------------------------ |
| NOTION\_API\_KEY     | Notionの内部インテグレーションシークレット |
| NOTION\_DATABASE\_ID | Notionの対象データベースID        |
| YOUTUBE\_API\_KEY    | YouTube Data APIキー       |

---

### config.jsonの例

```json
{
  "url_property_name": "ミュージックビデオURL",
  "view_count_property_name": "再生回数"
}
```

---

### 実行コマンド

```bash
python get_youtube_views.py
```

---

## GitHub Actionsによる定期実行

`.github/workflows/schedule.yml` 例：

```yaml
name: Update YouTube Views Weekly

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜 0時(UTC)

jobs:
  update_views:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - name: Install dependencies
        run: pip install notion-client requests
      - name: Run view count update
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          NOTION_DATABASE_ID: ${{ secrets.NOTION_DATABASE_ID }}
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: python get_youtube_views.py
```

---

## 注意事項

* YouTube Data APIのキーは有効であることを確認してください。
* Notion APIトークンは対象データベースにアクセス権があること。
* GitHub ActionsでSecretsを正しく設定してください。
* 実行はUTC基準の時間に行われます。日本時間で設定したい場合は時差を考慮してください。

---

## トラブルシューティング

* **再生回数が取得できない場合**

  * APIキーの権限や使用制限を確認。
  * 動画IDの抽出が正しいかログを確認。
* **401 Unauthorized エラー**

  * Notion APIキーが間違っているか、環境変数が設定されていない。
* **403 Forbidden エラー**

  * YouTube APIキーが間違っているか、APIの利用制限に達している。

---

## ライセンス

MIT License

---
