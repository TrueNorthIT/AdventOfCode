import java.util.ArrayList;
import java.util.Collections;

public class DayOne {

    ArrayList<Integer> list_one = new ArrayList<Integer>();
    ArrayList<Integer> list_two = new ArrayList<Integer>();
    int total_distance = 0;
    int similarity = 0;

    public void parseInput(String input) {
        String[] split_input = input.split("\n");
        for (String row: split_input) {
            list_one.add(Integer.valueOf(row.split(" {3}")[0]));
            list_two.add(Integer.valueOf(row.split(" {3}")[1]));
        }
        Collections.sort(list_one);
        Collections.sort(list_two);
    }

    public void partOne() {
        for (int i = 0; i < list_one.size(); i++) {
            total_distance += Math.abs(list_one.get(i) - list_two.get(i));
        }
        System.out.println(total_distance);
    }

    public void partTwo() {
        for (Integer i : list_one) {
            similarity += i * Collections.frequency(list_two, i);
        }
        System.out.println(similarity);
    }
}
