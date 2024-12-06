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

        DayFour day_four = new DayFour();
        day_four.parseInput(data);
        day_four.partOne();
        day_four.partTwo();
    }
}