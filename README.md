# Server Monitor

Flaskを使用した軽量なサーバー監視ウェブアプリケーションです。指定されたURLの稼働状況を定期的にチェックし、ステータス（稼働中、応答遅延、ダウン）とレイテンシ（応答時間）を視覚的なダッシュボードに表示します。

## 主な機能

- **定期的な死活監視**: バックグラウンドのスレッドを使用して約10秒間隔でターゲットを自動的にチェックします。
- **リアルタイムダッシュボード**: JavaScriptを使用した非同期通信により、ページをリロードせずにサーバーの状態を更新します。

## 必要環境

- Python 3.x
- Flask
- requests

## インストールと実行方法

1. 仮想環境を作成し、有効化することを推奨します。
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate   # Windows
   ```

2. 必要なPythonパッケージをインストールします。
   ```bash
   pip install flask requests
   ```

3. アプリケーションを実行します。
   ```bash
   python app.py
   ```

4. Webブラウザで以下のURLにアクセスしてダッシュボードを開きます。
   ```
   http://127.0.0.1:5000
   ```

## 監視ターゲットの設定

監視対象のサーバーを追加、変更する場合は、
1. `app.py` ファイル内の `TARGETS` 辞書を直接編集してください。

```python
TARGETS = {
    "google": "https://www.google.com",
    "github": "https://github.com",
    # 追加のURLをここに記述
    # "my_server": "https://my-example-server.com",
}
```

2. `static/js/monitor.js`の`updateStatus`関数内の`updateElement`の部分を直接編集してください。

```javascript
async function updateStatus() {
    try {
        const response = await fetch('/getinfo');
        const data = await response.json();

        updateElement("google", data.google);
        updateElement("github", data.github);
        // 追加するサイトの名前を入力（空白不可、半角英数字を強く推奨）
        // updateElement("my_server", data.my_server);

    } catch (err) {
        console.error("更新エラー:", err);
    }
}
```

3. `templates/index.html`の`<div class="container">`内の`<div class="card">`を編集してください。

```html
<div class="container">
   <div id="card-google" class="card">
      <h3>Google</h3>
      <img id="icon-google" src="/static/icons/ok.svg" width="50" height="50" alt="ステータス">
      <p>状態: <span id="status-google" class="val">--</span></p>
      <p>レイテンシ: <span id="latency-google" class="val">--</span> ms</p>
   </div>
   <div id="card-github" class="card">
      <h3>GitHub</h3>
      <img id="icon-github" src="/static/icons/ok.svg" width="50" height="50" alt="ステータス">
      <p>状態: <span id="status-github" class="val">--</span></p>
      <p>レイテンシ: <span id="latency-github" class="val">--</span> ms</p>
   </div>
   <!-- 追加した監視対象を表示するカードを追加 --->
    <!--
    <div id="card-my_server" class="card">
      <h3>My Server</h3>
      <img id="icon-my_server" src="/static/icons/ok.svg" width="50" height="50" alt="ステータス">
      <p>状態: <span id="status-my_server" class="val">--</span></p>
      <p>レイテンシ: <span id="latency-my_server" class="val">--</span> ms</p>
   </div>
    -->
```