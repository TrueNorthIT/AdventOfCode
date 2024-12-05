import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {
        // Parse Input
        File input = new File("input.txt");
        Scanner inputReader = new Scanner(input);
        String data = "";
        while (inputReader.hasNextLine()) {
            data = data.concat(inputReader.nextLine()+"\n");
        }

        DayThree day_three = new DayThree();
        day_three.parseInput(data);
        day_three.partOne();
        day_three.partTwo();
    }
}