#!/bin/bash

readonly script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
readonly install_dir="/etc/systemd/system/"

if [ "$script_dir" != "/opt/worfometer" ]; then
    echo "I didn't make this thing flexible, put it in /opt/worfometer and try again."
    exit 1
fi

set -e

rm -f /etc/nginx/sites-enabled/*
ln -s -f "${script_dir}/web/worfometer-nginx.conf" "/etc/nginx/nginx.conf"
systemctl reload nginx

ln -s -f "${script_dir}/monitor/worfometer-monitor.service" "${install_dir}"
ln -s -f "${script_dir}/web/worfometer-web.service" "${install_dir}"

systemctl daemon-reload

systemctl enable worfometer-monitor.service
systemctl enable worfometer-web.service

systemctl start worfometer-monitor.service
systemctl start worfometer-web.service
