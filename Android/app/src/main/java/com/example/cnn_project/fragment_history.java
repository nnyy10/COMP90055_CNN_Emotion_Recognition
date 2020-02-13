package com.example.cnn_project;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class fragment_history extends Fragment {

    private ListView list_history;

    private List<History> historyList;
    private HistoryAdapter adapter;

    private DatabaseReference ref;

    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private FirebaseUser user = firebaseAuth.getCurrentUser();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_history, container, false);
        String uid = user.getUid();
        ref = FirebaseDatabase.getInstance().getReference("users/"+uid);
        historyList = new ArrayList<>();
        adapter = new HistoryAdapter(fragment_history.this.getActivity(), historyList);
        list_history =view.findViewById(R.id.list_history);
        return view;

    }

    @Override
    public void onStart() {
        ref.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                historyList.clear();
                for(DataSnapshot historySnapshot : dataSnapshot.getChildren()){
                    History history = historySnapshot.getValue(History.class);
                    historyList.add(history);
                    System.out.println(history);
                }

//                HistoryAdapter adapter = new HistoryAdapter(fragment_history.this.getActivity(), historyList);
                list_history.setAdapter(adapter);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        super.onStart();
    }
}
