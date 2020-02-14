//package com.example.cnn_project;
//
//public class ResultAdapter {
//}


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

public class ResultAdapter extends ArrayAdapter<Result> {

    private TextView result_id_layout, result_result_layout;
    private ImageView result_image_layout;

    private Activity context;
    private List<Result> resultList;

    public ResultAdapter(Activity context, List<Result> resultList){
        super(context, R.layout.result_layout, resultList);
        this.context = context;
        this.resultList = resultList;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View listViewItem = inflater.inflate(R.layout.result_layout, null, true);

        result_id_layout = listViewItem.findViewById(R.id.result_id_layout);
        result_result_layout = listViewItem.findViewById(R.id.result_result_layout);
        result_image_layout = listViewItem.findViewById(R.id.result_image_layout);

        Result result = resultList.get(position);
        result_id_layout.setText(result.getResult_id());
        result_result_layout.setText(result.getResult_reslut());

        Picasso.get().load(result.getResult_image()).into(result_image_layout);

        return listViewItem;
    }
}
