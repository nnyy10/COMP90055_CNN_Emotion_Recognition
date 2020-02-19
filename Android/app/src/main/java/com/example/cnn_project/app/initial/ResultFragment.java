package com.example.cnn_project.app.initial;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.example.cnn_project.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class ResultFragment extends Fragment {


    private RecyclerView recyclerView;
    private Context mContext;
    private JSONObject response;
    private ImageView imageView_response_image;

    public ResultFragment(JSONObject response) {
        this.response = response;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.fragment_response, container, false);

        recyclerView = view.findViewById(R.id.faceRecyclerView);
        imageView_response_image = view.findViewById(R.id.imageView_response_image);
        byte[] decodedString;
        try {
            decodedString = Base64.decode((String) response.get("image"), Base64.DEFAULT);
            Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
            imageView_response_image.setImageBitmap(decodedByte);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        mContext = getContext();

        try {
            JSONArray faceList = (JSONArray) response.get("faces");

            ArrayList<JSONObject> faceArrayList = new ArrayList<>();

            for (int i = 0; i < faceList.length(); i++) {
                JSONObject jsonFace = (JSONObject) faceList.get(i);
                faceArrayList.add(jsonFace);
            }


            FacesViewAdapter adapter = new FacesViewAdapter(getActivity(), faceArrayList);
            recyclerView.setAdapter(adapter);
            recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
            recyclerView.addItemDecoration(new DividerItemDecoration(mContext, DividerItemDecoration.VERTICAL));
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return view;
    }
}
