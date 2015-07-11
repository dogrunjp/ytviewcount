# ytviewcount

## このアプリケーションは

YouTube Analytics APIを使って自分のGoogleアカウントが管理するチャンネルの再生回数（デフォルトではTOP10）をJSONで取得する
Pythonのアプリケーションです。Python2.7な環境でテストしています。

## 必用そうなもの
YouTube Analytics APIとYouTube Data API v3を利用するので、
Google Developers Consoleで自分の管理するアカウントにアプリケーションを作りこの２つのAPIを有効にしておく必用があります。

また、YT Analytics APIはOAuth2.0なので認証情報（ネイティブクライアント=NaClのもの）のJSONをダウンロードしておく必用があります。
あと、video idからタイトルの取得にData APIを利用していますが、こちらは公開APIのAPIキーが必用です。どちらもGoogle Developer Consoleで取得できます。

## サーバでの認証
Macでこのアプリケーションを最初に起動すると、認証のためブラウザが起動し、Googleアカウントの認証を行います。

サーバでアプリケーションを起動した場合
最初の起動時に
```
python ytviewcount.py --noauth_local_webserver
```
のようにオプションを付けます。

```
Go to the following link in your browser:
```
というメッセージに続けて、認証用のURLが表示されるのでこのURLをMac等のブラウザで開き自分のGoogleアカウントの認証を行います。認証が成功するとブラウザにvirification codeが表示されるのでこれをコピーして、サーバのコンソールに表示される
```
Enter verification code:
```
に続けて入力します。
