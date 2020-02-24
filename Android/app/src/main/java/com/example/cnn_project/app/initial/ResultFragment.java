package com.example.cnn_project.app.initial;

import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.cnn_project.R;
import com.example.cnn_project.app.utils;
import com.example.cnn_project.object.DatabaseEntry;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Map;

/**
 * This is the result page. When users successfully upload an image and there is a detected face
 * image, the page will go from upload page to result page.  It shows the processed image on the
 * top and detailed results. Detailed results are defined in FacesViewAdapter.
 */

public class ResultFragment extends Fragment {

    private RecyclerView recyclerView;
    private Context mContext;
    private JSONObject response;
    private String imgName;
    private ImageView imageView_response_image;

    private FirebaseAuth mAuth;
    private ProgressDialog progressDialog;
    private String modelToUse;

    public ResultFragment(JSONObject response, String imgName, Context mContext, String modelToUse) {
        this.mContext = mContext;
        this.response = response;
        this.imgName = imgName;
        this.modelToUse = modelToUse;
    }

    /**
     * If there is an account in login state, the detected results will be uploaded to realtime
     * database of the firebase. Otherwise, will not.
     */
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        final View view = inflater.inflate(R.layout.fragment_response, container, false);

        mAuth = FirebaseAuth.getInstance();
        FirebaseUser currentUser = mAuth.getCurrentUser();

        if (currentUser != null && !modelToUse.equals("yolo3")) {
            progressDialog = ProgressDialog.show(getActivity(), "","Please wait while the result is being uploaded to database...", true);
            uploadToFirebase(this.response, currentUser);
        }

        recyclerView = view.findViewById(R.id.faceRecyclerView);
        imageView_response_image = view.findViewById(R.id.imageView_response_image);
        byte[] decodedString;
        try {
            decodedString = Base64.decode((String) response.get("image"), Base64.DEFAULT);
            Bitmap decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
            imageView_response_image.setImageBitmap(decodedByte);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        mContext = getContext();

        try {
            JSONArray faceList = (JSONArray) response.get("faces");

            ArrayList<JSONObject> faceArrayList = new ArrayList<>();

            for (int i = 0; i < faceList.length(); i++) {
                JSONObject jsonFace = (JSONObject) faceList.get(i);
                faceArrayList.add(jsonFace);
            }

            FacesViewAdapter adapter = new FacesViewAdapter(getActivity(), faceArrayList);
            recyclerView.setAdapter(adapter);
            recyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));
            recyclerView.addItemDecoration(new DividerItemDecoration(mContext, DividerItemDecoration.VERTICAL));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return view;
    }

    /**
     * This is the function to upload the related data to firebase. The processed images are stored
     * to storage, while the other results are stored to realtime database.
     */
    @SuppressLint("StaticFieldLeak")
    private void uploadToFirebase(final JSONObject response, final FirebaseUser currentUser) {
        new AsyncTask<Void, Void, Void>() {
            @Override
            protected Void doInBackground(Void... voids) {
                try {
                    final DatabaseReference database = FirebaseDatabase.getInstance().getReference();
                    StorageReference storage = FirebaseStorage.getInstance().getReference();

                    final String userID = currentUser.getUid();
                    String currentDateTime = utils.getCurrentTime();
                    DatabaseReference newRef = database.child("users").child(userID).push();
                    DatabaseEntry entry = new DatabaseEntry(imgName, currentDateTime);
                    newRef.setValue(entry);
                    final String databaseEntryName = newRef.getKey();
                    String imgBase64 = (String) response.get("image");
                    byte[] decodedString;
                    decodedString = Base64.decode(imgBase64, Base64.DEFAULT);
                    final StorageReference imgRef = storage.child("upload").child(userID).child(databaseEntryName).child(newRef.getKey() + ".jpg");
                    imgRef.putBytes(decodedString).addOnSuccessListener(
                            new OnSuccessListener<UploadTask.TaskSnapshot>() {
                                @Override
                                public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                                    imgRef.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
                                        @Override
                                        public void onSuccess(Uri uri) {
                                            database.child("users").child(userID).child(databaseEntryName).child("image_location").setValue(uri.toString());
                                        }
                                    });
                                }
                            });

                    final JSONArray jsonFaces = response.getJSONArray("faces");
                    for (int i = 0; i < jsonFaces.length(); i++){
                        Map<String, Object> mapFaces = utils.jsonToMap((JSONObject) response.getJSONArray("faces").get(i));
                        database.child("users").child(userID).child(databaseEntryName).child("result").child(Integer.toString(i)).setValue(mapFaces.get("prediction"));
                        String faceBase64 = (String) mapFaces.get("face");
                        byte[] faceBytes;
                        faceBytes = Base64.decode(faceBase64, Base64.DEFAULT);
                        final StorageReference faceRef = storage.child("upload").child(userID).child(databaseEntryName).child(Integer.toString(i) + ".jpg");
                        final int finalI = i;
                        faceRef.putBytes(faceBytes).addOnSuccessListener(
                                new OnSuccessListener<UploadTask.TaskSnapshot>() {
                                    @Override
                                    public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                                        faceRef.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
                                            @Override
                                            public void onSuccess(Uri uri) {
                                                database.child("users").child(userID).child(databaseEntryName).child("result").child(Integer.toString(finalI)).child("image_location").setValue(uri.toString());
                                                if (finalI == jsonFaces.length()-1)
                                                    progressDialog.dismiss();
                                            }
                                        });
                                    }
                                });
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                return null;
            }
        }.execute();
    }
}
