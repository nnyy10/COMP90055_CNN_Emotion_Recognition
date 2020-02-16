package com.example.cnn_project;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.google.common.collect.Iterables;
import com.google.common.collect.Iterators;
import com.google.firebase.database.DataSnapshot;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class FaceResultViewAdapter extends RecyclerView.Adapter<FaceResultViewAdapter.ViewHolder>{
    private ArrayList facesList;
    private Activity mActivity;

    public FaceResultViewAdapter(Activity context, ArrayList facesList) {
        this.facesList = facesList;
        this.mActivity = context;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.layout_recyclerview, parent, false);
        ViewHolder holder = new ViewHolder(view);
        return holder;
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, final int position) {
        holder.faceNumberText.setText(Integer.toString(position + 1) + ". ");

        Face face = (Face) facesList.get(position);
        Picasso.get().load(face.image_location).into(holder.faceImageView);


        try {
            String textToSet = getTextForFace(face.emotions);
            holder.emotionText.setText(textToSet);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    private String getTextForFace(ArrayList<JSONObject> face) throws JSONException {
        StringBuilder output = new StringBuilder();
        for (int i = 0; i< face.size(); i++) {
            String emotion = (String) face.get(i).get("emotion");
            String prediction = face.get(i).get("probability").toString();
            output.append(emotion).append(": ").append(prediction).append(", ");
        }
        String text = output.toString();
        text = text.substring(0, text.length() - 2);
        return text;
    }
    @Override
    public int getItemCount() {
        return facesList.size();
    }


    public class ViewHolder extends RecyclerView.ViewHolder{
        TextView faceNumberText;
        TextView emotionText;
        ImageView faceImageView;

        public ViewHolder(View itemView) {
            super(itemView);
            faceNumberText = itemView.findViewById(R.id.faceNumberText);
            faceImageView = itemView.findViewById(R.id.faceImageView);
            emotionText = itemView.findViewById(R.id.emotionPredictionTextView);
        }
    }
}





