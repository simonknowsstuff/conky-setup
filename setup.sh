CURRENT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")/")
echo "Copying files to ~/.cache/conky-weather"
mkdir -p ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/weather-icons ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/forecast_data.py ~/.local/share/conky-weather/
cp -r $CURRENT_DIR/.conkyrc ~/.local/share/conky-weather/
echo "Run conky -c ~/.local/share/conky-weather/.conkyrc to run configuration."