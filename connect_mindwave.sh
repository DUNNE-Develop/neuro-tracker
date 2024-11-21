#!/bin/bash

DEVICE_MAC="E0:7D:EA:E6:46:54"  # Dirección MAC de tu MindWave
sleep 2

# Paso 1: Conectar el dispositivo usando bluetoothctl
echo -e "power on\nconnect $DEVICE_MAC\nexit" | bluetoothctl
sleep 2

# Paso 2: Configurar RFCOMM
sudo rfcomm connect hci0 $DEVICE_MAC
sleep 2
