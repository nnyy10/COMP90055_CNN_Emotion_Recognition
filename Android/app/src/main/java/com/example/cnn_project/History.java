package com.example.cnn_project;

import com.google.firebase.database.DataSnapshot;

import java.util.ArrayList;

public class History {
    public String image_id;
    public String image_location;
    public String image_name;
    public String submit_time;
    public Iterable<DataSnapshot> facesSnapshot;


    public History(String image_id, String image_location, String image_name, String submit_time, Iterable<DataSnapshot> facesSnapshot) {
        this.image_id = image_id;
        this.image_location = image_location;
        this.image_name = image_name;
        this.submit_time = submit_time;
        this.facesSnapshot = facesSnapshot;
    }
}
