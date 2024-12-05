import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import static java.lang.Math.abs;

public class DayThree {

    String string;
    ArrayList<Integer> mult_list = new ArrayList<>();
    int sum = 0;
    String regex = "mul\\((\\d{1,3})(,)(\\d{1,3})(\\))";
    String regex_2 = "((don't\\(\\)|do\\(\\)).*?)?(mul\\((\\d{1,3}))(,)(\\d{1,3})(\\))";
    Boolean do_match = true;
    public void parseInput(String input) {
        string = input.replaceAll("\\n", "");
    }

    public void partOne() {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(string);
        while (matcher.find()) {
            mult_list.add(Integer.parseInt(matcher.group(1)) * Integer.parseInt(matcher.group(3)));
        }
        for (Integer mult: mult_list) {
            sum += mult;
        }
        System.out.println(sum);
    }
    public void partTwo() {
        sum = 0;
        mult_list.clear();
        Pattern pattern = Pattern.compile(regex_2);
        Matcher matcher = pattern.matcher(string);
        while (matcher.find()) {
            if (do_match) {
                if (matcher.group(1) != null && matcher.group(1).startsWith("don't()")) {
                    do_match = false;
                } else {
                    mult_list.add(Integer.parseInt(matcher.group(4)) * Integer.parseInt(matcher.group(6)));
                }
            } else {
                if (matcher.group(1) != null && matcher.group(1).startsWith("do()")) {
                    do_match = true;
                    mult_list.add(Integer.parseInt(matcher.group(4)) * Integer.parseInt(matcher.group(6)));
                }
            }
        }
        for (Integer mult: mult_list) {
            sum += mult;
        }
        System.out.println(sum);
    }
}
