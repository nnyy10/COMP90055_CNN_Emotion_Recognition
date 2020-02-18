package com.example.cnn_project.app.home;

import android.graphics.drawable.AnimationDrawable;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.cnn_project.R;

public class HomeFragment extends Fragment {

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        getActivity().setTitle("Home");

        int duration = 3500;
        int fade_duration = 2500;
        AnimationDrawable animation = new AnimationDrawable();
        animation.addFrame(getResources().getDrawable(R.drawable.angry), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.disgust), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.fear), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.happy), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.sad), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.neutral), duration);
        animation.addFrame(getResources().getDrawable(R.drawable.surprise), duration);
        animation.setOneShot(false);
        animation.setEnterFadeDuration(fade_duration);
        ImageView imageAnim = view.findViewById(R.id.imageView);
        imageAnim.setBackgroundDrawable(animation);

        animation.start();

        return view;
    }
}
