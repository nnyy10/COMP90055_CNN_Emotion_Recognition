package com.example.cnn_project.app.initial;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.provider.Settings;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RadioButton;
import android.widget.Toast;

import androidx.core.content.FileProvider;

import com.example.cnn_project.R;
import com.example.cnn_project.app.utils;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.Date;

import static android.app.Activity.RESULT_CANCELED;
import static android.app.Activity.RESULT_OK;
import com.example.cnn_project.app.Global;

public class UploadFragment extends PermissionFragment {

    private Button choose, upload;
    private ImageView imageView;
    private Context mContext;
    private RadioButton radio_inception_resnet, radio_mobilenetv2, radio_yolo3;

    private String fileString;
    private Uri tempPathUri;
    private String tempPathString;

    private ProgressDialog progressDialog;

    private String modelUsed = "";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.mContext = getActivity();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_initial, container, false);

        getActivity().setTitle("Upload");

        choose = view.findViewById(R.id.choose);
        upload = view.findViewById(R.id.upload);
        imageView = view.findViewById(R.id.ImageView);
        radio_inception_resnet = view.findViewById(R.id.radioButton_inception_resnet);
        radio_mobilenetv2 = view.findViewById(R.id.radioButton_mobilenetv2);
        radio_yolo3 = view.findViewById(R.id.radioButton_yolo3);

        radio_inception_resnet.setChecked(true);

        choose.setOnClickListener(chooseListener);
        upload.setOnClickListener(uploadListender);

        return view;
    }

    private View.OnClickListener uploadListender = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if (null != imageView.getDrawable()) {
                progressDialog = ProgressDialog.show(mContext, "",
                        "Please wait while the image is being processed...", true);
                Thread thread = new Thread() {
                    @Override
                    public void run() {
                        BitmapDrawable drawable = (BitmapDrawable) imageView.getDrawable();
                        Bitmap bitmap = drawable.getBitmap();
                        ByteArrayOutputStream bos = new ByteArrayOutputStream();
                        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, bos);
                        byte[] bb = bos.toByteArray();
                        String image = Base64.encodeToString(bb, 0);

                        String model = "inception-resnet";
                        if (radio_mobilenetv2.isChecked())
                            model = "mobilenetv2";
                        else if (radio_yolo3.isChecked())
                            model = "yolo3";

                        modelUsed = model;

                        JSONObject postData = new JSONObject();
                        try {
                            postData.put("image", image);
                            postData.put("model", model);

                            AsyncHttpTask task = new AsyncHttpTask();
                            task.execute(Global.URL + Global.API_NAME, postData.toString());
                        } catch (JSONException e) {
                            Toast.makeText(mContext, "Error: Unable to construct out going JSON.", Toast.LENGTH_LONG).show();
                            progressDialog.dismiss();
                        }
                    }
                };
                thread.start();
            } else {
                Toast.makeText(mContext, "No photo selected!", Toast.LENGTH_SHORT).show();
            }
        }
    };

    private void processResponse(String response) {
        progressDialog.dismiss();
        if (response == null){
            Toast.makeText(mContext, "An error has occured. Cannot connect to the prediction server.", Toast.LENGTH_LONG).show();
            return;
        }
        try {
            JSONObject obj = new JSONObject(response);
            if((boolean) obj.get("found")) {
                Toast.makeText(mContext, "found face", Toast.LENGTH_LONG).show();
                String fileName = fileString.substring(fileString.lastIndexOf("/")+1);
                ResultFragment resultFragment = new ResultFragment(obj, fileName, this.mContext, modelUsed);
                getActivity()
                        .getSupportFragmentManager()
                        .beginTransaction()
                        .replace(R.id.fragment_container, resultFragment)
                        .addToBackStack(null)
                        .commit();
            }
            else if(!((boolean) obj.get("found")))
                Toast.makeText(mContext, "No face detected in image, try another image.", Toast.LENGTH_LONG).show();
        } catch (JSONException e) {
            Toast.makeText(mContext, "Error: Unable to parse JSON response from server.", Toast.LENGTH_LONG).show();
        }
    }


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
                        } catch (IOException ex) {
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
        if (resultCode != RESULT_CANCELED) {
            Uri fileURI;
            switch (requestCode) {
                case 0:
                    if (resultCode == RESULT_OK) {
                        this.fileString = tempPathString;
                        tempPathString = "";
                        fileURI = tempPathUri;
                        tempPathUri = null;
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
                        switch (orientation) {
                            case ExifInterface.ORIENTATION_ROTATE_90:
                                rotatedBitmap = utils.rotateImage(bitmap, 90);
                                break;
                            case ExifInterface.ORIENTATION_ROTATE_180:
                                rotatedBitmap = utils.rotateImage(bitmap, 180);
                                break;
                            case ExifInterface.ORIENTATION_ROTATE_270:
                                rotatedBitmap = utils.rotateImage(bitmap, 270);
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
                        Uri selectedImage = data.getData();
                        String[] filePathColumn = {MediaStore.Images.Media.DATA};
                        if (selectedImage != null) {
                            Cursor cursor = this.getActivity().getContentResolver().query(selectedImage,
                                    filePathColumn, null, null, null);
                            if (cursor != null) {
                                cursor.moveToFirst();

                                int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
                                String picturePath = cursor.getString(columnIndex);
                                fileURI = Uri.parse(picturePath);
                                this.fileString = picturePath;
                                imageView.setImageURI(selectedImage);
                                cursor.close();
                            }
                        }
                    }
                    break;
            }
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


    class AsyncHttpTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {

            HttpURLConnection httpURLConnection = null;
            try {

                httpURLConnection = (HttpURLConnection) new URL(params[0]).openConnection();
                httpURLConnection.setRequestMethod("POST");
                httpURLConnection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");

                httpURLConnection.setDoOutput(true);

                DataOutputStream wr = new DataOutputStream(httpURLConnection.getOutputStream());
                wr.writeBytes(params[1]);
                wr.flush();
                wr.close();

                int status = httpURLConnection.getResponseCode();

                switch (status) {
                    case 200:
                        BufferedReader br = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
                        StringBuilder sb = new StringBuilder();
                        String line;
                        while ((line = br.readLine()) != null) {
                            sb.append(line + "\n");
                        }
                        br.close();
                        return sb.toString();
                }
            } catch (Exception e) {
                return null;
            } finally {
                if (httpURLConnection != null) {
                    httpURLConnection.disconnect();
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(String result) {
            processResponse(result);
        }
    }
}

