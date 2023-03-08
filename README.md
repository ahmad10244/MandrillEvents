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
to see the user interface. \
Insert app websocket url (`http://<ip>:5000/events`) and click `Connect` button.

![Home Page!](images/home.png)

> ### **Step 3** - Add app url to Mandrill webhooks

- Goto Mandrill Webhooks setting [Link](https://mandrillapp.com/settings/webhooks)
- Click on `Add a webhook` button
- Put app url on `Post To URL`. The app webhook url is `http://<ip>:5000/events`
- You can test app with `send test` button
