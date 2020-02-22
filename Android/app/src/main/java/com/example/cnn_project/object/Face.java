package com.example.cnn_project.object;

import org.json.JSONObject;

import java.util.ArrayList;

/**
 * This function is used to define the Face class, which is mainly used in FaceViewAdapter. The
 * image_location means the image location stored in storage. The emotions has the detected emotions
 * along with their probabilities.
 */

public class Face {

    public String image_location;
    public ArrayList<JSONObject> emotions;

    public Face(String image_location, ArrayList<JSONObject> emotions) {
        this.image_location = image_location;
        this.emotions = emotions;
    }
}
