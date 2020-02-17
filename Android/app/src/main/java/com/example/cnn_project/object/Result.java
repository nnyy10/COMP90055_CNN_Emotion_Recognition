package com.example.cnn_project.object;

public class Result {
    String result_id;
    String result_image;
    String result_reslut;

    public Result(){

    }

    public Result(String result_id, String result_image, String result_reslut) {
        this.result_id = result_id;
        this.result_image = result_image;
        this.result_reslut = result_reslut;
    }

    public String getResult_id() {
        return result_id;
    }

    public void setResult_id(String result_id) {
        this.result_id = result_id;
    }

    public String getResult_image() {
        return result_image;
    }

    public void setResult_image(String result_image) {
        this.result_image = result_image;
    }

    public String getResult_reslut() {
        return result_reslut;
    }

    public void setResult_reslut(String result_reslut) {
        this.result_reslut = result_reslut;
    }
}
