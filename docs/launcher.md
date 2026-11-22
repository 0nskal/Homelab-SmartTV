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

## Look and smart-home widget

- **Background:** a perspective dot grid slowly waves, with accent-coloured patches of varied size drifting over it. It uses the `--acc` colour and runs on a plain 2D canvas at about 25 fps. Set `wallpaper` in `config.js` to replace it with your own image.
- **Carousel:** the focused icon is big and labelled, the rest are smaller and dimmed.
- **Lights widget (optional, Tuya):** smart plugs and lamps that work in the Tuya Smart / Smart Life app (for example LSC Smart Connect from Action) show up as tiles in the top right. Press UP from the app row, OK toggles; the wide button under the tiles turns everything on or off (commands go out one by one and are verified, because some plugs drop commands sent at once). It is hidden when `assets/tuya.json` is missing.
  1. On iot.tuya.com create a Cloud project (Smart Home, your data centre; Central Europe for Poland) and enable *IoT Core* and *Authorization Token Management*.
  2. In the project: Devices, Link App Account, scan the QR code in the Tuya Smart app.
  3. Copy `launcher/assets/tuya.example.json` to `launcher/assets/tuya.json`, fill in the Access ID and Secret and list your devices (`id`, `name`, `code`, usually `switch`; some plugs use `switch_1`). The file is git-ignored, never commit it.
  4. Rebuild and install. The keys end up only inside your own APK.
  The free IoT Core service on a Tuya developer account is time-limited and has to be renewed in the console now and then; if every tile shows "no connection", check that first.

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

## Wygląd i widżet smart home

- **Tło:** siatka kropek w perspektywie powoli faluje, a po niej dryfują plamy w kolorze akcentu o różnej wielkości. Używa koloru `--acc` i zwykłego canvasu 2D przy ok. 25 klatkach na sekundę. Ustaw `wallpaper` w `config.js`, żeby zastąpić je własnym obrazem.
- **Karuzela:** zaznaczona ikona jest duża i podpisana, pozostałe mniejsze i przygaszone.
- **Widżet świateł (opcjonalny, Tuya):** gniazdka i lampki działające w aplikacji Tuya Smart / Smart Life (np. LSC Smart Connect z Action) pojawiają się jako kafelki w prawym górnym rogu. Strzałka w górę z rzędu aplikacji, OK przełącza; szeroki przycisk pod kafelkami włącza lub wyłącza wszystko (polecenia idą po kolei i są weryfikowane, bo niektóre gniazdka gubią komendy wysłane naraz). Gdy brakuje `assets/tuya.json`, widżet jest ukryty.
  1. Na iot.tuya.com utwórz projekt Cloud (Smart Home, Twoje centrum danych; dla Polski Central Europe) i włącz *IoT Core* oraz *Authorization Token Management*.
  2. W projekcie: Devices, Link App Account, zeskanuj kod QR w aplikacji Tuya Smart.
  3. Skopiuj `launcher/assets/tuya.example.json` do `launcher/assets/tuya.json`, wpisz Access ID i Secret oraz listę urządzeń (`id`, `name`, `code`, zwykle `switch`; niektóre gniazdka mają `switch_1`). Plik jest w `.gitignore`, nigdy go nie commituj.
  4. Przebuduj i zainstaluj. Klucze trafiają tylko do Twojego APK.
  Darmowa usługa IoT Core na koncie deweloperskim Tuya jest czasowa i trzeba ją co jakiś czas odnowić w konsoli; jeśli wszystkie kafelki pokazują "brak połączenia", sprawdź to najpierw.

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
