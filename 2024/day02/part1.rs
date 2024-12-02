pub mod part1{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;

    pub fn run(){
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);

        let mut line_vec = vec![];
        let mut last_num: i32 = 0;
        let mut current_num: i32 = 0;
        let mut safe_reports = 0;
        let mut safe = true;
        let mut line_counter = 0;
        let mut increasing: bool;
        let mut decreasing: bool;

        for line in buf_reader.lines() {
            increasing = false;
            decreasing = false;
            line_counter += 1;
            last_num = 0;

            let l = line.unwrap();
            l.split_whitespace().for_each(|n| {
                line_vec.push(n.parse().unwrap());
                current_num = *line_vec.last().unwrap();
                if last_num != 0 {

                    if(!increasing && !decreasing){
                        if last_num < current_num {
                            increasing = true;
                        } else if last_num > current_num {
                            decreasing = true;
                        }
                    }

                    if last_num == current_num {
                        safe = false;
                        println!("same number, {} - {}, on line: {}", last_num, current_num, line_counter);
                    }
                    else if !((last_num - current_num).abs() >= 1 && (last_num - current_num).abs() <= 3) {
                        safe = false;
                        println!("gap too large, {} - {}, on line: {}", last_num, current_num, line_counter);
                    }
                    else if increasing && (last_num > current_num) {
                        safe = false;
                        println!("flipped, {} - {}, on line: {}", last_num, current_num, line_counter);
                    }
                    else if decreasing && (last_num < current_num) {
                        safe = false;
                        println!("flipped, {} - {}, on line: {}", last_num, current_num, line_counter);
                    }
                }

                last_num = current_num;
            });

            if safe { safe_reports += 1; }
            safe = true;
        }

        println!("Safe reports: {}", safe_reports);
    }
}