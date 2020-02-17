package com.example.cnn_project;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class fragment_profile extends Fragment {

    private TextView email_profile;
    private Button logout;

    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private FirebaseUser user = firebaseAuth.getCurrentUser();

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view =inflater.inflate(R.layout.fragment_profile, container,false);
        getActivity().setTitle("Profile");
        email_profile = view.findViewById(R.id.email_profile);
//        history_profile = view.findViewById(R.id.history_profile);
        logout = view.findViewById(R.id.logout);

        logout.setOnClickListener(logoutListener);


        if (user != null) {
            String email = user.getEmail();
            String uid = user.getUid();

            email_profile.setText("Email: " + email);
//            history_profile.setText("Count of History: " + uid);
        }


        return view;
    }

    private View.OnClickListener logoutListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            showNormalDialog();
        }
    };

    private void showNormalDialog(){

        final AlertDialog.Builder normalDialog = new AlertDialog.Builder(getActivity());
        normalDialog.setMessage("Are you sure you want to log out?");
        normalDialog.setPositiveButton("Yes",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        FirebaseAuth.getInstance().signOut();
                        Intent loginIntent = new Intent(getActivity(), LoginActivity.class);
                        startActivity(loginIntent);
                    }
                });
        normalDialog.setNegativeButton("Close",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                    }
                });
        normalDialog.show();
    }

}
