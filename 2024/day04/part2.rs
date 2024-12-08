pub mod part2{
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

        let directions = [(1, 1), (1, -1)];


        for (index_X, _) in wordsearch.rows().into_iter().enumerate() {
            for (index_Y, ch) in wordsearch.row(index_X).iter().enumerate() {
                if *ch == 'A' {
                    println!("Found: {} at: {},{}", ch, index_X, index_Y);
                    let mut match_count = 0;
                    for (dx, dy) in directions.iter() {

                        let mut i = index_X as i32 + dx;
                        let mut j = index_Y as i32 + dy;
                        println!("dx: {}, dy: {}", dx, dy);
                        println!("i: {}, j: {}", i, j);

                        if !bounds_check(i, j, x, y) {
                            break;
                        }

                        match wordsearch[[i as usize, j as usize]] {
                            'M' => {
                                println!("Matching: {} at: {},{}", wordsearch[[i as usize, j as usize]], i, j);
                                let mut i = index_X as i32 - dx;
                                let mut j = index_Y as i32 - dy;

                                if bounds_check(i, j, x, y) {
                                    println!("In bounds: {},{}", i, j);
                                } else {
                                    println!("Out of bounds: {},{}", i, j);
                                    break;
                                }
                                if wordsearch[[i as usize, j as usize]].eq_ignore_ascii_case(&'S') {
                                    println!("2nd level matching: {} at: {},{}", wordsearch[[i as usize, j as usize]], i, j);
                                    match_count += 1;
                                }

                            },
                            'S' => {
                                println!("Matching: {} at: {},{}", wordsearch[[i as usize, j as usize]], i, j);
                                let mut i = index_X as i32 - dx;
                                let mut j = index_Y as i32 - dy;

                                if bounds_check(i, j, x, y) {
                                    println!("In bounds: {},{}", i, j);
                                } else {
                                    println!("Out of bounds: {},{}", i, j);
                                    break;
                                }
                                if wordsearch[[i as usize, j as usize]].eq_ignore_ascii_case(&'M') {
                                    println!("2nd level matching: {} at: {},{}", wordsearch[[i as usize, j as usize]], i, j);
                                    match_count += 1;
                                }

                            }
                            _ => {
                                println!("Matched a non search char: {} at: {},{}", wordsearch[[i as usize, j as usize]], i, j);
                                break;
                            }
                        }
                        if match_count == 2 {
                            println!("Found X-MAS at: {},{}", index_X, index_Y);
                            total += 1;
                        }
                    }
                    println!("--------------");
                }
            }
        }
        println!("Total: {}", total);
    }

    fn bounds_check(i: i32, j: i32, x: i32, y: i32) -> bool {
        let index_bounds_x = 0..x;
        let index_bounds_y = 0..y;

        if index_bounds_x.contains(&i) && index_bounds_y.contains(&j) {
            println!("In bounds: {},{}", i, j);
            true
        } else {
            println!("Out of bounds: {},{}", i, j);
            false
        }
    }
}