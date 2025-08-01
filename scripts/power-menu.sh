#!/bin/bash

# Opciones del menú
options="⏻  Power Off\n  Reboot\n  Suspend\n  Hibernate\n  Lock\n󰜺  Cancel"

# Mostrar el menú con Rofi
choice=$(echo -e "$options" | rofi -dmenu -i -p "Power Menu")

case "$choice" in
    "⏻  Power Off")
        systemctl poweroff
        ;;
    "  Reboot")
        systemctl reboot
        ;;
    "  Suspend")
        systemctl suspend
        ;;
    "  Hibernate")
        systemctl hibernate
        ;;
    "  Lock")
        hyprlock
        ;;
    "󰜺  Cancel")
        # Simplemente salir sin hacer nada
        exit 0
        ;;
    *)
        # Si se cierra sin elegir, no hacer nada
        exit 0
        ;;
esac