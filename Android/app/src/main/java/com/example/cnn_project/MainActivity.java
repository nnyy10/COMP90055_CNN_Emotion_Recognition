package com.example.cnn_project;


import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Fragment cameraFragment = new fragment_camera();
        getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container,
                cameraFragment).commit();

    }
}