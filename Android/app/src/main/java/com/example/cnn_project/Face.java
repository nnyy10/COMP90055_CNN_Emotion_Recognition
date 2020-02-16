package com.example.cnn_project;


import org.json.JSONObject;

import java.util.ArrayList;

public class Face {

    public String image_location;
    public ArrayList<JSONObject> emotions;

    public Face(String image_location, ArrayList<JSONObject> emotions) {
        this.image_location = image_location;
        this.emotions = emotions;
    }
}
