package com.example.cnn_project;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.google.firebase.storage.StorageReference;
import com.squareup.picasso.Picasso;

import java.util.List;

public class HistoryAdapter extends ArrayAdapter<History> {

    private TextView image_name_layout, result_layout, submit_time_layout;
    private ImageView image_layout;

    private Activity context;
    private List<History> historyList;

    public HistoryAdapter(Activity context, List<History> historyList){
        super(context, R.layout.history_layout, historyList);
        this.context = context;
        this.historyList = historyList;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View listViewItem = inflater.inflate(R.layout.history_layout, null, true);

        image_name_layout = listViewItem.findViewById(R.id.image_name_layout);
        result_layout = listViewItem.findViewById(R.id.result_layout);
        submit_time_layout = listViewItem.findViewById(R.id.submit_time_layout);
        image_layout = listViewItem.findViewById(R.id.image_layout);

        History history = historyList.get(position);
        image_name_layout.setText(history.getImage_name());
        submit_time_layout.setText(history.getSubmit_time());
        result_layout.setText("Click");
//        result_layout.setText(history.getResult());

        Picasso.get().load(history.getImage_location()).into(image_layout);

        return listViewItem;
    }
}
