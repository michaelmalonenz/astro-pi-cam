#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

systemctl link "$DIR"/astropicam.service
systemctl enable astropicam.service
systemctl start --no-block astropicam.service

ln -s "$DIR"/astropicam_nginx.conf /etc/nginx/sites-enabled/astropicam.conf

systemctl restart nginx
