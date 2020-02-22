package com.example.cnn_project.app.initial;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.example.cnn_project.R;
import com.example.cnn_project.app.authentication.LoginActivity;

/**
 * This is the main activity. When users enter this application, it first runs this activity and
 * shows UploadFragment in the fragment container.
 */

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Fragment initialFragment = new UploadFragment();
        getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,
                initialFragment).commit();
    }

    /**
     * There is a "sign in" button in the menu. When clicking it, the page will from the current
     * page to the log in page.
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        switch (item.getItemId()) {
            case R.id.main_signin:
                startActivity(new Intent(this, LoginActivity.class));
                break;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * If users press the back button in the main activity, it will exit this application and
     * return to the mobile page.
     */
    @Override
    public void onBackPressed(){
        Fragment fragment = getSupportFragmentManager().findFragmentById(R.id.fragment_container);
        if (fragment instanceof UploadFragment) {
            Intent homeIntent = new Intent(Intent.ACTION_MAIN);
            homeIntent.addCategory( Intent.CATEGORY_HOME );
            homeIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(homeIntent);
        } else{
            super.onBackPressed();
        }
    }
}