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

        DayTwo day_two = new DayTwo();

        day_two.parseInput(data);
        day_two.partOne();
        day_two.partTwo();

    }

}