package com.example.cnn_project;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Map;

public class fragment_result extends Fragment {


    private RecyclerView recyclerView;
    private Context mContext;
    private String imageLocation;
    private ImageView imageView_response_image;
    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private String userID = firebaseAuth.getCurrentUser().getUid();
    private Iterable<DataSnapshot> facesSnapshot;

    public fragment_result(String imageLocation, Iterable<DataSnapshot> facesSnapshot) {
        this.imageLocation = imageLocation;
        this.facesSnapshot = facesSnapshot;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        final View view = inflater.inflate(R.layout.fragment_response, container, false);


        imageView_response_image = view.findViewById(R.id.imageView_response_image);
        recyclerView = view.findViewById(R.id.faceRecyclerView);
        mContext = getContext();

        Picasso.get().load(imageLocation).into(imageView_response_image);


        ArrayList faceList = new ArrayList();
        for(DataSnapshot faceSnapshot: facesSnapshot){


            ArrayList<JSONObject> emotions = new ArrayList<>();
            for (int i = 0; i < 7; i++) {
                try {
                    JSONObject emotion = new JSONObject(faceSnapshot.child(Integer.toString(i)).getValue().toString());
                    emotions.add(emotion);
                } catch (JSONException e) { e.printStackTrace(); }
            }


            Face faceObject = new Face(faceSnapshot.child("image_location").getValue().toString(), emotions);
            faceList.add(faceObject);
        }




        FaceResultViewAdapter adapter = new FaceResultViewAdapter(getActivity(), faceList);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
        recyclerView.addItemDecoration(new DividerItemDecoration(mContext,DividerItemDecoration.VERTICAL));


        return view;
    }


}
