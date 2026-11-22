# Troubleshooting

Format: **Problem** → cause → fix.

## Connection

- **Port 5555 closed / connection refused** → network ADB is off, or Android 11+ (port is random) → enable USB debugging (Android 9–10) or Wireless debugging (11+), see [enable-adb.md](enable-adb.md).
- **`unauthorized` / `failed to authenticate` / `still authorizing`** → the TV did not get your approval → accept the dialog on the TV with "Always allow". If no dialog: Developer options → "Revoke USB debugging authorizations", then retry. Also `adb kill-server` and reconnect.
- **`device offline`, connection drops often** → weak TV Wi-Fi, TV asleep, or an overloaded TV (load average around 100 with 1.4 GB RAM) → diagnose: open repeated TCP connections from the computer to the TV on the LAN and measure loss and latency; ping the router for comparison. If only the TV is bad, fix: LAN cable, change the 5 GHz channel, move the router closer, reboot the TV.
- **After a TV reboot it does not connect** → authorization or port reset → reconnect (`adb connect`), approve again; on Android 11+ the port changes (`adb mdns services`).
- **Android 11+ pairing fails** → pairing code and port differ from the connect port and both expire → run `adb pair IP:PAIRPORT`, then `adb connect IP:PORT` using the port from `adb mdns services`.
- **Network scan does not find the TV** → TV asleep, different subnet, VLAN, or Wi-Fi AP isolation → wake the TV, use the same subnet, disable client isolation.
- **Several adb devices** → use `adb -s 192.168.1.50:5555 ...`.
- **`adb` not in PATH** → `tv.py` downloads platform-tools into `tools/` and uses it; for manual use run `tools/platform-tools/adb`.
- **Samsung / LG do not work** → they have no ADB, see [enable-adb.md](enable-adb.md).
- **Fire OS** → ADB debugging is under Settings → My Fire TV → Developer options. Some system packages cannot be disabled and updates may re-enable them.

## Shells on Windows

- **Git Bash mangles `/sdcard/...`** → set `MSYS_NO_PATHCONV=1` before the command.
- **`adb pull` to a path like `/c/...`** → use a Windows path (`C:\...`) in PowerShell, or a relative path.
- **PowerShell vs Bash** → quoting and path rules differ. Use one shell consistently; in PowerShell quote arguments with spaces.

## Performance

- **YouTube/streaming stutters even at low resolution** → usually the Wi-Fi link, not the system. On a weak SoC, VP9/AV1 and 4K/60 are heavy. With 1.4 GB RAM and full swap everything is slow → test the network first, lower the quality, reboot.
- **Launcher animation is choppy or the remote feels laggy** → weak GPU and full swap. Set the animation scales to 0.5, force-stop apps that linger in the background (`adb shell am force-stop <package>`), reboot after days of uptime. The launcher already throttles its background while you navigate; to remove the cost completely set a `wallpaper` in `config.js` (static image, no animation).
- **Tuya tile says "no connection"** → the IoT Core service of your developer project expired (free tier is time-limited, renew it in the console), or the keys in `launcher/assets/tuya.json` are wrong, or the TV has no internet.
- **A smart plug ignores commands (cloud says success, state does not change)** → the plug itself (weak Wi-Fi, firmware). Check that it reacts from the Tuya Smart app; sending commands one at a time helps, which the "all on/off" button already does, with verification and up to two retries.
- **`TotalTime: 0`** → invalid measurement (app already in foreground) → close the app, retry.

## After changes

- **Something stopped working after a package was disabled** → `adb shell pm enable PKG` (see [debloat.md](debloat.md#restoring)).
- **`pm uninstall` fails (no space / permission)** → the package is protected or storage is full → use `pm disable-user --user 0 PKG` instead.
- **HOME does not open the custom launcher** → `launcherx` and `setupwraith` have higher HOME priority → disable both, see [launcher.md](launcher.md).
- **"Apps only" mode removed the Play Store from home** → expected behavior of Google TV; use a custom launcher with a tile for the Store.
- **Apps missing from the launcher list** → Android package visibility; the launcher needs the `QUERY_ALL_PACKAGES` permission (declared in its manifest) to list installed apps.

## Backups

- **Backup is large** → it contains full package lists and all settings namespaces. MAC addresses and serial numbers are masked; other settings stay as is. Review before sharing, see [privacy.md](privacy.md).

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Rozwiązywanie problemów

Format: **Problem** → przyczyna → rozwiązanie.

## Połączenie

- **Port 5555 zamknięty / connection refused** → ADB po sieci wyłączone albo Android 11+ (port jest losowy) → włącz Debugowanie USB (Android 9–10) lub Debugowanie bezprzewodowe (11+), zobacz [enable-adb.md](enable-adb.md).
- **`unauthorized` / `failed to authenticate` / `still authorizing`** → TV nie dostał Twojej zgody → zatwierdź okno na TV, „Zawsze zezwalaj”. Jeśli okna nie ma: Opcje programisty → „Odwołaj dostęp do debugowania USB”, potem ponów. Zrób też `adb kill-server` i połącz ponownie.
- **`device offline`, częste zrywanie połączenia** → słabe Wi-Fi telewizora, TV w uśpieniu albo przeciążony TV (load average rzędu 100 przy 1.4 GB RAM) → diagnoza: wielokrotne połączenia TCP z komputera do TV w LAN i pomiar strat i opóźnień; dla porównania ping do routera. Jeśli zły jest tylko TV, naprawa: kabel LAN, zmiana kanału 5 GHz, bliższy router, restart TV.
- **Po restarcie TV nie łączy** → reset autoryzacji lub portu → połącz ponownie (`adb connect`), zatwierdź jeszcze raz; na Androidzie 11+ port się zmienia (`adb mdns services`).
- **Parowanie na Androidzie 11+ nie działa** → kod i port parowania są inne niż port połączenia i oba wygasają → `adb pair IP:PORTPAROWANIA`, potem `adb connect IP:PORT` na port z `adb mdns services`.
- **Skan sieci nie widzi TV** → TV uśpiony, inna podsieć, VLAN albo izolacja klientów Wi-Fi (AP isolation) → obudź TV, użyj tej samej podsieci, wyłącz izolację klientów.
- **Wiele urządzeń adb** → użyj `adb -s 192.168.1.50:5555 ...`.
- **`adb` nie ma w PATH** → `tv.py` pobiera platform-tools do `tools/` i go używa; ręcznie uruchom `tools/platform-tools/adb`.
- **Samsung / LG nie działają** → nie mają ADB, zobacz [enable-adb.md](enable-adb.md).
- **Fire OS** → debugowanie ADB jest w Ustawienia → Mój Fire TV → Opcje programisty. Niektórych pakietów systemowych nie da się wyłączyć, a aktualizacje mogą je włączyć z powrotem.

## Powłoki w Windows

- **Git Bash psuje ścieżki `/sdcard/...`** → ustaw `MSYS_NO_PATHCONV=1` przed poleceniem.
- **`adb pull` do ścieżki typu `/c/...`** → użyj ścieżki Windows (`C:\...`) w PowerShellu albo ścieżki względnej.
- **PowerShell a Bash** → inne zasady cytowania i ścieżek. Trzymaj się jednej powłoki; w PowerShellu cytuj argumenty ze spacjami.

## Wydajność

- **YouTube/streaming się tnie nawet w niskiej rozdzielczości** → zwykle winne jest łącze Wi-Fi, nie system. Na słabym SoC VP9/AV1 i 4K/60 są ciężkie. Przy 1.4 GB RAM i pełnym swapie wszystko zwalnia → najpierw sprawdź sieć, obniż jakość, zrestartuj TV.
- **Animacja launchera się tnie albo pilot ma opóźnienie** → słaby GPU i pełny swap. Ustaw skale animacji na 0.5, zamknij aplikacje zalegające w tle (`adb shell am force-stop <pakiet>`), zrestartuj TV po kilku dniach pracy. Launcher sam zwalnia tło podczas nawigacji; żeby całkiem usunąć koszt, ustaw `wallpaper` w `config.js` (statyczny obraz, bez animacji).
- **Kafelek Tuya pokazuje „brak połączenia”** → wygasła usługa IoT Core w projekcie deweloperskim (darmowa jest czasowa, odnów w konsoli), albo klucze w `launcher/assets/tuya.json` są błędne, albo TV nie ma internetu.
- **Gniazdko ignoruje polecenia (chmura mówi „sukces”, stan się nie zmienia)** → wina gniazdka (słabe Wi-Fi, firmware). Sprawdź, czy reaguje z aplikacji Tuya Smart; pomaga wysyłanie poleceń po jednym, co robi przycisk „włącz/wyłącz wszystko” z weryfikacją i dwoma ponowieniami.
- **`TotalTime: 0`** → nieważny pomiar (aplikacja już na pierwszym planie) → zamknij aplikację, powtórz.

## Po zmianach

- **Po wyłączeniu pakietu coś przestało działać** → `adb shell pm enable PKG` (zobacz [debloat.md](debloat.md#restoring)).
- **`pm uninstall` nie działa (brak miejsca / uprawnienia)** → pakiet jest chroniony albo brakuje miejsca → użyj `pm disable-user --user 0 PKG`.
- **HOME nie otwiera własnego launchera** → `launcherx` i `setupwraith` mają wyższy priorytet HOME → wyłącz oba, zobacz [launcher.md](launcher.md).
- **Tryb „tylko aplikacje” usunął Sklep Play z ekranu głównego** → tak działa Google TV; użyj własnego launchera z kafelkiem Sklepu.
- **Brak aplikacji na liście launchera** → widoczność pakietów w Androidzie; launcher potrzebuje uprawnienia `QUERY_ALL_PACKAGES` (zadeklarowane w jego manifeście), żeby wylistować zainstalowane aplikacje.

## Backupy

- **Backup jest duży** → zawiera pełne listy pakietów i wszystkie przestrzenie ustawień. Adresy MAC i numery seryjne są maskowane; reszta ustawień zostaje bez zmian. Przejrzyj przed udostępnieniem, zobacz [privacy.md](privacy.md).

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
