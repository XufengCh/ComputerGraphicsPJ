import processing.core.PApplet;
import ddf.minim.AudioPlayer;
import ddf.minim.Minim;
import ddf.minim.analysis.FFT;

import java.io.File;

public class MusicVisualization extends PApplet{
    private static String fileName;
    private static boolean isLoaded = false;

    private Minim minim;
    private AudioPlayer player;
    private FFT fft;

    @Override
    public void settings() {
        size(512, 400, P3D);
    }

    @Override
    public void setup() {
        background(0x000000);
        selectInput("请选择输入的音频文件： ", "loadFile");
    }

    public void loadFile(File file){
        if(file == null){
            println("No file selected. Exit. ");
            exit();
        }else{
            fileName = file.getName();
            println("User Select: " + file.getAbsolutePath());

            //load file
            minim = new Minim(this);
            player = minim.loadFile(file.getAbsolutePath());
            fft = new FFT(player.bufferSize(), player.sampleRate());
            println(fileName + " is playing...");
            isLoaded = true;
            player.play();
        }
    }

    @Override
    public void stop(){
        if(player != null){
            player.close();
            minim.stop();
        }
        super.stop();
    }

    @Override
    public void draw() {
        if(!isLoaded) return;

        background(0x000000);
        displayFileName();
        drawWaveform();
        drawFrequecySpectrum();
    }

    public void displayFileName(){
        fill(119, 119, 119);
        textAlign(CENTER, CENTER);
        textMode(SHAPE);
        textSize(13);
        text(fileName, width/2, height - 100);
    }

    public void drawWaveform(){
        int circleX = width/2;
        int circleY = 150;
        float a = 0;
        int slices = player.bufferSize();
        float angle = (2 * PI) / slices;
        for(int i = 0; i < slices - 1; i++){
            // the left sound channel
            float left_x1 = circleX + cos(a) * (50 * player.left.get(i) + 75);
            float left_y1 = circleY + sin(a) * (50 * player.left.get(i) + 75);
            float left_x2 = circleX + cos(a + angle) * (50 * player.left.get(i + 1) + 75);
            float left_y2 = circleY + sin(a + angle) * (50 * player.left.get(i + 1) + 75);
            // the right sound channel
            float right_x1 = circleX + cos(a) * (50 * player.right.get(i) + 75);
            float right_y1 = circleY + sin(a) * (50 * player.right.get(i) + 75);
            float right_x2 = circleX + cos(a + angle) * (50 * player.right.get(i + 1) + 75);
            float right_y2 = circleY + sin(a + angle) * (50 * player.right.get(i + 1) + 75);
            a += angle;
            // draw
            stroke(0, 221, 119, 127);
            line(left_x1, left_y1, left_x2, left_y2);
            stroke(0, 187, 255, 127);
            line(right_x1, right_y1, right_x2, right_y2);
        }
        noStroke();
    }

    public void drawFrequecySpectrum(){
        fft.forward(player.mix);

        noStroke();
        fill(238, 119, 0, 190);
        for(int i = 0; i < width/4; i++){
            float b = fft.getBand(i);
            rect(i * 4, height - b, 4, b);
        }
    }

    public static void main(String[] args){
        PApplet.main(new String[] {"MusicVisualization"});
    }
}
