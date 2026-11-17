# Debloating

## Judging a package

- Read the package name: `com.vendor.component`. The vendor part tells who owns it.
- List packages with paths, including disabled ones: `adb shell pm list packages -f -u`.
- Inspect one: `adb shell dumpsys package com.example.app` (components, permissions, whether it handles HOME, install location).
- If you cannot tell what it does, do not disable it.

## Usually safe to disable

- Vendor telemetry and analytics.
- Store demo / retail mode packages.
- Recommendation overlays (PatchWall-style content feeds).
- Vendor media players and galleries you do not use.
- Feedback and bugreport tools.
- Play Games, Play Movies & TV.

## Do not touch

- The launcher (the active HOME app).
- Google Play services (`com.google.android.gms`) and Google Play Store.
- Settings, setup wizard, system UI, input and remote services, Bluetooth, network, DRM.

## disable-user vs uninstall

- `pm disable-user --user 0 PKG`: hides and stops the package, keeps the APK. Reversible. Use for system packages.
- `pm uninstall --user 0 PKG`: removes it for user 0. Use for normal third-party apps (they come back from the store). On system packages it is harder to undo.

## Restoring

- `adb shell pm enable PKG`
- `adb shell cmd package install-existing PKG` (brings back an uninstalled system package)
- Last resort: factory reset.

## Animations 0.5x

Makes weak TVs feel faster:

```
adb shell settings put global window_animation_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global animator_duration_scale 0.5
```

Set `1.0` to revert.

## Reboot

Long uptime plus little RAM hurts. Example: a TV with 1.4 GB RAM after 21 days had its swap almost full and was sluggish. Reboot it from time to time (check with `adb shell cat /proc/meminfo` and `adb shell uptime`).

## Measuring speed

- App start time: `adb shell am start -W -n PKG/ACTIVITY`. Read `TotalTime` (ms). Run it 3–5 times, compare before and after.
- Memory: `adb shell cat /proc/meminfo` (MemAvailable, SwapTotal, SwapFree).
- Note: `TotalTime: 0` means the measurement is invalid (app already in foreground, or activity not launched). Close the app and retry.

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Odchudzanie systemu

## Jak ocenić pakiet

- Przeczytaj nazwę pakietu: `com.producent.komponent`. Człowiek z nazwy poznaje właściciela.
- Lista pakietów ze ścieżkami, także wyłączonych: `adb shell pm list packages -f -u`.
- Szczegóły jednego: `adb shell dumpsys package com.example.app` (komponenty, uprawnienia, czy obsługuje HOME, miejsce instalacji).
- Jeśli nie wiesz, co robi, nie wyłączaj.

## Zwykle bezpieczne do wyłączenia

- Telemetria i analityka producenta.
- Pakiety demo sklepowego / trybu retail.
- Nakładki z rekomendacjami (w stylu PatchWall).
- Odtwarzacze i galerie producenta, których nie używasz.
- Narzędzia feedback i bugreport.
- Play Gry, Play Filmy.

## Nie ruszać

- Launchera (aktywnej aplikacji HOME).
- Usług Google Play (`com.google.android.gms`) i Sklepu Google Play.
- Ustawień, kreatora konfiguracji (setup), system UI, usług pilota i wejść, Bluetooth, sieci, DRM.

## disable-user a uninstall

- `pm disable-user --user 0 PKG`: ukrywa i zatrzymuje pakiet, zostawia APK. Odwracalne. Używaj dla pakietów systemowych.
- `pm uninstall --user 0 PKG`: usuwa dla użytkownika 0. Używaj dla zwykłych aplikacji 3rd-party (wrócą ze sklepu). Dla pakietów systemowych trudniej to cofnąć.

## Przywracanie {#restoring}

- `adb shell pm enable PKG`
- `adb shell cmd package install-existing PKG` (przywraca odinstalowany pakiet systemowy)
- Ostateczność: reset fabryczny.

## Animacje 0.5×

Słabe telewizory działają wtedy żwawiej:

```
adb shell settings put global window_animation_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global animator_duration_scale 0.5
```

Wróć do `1.0`, żeby cofnąć.

## Restart

Długi uptime i mało RAM-u szkodzą. Przykład: TV z 1.4 GB RAM po 21 dniach miał prawie pełny swap i mulił. Restartuj go co jakiś czas (sprawdź: `adb shell cat /proc/meminfo` i `adb shell uptime`).

## Mierzenie szybkości

- Czas startu aplikacji: `adb shell am start -W -n PKG/ACTIVITY`. Czytaj `TotalTime` (ms). Zrób 3–5 pomiarów, porównaj przed i po.
- Pamięć: `adb shell cat /proc/meminfo` (MemAvailable, SwapTotal, SwapFree).
- Uwaga: `TotalTime: 0` oznacza nieważny pomiar (aplikacja już na pierwszym planie albo activity się nie uruchomiło). Zamknij aplikację i powtórz.

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
