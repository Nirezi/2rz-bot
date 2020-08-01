#!/usr/bin/env bash
# outputディレクトリ内のファイルをrsync over SSHで転送
# shellcheck disable=SC2164
cd /home/user/2rz-bot
git pull origin master
sudo systemctl restart bot