# Privacy

## Backups

- Backups in `devices/` contain package lists and device settings.
- `tv.py` masks MAC addresses and serial numbers. It cannot know what else a vendor stores in settings: account names, Wi-Fi SSIDs, device names, IP addresses.
- Before you publish anything, search the backup:

```
grep -rniE "ssid|account|mail|@|([0-9]{1,3}\.){3}[0-9]{1,3}" devices/
```

and read the result by hand.

## Rules

- `devices/` is in `.gitignore`. Do not force-add it. Do not commit it to a public fork.
- No keys, tokens, passwords or your network's IP addresses in issues or pull requests. Use `192.168.1.50` and `XX:XX:XX:XX:XX:XX` in examples.
- `logcat` output can contain personal data (accounts, app activity, network names). Trim it before sharing.
- Screenshots of the TV can show account names and recommendations. Crop or blur them.

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Prywatność

## Backupy

- Backupy w `devices/` zawierają listy pakietów i ustawienia urządzenia.
- `tv.py` maskuje adresy MAC i numery seryjne. Nie wie, co jeszcze producent trzyma w ustawieniach: nazwy kont, SSID Wi-Fi, nazwy urządzeń, adresy IP.
- Zanim cokolwiek opublikujesz, przeszukaj backup:

```
grep -rniE "ssid|account|mail|@|([0-9]{1,3}\.){3}[0-9]{1,3}" devices/
```

i przeczytaj wynik ręcznie.

## Zasady

- `devices/` jest w `.gitignore`. Nie dodawaj go na siłę. Nie commituj go do publicznego forka.
- Żadnych kluczy, tokenów, haseł ani adresów IP swojej sieci w zgłoszeniach (issues) i pull requestach. W przykładach używaj `192.168.1.50` i `XX:XX:XX:XX:XX:XX`.
- Wynik `logcat` może zawierać dane osobiste (konta, aktywność aplikacji, nazwy sieci). Przytnij go przed udostępnieniem.
- Zrzuty ekranu TV mogą pokazywać nazwy kont i rekomendacje. Przytnij je lub zamaż.

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
