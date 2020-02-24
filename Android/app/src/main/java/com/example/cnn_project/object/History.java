package com.example.cnn_project.object;

import com.google.firebase.database.DataSnapshot;

import java.util.ArrayList;

/**
 * This is the History class, which declares data types of the information of histories. It has
 * five variables. The image_id means the id of image. The image_location means the stored location
 * in the storage of the firebase. The image_name is the name of image. The submit_time is the time
 * when uploading the image, while the facesSnapshot stores detailed detection results of the image.
 * It is mainly used in HistoryAdapter.
 */

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
