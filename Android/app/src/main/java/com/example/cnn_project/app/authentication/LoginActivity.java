package com.example.cnn_project.app.authentication;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.cnn_project.app.home.HomeActivity;
import com.example.cnn_project.R;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.FirebaseTooManyRequestsException;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException;
import com.google.firebase.auth.FirebaseUser;

public class LoginActivity extends AppCompatActivity {

    private EditText email_Login, password_Login;
    private Button loginBtnLogin, signupBtnLogin;
    private TextView messageTextView;

    private FirebaseAuth firebaseAuth = FirebaseAuth.getInstance();
    private FirebaseAuth.AuthStateListener mAuthStateListener;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        email_Login = findViewById(R.id.email_Login);
        password_Login = findViewById(R.id.password_Login);
        loginBtnLogin = findViewById(R.id.loginBtnLogin);
        signupBtnLogin = findViewById(R.id.signupBtnLogin);
        messageTextView = findViewById(R.id.messageTextViewLogin);

        loginBtnLogin.setOnClickListener(loginListener);
        signupBtnLogin.setOnClickListener(signupListener);

        mAuthStateListener = new FirebaseAuth.AuthStateListener() {
            @Override
            public void onAuthStateChanged(@NonNull FirebaseAuth firebaseAuth) {
                FirebaseUser firebaseUser = firebaseAuth.getCurrentUser();
                if(firebaseUser != null){
                    Intent loginIntent = new Intent(LoginActivity.this, HomeActivity.class);
                    startActivity(loginIntent);
                }
            }
        };
    }

    private View.OnClickListener signupListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            startActivity(new Intent(LoginActivity.this, SignUpActivity.class));
        }
    };

    private View.OnClickListener loginListener = new View.OnClickListener() {
        public void onClick(View v) {
            final String email = email_Login.getText().toString();
            String password = password_Login.getText().toString();
            if (TextUtils.isEmpty(email)){
                Toast.makeText(LoginActivity.this, "Please enter email!", Toast.LENGTH_SHORT).show();
                email_Login.requestFocus();
            } else if (TextUtils.isEmpty(password)) {
                Toast.makeText(LoginActivity.this, "Please enter password!", Toast.LENGTH_SHORT).show();
                password_Login.requestFocus();
            } else {
                firebaseAuth.signInWithEmailAndPassword(email, password).addOnCompleteListener(LoginActivity.this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(!task.isSuccessful()){
                            try {
                                throw task.getException();
                            } catch(FirebaseAuthInvalidCredentialsException e) {
                                String msg = "Log in failed, wrong email or password, \nplease try again.";
                                messageTextView.setText(msg);
                                messageTextView.requestFocus();
                            } catch(FirebaseTooManyRequestsException e) {
                                String msg = "Too many failed login attempts, try again later.";
                                messageTextView.setText(msg);
                                messageTextView.requestFocus();
                            } catch(Exception e) {
                                String msg = e.getMessage();
                                messageTextView.setError(msg);
                                messageTextView.setText(msg);
                                Toast.makeText(LoginActivity.this, e.toString(), Toast.LENGTH_SHORT).show();
                            }
                        } else{
                            Toast.makeText(LoginActivity.this, "Successful log in!", Toast.LENGTH_SHORT).show();
                            Intent homeIntent = new Intent(LoginActivity.this, HomeActivity.class);
                            startActivity(homeIntent);
                        }
                    }
                });
            }
        }
    };

    @Override
    protected void onStart(){
        super.onStart();
        firebaseAuth.addAuthStateListener(mAuthStateListener);
    }

}
