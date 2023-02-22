#!/bin/zsh
# Description: Bundles the executable for distribution

echo "Bundling executable..."
pyinstaller --onefile --noconfirm --windowed --name Conquerors-of-Catan --icon=src/assets/icon.ico src/__main__.py
