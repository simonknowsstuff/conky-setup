#!/bin/sh
CURRENT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")/")
echo "Installing requests"
python -m pip install requests

read -p "Enter the latitude of your location: " latitude
read -p "Enter the longitude of your location: " longitude
echo -e "$latitude\n$longitude" > lat_lon.txt

echo "Copying files to ~/.local/share/conky-weather"
mkdir -p ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/weather-icons ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/forecast_data.py ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/.conkyrc ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/lat_lon.txt ~/.local/share/conky-weather/
python ~/.local/share/conky-weather/forecast_data.py
echo "Run conky -c ~/.local/share/conky-weather/.conkyrc to run configuration."
