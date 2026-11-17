#!/usr/bin/env bash
# Manual APK build without Gradle: aapt2 -> javac -> R8/D8 -> zipalign -> apksigner.
# Reczny build APK bez Gradle.
#
# Usage / Uzycie:
#   ./build.sh                 build build/launcher.apk (downloads tools on first run)
#   ./build.sh install         build and `adb install -r` (needs ADB_SERIAL=<ip:port>)
#   TOOLS=/path/to/tools ./build.sh   reuse an existing tools directory
#
# Downloads (first run only, ~600 MB, official sources): Temurin JDK 21 (adoptium.net),
# Android command-line tools + platform 34 + build-tools 34.0.0 + platform-tools (dl.google.com),
# R8 (dl.google.com/dl/android/maven2). R8 replaces d8 because d8 from build-tools 34.0.0 crashes on JDK 21 classes.
set -euo pipefail
export MSYS_NO_PATHCONV=1
cd "$(dirname "$0")"

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) OS=windows; EXE=.exe; BAT=.bat ;;
  Linux*)               OS=linux;   EXE="";   BAT="" ;;
  Darwin*)              OS=mac;     EXE="";   BAT="" ;;
  *) echo "Unsupported OS"; exit 1 ;;
esac

TOOLS="${TOOLS:-$(cd .. && pwd)/tools}"
mkdir -p "$TOOLS"
TOOLS="$(cd "$TOOLS" && (pwd -W 2>/dev/null || pwd))"
SDK="$TOOLS/android-sdk"
JDK="$TOOLS/jdk"
BT="$SDK/build-tools/34.0.0"
PLATFORM="$SDK/platforms/android-34/android.jar"
ADB="$TOOLS/platform-tools/adb$EXE"
KS="$TOOLS/debug.keystore"
R8="$TOOLS/r8.jar"
OUT=build

fetch() { curl -fsSL --retry 3 -o "$2" "$1"; }

ensure_tools() {
  if [ ! -x "$JDK/bin/javac$EXE" ]; then
    echo "[tools] JDK 21 (Temurin)"
    case "$OS" in
      windows) A=windows; EXT=zip ;; linux) A=linux; EXT=tar.gz ;; mac) A=mac; EXT=tar.gz ;;
    esac
    ARCH=x64; [ "$(uname -m)" = "aarch64" -o "$(uname -m)" = "arm64" ] && ARCH=aarch64
    fetch "https://api.adoptium.net/v3/binary/latest/21/ga/$A/$ARCH/jdk/hotspot/normal/eclipse" "$TOOLS/jdk.$EXT"
    mkdir -p "$TOOLS/jdk-x"
    if [ "$EXT" = zip ]; then unzip -q -o "$TOOLS/jdk.zip" -d "$TOOLS/jdk-x"; else tar -xzf "$TOOLS/jdk.tar.gz" -C "$TOOLS/jdk-x"; fi
    rm -rf "$JDK"; mv "$TOOLS"/jdk-x/* "$JDK"; rmdir "$TOOLS/jdk-x"; rm -f "$TOOLS"/jdk.zip "$TOOLS"/jdk.tar.gz
    [ "$OS" = mac ] && [ -d "$JDK/Contents/Home" ] && JDK="$JDK/Contents/Home"
  fi
  export JAVA_HOME="$JDK"; export PATH="$(cygpath -u "$JDK" 2>/dev/null || echo "$JDK")/bin:$PATH"

  if [ ! -f "$BT/aapt2$EXE" ] || [ ! -f "$PLATFORM" ]; then
    echo "[tools] Android command-line tools, platform 34, build-tools 34.0.0"
    P=$OS; [ "$OS" = mac ] && P=mac
    fetch "https://dl.google.com/android/repository/commandlinetools-$P-11076708_latest.zip" "$TOOLS/cmdline.zip"
    mkdir -p "$SDK/cmdline-tools"; unzip -q -o "$TOOLS/cmdline.zip" -d "$SDK/cmdline-tools"
    rm -rf "$SDK/cmdline-tools/latest"; mv "$SDK/cmdline-tools/cmdline-tools" "$SDK/cmdline-tools/latest"; rm -f "$TOOLS/cmdline.zip"
    yes | "$SDK/cmdline-tools/latest/bin/sdkmanager$BAT" --sdk_root="$SDK" --licenses >/dev/null || true
    "$SDK/cmdline-tools/latest/bin/sdkmanager$BAT" --sdk_root="$SDK" "platforms;android-34" "build-tools;34.0.0"
  fi

  if [ ! -f "$ADB" ]; then
    echo "[tools] platform-tools (adb)"
    fetch "https://dl.google.com/android/repository/platform-tools-latest-$OS.zip" "$TOOLS/pt.zip"
    unzip -q -o "$TOOLS/pt.zip" -d "$TOOLS"; rm -f "$TOOLS/pt.zip"
  fi

  [ -f "$R8" ] || fetch "https://dl.google.com/dl/android/maven2/com/android/tools/r8/8.5.35/r8-8.5.35.jar" "$R8"

  if [ ! -f "$KS" ]; then
    keytool -genkeypair -keystore "$KS" -storepass android -keypass android \
      -alias debug -keyalg RSA -keysize 2048 -validity 10000 \
      -dname "CN=SmartTV Dashboard Debug,O=Homelab SmartTV" >/dev/null
  fi
}

ensure_tools

rm -rf "$OUT"; mkdir -p "$OUT/compiled" "$OUT/classes" "$OUT/dex"

echo "[1/6] aapt2 compile"
"$BT/aapt2$EXE" compile --dir res -o "$OUT/compiled"

echo "[2/6] aapt2 link"
"$BT/aapt2$EXE" link -o "$OUT/unsigned.apk" -I "$PLATFORM" \
  --manifest AndroidManifest.xml -A assets \
  --min-sdk-version 28 --target-sdk-version 34 \
  --java "$OUT/gen" "$OUT/compiled"/*.flat

echo "[3/6] javac"
javac --release 17 -classpath "$PLATFORM" -d "$OUT/classes" \
  $(find src "$OUT/gen" -name '*.java')

echo "[4/6] R8/D8"
java -cp "$R8" com.android.tools.r8.D8 --release --min-api 28 --lib "$PLATFORM" --output "$OUT/dex" \
  $(find "$OUT/classes" -name '*.class')

echo "[5/6] add classes.dex + zipalign"
cp "$OUT/dex/classes.dex" "$OUT/classes.dex"
( cd "$OUT" && jar -uf unsigned.apk classes.dex )
"$BT/zipalign$EXE" -f -p 4 "$OUT/unsigned.apk" "$OUT/aligned.apk"

echo "[6/6] apksigner"
"$BT/apksigner$BAT" sign --ks "$KS" --ks-pass pass:android --key-pass pass:android \
  --out "$OUT/launcher.apk" "$OUT/aligned.apk"

echo "OK: $OUT/launcher.apk ($(du -h "$OUT/launcher.apk" | cut -f1))"

if [ "${1:-}" = "install" ]; then
  if [ -z "${ADB_SERIAL:-}" ]; then
    echo "Set ADB_SERIAL=<ip:port> (e.g. ADB_SERIAL=192.168.1.50:5555) / Ustaw ADB_SERIAL=<ip:port>"; exit 1
  fi
  "$ADB" -s "$ADB_SERIAL" install -r "$OUT/launcher.apk"
fi
