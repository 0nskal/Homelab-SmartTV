# Contributing

Thanks for helping. This is a hobby project, so keep changes small and safe.

## How to contribute

1. Fork the repo and create a branch (`feat/…`, `fix/…`, `docs/…`).
2. Make the change. Add or update tests in `tests/` for logic changes.
3. Run `python -m unittest discover -s tests` and `python tv.py --help`.
4. Open a pull request against `main` using the template. **Title in Conventional Commits** (`feat: add TCL profile`), description in **English and Polish**.
5. **Screenshots:** every visible change (launcher UI, docs layout, icon) needs screenshots in the PR description, before and after when you change something existing. No visible change → write `No UI change`. Upload screenshots to the `pr-screenshots` branch (one folder per PR, e.g. `pr-12/before.png`) and link them with raw URLs; do not commit them to `main`.
6. The maintainer reviews and merges. `main` is protected: PR, code owner approval, and checks `test`, `title`, `screenshots` must pass.

## Rules for content

- **No personal data.** No real IP addresses of your network, SSIDs, MAC addresses, serial numbers, accounts, emails, or device dumps in code, docs, issues, or screenshots. Use `192.168.1.50` and `XX:XX:XX:XX:XX:XX`. Blur anything personal in screenshots.
- **Two languages.** User-facing text in `tv.py` exists in `en` and `pl`. Docs are English first, then Polish.
- **Safety first.** Nothing is disabled or uninstalled without an explicit flag; prefer reversible actions; never target the system launcher, Google Play services, or the Play Store by default.
- **New brand profile?** Add it to `data/brands.json` with `os`, `adb`, and either a `bloat` regex or `note_en` and `note_pl`. Say in the PR which model and Android version you tested on.
- **No new dependency** (the script is standard library only) or network host without a reason in the PR.

---

# Współtworzenie

Dzięki za pomoc. To projekt hobbystyczny, więc zmiany niech będą małe i bezpieczne.

## Jak zgłosić zmianę

1. Zrób fork i gałąź (`feat/…`, `fix/…`, `docs/…`).
2. Wprowadź zmianę. Przy zmianach logiki dodaj lub zaktualizuj testy w `tests/`.
3. Uruchom `python -m unittest discover -s tests` oraz `python tv.py --help`.
4. Otwórz pull request do `main` według szablonu. **Tytuł w formacie Conventional Commits** (`feat: add TCL profile`), opis po **angielsku i polsku**.
5. **Zrzuty ekranu:** każda widoczna zmiana (interfejs launchera, układ dokumentacji, ikona) wymaga zrzutów w opisie PR, przed i po przy zmianie istniejącego elementu. Brak zmiany widocznej → napisz `No UI change`. Zrzuty wrzucaj na gałąź `pr-screenshots` (folder na PR, np. `pr-12/before.png`) i linkuj surowymi URL-ami; nie commituj ich do `main`.
6. Opiekun robi przegląd i scala. `main` jest chroniony: PR, akceptacja code ownera i checki `test`, `title`, `screenshots` muszą przejść.

## Zasady treści

- **Żadnych danych osobistych.** Bez prawdziwych adresów IP swojej sieci, SSID, adresów MAC, numerów seryjnych, kont, maili ani zrzutów urządzeń w kodzie, dokumentacji, zgłoszeniach i zrzutach ekranu. Używaj `192.168.1.50` i `XX:XX:XX:XX:XX:XX`. Zamazuj dane osobiste na zrzutach.
- **Dwa języki.** Teksty dla użytkownika w `tv.py` istnieją po `en` i `pl`. Dokumentacja: najpierw angielski, potem polski.
- **Bezpieczeństwo przede wszystkim.** Nic nie jest wyłączane ani odinstalowywane bez jawnej flagi; preferuj działania odwracalne; domyślnie nie ruszaj launchera systemowego, usług Google Play ani Sklepu Play.
- **Nowy profil marki?** Dodaj go do `data/brands.json` z `os`, `adb` oraz `bloat` (regex) albo `note_en` i `note_pl`. W PR napisz, na jakim modelu i wersji Androida testowałeś.
- **Bez nowych zależności** (skrypt używa tylko biblioteki standardowej) ani hostów sieciowych bez uzasadnienia w PR.
