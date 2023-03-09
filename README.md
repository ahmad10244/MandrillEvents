# Mandrill events dashboard

## Description

This project captures Mandrills events, Store them for later usage and notify some \
simple user interface in real time about those events. \
Every time new event received from Mandrill it will be saved on database \
and also notify to user interface.

## Docker

> ### **Step 1** - Download the code from the GitHub repository (using `GIT`)

``` bash
git clone https://github.com/ahmad10244/MandrillEvents && cd MandrillEvents
```

> ### **Step 2** - Start the app in Docker

``` bash
docker-compose up --build
```

Visit `http://localhost:5000/` in your browser or simply open `templates/index.html` \
in your browser to see the user interface. \
Insert app websocket url in the input box (`http://<ip>:5000/events`) and click `Connect` button.

![Home Page!](images/home.png)

> ### **Step 3** - Add app url to Mandrill webhooks

- Goto Mandrill Webhooks setting [Link](https://mandrillapp.com/settings/webhooks)
- Click on `Add a webhook` button
- Insert app webhook url on `Post To URL` input box. The app webhook url is `http://<ip>:5000/event`
- You can test app with `send test` button

## How it works

This app use [MongoDB](https://www.mongodb.com/) for saving captured events\
and [Flask](https://flask.palletsprojects.com/) For the webhook API \
and [Flask-SocketIO](https://flask-socketio.readthedocs.io/) for websocket. \
In user interface this app use [Socket.IO](https://socket.io/) for connectiong and \
communicating with backend websocket and [Bootstrap](https://getbootstrap.com/) for design. \
After an event (or events) is got through the backend webhook API from Mandrill, the events will be stored on MongoDB \
and also the app will send a notification message through the websocket to the user interface.

## Contributing

> ### **Step 1**

Install python3.10, pip3, virtualenv, MongoDB in your system

> ### **Step 2** - Clone source code from the GitHub repository and setup virtualenv

``` bash
git clone https://github.com/ahmad10244/MandrillEvents && cd MandrillEvents
python3 -m virtualenv venv
source venv/bin/activate
```

> ### **Step 3** - Install requirements

``` bash
pip install -r requirements.txt
```

> ### **Step 4** - Set configs

``` bash
export MONGODB=mongodb://username:password@host:port
export SECRET_KEY='random string with symbols, digits, chars, ...'
export MONGODB_DATABSE='MongoDB database name'
export MONGODB_DATABSE_COLLECTION='MongoDB database collection name'
```

> ### **Step 5** - Run in development mode

``` bash
python3 app.py
```

or using `gunicorn`

``` bash
gunicorn -k gevent -w 1 app:app -b 0.0.0.0:5000
```
