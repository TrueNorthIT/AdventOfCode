pub mod part2{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;

    pub fn run() {
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);

        let mut numbers1: Vec<i32> = Vec::new();
        let mut numbers2: Vec<i32> = Vec::new();
        let mut flag = true;
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

        let mut similarity_score = 0;
        let mut occurrences = 0;

        for number1 in numbers1.iter(){
            for number2 in numbers2.iter(){
                if number1 == number2{
                    occurrences += 1;
                }
            }
            similarity_score += occurrences * number1;
            occurrences = 0;
        }

        println!("Similarity score: {}", similarity_score);
    }
}