#!/bin/bash
set -e

APPDIR="AppDir"
APPIMAGE_NAME="hei-vpn"
APPIMAGE_TOOL="./tools/appimagetool.AppImage"

echo "🧹 Nettoyage..."
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

echo "🛠 Construction du binaire avec PyInstaller..."
pyinstaller hei_vpn.spec

echo "📦 Copie des fichiers nécessaires dans AppDir..."
cp dist/$APPIMAGE_NAME "$APPDIR/"
cp resources/AppRun "$APPDIR/"
cp resources/hei-vpn.desktop "$APPDIR/usr/share/applications/"
cp resources/hei-vpn.desktop "$APPDIR/"
cp resources/hei-vpn.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/"
cp resources/hei-vpn.png "$APPDIR/"

echo "🔍 Vérification de appimagetool..."
if [ ! -f "$APPIMAGE_TOOL" ]; then
  echo "⬇️  Téléchargement de appimagetool..."
  mkdir -p tools
  curl -L "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage" -o "$APPIMAGE_TOOL"
  chmod +x "$APPIMAGE_TOOL"
fi

echo "🔍 Vérification du contenu de hei-vpn.desktop"
cat "$APPDIR/usr/share/applications/hei-vpn.desktop"

echo "📦 Création de l'AppImage..."
"$APPIMAGE_TOOL" "$APPDIR" "$APPIMAGE_NAME.AppImage"

echo "✅ Fini ! AppImage générée : $APPIMAGE_NAME.AppImage"
