package dev.homelab.smarttv.dashboard;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Base64;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Jedyna Activity: pelnoekranowy WebView z lokalnym dashboardem. */
public class MainActivity extends Activity {

    private WebView web;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setBackgroundDrawable(new ColorDrawable(Color.parseColor("#121011")));

        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#121011"));
        web.setVerticalScrollBarEnabled(false);
        web.setHorizontalScrollBarEnabled(false);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);

        web.setWebViewClient(new WebViewClient());
        web.addJavascriptInterface(new Bridge(), "Android");
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        // HOME (lub ponowne uruchomienie) zawsze wraca do dashboardu
        js("window.goHome && goHome()");
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
        js("window.onShow && onShow()");
        web.requestFocus();
    }

    @Override
    protected void onPause() {
        web.onPause();
        super.onPause();
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.KEYCODE_BACK) {
            // BACK nigdy nie zamyka launchera; JS zamyka tylko siatke aplikacji
            if (e.getAction() == KeyEvent.ACTION_UP) js("window.onBack && onBack()");
            return true;
        }
        return super.dispatchKeyEvent(e);
    }

    @Override
    public void onBackPressed() { /* nic */ }

    // ---------------- Tuya Cloud (switching smart plugs, optional) ----------------
    private String tuyaToken = ""; private long tuyaExp = 0; private JSONObject tuyaCfg;

    private JSONObject tuyaConfig() throws Exception {
        if (tuyaCfg == null) {
            InputStream in = getAssets().open("tuya.json");
            ByteArrayOutputStream o = new ByteArrayOutputStream(); byte[] b = new byte[2048]; int n;
            while ((n = in.read(b)) > 0) o.write(b, 0, n);
            in.close(); tuyaCfg = new JSONObject(o.toString("UTF-8"));
        }
        return tuyaCfg;
    }
    private static String hex(byte[] d) { StringBuilder sb = new StringBuilder(); for (byte x : d) sb.append(String.format("%02x", x)); return sb.toString(); }
    private String tuyaHttp(String method, String path, String body, String tok) throws Exception {
        JSONObject c = tuyaConfig();
        String t = String.valueOf(System.currentTimeMillis());
        String bodyHash = hex(MessageDigest.getInstance("SHA-256").digest((body == null ? "" : body).getBytes("UTF-8")));
        String sts = method + "\n" + bodyHash + "\n\n" + path;
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(c.getString("secret").getBytes("UTF-8"), "HmacSHA256"));
        String sign = hex(mac.doFinal((c.getString("id") + tok + t + sts).getBytes("UTF-8"))).toUpperCase(Locale.ROOT);
        HttpURLConnection h = (HttpURLConnection) new URL(c.getString("host") + path).openConnection();
        h.setConnectTimeout(8000); h.setReadTimeout(8000); h.setRequestMethod(method);
        h.setRequestProperty("client_id", c.getString("id")); h.setRequestProperty("sign", sign);
        h.setRequestProperty("t", t); h.setRequestProperty("sign_method", "HMAC-SHA256");
        h.setRequestProperty("Content-Type", "application/json");
        if (tok.length() > 0) h.setRequestProperty("access_token", tok);
        if (body != null) { h.setDoOutput(true); h.getOutputStream().write(body.getBytes("UTF-8")); }
        InputStream in = h.getResponseCode() >= 400 ? h.getErrorStream() : h.getInputStream();
        ByteArrayOutputStream o = new ByteArrayOutputStream(); byte[] b = new byte[2048]; int n;
        while ((n = in.read(b)) > 0) o.write(b, 0, n);
        return o.toString("UTF-8");
    }
    private synchronized String tuyaTok() throws Exception {
        if (tuyaToken.length() > 0 && System.currentTimeMillis() < tuyaExp) return tuyaToken;
        JSONObject r = new JSONObject(tuyaHttp("GET", "/v1.0/token?grant_type=1", null, ""));
        JSONObject res = r.getJSONObject("result");
        tuyaToken = res.getString("access_token");
        tuyaExp = System.currentTimeMillis() + (res.getLong("expire_time") - 120) * 1000L;
        return tuyaToken;
    }
    /** The result comes back asynchronously przez window.onTuya(reqId, json). */
    private void tuyaAsync(final String reqId, final String method, final String path, final String body) {
        new Thread(new Runnable() { @Override public void run() {
            String out;
            try {
                String r = tuyaHttp(method, path, body, tuyaTok());
                if (r.contains("token invalid") || r.contains("1010")) { tuyaToken = ""; r = tuyaHttp(method, path, body, tuyaTok()); }
                out = r;
            } catch (Exception ex) { out = "{\"success\":false,\"msg\":\"" + String.valueOf(ex.getMessage()).replace("\"", "'") + "\"}"; }
            js("window.onTuya && onTuya(" + JSONObject.quote(reqId) + "," + JSONObject.quote(out) + ")");
        }}).start();
    }

    private void js(final String code) {
        runOnUiThread(new Runnable() {
            @Override public void run() { if (web != null) web.evaluateJavascript(code, null); }
        });
    }

    /** Most JS <-> Android (obiekt Android). */
    private class Bridge {
        private Intent launchIntent(String pkg) {
            PackageManager pm = getPackageManager();
            Intent i = pm.getLeanbackLaunchIntentForPackage(pkg);
            if (i == null) i = pm.getLaunchIntentForPackage(pkg);
            return i;
        }

        @JavascriptInterface
        public String tuyaConfig() {
            try { JSONObject c = new JSONObject(MainActivity.this.tuyaConfig().toString()); c.remove("secret"); c.remove("id"); return c.toString(); }
            catch (Exception ex) { return ""; }
        }
        @JavascriptInterface
        public void tuya(String reqId, String method, String path, String body) {
            tuyaAsync(reqId, method, path, (body == null || body.length() == 0) ? null : body);
        }

        @JavascriptInterface
        public void launch(final String pkg) {
            final Intent i = launchIntent(pkg);
            if (i == null) return;
            runOnUiThread(new Runnable() {
                @Override public void run() {
                    try {
                        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        startActivity(i);
                    } catch (Exception ex) { /* brak aktywnosci: ignoruj */ }
                }
            });
        }

        @JavascriptInterface
        public String listApps() {
            try {
                PackageManager pm = getPackageManager();
                Map<String, String> found = new HashMap<>();
                String[] cats = { Intent.CATEGORY_LEANBACK_LAUNCHER, Intent.CATEGORY_LAUNCHER };
                for (String cat : cats) {
                    Intent q = new Intent(Intent.ACTION_MAIN).addCategory(cat);
                    for (ResolveInfo ri : pm.queryIntentActivities(q, 0)) {
                        String p = ri.activityInfo.packageName;
                        if (p.equals(getPackageName()) || found.containsKey(p)) continue;
                        found.put(p, String.valueOf(ri.loadLabel(pm)));
                    }
                }
                final Collator col = Collator.getInstance(new Locale("pl", "PL"));
                List<Map.Entry<String, String>> list = new ArrayList<>(found.entrySet());
                Collections.sort(list, new java.util.Comparator<Map.Entry<String, String>>() {
                    @Override public int compare(Map.Entry<String, String> a, Map.Entry<String, String> b) {
                        return col.compare(a.getValue(), b.getValue());
                    }
                });
                JSONArray arr = new JSONArray();
                for (Map.Entry<String, String> en : list) {
                    JSONObject o = new JSONObject();
                    o.put("label", en.getValue());
                    o.put("package", en.getKey());
                    arr.put(o);
                }
                return arr.toString();
            } catch (Exception ex) {
                return "[]";
            }
        }

        /** Ikona (a gdy brak, banner) aplikacji jako base64 PNG. */
        @JavascriptInterface
        public String icon(String pkg) {
            try {
                PackageManager pm = getPackageManager();
                ApplicationInfo ai = pm.getApplicationInfo(pkg, 0);
                Drawable d = pm.getApplicationIcon(ai);
                if (d == null) d = pm.getApplicationBanner(ai);
                if (d == null) return "";
                int size = 192;
                Bitmap bmp = Bitmap.createBitmap(size, size, Bitmap.Config.ARGB_8888);
                Canvas c = new Canvas(bmp);
                d.setBounds(0, 0, size, size);
                d.draw(c);
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                bmp.compress(Bitmap.CompressFormat.PNG, 100, out);
                bmp.recycle();
                return Base64.encodeToString(out.toByteArray(), Base64.NO_WRAP);
            } catch (Exception ex) {
                return "";
            }
        }
    }
}
