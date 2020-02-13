package com.example.cnn_project;

public class History {
    String image_location;
    String image_name;
    String result;
    String submit_time;

    public History(){

    }

    public History(String image_location, String image_name, String result, String submit_time) {
        this.image_location = image_location;
        this.image_name = image_name;
        this.result = result;
        this.submit_time = submit_time;
    }

    public String getImage_location() {
        return image_location;
    }

    public void setImage_location(String image_location) {
        this.image_location = image_location;
    }

    public String getImage_name() {
        return image_name;
    }

    public void setImage_name(String image_name) {
        this.image_name = image_name;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public String getSubmit_time() {
        return submit_time;
    }

    public void setSubmit_time(String submit_time) {
        this.submit_time = submit_time;
    }
}
