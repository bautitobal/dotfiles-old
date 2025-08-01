#!/bin/bash

# Obtener información del disco raíz
read -r used total percent <<< $(df -h / | awk 'NR==2 {print $3, $2, $5}')

# Mostrar con ícono y porcentaje
echo " $used / $total ($percent)"