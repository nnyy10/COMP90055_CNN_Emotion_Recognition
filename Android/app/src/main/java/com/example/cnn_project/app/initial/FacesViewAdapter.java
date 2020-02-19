package com.example.cnn_project.app.initial;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.example.cnn_project.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class FacesViewAdapter extends RecyclerView.Adapter<FacesViewAdapter.ViewHolder>{
    private ArrayList<JSONObject> faceList;
    private Activity mActivity;

    public FacesViewAdapter(Activity context, ArrayList<JSONObject> faceList) {
        this.faceList = faceList;
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
        try {
            JSONArray predictionlist = (JSONArray) faceList.get(position).get("prediction");
            String textToSet = getTextForFace(predictionlist);
            holder.emotionText.setText(textToSet);
            String faceData = (String) faceList.get(position).get("face");
            byte[] decodedString;
            decodedString = Base64.decode(faceData, Base64.DEFAULT);
            Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
            holder.faceImageView.setImageBitmap(decodedByte);
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }

    private String getTextForFace(JSONArray face) throws JSONException {
        StringBuilder output = new StringBuilder();
        for (int i = 0; i< face.length(); i++) {
            String emotion = (String) ((JSONObject)face.get(i)).get("emotion");
            String prediction = (String) ((JSONObject)face.get(i)).get("probability");
            output.append(emotion).append(": ").append(prediction).append(", ");
        }
        String text = output.toString();
        text = text.substring(0, text.length() - 2);
        return text;
    }
    @Override
    public int getItemCount() {
        return faceList.size();
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





