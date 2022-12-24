# RY-Music

## 前言
”RY-Music“這個LineBot讓使用者能認識特定藝人，整合該藝人介紹、歷年作品總表、提供聽歌服務。

## 環境
- macOS Big Sur 11.6.8
- Python 3.11.1

## 使用教學
1. install `pipenv`
```shell
pip3 install pipenv
```
2. install 所需套件
```shell
pipenv install --three
// 若遇到pygraphviz安裝失敗，則嘗試下面這行
sudo apt-get install graphviz graphviz-dev
```
3. 從`.env.sample`產生出一個`.env`，並填入以下四個資訊

- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
- Olami
    - APP_KEY
    - APP_SECRET
4. install `ngrok`

```shell
sudo snap install ngrok
```
5. run `ngrok` to deploy Line Chat Bot locally
```shell
ngrok http 8000
```
6. execute app.py
```shell
python3 app.py
```

## 使用說明
- 基本操作
    - `music`
        - 進入音樂模式
            - 藝人介紹：藝人簡介以及Youtube/IG/FB連結
            - 作品總表：回傳歷屆作品圖片
            - 聽歌：精選十首熱門歌曲，提供Spotify/Youtube/KKBOX連結
    - `chat`
            - 切換到聊天模式
    - `restart`
        - reset所有資訊，返回initial state

## FSM
### state說明
- user:初始狀態
- initial:restart後的狀態
- input_search:音樂模式，輸入查詢項目
- intro:藝人介紹
- lists:作品總表
- intro:聽歌
- chat/chat2:聊天模式
- end:結束


## Deploy in Heroku
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    heroku config:set APP_KEY=your_olami_APP_KEY
    heroku config:set APP_SECRET=your_olami_APP_SECRET
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

