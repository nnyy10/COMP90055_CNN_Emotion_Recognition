package com.example.cnn_project;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
//import android.support.v4.app.ActivityCompat;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.ExecutionException;

import static android.app.Activity.RESULT_CANCELED;
import static android.app.Activity.RESULT_OK;

public class fragment_camera extends fragment_permission {

    //需要的权限数组 读/写/相机
    private static String[] PERMISSIONS_STORAGE = {Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.CAMERA };

    private TextView loginBtnCamera;
    private Button choose, upload;
    private ImageView imageView;
    private Context mContext;
    private RadioButton radio_inception_resnet, radio_mobilenetv2, radio_yolo3;

    private Uri filePath;

//    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
//    private FirebaseUser user = firebaseAuth.getCurrentUser();
//    FirebaseStorage storage = FirebaseStorage.getInstance();
//    StorageReference storageRef = storage.getReference();
//    StorageReference uidRef;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.mContext = getActivity();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        //通过参数中的布局填充获取对应布局
        View view = inflater.inflate(R.layout.fragment_camera, container, false);
        loginBtnCamera = view.findViewById(R.id.loginBtnCamera);
        choose = view.findViewById(R.id.choose);
        upload = view.findViewById(R.id.upload);
        imageView = view.findViewById(R.id.ImageView);
        radio_inception_resnet = view.findViewById(R.id.radioButton_inception_resnet);
        radio_mobilenetv2 = view.findViewById(R.id.radioButton_mobilenetv2);
        radio_yolo3 = view.findViewById(R.id.radioButton_yolo3);

        radio_inception_resnet.setChecked(true);

        loginBtnCamera.setOnClickListener(loginListener);
        choose.setOnClickListener(chooseListener);
        upload.setOnClickListener(uploadListender);


        return view;
    }

    private View.OnClickListener uploadListender = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(null!=imageView.getDrawable()){
                // photo
                BitmapDrawable drawable = (BitmapDrawable) imageView.getDrawable();
                Bitmap bitmap = drawable.getBitmap();
                ByteArrayOutputStream bos = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.PNG,100,bos);
                byte[] bb = bos.toByteArray();
                String image = Base64.encodeToString(bb, 0);

                String model = "inception-resnet";
                if (radio_mobilenetv2.isChecked())
                    model = "mobilenetv2";
                else if (radio_yolo3.isChecked())
                    model = "yolo3";

                JSONObject postData = new JSONObject();
                try {
                    postData.put("image", image);
                    postData.put("model", model);


                    AsyncHttpTask task = new AsyncHttpTask();
                    String response = task.execute("http://10.1.1.238:5000/predict_api", postData.toString()).get();

                    JSONObject obj = new JSONObject(response);

                    System.out.println("face found: " + obj.get("found").toString());

//                    Toast.makeText(mContext, result, Toast.LENGTH_SHORT).show();
                } catch (JSONException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
            } else{
                //no photo
            }
        }
    };

    private View.OnClickListener loginListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            startActivity(new Intent(getActivity(), LoginActivity.class));
        }
    };

    private View.OnClickListener chooseListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            final CharSequence[] options = {"Take Photo", "Choose from Gallery", "Cancel"};

            AlertDialog.Builder builder = new AlertDialog.Builder(mContext);
            builder.setTitle("Choose your profile picture");
            builder.setItems(options, new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int item) {

                    if (options[item].equals("Take Photo")) {
                        Intent takePicture = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
                        startActivityForResult(takePicture, 0);

                    } else if (options[item].equals("Choose from Gallery")) {
                        Intent pickPhoto = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                        startActivityForResult(pickPhoto, 1);

                    } else if (options[item].equals("Cancel")) {
                        dialog.dismiss();
                    }
                }
            });
            builder.show();
        }
    };

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(resultCode != RESULT_CANCELED) {
            switch (requestCode) {
                case 0:
                    if (resultCode == RESULT_OK && data != null) {
                        Bitmap selectedImage = (Bitmap) data.getExtras().get("data");
                        imageView.setImageBitmap(selectedImage);
                    }

                    break;
                case 1:
                    if (resultCode == RESULT_OK && data != null) {
                        Uri selectedImage =  data.getData();
                        String[] filePathColumn = {MediaStore.Images.Media.DATA};
                        if (selectedImage != null) {
                            Cursor cursor = this.getActivity().getContentResolver().query(selectedImage,
                                    filePathColumn, null, null, null);
                            if (cursor != null) {
                                cursor.moveToFirst();

                                int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
                                String picturePath = cursor.getString(columnIndex);
                                imageView.setImageBitmap(BitmapFactory.decodeFile(picturePath));
                                cursor.close();
                            }
                        }

                    }
                    break;
            }
        }
    }
}