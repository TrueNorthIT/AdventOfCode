pub mod part1{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;

    pub fn run() {

        //read in the file
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);

        let mut numbers1: Vec<i32> = Vec::new();
        let mut numbers2: Vec<i32> = Vec::new();
        let mut flag = true; //flag to determine which vector to push to (was feeling lazy)

        //for each line in the file split on whitespace and push to the appropriate vector
        for line in buf_reader.lines() {
            let l = line.unwrap();
            l.split_whitespace().for_each(|w| {
                if flag {
                    numbers1.push(w.parse::<i32>().unwrap());
                } else {
                    numbers2.push(w.parse::<i32>().unwrap());
                }
                flag = !flag;
            });
        }

        println!("numbers1 length: {}", numbers1.len());
        println!("numbers2 length: {}", numbers2.len());

        numbers1.sort_unstable();
        numbers2.sort_unstable();

        let mut total_distance = 0;

        //for each element in the vectors calculate the absolute difference and add to the total distance
        for i in 0..numbers1.len() {
            total_distance += (numbers1[i] - numbers2[i]).abs();
        }

        println!("Total distance: {}", total_distance);
    }
}