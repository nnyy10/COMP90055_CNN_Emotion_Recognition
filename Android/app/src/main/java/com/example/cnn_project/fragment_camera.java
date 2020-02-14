package com.example.cnn_project;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
//import android.support.v4.app.ActivityCompat;
import android.util.Base64;
import android.util.Log;
import android.util.TimingLogger;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.core.content.FileProvider;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;
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

    private Uri fileURI;
    private String fileString;

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

//                System.out.println(image);
                String model = "inception-resnet";
                if (radio_mobilenetv2.isChecked())
                    model = "mobilenetv2";
                else if (radio_yolo3.isChecked())
                    model = "yolo3";

                JSONObject postData = new JSONObject();
                try {
                    postData.put("image", image);
                    postData.put("model", model);


//                    new AsyncHttpTask().execute("http://10.1.1.238:5000/predict_api", postData.toString());
//                    task.execute();

//                    JSONObject obj = new JSONObject(response);

//                    System.out.println("face found: " + obj.get("found").toString());

//                    Toast.makeText(mContext, result, Toast.LENGTH_SHORT).show();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
//                } catch (InterruptedException e) {
//                    e.printStackTrace();
//                } catch (ExecutionException e) {
//                    e.printStackTrace();
//                }
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

    Uri tempPathUri;
    String tempPathString;
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

                        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                        // Create the File where the photo should go
                        File photoFile = null;
                        try {
                            photoFile = createImageFile();
                        } catch (IOException ex){
                            ex.printStackTrace();
                        }

                        if (photoFile != null) {
                            Uri photoURI = FileProvider.getUriForFile(mContext,
                                    "com.example.android.fileprovider",
                                    photoFile);
                            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                            startActivityForResult(takePictureIntent, 0);
                        }

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
                    System.out.println("debug1");
                    System.out.println(resultCode);
                    System.out.println(RESULT_OK);
                    System.out.println(data == null);
                    if (resultCode == RESULT_OK) {
                        System.out.println("debug2");
                        this.fileString = tempPathString;
                        tempPathString = "";
                        this.fileURI = tempPathUri;
                        tempPathUri = null;
//                        Bitmap selectedImage = (Bitmap) data.getExtras().get("data");
//                        imageView.setImageBitmap(selectedImage);
                        Bitmap bitmap = BitmapFactory.decodeFile(fileString);
                        ExifInterface ei = null;
                        try {
                            ei = new ExifInterface(fileString);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        int orientation = ei.getAttributeInt(ExifInterface.TAG_ORIENTATION,
                                ExifInterface.ORIENTATION_UNDEFINED);

                        Bitmap rotatedBitmap = null;
                        switch(orientation) {

                            case ExifInterface.ORIENTATION_ROTATE_90:
                                rotatedBitmap = rotateImage(bitmap, 90);
                                break;

                            case ExifInterface.ORIENTATION_ROTATE_180:
                                rotatedBitmap = rotateImage(bitmap, 180);
                                break;

                            case ExifInterface.ORIENTATION_ROTATE_270:
                                rotatedBitmap = rotateImage(bitmap, 270);
                                break;

                            case ExifInterface.ORIENTATION_NORMAL:
                            default:
                                rotatedBitmap = bitmap;
                        }

                        imageView.setImageBitmap(rotatedBitmap);

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
                                this.fileURI = Uri.parse(picturePath);
                                this.fileString = picturePath;
                                imageView.setImageBitmap(BitmapFactory.decodeFile(picturePath));
                                cursor.close();
                            }
                        }

                    }
                    break;
            }
            System.out.println(fileString.toString());
        }
    }


    private File createImageFile() throws IOException {
        // Create an image file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = mContext.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",         /* suffix */
                storageDir      /* directory */
        );

        tempPathString = image.getAbsolutePath();
        tempPathUri = Uri.parse(tempPathString);
        return image;
    }

    public static Bitmap rotateImage(Bitmap source, float angle) {
        Matrix matrix = new Matrix();
        matrix.postRotate(angle);
        return Bitmap.createBitmap(source, 0, 0, source.getWidth(), source.getHeight(),
                matrix, true);
    }
}