# Custom launcher

## Why

- Google TV "apps only" mode removes the Play Store from the home screen.
- Ready-made launchers often put features behind a paywall (for example a custom wallpaper in Premium).
- So this repo has a small launcher of its own in `launcher/`: clock, weather (Open-Meteo), app tiles.

## Architecture

- A Java app with one `WebView`.
- UI is `assets/index.html` (HTML, CSS, JS).
- A JS bridge exposes `Android.launch(pkg)`, `Android.listApps()`, `Android.icon(pkg)`.
- No Gradle: built by hand with `launcher/build.sh`.

## Configuration

Edit `launcher/assets/config.js`:

- weather location: city name and latitude/longitude,
- list of app package names shown as tiles,
- wallpaper.

## Building

```
cd launcher
./build.sh
```

The script downloads JDK 21 (Temurin), Android command-line tools, platform 34 and build-tools 34.0.0. It uses R8 instead of d8, because d8 34.0.0 crashes on JDK 21 classes.

## Installing

```
adb install -r launcher/build/launcher.apk
```

(Adjust the path to the output file printed by `build.sh`.)

## Setting it as the home screen

On Google TV, `com.google.android.apps.tv.launcherx` and `com.google.android.tungsten.setupwraith` have a higher HOME priority than any custom launcher. Disable both, then HOME opens your launcher:

```
adb shell pm disable-user --user 0 com.google.android.apps.tv.launcherx
adb shell pm disable-user --user 0 com.google.android.tungsten.setupwraith
```

Revert:

```
adb shell pm enable com.google.android.apps.tv.launcherx
adb shell pm enable com.google.android.tungsten.setupwraith
adb shell cmd package set-home-activity com.google.android.apps.tv.launcherx/.home.HomeActivity
```

On older Android TV (9) the default launcher is `com.google.android.tvlauncher`.

**Warning:** do not make it the default until you confirmed it works and you have working ADB access to undo it.

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Własny launcher

## Po co

- Tryb „tylko aplikacje” w Google TV usuwa Sklep Play z ekranu głównego.
- Gotowe launchery często mają płatne funkcje (np. własna tapeta w Premium).
- Dlatego to repo ma mały własny launcher w `launcher/`: zegar, pogoda (Open-Meteo), kafle aplikacji.

## Architektura

- Aplikacja Java z jednym `WebView`.
- Interfejs to `assets/index.html` (HTML, CSS, JS).
- Most JS udostępnia `Android.launch(pkg)`, `Android.listApps()`, `Android.icon(pkg)`.
- Bez Gradle: budowanie ręczne skryptem `launcher/build.sh`.

## Konfiguracja

Edytuj `launcher/assets/config.js`:

- lokalizacja pogody: nazwa miasta oraz współrzędne,
- lista pakietów aplikacji pokazywanych jako kafle,
- tapeta.

## Budowanie

```
cd launcher
./build.sh
```

Skrypt pobiera JDK 21 (Temurin), Android command-line tools, platformę 34 i build-tools 34.0.0. Używa R8 zamiast d8, bo d8 34.0.0 wywala się na klasach JDK 21.

## Instalacja

```
adb install -r launcher/build/launcher.apk
```

(Dostosuj ścieżkę do pliku wyjściowego, który wypisze `build.sh`.)

## Ustawienie jako ekran główny

Na Google TV pakiety `com.google.android.apps.tv.launcherx` i `com.google.android.tungsten.setupwraith` mają wyższy priorytet HOME niż własny launcher. Wyłącz oba, wtedy HOME otworzy Twój launcher:

```
adb shell pm disable-user --user 0 com.google.android.apps.tv.launcherx
adb shell pm disable-user --user 0 com.google.android.tungsten.setupwraith
```

Powrót:

```
adb shell pm enable com.google.android.apps.tv.launcherx
adb shell pm enable com.google.android.tungsten.setupwraith
adb shell cmd package set-home-activity com.google.android.apps.tv.launcherx/.home.HomeActivity
```

Na starszych Android TV (9) domyślny launcher to `com.google.android.tvlauncher`.

**Ostrzeżenie:** nie ustawiaj własnego launchera jako domyślnego, dopóki nie sprawdzisz, że działa i że masz działający ADB do cofnięcia zmian.

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
