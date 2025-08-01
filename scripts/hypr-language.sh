#!/bin/bash

in_block=false

hyprctl devices | while read -r line; do
    # Si empieza un nuevo teclado
    if [[ "$line" =~ ^Keyboard\ at ]]; then
        in_block=true
        keymap=""
        continue
    fi

    # Si termina el bloque (línea vacía)
    if [[ -z "$line" ]]; then
        in_block=false
        continue
    fi

    # Si estamos en el teclado correcto (main: yes)
    if $in_block && [[ "$line" =~ main:\ yes ]]; then
        # Si dentro del mismo bloque encontramos la keymap
        if [[ "$keymap" =~ active\ keymap:\ (.+) ]]; then
            full_keymap="${BASH_REMATCH[1]}"
            short_keymap=""
            
            # Abreviamos
            case "$full_keymap" in
                "Spanish (Latin American)")
                    short_keymap="LAT"
                    ;;
                "English (US)")
                    short_keymap="EN"
                    ;;
                *)
                    short_keymap="??"
                    ;;
            esac

            # Mostramos en formato JSON
            echo "{\"text\": \"   $short_keymap \", \"tooltip\": \"$full_keymap\"}"
            exit 0
        fi
    fi

    # Si estamos en un bloque, guardamos la línea del keymap si aparece
    if $in_block && [[ "$line" =~ active\ keymap:\ (.+) ]]; then
        keymap="$line"
    fi
done