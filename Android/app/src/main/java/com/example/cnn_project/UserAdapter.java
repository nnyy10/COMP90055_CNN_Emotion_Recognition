package com.example.cnn_project;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.List;

public class UserAdapter extends ArrayAdapter<User> {

    private TextView nane_layout, id_layout;

    private Activity context;
    private List<User> userList;

    public UserAdapter(Activity context, List<User> userList){
        super(context, R.layout.user_layout, userList);
        this.context = context;
        this.userList = userList;
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        LayoutInflater inflater = context.getLayoutInflater();
        View listViewItem = inflater.inflate(R.layout.user_layout, null, true);

        nane_layout = listViewItem.findViewById(R.id.nane_layout);
        id_layout = listViewItem.findViewById(R.id.id_layout);

        User user = userList.get(position);
        nane_layout.setText(user.getName());
        id_layout.setText(user.getId());

        return listViewItem;
    }
}
