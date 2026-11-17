# Working agreements / Ustalenia robocze

For humans and AI agents (Claude Code, Codex, …) working on this repository. `CLAUDE.md` points here.
Dla ludzi i agentów AI pracujących nad tym repozytorium.

## What this project is

Homelab - SmartTV is a public, free, hobby project: tools and guides for cleaning up and configuring Android TV / Google TV devices over ADB on your home network (backup, debloat, custom launcher). It stands on its own: no personal branding, no personal data, no recordings of anyone's devices in the repo.

## Rules that always apply

1. **Public repo, changes only through pull requests.** Outside contributors work from forks; the maintainer (@0nskal) reviews and merges. `main` is protected: PR + code owner approval + checks `test`, `title`, `screenshots`. The maintainer may push release commits directly.
2. **Same model as [noyex/burn](https://github.com/noyex/burn):** every visible change (launcher UI, docs layout, icon) needs **screenshots** in the PR description (before and after when changing something existing). Not visible → write "No UI change". Details: [CONTRIBUTING.md](CONTRIBUTING.md).
3. **PR title = Conventional Commits** in English (`feat: …`, `fix: …`, `docs: …`). Description in English and Polish. Use `.github/pull_request_template.md`.
4. **PR screenshots live on the orphan branch `pr-screenshots`** (folder per PR), linked by raw URL, never committed to `main`.
5. **Releases:** update `CHANGELOG.md` (English first, Polish below), bump `__version__` in `tv.py`, tag `vX.Y.Z`. Release only when the maintainer asks.
6. **Before every PR:** `python -m unittest discover -s tests` passes and `python tv.py --help` runs. CI runs the same.
7. **Two languages:** every user-facing text in `tv.py` exists in `en` and `pl`; README, CHANGELOG, CONTRIBUTING and `docs/` stay bilingual (English first, then Polish).
8. **Safety:** nothing is disabled or uninstalled on a device without an explicit flag (`--disable`); prefer reversible `pm disable-user`; take a backup first; never touch the system launcher, Google Play services or the Play Store by default.
9. **Privacy:** never commit or paste personal data: no real IP addresses of your network, SSIDs, MAC addresses, serial numbers, accounts, emails, device dumps (`devices/` is git-ignored). The script scrubs MACs and serials from backups; still review before sharing. No new dependency or network host without a reason in the PR.
10. **No brand names as logos:** the icon and launcher use neutral artwork; do not add manufacturer logos.

## Ustalenia po polsku (skrót)

Repo publiczne; zmiany tylko przez PR z forka ze zrzutami ekranu (jak w Burn); tytuł PR w formacie Conventional Commits po angielsku, opis po angielsku i polsku; zrzuty trzymamy na gałęzi `pr-screenshots`; przed PR testy (`python -m unittest discover -s tests`); teksty w dwóch językach (angielski pierwszy); nic nie jest wyłączane bez jawnej flagi `--disable`, najpierw backup; żadnych danych osobistych w repo (IP swojej sieci, SSID, MAC, numery seryjne, konta, zrzuty urządzeń); wydanie tylko na prośbę opiekuna.
