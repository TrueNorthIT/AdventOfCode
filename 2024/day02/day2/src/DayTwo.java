import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

import static java.lang.Math.abs;

public class DayTwo {

    ArrayList<ArrayList<Integer>> reports = new ArrayList<>();
    Boolean increasing;
    Boolean safe;
    int safe_levels = 0;

    public void parseInput(String input) {
        String[] lines = input.split("\n");
        for (String line: lines) {
            List<String> temp = List.of(line.split(" "));
            reports.add((ArrayList<Integer>) temp.stream().map(Integer::valueOf).collect(Collectors.toList()));
        }
    }

    public void partOne() {
        for (List<Integer> report: reports) {
            safe = true;
            increasing = report.get(1) > report.get(0);
            int diff = abs(report.get(1) - report.get(0));
            if (!(diff >= 1 && diff <= 3)) {
                continue;
            }
            for (int i=2; i < report.size(); i++) {
                diff = report.get(i) - report.get(i - 1);
                if ((diff > 0 && !increasing) || (diff < 0 && increasing)) {
                    safe = false;
                    break;
                } else if (!(abs(diff) >= 1 && abs(diff) <= 3)) {
                    safe = false;
                    break;
                }
            }
            safe_levels = safe ? safe_levels + 1 : safe_levels;
        }
        System.out.println(safe_levels);
    }

    public boolean oneReport(List<Integer> report) {
        safe = true;
        increasing = report.get(1) > report.get(0);
        int diff = abs(report.get(1) - report.get(0));
        if (!(diff >= 1 && diff <= 3)) {
            return false;
        }
        for (int i=2; i < report.size(); i++) {
            diff = report.get(i) - report.get(i - 1);
            if ((diff > 0 && !increasing) || (diff < 0 && increasing)) {
                safe = false;
                break;
            } else if (!(abs(diff) >= 1 && abs(diff) <= 3)) {
                safe = false;
                break;
            }
        }
        return safe;
    }

    public void partTwo() {
        safe_levels = 0;
        for (List<Integer> report: reports) {
            boolean currentSafe = false;
            currentSafe = oneReport(report);
            if (!currentSafe) {
                for (int i=0; i<report.size(); i++) {
                    ArrayList<Integer> temp = new ArrayList<>(List.copyOf(report));
                    temp.remove(i);
                    currentSafe = oneReport(temp);
                    if (currentSafe) {
                        break;
                    }
                }
            }
            safe_levels = currentSafe ? safe_levels + 1 : safe_levels;
        }
        System.out.println(safe_levels);
    }
}
