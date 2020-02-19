package com.example.cnn_project.app.authentication;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.cnn_project.R;
import com.example.cnn_project.app.home.HomeActivity;
import com.example.cnn_project.app.initial.MainActivity;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException;
import com.google.firebase.auth.FirebaseAuthUserCollisionException;
import com.google.firebase.auth.FirebaseAuthWeakPasswordException;


public class SignUpActivity extends AppCompatActivity {

    private EditText email_Signup, password_Signup, password2_Signup;
    private Button signupBtnSignup, backBtnSignup;
    private TextView messageTextView;

    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();

    private ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        setTitle("Sign up");

        email_Signup = findViewById(R.id.email_Signup);
        password_Signup = findViewById(R.id.password_Signup);
        password2_Signup = findViewById(R.id.password2_Signup);

        signupBtnSignup = findViewById(R.id.signupBtnSignup);
        backBtnSignup = findViewById(R.id.backBtnSignup);
        messageTextView = findViewById(R.id.messageTextViewSignup);
        firebaseAuth = FirebaseAuth.getInstance();

        backBtnSignup.setOnClickListener(backBtnOnClickListener);
        signupBtnSignup.setOnClickListener(signupBtnOnClickListener);
    }

    private View.OnClickListener signupBtnOnClickListener = new View.OnClickListener() {
        public void onClick(View v) {
            final String email = email_Signup.getText().toString();
            final String password = password_Signup.getText().toString();
            final String password2 = password2_Signup.getText().toString();

            if(TextUtils.isEmpty(email)){
                Toast.makeText(SignUpActivity.this, "Please enter email!", Toast.LENGTH_SHORT).show();
                email_Signup.requestFocus();
            }else if(TextUtils.isEmpty(password)){
                Toast.makeText(SignUpActivity.this, "Please enter password!", Toast.LENGTH_SHORT).show();
                password_Signup.requestFocus();
            }else if(TextUtils.isEmpty(password2)){
                Toast.makeText(SignUpActivity.this, "Please repeat your password!", Toast.LENGTH_SHORT).show();
                password2_Signup.requestFocus();
            }else if(!password.equals(password2)){
                Toast.makeText(SignUpActivity.this, "Passwords are different!", Toast.LENGTH_SHORT).show();
                password2_Signup.requestFocus();
            }else{
                progressDialog = ProgressDialog.show(SignUpActivity.this, "",
                        "Creating you account, please wait...", true);
                firebaseAuth.createUserWithEmailAndPassword(email, password)
                        .addOnCompleteListener(SignUpActivity.this, new OnCompleteListener<AuthResult>() {
                            @Override
                            public void onComplete(@NonNull Task task) {
                                if (!task.isSuccessful()) {
                                    progressDialog.dismiss();
                                    try {
                                        throw task.getException();
                                    } catch (FirebaseAuthWeakPasswordException e) {
                                        String msg = "The password you entered is too weak, please use another email.";
                                        password_Signup.setError(msg);
                                        password_Signup.requestFocus();
                                    } catch (FirebaseAuthInvalidCredentialsException e) {
                                        String msg = "The email you entered is invalid, please try again.";
                                        email_Signup.setError(msg);
                                        email_Signup.requestFocus();
                                    } catch (FirebaseAuthUserCollisionException e) {
                                        String msg = "The email is already registered, please try again.";
                                        email_Signup.setError(msg);
                                        email_Signup.requestFocus();
                                    } catch (Exception e) {
                                        String msg = e.getMessage();
                                        messageTextView.setError(msg);
                                        messageTextView.setText(msg);
                                    }
                                } else {
                                    progressDialog.dismiss();
                                    Toast.makeText(SignUpActivity.this, "Sign up successful!", Toast.LENGTH_SHORT).show();
                                    startActivity(new Intent(SignUpActivity.this, HomeActivity.class));
                                }
                            }
                        });
            }
            }

    };

    private View.OnClickListener backBtnOnClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            startActivity(new Intent(SignUpActivity.this, MainActivity.class));
        }
    };

    @Override
    public void onBackPressed() {
        Intent loginIntent = new Intent(this, LoginActivity.class);
        startActivity(loginIntent);
    }
}
