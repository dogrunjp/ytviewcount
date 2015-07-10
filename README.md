# ytviewcount

## このアプリケーションは

YouTube Analytics APIを使って自分のGoogleアカウントが管理するチャンネルの再生回数（デフォルトではTOP10）をJSONで取得する
Pythonのアプリケーションです。Python2.7な環境でテストしています。

## 必用そうなもの
YouTube Analytics APIとYouTube Data API v3を利用するので、
Google Developers Consoleで自分の管理するアカウントにアプリケーションを作りこの２つのAPIを有効にしておく必用があります。

また、YT Analytics APIはOAuth2.0なので認証情報（ネイティブクライアント=NaClのもの）のJSONをダウンロードしておく必用があります。
あと、video idからタイトルの取得にData APIを利用していますが、こちらは公開APIのAPIキーが必用です。どちらもGoogle Developer Consoleで取得できます。

## 不安
Macでテストしていますが、サーバで動かしたときの認証をテストしていないためそこは何か起きるかも。
"--noauth_local_webserver"的なオプションを初回のアプリケーションの起動で付けてアクセストークンを取得するような雰囲気。です。。
