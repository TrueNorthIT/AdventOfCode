pub mod part1{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;
    use ndarray::Array2;

    pub fn run() {
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);
        let mut temp_input_holder: Vec<String> = Vec::new();
        let mut x:i32 = 0;
        let mut y:i32 = 0;
        let mut total:i32 = 0;

        //get size for array because I am too lazy to figure out dynamic sizing
        for line in buf_reader.lines() {
            let l = line.unwrap();
            if y == 0 {
                for _ in l.chars() {
                    y += 1;
                }
            }
            x += 1;
            temp_input_holder.push(l);
        }

        let mut wordsearch = Array2::<char>::default((x as usize,y as usize));

        //fill array with values from file
        for (index_X, line) in temp_input_holder.iter().enumerate() {
            for (index_Y, ch) in line.chars().enumerate() {
                wordsearch[[index_X, index_Y]] = ch;
            }
        }

        println!("{:?}", wordsearch);

        let search = "XMAS";

        let directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)];

        for (index_X, _) in wordsearch.rows().into_iter().enumerate() {
            for (index_Y, ch) in wordsearch.row(index_X).iter().enumerate() {
                if *ch == search.chars().next().unwrap() {
                    for (dx, dy) in directions.iter() {
                        let mut i = index_X as i32;
                        let mut j = index_Y as i32;
                        let mut match_count = 1;

                        println!("--------------");

                        while match_count <= search.len() && i >= 0 && i < x as i32 && j >= 0 && j < y as i32 {
                            if wordsearch[[i as usize, j as usize]] == search.chars().nth(match_count - 1).unwrap() {
                                println!("Found: {} at: {},{}", search.chars().nth(match_count - 1).unwrap(), i, j);
                                match_count += 1;
                            } else {
                                break;
                            }
                            i += dx;
                            j += dy;
                        }

                        if match_count == search.len() + 1 {
                            println!("Found {} at: {},{}. Direction: {},{}", search, index_X, index_Y, dx, dy);
                            total += 1;
                        }
                    }
                }
            }
        }
        println!("Total: {}", total);
    }
}