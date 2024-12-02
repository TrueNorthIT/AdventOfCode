pub mod part2 {
    use std::fs::File;
    use std::io;
    use std::io::BufRead;

    pub fn run() {
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);

        let mut line_vec: Vec<i32> = vec![];
        let mut safe_reports = 0;
        let mut line_counter = 0;

        for line in buf_reader.lines() {
            line_vec.clear();
            line_counter += 1;

            let l = line.unwrap();
            l.split_whitespace().for_each(|n| {
                line_vec.push(n.parse().unwrap());
            });

            let mut safe = check_line(line_counter, line_vec.clone());

            if !safe {
                safe = dampener(line_counter, line_vec.clone());
            } else {
                println!("Line {} is safe without dampening", line_counter);
            }

            if safe {
                safe_reports += 1;
            } else { println!("Line {} is not safe", line_counter); }


            println!("Line {}: {:?}", line_counter, line_vec);
        }

        println!("Safe reports: {}", safe_reports);
    }

    fn check_line(line_counter: i32, line_vec: Vec<i32>) -> bool {
        let mut last_num: i32 = 0;
        let mut current_num: i32 = 0;
        let mut safe: bool = true;
        let mut increasing: bool = false;
        let mut decreasing: bool = false;

        for (index, number) in line_vec.iter().enumerate() {
            current_num = number.clone();
            if last_num != 0 {
                if (!increasing && !decreasing) {
                    if last_num < current_num {
                        increasing = true;
                    } else if last_num > current_num {
                        decreasing = true;
                    }
                }

                if last_num == current_num {
                    safe = false;
                    println!("same number, {} - {}, on line: {}", last_num, current_num, line_counter);
                    break;
                } else if !((last_num - current_num).abs() >= 1 && (last_num - current_num).abs() <= 3) {
                    safe = false;
                    println!("gap too large, {} - {}, on line: {}", last_num, current_num, line_counter);
                    break;
                } else if increasing && (last_num > current_num) {
                    safe = false;
                    println!("flipped, {} - {}, on line: {}", last_num, current_num, line_counter);
                    break;
                } else if decreasing && (last_num < current_num) {
                    safe = false;
                    println!("flipped, {} - {}, on line: {}", last_num, current_num, line_counter);
                    break;
                }
            }

            last_num = current_num;
        }

        safe
    }

    fn dampener(line_counter: i32, line_vec: Vec<i32>) -> bool {
        println!("the dampener has been let loose on line: {}", line_counter);

        let mut safe: bool = false;
        for (index, number) in line_vec.iter().enumerate() {
            let mut dampen_target = line_vec.clone();
            dampen_target.remove(index);
            let safe = check_line(line_counter, dampen_target);
            if safe {
                println!("The Dampener has deemed line: {} safe, I guess...", line_counter);
                return safe;
            }
        }

        println!("The Dampener has failed to make line: {} safe", line_counter);
        safe
    }
}