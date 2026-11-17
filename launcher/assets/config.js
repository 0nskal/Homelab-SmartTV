/* Dashboard settings. Edit and rebuild (launcher/build.sh install).
   Ustawienia dashboardu. Edytuj i przebuduj (launcher/build.sh install). */
window.CONFIG = {
  lang: "auto",            // "en", "pl" or "auto" (browser language) / "en", "pl" albo "auto"
  wallpaper: "",           // optional image in launcher/assets, e.g. "wallpaper.jpg" (1920x1080) / opcjonalny obraz w launcher/assets
  weather: {
    lat: 51.51,            // your latitude / Twoja szerokość geograficzna
    lon: -0.13,            // your longitude / Twoja długość geograficzna
    timezone: "Europe/London",
    label: "London",       // shown next to the weather / pokazywane przy pogodzie ("" = hide)
    unit: "celsius"        // "celsius" or "fahrenheit"
  },
  // [label, Android package]. Apps that are not installed are skipped.
  // [nazwa, pakiet Androida]. Niezainstalowane aplikacje są pomijane.
  apps: [
    ["Netflix", "com.netflix.ninja"],
    ["YouTube", "com.google.android.youtube.tv"],
    ["Spotify", "com.spotify.tv.android"],
    ["Disney+", "com.disney.disneyplus"],
    ["Prime Video", "com.amazon.amazonvideo.livingroom"],
    ["Play Store", "com.android.vending"]
  ]
};
