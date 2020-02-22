package com.example.cnn_project.object;

/**
 * This function is used to define the data types, which are stored to database.
 */

public class DatabaseEntry {
    public String image_name;
    public String submit_time;

    public DatabaseEntry(String image_name, String submit_time){
        this.image_name = image_name;
        this.submit_time = submit_time;
    }
}
