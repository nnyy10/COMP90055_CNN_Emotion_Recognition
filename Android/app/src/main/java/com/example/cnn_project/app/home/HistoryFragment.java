package com.example.cnn_project.app.home;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.example.cnn_project.R;
import com.example.cnn_project.object.History;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

/**
 * This is the history page, which shows all previous predictions. It has four sections,
 * Submit time, Image name, Image and Result. These history data is retrieved from realtime
 * database of firebase through reference.
 */

public class HistoryFragment extends Fragment {

    private ListView list_history;
    private List<History> historyList;
    private HistoryAdapter adapter;

    private DatabaseReference uidRef;
    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private FirebaseUser user = firebaseAuth.getCurrentUser();

    /**
     * When retrieving histories, the user's uid is used to find the stored reference.
     */
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_history, container, false);
        getActivity().setTitle("History");
        String uid = user.getUid();
        uidRef = FirebaseDatabase.getInstance().getReference("users/" + uid);
        historyList = new ArrayList<>();
        adapter = new HistoryAdapter((AppCompatActivity) getContext(), historyList);
        list_history =view.findViewById(R.id.list_history);
        return view;
    }

    /**
     * These stored information will transfer to History object through the declared constructor
     * of History.
     */
    @Override
    public void onStart() {
        uidRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                historyList.clear();
                for(DataSnapshot historySnapshot : dataSnapshot.getChildren()){
                    String imageId = historySnapshot.getKey();
                    String imageUrl = (String) historySnapshot.child("image_location").getValue();
                    String imageSubmitTime = (String) historySnapshot.child("submit_time").getValue();
                    String imageName = (String) historySnapshot.child("image_name").getValue();
                    Iterable<DataSnapshot> facesSnapshot = historySnapshot.child("result").getChildren();
                    History history = new History(imageId, imageUrl, imageName, imageSubmitTime, facesSnapshot);
                    historyList.add(history);
                }
                list_history.setAdapter(adapter);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        super.onStart();
    }
}
