package com.example.cnn_project;

//public class permission_fragment {
//}

//package com.example.cnn_project;

import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;

public class permission_fragment extends Fragment {

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //跳转相机动态权限
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
            StrictMode.setVmPolicy(builder.build());
        }
    }

    /**
     * 检查是否有对应权限
     *
     * @param activity 上下文
     * @param permission 要检查的权限
     * @return  结果标识
     */
    public int verifyPermissions(Activity activity, java.lang.String permission) {
        int Permission = ActivityCompat.checkSelfPermission(activity,permission);
        if (Permission == PackageManager.PERMISSION_GRANTED) {
//            L.e("已经同意权限");
            return 1;
        }else{
//            L.e("没有同意权限");
            return 0;
        }
    }
}

