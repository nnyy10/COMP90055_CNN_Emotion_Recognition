package com.example.cnn_project.app.home;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.example.cnn_project.R;
import com.example.cnn_project.object.Face;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class FaceViewAdapter extends RecyclerView.Adapter<FaceViewAdapter.ViewHolder>{
    private ArrayList facesList;
    private Activity mActivity;

    public FaceViewAdapter(Activity context, ArrayList facesList) {
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





