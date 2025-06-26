# GTNH Discord Bot

## Dev Setup

1. Fill in your Discord Api Token and Database Password (```.env.example```)
2. Rename ```.env.example``` into ```.env```
3. Open Terminal ```docker compose up```


### Systemd
1. Fill user and path to this repo in gtnh-discord-bot.service
2. Copy gtnh-discord-bot.service to /lib/systemd/system/ (``sudo cp gtnh-discord-bot.service /lib/systemd/system/``)
3. ``sudo systemctl daemon-reload``
4. ``sudo systemctl enable gtnh-discord-bot.service``
5. ``sudo systemctl restart gtnh-discord-bot.service``