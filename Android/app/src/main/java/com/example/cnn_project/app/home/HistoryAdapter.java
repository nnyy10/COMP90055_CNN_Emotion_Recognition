package com.example.cnn_project.app.home;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.cnn_project.R;
import com.example.cnn_project.object.History;
import com.squareup.picasso.Picasso;

import java.util.List;

public class HistoryAdapter extends ArrayAdapter<History> {

    private TextView image_name_layout, result_layout, submit_time_layout;
    private ImageView image_layout;

    private AppCompatActivity context;
    private List<History> historyList;

    public HistoryAdapter(AppCompatActivity context, List<History> historyList){
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

        final History history = historyList.get(position);
        image_name_layout.setText(" " + history.image_name);
        submit_time_layout.setText(" " + history.submit_time);
        result_layout.setText(" Click");

        Picasso.get().load(history.image_location).into(image_layout);

        result_layout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ResultFragment resultFragment = new ResultFragment(history.image_location, history.facesSnapshot);
                context.getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, resultFragment).commit();
            }
        });

        return listViewItem;
    }
}
