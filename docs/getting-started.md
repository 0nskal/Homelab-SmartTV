# Getting started

## Requirements

- Python 3.10 or newer.
- Computer and TV on the same LAN (same subnet, no Wi-Fi client isolation).
- A TV or box running Android TV / Google TV / Fire OS.
- Nothing else to install. `tv.py` downloads `adb` (platform-tools) into `tools/` by itself.

## Steps

1. **Enable ADB on the TV.** See [enable-adb.md](enable-adb.md). Note the TV's IP address (Settings → Network), e.g. `192.168.1.50`.
2. **Get the repo.** `git clone` it or download the ZIP, then open a terminal in the folder.
3. **Check the profiles.** `python tv.py --list-profiles` lists brands: sony, philips, tcl, xiaomi, hisense, tv-box, firetv, samsung, lg, roku, android-tv.
4. **Connect and back up.** Run `python tv.py sony --ip 192.168.1.50`. Accept the authorization prompt on the TV ("Always allow"). On Android 11+ pair first: `python tv.py sony --pair 192.168.1.50:37215 123456` (pairing port and code come from the TV screen). The script saves the package list and settings to `devices/` (MAC addresses and serial numbers are masked).
5. **Review the bloatware list.** The script prints packages from the brand profile that are installed on your TV. Read each name. Remove from the list anything you use.
6. **Disable in small batches.** `python tv.py sony --ip 192.168.1.50 --disable com.example.demo com.example.feedback`. Test the TV. Undo with `--enable com.example.demo`.

Use `--lang pl` for Polish output, `--name NAME` to label the backup folder, `--port N` for a non-default port.

## Safety rules

- Back up first. Always.
- For system packages use `pm disable-user` (reversible), not uninstall.
- Change a few packages at a time, then test. Reboot the TV once between batches.
- Never touch: the launcher, Google services (`gms`), Google Play Store, Settings, setup wizard packages.
- If something breaks, see [troubleshooting.md](troubleshooting.md) and [debloat.md](debloat.md#restoring).

## Safety note

You use this at your own risk and only on devices you own. Changes are reversible, but there is no warranty.

---

# Pierwsze kroki

## Wymagania

- Python 3.10 lub nowszy.
- Komputer i telewizor w tej samej sieci LAN (ta sama podsieć, bez izolacji klientów Wi-Fi).
- Telewizor lub przystawka z Android TV / Google TV / Fire OS.
- Nic więcej nie trzeba instalować. `tv.py` sam pobiera `adb` (platform-tools) do `tools/`.

## Kroki

1. **Włącz ADB na telewizorze.** Zobacz [enable-adb.md](enable-adb.md). Zapisz adres IP telewizora (Ustawienia → Sieć), np. `192.168.1.50`.
2. **Pobierz repo.** `git clone` albo ZIP, potem otwórz terminal w folderze.
3. **Sprawdź profile.** `python tv.py --list-profiles` pokazuje marki: sony, philips, tcl, xiaomi, hisense, tv-box, firetv, samsung, lg, roku, android-tv.
4. **Połącz i zrób backup.** Uruchom `python tv.py sony --ip 192.168.1.50`. Zatwierdź okno autoryzacji na TV („Zawsze zezwalaj”). Na Androidzie 11+ najpierw sparuj: `python tv.py sony --pair 192.168.1.50:37215 123456` (port i kod parowania są na ekranie TV). Skrypt zapisze listę pakietów i ustawienia w `devices/` (adresy MAC i numery seryjne są maskowane).
5. **Przejrzyj listę bloatware.** Skrypt wypisze pakiety z profilu marki, które są na Twoim TV. Przeczytaj każdą nazwę. Usuń z listy to, czego używasz.
6. **Wyłączaj małymi partiami.** `python tv.py sony --ip 192.168.1.50 --disable com.example.demo com.example.feedback`. Przetestuj TV. Cofnięcie: `--enable com.example.demo`.

`--lang pl` daje polskie komunikaty, `--name NAZWA` nazywa folder backupu, `--port N` ustawia inny port.

## Zasady bezpieczeństwa

- Najpierw backup. Zawsze.
- Dla pakietów systemowych używaj `pm disable-user` (odwracalne), nie odinstalowania.
- Zmieniaj kilka pakietów naraz i testuj. Zrestartuj TV raz między partiami.
- Nigdy nie ruszaj: launchera, usług Google (`gms`), Sklepu Google Play, Ustawień, pakietów kreatora konfiguracji (setup).
- Jeśli coś przestanie działać, zobacz [troubleshooting.md](troubleshooting.md) i [debloat.md](debloat.md#restoring).

## Uwaga o bezpieczeństwie

Używasz na własne ryzyko i tylko na swoich urządzeniach. Zmiany są odwracalne, ale nie dajemy gwarancji.
