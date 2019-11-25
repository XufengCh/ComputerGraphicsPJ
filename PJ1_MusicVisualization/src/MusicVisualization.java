import ddf.minim.analysis.*;
import ddf.minim.Minim;
import ddf.minim.AudioPlayer;
import processing.core.PApplet;

import java.io.File;

public class MusicVisualization extends PApplet{
    private static String fileName;
    private static boolean isRunning = false;

    private Minim minim;
    private AudioPlayer player;
    private FFT fft;

    private int circleX;
    private int circleY;

    /**
     * select the file to open
     * @param file the file to open
     */
    public void fileSelect(File file){
        if(file == null){
            println("No file selected. Exit. ");
            stop();
        }else{
            String filePath = file.getAbsolutePath();
            fileName = file.getName();
            isRunning = true;
            println("User selected: " + filePath);
            // load file
            minim = new Minim(this);
            player = minim.loadFile(filePath);
            fft = new FFT(player.bufferSize(), player.sampleRate());
            player.play();
            println(fileName + " is playing...");
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
    public void settings(){
        size(512, 512);
    }

    @Override
    public void setup(){
        size(512, 512);
        background(0x000000);
        selectInput("Select a file: ", "fileSelect");

        circleX = width/2;
        circleY = 145;
    }

    private void displayFileName(){
        /*PFont font = createFont("Arial",16,true);
        textFont(font, 16);*/
        //        fill(0xffffff);
        //        textAlign(CENTER, CENTER);
        //        //fill(0x777777);
        text(fileName, 256, height - 200);
    }

    private void drawWaveform(){
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
            float right_y1 = circleX + sin(a) * (50 * player.right.get(i) + 75);
            float right_x2 = circleX + cos(a + angle) * (50 * player.right.get(i + 1) + 75);
            float right_y2 = circleX + sin(a + angle) * (50 * player.right.get(i + 1) + 75);
            a += angle;
            // draw
            stroke(0xffee99, (float) 0.5);
            line(left_x1, left_y1, left_x2, left_y2);
            line(right_x1, right_y1, right_x2, right_y2);
        }
    }

    private void drawFrequencySpectrum(){
        fft.forward(player.mix);

        noStroke();
        fill(0xee7700, (float) 0.3);
        for(int i = 0; i < width/4; i++){
            float b = fft.getBand(i);
            rect(i * 4, height - b, 4, b);
        }
    }

    @Override
    public void draw(){
        if(!isRunning) return;

        background(0x000000);
        // fileName
        displayFileName();
        /*// waveform
        fill(0x9999ff, (float) 0.7);
        ellipse(circleX, circleY, 25, 25);
        fill(0xffee99, (float) 0.7);
        ellipse(circleX, circleY, 20, 20);
        drawWaveform();
        // frequency spectrum
        drawFrequencySpectrum();*/
    }

    public static void main(String[] args){
        PApplet.main(new String[] {"MusicVisualization"});
    }
}
