import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.lang.Math.abs;

public class DayFour {
    int count = 0;
    ArrayList<List<String>> letters = new ArrayList<>();
    int dirs[][] = {{1,0},{-1,0},{0,1},{0,-1},{1,1},{-1,1}, {1,-1},{-1,-1}};
    String word = "XMAS";
    public void parseInput(String input) {
        String[] lines = input.split("\n");
        for (String line: lines) {
            List<String> temp = List.of(line.split(""));
            letters.add(temp);
        }
    }

    public void partOne() {
        for (int i=0; i<letters.size(); i++) {
            for (int j=0; j<letters.get(0).size(); j++) {
                if (Objects.equals(letters.get(i).get(j), "X")) {
                    count += findXmas(i,j);
                }
            }
        }
        System.out.println(count);
    }

    public int findXmas(int i, int j) {
        int matches_from_first_letter = 0;
        for (int[] dir : dirs) {
            if ((i + (dir[0]*(word.length()-1))) >= 0 && (i + (dir[0]*(word.length()-1))) < letters.size()) {
                if ((j + (dir[1]*(word.length()-1))) >= 0 && (j + (dir[1]*(word.length()-1))) < letters.get(0).size()) {
                    int temp_i = i;
                    int temp_j = j;
                    boolean correct = true;
                    for (String find_letter: word.split("")) {
                        if (Objects.equals(find_letter, "X")) {
                            continue;
                        }
                        temp_i += dir[0];
                        temp_j += dir[1];
                        if (Objects.equals(find_letter, letters.get(temp_i).get(temp_j))) {
                            continue;
                        } else {
                            correct = false;
                            break;
                        }
                    }
                    if (correct) {
                        matches_from_first_letter += 1;
                    }
                }
            }
        }
        return matches_from_first_letter;
    }

    public void partTwo() {

    }
}
