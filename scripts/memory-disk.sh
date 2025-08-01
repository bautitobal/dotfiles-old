#!/bin/bash

STATE_FILE="/tmp/memory_disk_state"

# Si no existe el archivo, asumimos RAM por defecto
if [ ! -f "$STATE_FILE" ]; then
    echo "RAM" > "$STATE_FILE"
fi

STATE=$(cat "$STATE_FILE")

if [ "$1" = "toggle" ]; then
    if [ "$STATE" = "RAM" ]; then
        echo "DISK" > "$STATE_FILE"
    else
        echo "RAM" > "$STATE_FILE"
    fi
    exit 0
fi

if [ "$STATE" = "RAM" ]; then
    used=$(free -h | awk '/Mem:/ {print $3}' | sed 's/i//g')
    total=$(free -h | awk '/Mem:/ {print $2}' | sed 's/i//g')
    percent=$(free | awk '/Mem:/ {printf("%.0f", $3/$2 * 100)}')

    # Espacio entre ícono y texto
    echo "{\"text\": \"<span color='#b48ead'>  </span>${used} (${percent}%)\", \"tooltip\": \"${used} / ${total} (${percent}%)\"}"
else
    read -r used total percent <<< $(df -h / | awk 'NR==2 {print $3, $2, $5}' | sed 's/i//g')

    echo "{\"text\": \"<span color='#b48ead'>  </span>${used} (${percent})\", \"tooltip\": \"${used} / ${total} (${percent})\"}"
fi

