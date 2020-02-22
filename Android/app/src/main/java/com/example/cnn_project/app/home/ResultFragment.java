package com.example.cnn_project.app.home;

import android.content.Context;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.example.cnn_project.R;
import com.example.cnn_project.object.Face;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

/**
 * This is the result page. When users click the "click" button in the history page, the page will go
 * from history page to result page. It shows the processed image on the top and detailed results.
 * Detailed results are defined in FaceViewAdapter.
 */

public class ResultFragment extends Fragment {

    private RecyclerView recyclerView;
    private Context mContext;
    private String imageLocation;
    private ImageView imageView_response_image;
    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private String userID = firebaseAuth.getCurrentUser().getUid();
    private Iterable<DataSnapshot> facesSnapshot;

    public ResultFragment(String imageLocation, Iterable<DataSnapshot> facesSnapshot) {
        this.imageLocation = imageLocation;
        this.facesSnapshot = facesSnapshot;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.fragment_result, container, false);
        getActivity().setTitle("Result");

        imageView_response_image = view.findViewById(R.id.imageView_response_image);
        recyclerView = view.findViewById(R.id.faceRecyclerView);
        mContext = getContext();

        Picasso.get().load(imageLocation).into(imageView_response_image);

        ArrayList faceList = new ArrayList();
        for(DataSnapshot faceSnapshot: facesSnapshot){
            ArrayList<JSONObject> emotions = new ArrayList<>();
            for (int i = 0; i < 7; i++) {
                try {
                    if(faceSnapshot.child(Integer.toString(i)).getValue() == null)
                        break;
                    JSONObject emotion = new JSONObject(faceSnapshot.child(Integer.toString(i)).getValue().toString());
                    emotions.add(emotion);
                } catch (JSONException e) { e.printStackTrace(); }
            }
            Face faceObject = new Face(faceSnapshot.child("image_location").getValue().toString(), emotions);
            faceList.add(faceObject);
        }

        FaceViewAdapter adapter = new FaceViewAdapter(getActivity(), faceList);
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
        recyclerView.addItemDecoration(new DividerItemDecoration(mContext,DividerItemDecoration.VERTICAL));

        return view;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setHasOptionsMenu(true);
    }

    /**
     * There is a "back" button in the menu. When clicking it, the page will go from the result
     * page to the history page.
     */

    @Override
    public void onCreateOptionsMenu(Menu menu, MenuInflater inflater) {
        inflater.inflate(R.menu.menu_result, menu);
        super.onCreateOptionsMenu(menu, inflater);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item){
        switch (item.getItemId()) {
            case R.id.main_back:
                getActivity()
                        .getSupportFragmentManager()
                        .beginTransaction()
                        .replace(R.id.fragment_container, new HistoryFragment())
                        .commit();
                break;
        }
        return super.onOptionsItemSelected(item);
    }
}
