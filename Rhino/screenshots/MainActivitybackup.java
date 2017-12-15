package drawable;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.CheckBox;
import android.widget.ImageView;

import com.josfeenstra.mrpotatohead.R;

import java.util.HashMap;

public class MainActivitybackup extends AppCompatActivity {
    CheckBox cb;
    ImageView image;
//
//
//    HashMap<String, integer> imageState = new HashMap<String, Boolean>();
//    imageState.put("arms", false);
//
//    String var= imageState.get();




    //    HashMap[] IMAGE_NAMES = {"arms", "body", "ears", "eyebrows", "eyes",
//                           "glasses", "hat", "mouth", "mustache", "nose", "shoes"};




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d("TEST","somethings");

        updateView();
    }


    public void updateView() {

    }

    public void buttonArmsClicked(View view) {
        cb = findViewById(R.id.checkBoxArms);
        image = findViewById(R.id.imageViewArms);


        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonEarsClicked(View view) {
        cb = findViewById(R.id.checkBoxEars);
        image = findViewById(R.id.imageViewEars);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonEyebrowsClicked(View view) {
        cb = findViewById(R.id.checkBoxEyebrows);
        image = findViewById(R.id.imageViewEyebrows);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonEyesClicked(View view) {
        cb = findViewById(R.id.checkBoxEyes);
        image = findViewById(R.id.imageViewEyes);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }


    public void buttonGlassesClicked(View view) {
        cb = findViewById(R.id.checkBoxGlasses);
        image = findViewById(R.id.imageViewGlasses);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonHatClicked(View view) {
        cb = findViewById(R.id.checkBoxHat);
        image = findViewById(R.id.imageViewHat);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonMouthClicked(View view) {
        cb = findViewById(R.id.checkBoxMouth);
        image = findViewById(R.id.imageViewMouth);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonMustacheClicked(View view) {
        cb = findViewById(R.id.checkBoxMustache);
        image = findViewById(R.id.imageViewMustache);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonNoseClicked(View view) {
        cb = findViewById(R.id.checkBoxNose);
        image = findViewById(R.id.imageViewNose);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }

    public void buttonShoesClicked(View view) {
        cb = findViewById(R.id.checkBoxShoes);
        image = findViewById(R.id.imageViewShoes);

        if(cb.isChecked()) {
            image.setVisibility(View.VISIBLE);
        }
        else {
            image.setVisibility(View.INVISIBLE);
        }
    }


}
