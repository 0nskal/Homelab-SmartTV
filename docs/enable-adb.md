# Enabling ADB

## Developer options (all Android devices)

1. Settings → Device Preferences → About.
2. Tap **Build number** 7 times. A message says you are a developer.
3. Go back: **Developer options** now exists (under Device Preferences or System).

## Android TV 9–10

1. Developer options → turn on **USB debugging**. On these versions this also opens ADB over the network on port 5555.
2. Run `python tv.py <brand> --ip 192.168.1.50`.
3. A dialog appears on the TV: "Allow USB debugging?". Tick **Always allow**, confirm.

## Android 11+ and Chromecast with Google TV

Port 5555 is closed by default. Use wireless debugging.

1. Developer options → turn on **Wireless debugging**.
2. Choose **Pair device with pairing code**. The TV shows a 6-digit code and `IP:port` for pairing.
3. On the computer: `adb pair 192.168.1.50:PAIRPORT` and enter the code (or `python tv.py <brand> --pair 192.168.1.50:PAIRPORT CODE`).
4. The connection port is different and random. Find it on the Wireless debugging screen or run `adb mdns services`.
5. `adb connect 192.168.1.50:CONNECTPORT` (or `python tv.py <brand> --ip 192.168.1.50 --port CONNECTPORT`).

The pairing code and pairing port expire quickly. If pairing fails, open the pairing dialog again for a fresh pair.

## Brands without ADB

- **Samsung Tizen:** no ADB. Enable Developer Mode (Apps → type 12345 on the remote → set the host IP), then use `sdb` from Tizen Studio. Debloating is very limited.
- **LG webOS:** no ADB. Enable Developer Mode (Developer Mode app from LG Content Store), then use `ares-cli`. Rooting tools such as Homebrew Channel exist, but follow their own docs and risks.
- **Roku:** no ADB. Developer mode exists only for sideloading your own channels.
- **Alternative for all of them:** block ads and telemetry at network level with Pi-hole or AdGuard Home, set as the DNS server on the router or on the TV.

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Włączanie ADB

## Opcje programisty (każdy Android)

1. Ustawienia → Preferencje urządzenia → Informacje.
2. Kliknij **Numer kompilacji** 7 razy. Pojawi się komunikat, że jesteś programistą.
3. Wróć: jest już **Opcje programisty** (w Preferencjach urządzenia albo w Systemie).

## Android TV 9–10

1. Opcje programisty → włącz **Debugowanie USB**. Na tych wersjach otwiera to też ADB po sieci na porcie 5555.
2. Uruchom `python tv.py <marka> --ip 192.168.1.50`.
3. Na TV pojawi się okno „Zezwolić na debugowanie USB?”. Zaznacz **Zawsze zezwalaj**, potwierdź.

## Android 11+ i Chromecast z Google TV

Port 5555 jest domyślnie zamknięty. Użyj debugowania bezprzewodowego.

1. Opcje programisty → włącz **Debugowanie bezprzewodowe**.
2. Wybierz **Sparuj urządzenie za pomocą kodu**. TV pokaże 6-cyfrowy kod i `IP:port` do parowania.
3. Na komputerze: `adb pair 192.168.1.50:PORTPAROWANIA` i wpisz kod (albo `python tv.py <marka> --pair 192.168.1.50:PORTPAROWANIA KOD`).
4. Port połączenia jest inny i losowy. Zobaczysz go na ekranie Debugowania bezprzewodowego albo w `adb mdns services`.
5. `adb connect 192.168.1.50:PORTPOLACZENIA` (albo `python tv.py <marka> --ip 192.168.1.50 --port PORTPOLACZENIA`).

Kod i port parowania szybko wygasają. Jeśli parowanie nie działa, otwórz okno parowania ponownie, żeby dostać nowe dane.

## Marki bez ADB

- **Samsung Tizen:** brak ADB. Włącz Developer Mode (Aplikacje → wpisz 12345 na pilocie → ustaw IP hosta), potem użyj `sdb` z Tizen Studio. Odchudzanie jest bardzo ograniczone.
- **LG webOS:** brak ADB. Włącz Developer Mode (aplikacja Developer Mode z LG Content Store), potem użyj `ares-cli`. Istnieją narzędzia z rootem, np. Homebrew Channel, ale stosuj się do ich własnej dokumentacji i ryzyka.
- **Roku:** brak ADB. Tryb programisty służy tylko do instalowania własnych kanałów.
- **Alternatywa dla wszystkich:** blokuj reklamy i telemetrię na poziomie sieci przez Pi-hole albo AdGuard Home, ustawione jako serwer DNS na routerze lub w TV.

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
