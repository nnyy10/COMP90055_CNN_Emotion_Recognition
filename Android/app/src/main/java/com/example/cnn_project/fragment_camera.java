package com.example.cnn_project;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
//import android.support.v4.app.ActivityCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import androidx.fragment.app.Fragment;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;

import java.io.File;
import java.io.IOException;

import static android.app.Activity.RESULT_CANCELED;

public class fragment_camera extends fragment_permission {

    //需要的权限数组 读/写/相机
    private static String[] PERMISSIONS_STORAGE = {Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.CAMERA };

    private TextView loginBtnCamera;
    private Button choose, upload;
    private ImageView ImageView;
    private Context mContext;

    private Uri filePath;

    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private FirebaseUser user = firebaseAuth.getCurrentUser();

    FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReference();
    StorageReference uidRef;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.mContext = getActivity();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        //通过参数中的布局填充获取对应布局
        View view =inflater.inflate(R.layout.fragment_camera, container,false);
        loginBtnCamera = view.findViewById(R.id.loginBtnCamera);
        choose = view.findViewById(R.id.choose);
        upload = view.findViewById(R.id.upload);
        ImageView = view.findViewById(R.id.ImageView);

        loginBtnCamera.setOnClickListener(loginListener);
        choose.setOnClickListener(chooseListener);

        return view;
    }

    private View.OnClickListener loginListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            startActivity(new Intent(getActivity(), LoginActivity.class));
        }
    };

    private View.OnClickListener chooseListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if(verifyPermissions(fragment_camera.this.getActivity(),PERMISSIONS_STORAGE[2]) == 0){
//                    L.e("提示是否要授权");
                ActivityCompat.requestPermissions(fragment_camera.this.getActivity(), PERMISSIONS_STORAGE, 3);
            }
            showTypeDialog();
        }
    };

    private void showTypeDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        final AlertDialog dialog = builder.create();
        View view = View.inflate(getActivity(), R.layout.fragment_profile_select, null);
        TextView select_gallery = view.findViewById(R.id.select_gallery);
        TextView select_camera = view.findViewById(R.id.select_camera);

        select_gallery.setOnClickListener(new View.OnClickListener() {// 在相册中选取
            @Override
            public void onClick(View v) {
                toPicture();
                dialog.dismiss();
            }
        });

        select_camera.setOnClickListener(new View.OnClickListener() {// 调用照相机
            @Override
            public void onClick(View v) {
                toCamera();
                dialog.dismiss();
            }
        });
        dialog.setView(view);
        dialog.show();
    }

    private File tempFile = null;   //新建一个 File 文件（用于相机拿数据）

    //获取 相机 或者 图库 返回的图片
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        //判断返回码不等于0
        if (requestCode != RESULT_CANCELED){    //RESULT_CANCELED = 0(也可以直接写“if (requestCode != 0 )”)
            //读取返回码
            switch (requestCode){
                case 100:   //相册返回的数据（相册的返回码）
//                    L.e("相册");
                    Uri uri01 = data.getData();
                    try {
                        Bitmap bitmap = BitmapFactory.decodeStream(this.getActivity().getContentResolver().openInputStream(uri01));
                        ImageView.setImageBitmap(bitmap);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                    break;
                case 101:  //相机返回的数据（相机的返回码）
//                    L.e("相机");
                    try {
                        tempFile = new File(Environment.getExternalStorageDirectory(),"fileImg.jpg");  //相机取图片数据文件
                        Uri uri02 = Uri.fromFile(tempFile);   //图片文件
                        Bitmap bitmap = BitmapFactory.decodeStream(this.getActivity().getContentResolver().openInputStream(uri02));
                        ImageView.setImageBitmap(bitmap);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    break;
            }
        }
    }

    //跳转相册
    private void toPicture() {
        Intent intent = new Intent(Intent.ACTION_PICK);  //跳转到 ACTION_IMAGE_CAPTURE
        intent.setType("image/*");
        startActivityForResult(intent,100);
//        Log.e("跳转相册成功");
    }

    //跳转相机
    private void toCamera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);  //跳转到 ACTION_IMAGE_CAPTURE
        //判断内存卡是否可用，可用的话就进行存储
        //putExtra：取值，Uri.fromFile：传一个拍照所得到的文件，fileImg.jpg：文件名
        intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(new File(Environment.getExternalStorageDirectory(), "fileImg.jpg")));
        startActivityForResult(intent, 101); // 101: 相机的返回码参数（随便一个值就行，只要不冲突就好）
        //Log.e("跳转相机成功");
    }
}