#!/usr/bin/env python3
"""tv.py - find an Android TV / Google TV on your network, back it up, list bloat candidates.
tv.py - znajdz Android TV / Google TV w sieci, zrob backup i pokaz kandydatow do wylaczenia.

EN: Scans the local subnet for ADB, connects over Wi-Fi (port 5555, or Android 11+
    Wireless debugging with --pair/--port), saves packages and settings to
    devices/<name>/ (MAC addresses and serial numbers are scrubbed) and lists packages
    that match the brand profile from data/brands.json. Nothing is disabled unless you
    explicitly pass --disable; --enable reverts it. Standard library only.
PL: Skanuje podsiec w poszukiwaniu ADB, laczy sie przez Wi-Fi (port 5555 albo
    Debugowanie bezprzewodowe Androida 11+ z --pair/--port), zapisuje pakiety i
    ustawienia do devices/<nazwa>/ (adresy MAC i numery seryjne sa usuwane) i wypisuje
    pakiety pasujace do profilu marki z data/brands.json. Nic nie jest wylaczane bez
    jawnego --disable; --enable to cofa. Tylko biblioteka standardowa.

Examples / Przyklady:
  python tv.py sony --ip 192.168.1.50 --name my-living-room-tv
  python tv.py --list-profiles --lang pl
"""
import argparse
import concurrent.futures as cf
import io
import json
import locale
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.request
import warnings
import zipfile
from datetime import datetime
from pathlib import Path

__version__ = "0.1.0"

ROOT = Path(__file__).parent
TOOLS = ROOT / "tools"
BRANDS_FILE = ROOT / "data" / "brands.json"
ADB_PORT = 5555
ADB_TIMEOUT = 120
MAC = re.compile(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}")
MAC_PLACEHOLDER = "XX:XX:XX:XX:XX:XX"
SCRUB = re.compile(r"serial|mac|bt_addr|wifi\.addr|imei|android_id|ethaddr", re.I)
PKG_LINE = re.compile(r"=([\w.]+)$")

# ---------------------------------------------------------------- i18n

T = {
    "en": {
        "description": "Find an Android TV / Google TV on your network, back it up and list "
                       "packages that are candidates for disabling.",
        "examples": (
            "examples:\n"
            "  python tv.py sony --ip 192.168.1.50 --name my-living-room-tv\n"
            "  python tv.py mi --ip 192.168.1.50 --port 38123          # Android 11+ Wireless debugging port\n"
            "  python tv.py mi --pair 192.168.1.50:41234 123456        # one-time pairing (address and code from the TV)\n"
            "  python tv.py sony --ip 192.168.1.50 --disable pkg.a pkg.b   # pm disable-user, reversible\n"
            "  python tv.py sony --ip 192.168.1.50 --enable pkg.a          # revert\n"
            "  python tv.py --list-profiles\n"
            "Nothing is disabled unless you pass --disable."
        ),
        "h_brand": "brand (sony, philips, tcl, xiaomi, samsung, lg...) or type (tv-box, firetv, tv = unknown)",
        "h_ip": "TV IP address, e.g. 192.168.1.50 (skips the network scan)",
        "h_name": "folder name under devices/, e.g. my-living-room-tv",
        "h_port": "ADB port (default 5555; for Android 11+ use the port shown in Wireless debugging)",
        "h_pair": "one-time pairing for Android 11+ Wireless debugging (address and code shown on the TV)",
        "h_disable": "disable the given packages (pm disable-user, reversible with --enable)",
        "h_enable": "re-enable the given packages",
        "h_list": "list available brand profiles and whether they support ADB, then exit",
        "h_lang": "interface language (default: from LANG/LC_ALL/system locale)",
        "h_version": "show version and exit",
        "brand_required": "brand is required (or use --list-profiles)",
        "unknown_brand": "Unknown brand '{name}', using the generic 'android-tv' profile.",
        "profile_line": "Profile: {key} | system: {os} | ADB: {adb}",
        "no_adb_default": "This brand does not support ADB.",
        "adb_yes": "yes",
        "adb_no": "no",
        "adb_partial": "partial",
        "profiles_header": "Available profiles (brand | system | ADB | aliases):",
        "downloading_adb": "Downloading adb (Google platform-tools)...",
        "scanning": "Scanning {prefix}.0/24 (ADB {port}, Tizen 8001, webOS 3000)...",
        "no_tv_found": "No TV with open ADB ({port}) found. Enable ADB debugging on the TV or pass --ip.",
        "choose": "Choose a number: ",
        "bad_choice": "Invalid choice.",
        "connecting": "Connecting to {ip} (accept the debugging authorization prompt on the TV)...",
        "bad_state": "State: '{state}'. Accept the authorization on the TV and run again.",
        "state_none": "none",
        "adb_error": "ADB error: {msg}",
        "adb_timeout": "ADB timed out after {sec}s ({cmd}). Check that the TV is on, reachable "
                       "at the given address/port and that debugging is enabled.",
        "disable_warning": "WARNING: disabling packages changes the TV. It is reversible: "
                           "python tv.py {brand} --ip {ip} --enable <package> ...",
        "device": "Device:",
        "backup_summary": "Backup: {out}\nPackages: {total}, candidates to disable: {count}",
        "disable_hint": "To disable (only if you agree): python tv.py {brand} --ip {ip} --disable <package> ...",
    },
    "pl": {
        "description": "Znajdz Android TV / Google TV w sieci, zrob backup i pokaz liste "
                       "pakietow, ktore mozna wylaczyc.",
        "examples": (
            "przyklady:\n"
            "  python tv.py sony --ip 192.168.1.50 --name my-living-room-tv\n"
            "  python tv.py mi --ip 192.168.1.50 --port 38123          # port z Debugowania bezprzewodowego (Android 11+)\n"
            "  python tv.py mi --pair 192.168.1.50:41234 123456        # jednorazowe parowanie (adres i kod z TV)\n"
            "  python tv.py sony --ip 192.168.1.50 --disable pkg.a pkg.b   # pm disable-user, odwracalne\n"
            "  python tv.py sony --ip 192.168.1.50 --enable pkg.a          # przywroc\n"
            "  python tv.py --list-profiles\n"
            "Nic nie jest wylaczane bez jawnego --disable."
        ),
        "h_brand": "marka (sony, philips, tcl, xiaomi, samsung, lg...) albo typ (tv-box, firetv, tv = nie wiem)",
        "h_ip": "adres IP telewizora, np. 192.168.1.50 (pomija skanowanie sieci)",
        "h_name": "nazwa folderu w devices/, np. my-living-room-tv",
        "h_port": "port ADB (domyslnie 5555; dla Androida 11+ port z Debugowania bezprzewodowego)",
        "h_pair": "jednorazowe parowanie Debugowania bezprzewodowego Androida 11+ (adres i kod z TV)",
        "h_disable": "wylacz podane pakiety (pm disable-user, odwracalne przez --enable)",
        "h_enable": "przywroc podane pakiety",
        "h_list": "wypisz dostepne profile marek i informacje o ADB, po czym zakoncz",
        "h_lang": "jezyk interfejsu (domyslnie z LANG/LC_ALL/ustawien systemu)",
        "h_version": "pokaz wersje i zakoncz",
        "brand_required": "podaj marke (albo uzyj --list-profiles)",
        "unknown_brand": "Nieznana marka '{name}', uzywam profilu ogolnego 'android-tv'.",
        "profile_line": "Profil: {key} | system: {os} | ADB: {adb}",
        "no_adb_default": "Ta marka nie wspiera ADB.",
        "adb_yes": "tak",
        "adb_no": "nie",
        "adb_partial": "czesciowo",
        "profiles_header": "Dostepne profile (marka | system | ADB | aliasy):",
        "downloading_adb": "Pobieram adb (platform-tools od Google)...",
        "scanning": "Skanuje {prefix}.0/24 (ADB {port}, Tizen 8001, webOS 3000)...",
        "no_tv_found": "Nie znaleziono TV z otwartym ADB ({port}). Wlacz debugowanie ADB na TV albo podaj --ip.",
        "choose": "Wybierz numer: ",
        "bad_choice": "Nieprawidlowy wybor.",
        "connecting": "Lacze z {ip} (na TV zatwierdz okno autoryzacji debugowania)...",
        "bad_state": "Stan: '{state}'. Zatwierdz autoryzacje na TV i uruchom ponownie.",
        "state_none": "brak",
        "adb_error": "Blad ADB: {msg}",
        "adb_timeout": "ADB nie odpowiedzial w {sec}s ({cmd}). Sprawdz, czy TV jest wlaczony, "
                       "osiagalny pod podanym adresem/portem i ma wlaczone debugowanie.",
        "disable_warning": "UWAGA: wylaczenie pakietow zmienia TV. Jest odwracalne: "
                           "python tv.py {brand} --ip {ip} --enable <pakiet> ...",
        "device": "Urzadzenie:",
        "backup_summary": "Backup: {out}\nPakietow: {total}, kandydatow do wylaczenia: {count}",
        "disable_hint": "Wylaczenie (po Twojej zgodzie): python tv.py {brand} --ip {ip} --disable <pakiet> ...",
    },
}

LANG = "en"


def detect_lang():
    """Return 'pl' if the environment/system locale is Polish, otherwise 'en'."""
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        val = os.environ.get(var)
        if val:
            return "pl" if val.lower().startswith("pl") else "en"
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            val = locale.getdefaultlocale()[0]
    except (AttributeError, ValueError):
        val = None
    return "pl" if val and val.lower().startswith("pl") else "en"


def set_lang(lang):
    global LANG
    LANG = lang if lang in T else "en"


def t(key, lang=None, **kw):
    """Translate key into `lang` (default: current language); falls back to English."""
    table = T.get(lang or LANG, T["en"])
    text = table.get(key, T["en"].get(key, key))
    return text.format(**kw) if kw else text


# ---------------------------------------------------------------- pure helpers


def load_profiles():
    return json.loads(BRANDS_FILE.read_text(encoding="utf-8"))["profiles"]


def _lookup(name, profiles):
    key = name.lower().strip()
    for k, p in profiles.items():
        if key == k or key in p.get("aliases", []):
            return k, p
    return None


def known_brand(name):
    return _lookup(name, load_profiles()) is not None


def profile_for(name):
    """Return (key, profile) for a brand name or alias; unknown -> generic 'android-tv'."""
    profiles = load_profiles()
    return _lookup(name, profiles) or ("android-tv", profiles["android-tv"])


def scrub_macs(text):
    return MAC.sub(MAC_PLACEHOLDER, text)


def scrub_text(text):
    """Drop lines with serial/MAC-like keys and mask any remaining MAC addresses."""
    kept = "\n".join(x for x in text.splitlines() if not SCRUB.search(x))
    return scrub_macs(kept)


def find_candidates(pm_list_output, regex):
    """Package names from `pm list packages -f` output that match regex (str or compiled)."""
    rx = re.compile(regex, re.I) if isinstance(regex, str) else regex
    names = set()
    for line in pm_list_output.splitlines():
        m = PKG_LINE.search(line.strip())
        if m and rx.search(m.group(1)):
            names.add(m.group(1))
    return sorted(names)


def slugify(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", name).strip("-") or "device"


def adb_label(value):
    if value is True:
        return t("adb_yes")
    if value is False:
        return t("adb_no")
    return t("adb_partial")


# ---------------------------------------------------------------- adb / network


def find_adb():
    exe = shutil.which("adb")
    if exe:
        return exe
    local = TOOLS / "platform-tools" / ("adb.exe" if os.name == "nt" else "adb")
    if not local.exists():
        plat = "windows" if os.name == "nt" else ("darwin" if sys.platform == "darwin" else "linux")
        print(t("downloading_adb"))
        url = f"https://dl.google.com/android/repository/platform-tools-latest-{plat}.zip"
        with urllib.request.urlopen(url) as r:
            zipfile.ZipFile(io.BytesIO(r.read())).extractall(TOOLS)
        if os.name != "nt":
            local.chmod(0o755)
    return str(local)


def run_adb(cmd, timeout=ADB_TIMEOUT):
    """Run an adb command; exit with a readable message on timeout."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        sys.exit(t("adb_timeout", sec=timeout, cmd=" ".join(cmd[1:4])))


def adb(exe, ip, *args, check=True):
    r = run_adb([exe, "-s", f"{ip}:{ADB_PORT}", *args])
    if check and r.returncode != 0:
        sys.exit(t("adb_error", msg=r.stderr.strip() or r.stdout.strip()))
    return r.stdout


def local_prefix():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ".".join(ip.split(".")[:3])


def open_ports(ip, ports, timeout=0.4):
    found = []
    for p in ports:
        try:
            with socket.create_connection((ip, p), timeout=timeout):
                found.append(p)
        except OSError:
            pass
    return found


def scan(prefix):
    print(t("scanning", prefix=prefix, port=ADB_PORT))
    ips = [f"{prefix}.{i}" for i in range(1, 255)]
    with cf.ThreadPoolExecutor(64) as ex:
        res = list(ex.map(lambda ip: (ip, open_ports(ip, [ADB_PORT, 8001, 3000])), ips))
    return [(ip, p) for ip, p in res if p]


# ---------------------------------------------------------------- cli


def list_profiles():
    print(t("profiles_header"))
    for key, p in load_profiles().items():
        aliases = ", ".join(p.get("aliases", [])) or "-"
        print(f"  {key:<11} | {p['os']} | ADB: {adb_label(p['adb'])} | {aliases}")


def build_parser():
    ap = argparse.ArgumentParser(description=t("description"), epilog=t("examples"),
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brand", nargs="?", help=t("h_brand"))
    ap.add_argument("--ip", help=t("h_ip"))
    ap.add_argument("--name", help=t("h_name"))
    ap.add_argument("--port", type=int, default=ADB_PORT, help=t("h_port"))
    ap.add_argument("--pair", nargs=2, metavar=("IP:PORT", "CODE"), help=t("h_pair"))
    ap.add_argument("--disable", nargs="+", metavar="PKG", help=t("h_disable"))
    ap.add_argument("--enable", nargs="+", metavar="PKG", help=t("h_enable"))
    ap.add_argument("--list-profiles", action="store_true", help=t("h_list"))
    ap.add_argument("--lang", choices=["en", "pl"], help=t("h_lang"))
    ap.add_argument("--version", action="version", version=f"tv.py {__version__}", help=t("h_version"))
    return ap


def main(argv=None):
    global ADB_PORT
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    # Pre-parse --lang so that --help is already localized.
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=["en", "pl"])
    known, _ = pre.parse_known_args(argv)
    set_lang(known.lang or detect_lang())

    ap = build_parser()
    a = ap.parse_args(argv)

    if a.list_profiles:
        list_profiles()
        return
    if not a.brand:
        ap.error(t("brand_required"))

    if not known_brand(a.brand):
        print(t("unknown_brand", name=a.brand))
    key, prof = profile_for(a.brand)
    print(t("profile_line", key=key, os=prof["os"], adb=adb_label(prof["adb"])))
    if prof["adb"] is False:
        sys.exit(prof.get(f"note_{LANG}") or prof.get("note_en") or t("no_adb_default"))

    ADB_PORT = a.port
    if a.pair:
        r = run_adb([find_adb(), "pair", *a.pair], timeout=30)
        print((r.stdout.strip() or r.stderr.strip()))
        return
    ip = a.ip
    if not ip:
        hits = [h for h in scan(local_prefix()) if ADB_PORT in h[1]]
        if not hits:
            sys.exit(t("no_tv_found", port=ADB_PORT))
        for i, (h, _) in enumerate(hits):
            print(f"  [{i}] {h}")
        idx = 0
        if len(hits) > 1:
            try:
                idx = int(input(t("choose")))
                hits[idx]
            except (ValueError, IndexError):
                sys.exit(t("bad_choice"))
        ip = hits[idx][0]

    exe = find_adb()
    print(t("connecting", ip=ip))
    run_adb([exe, "connect", f"{ip}:{ADB_PORT}"], timeout=30)
    state = adb(exe, ip, "get-state", check=False).strip()
    if state != "device":
        sys.exit(t("bad_state", state=state or t("state_none")))

    if a.disable or a.enable:
        if a.disable:
            print(t("disable_warning", brand=a.brand, ip=ip))
        for pkg in a.disable or []:
            print(f"disable {pkg}:", adb(exe, ip, "shell", "pm", "disable-user", "--user", "0", pkg).strip())
        for pkg in a.enable or []:
            print(f"enable  {pkg}:", adb(exe, ip, "shell", "pm", "enable", pkg).strip())
        return

    def prop(k):
        return adb(exe, ip, "shell", "getprop", k).strip()

    model = prop("ro.product.model") or "unknown"
    info = {"brand_arg": a.brand, "profile": key, "manufacturer": prop("ro.product.manufacturer"),
            "model": model, "device": prop("ro.product.device"), "android": prop("ro.build.version.release"),
            "sdk": prop("ro.build.version.sdk"), "build": prop("ro.build.display.id"),
            "date": datetime.now().isoformat(timespec="seconds")}
    slug = slugify(f"{key}-{model}")
    if a.name:
        slug = slugify(a.name)
        info["name"] = a.name
    out = ROOT / "devices" / slug
    (out / "backup").mkdir(parents=True, exist_ok=True)
    (out / "info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(t("device"), json.dumps(info, ensure_ascii=False))

    pkgs = adb(exe, ip, "shell", "pm", "list", "packages", "-f", "-u")
    dis = adb(exe, ip, "shell", "pm", "list", "packages", "-d")
    (out / "backup" / "packages-all.txt").write_text(scrub_macs(pkgs), encoding="utf-8")
    (out / "backup" / "packages-disabled.txt").write_text(scrub_macs(dis), encoding="utf-8")
    (out / "backup" / "getprop.txt").write_text(scrub_text(adb(exe, ip, "shell", "getprop")), encoding="utf-8")
    for ns in ("global", "secure", "system"):
        txt = scrub_text(adb(exe, ip, "shell", "settings", "list", ns))
        (out / "backup" / f"settings-{ns}.txt").write_text(txt, encoding="utf-8")

    cand = find_candidates(pkgs, prof.get("bloat", "retaildemo|partner|promo"))
    (out / "candidates.txt").write_text("\n".join(cand), encoding="utf-8")
    print("\n" + t("backup_summary", out=out, total=len(pkgs.splitlines()), count=len(cand)))
    for c in cand:
        print("  ", c)
    print("\n" + t("disable_hint", brand=a.brand, ip=ip))


if __name__ == "__main__":
    main()
