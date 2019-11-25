#!/bin/bash
#Place this file within [f]crontab.

CFG="${CONFIG_FILE:?CONFIG_FILE variable undefined!}"

SSH=`which ssh`
SSH="${SSH:?No SSH command found!}"

TUNNEL_HOST=`jq -r '.tunnel_host' ${CFG}`
TUNNEL_PORT=`jq -r '.tunnel_port' ${CFG}`
TUNNEL_IF=`jq -r '.tunnel_interface' ${CFG}`
REMOTE_PORT=`jq -r '.remote_port' ${CFG}`

function setupTunnel() {
    ${SSH} -f -N -T -R${TUNNEL_IF}:${TUNNEL_PORT}:0.0.0.0:${REMOTE_PORT} ${TUNNEL_HOST}
}

/bin/pidof ssh
if [[ $? -ne 0 ]]; then
    set -x
    if setupTunnel; then
        echo "Tunnel established successfully."
    else
        echo "An error occurred while connecting. Code was $?"
    fi
fi
