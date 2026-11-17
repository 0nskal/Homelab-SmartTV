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
