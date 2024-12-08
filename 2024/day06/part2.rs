pub mod part2{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;
    use ndarray::Array2;
    use std::sync::{Arc, Mutex};
    use std::thread;

    pub(crate) fn run() {
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);
        let mut temp_input_holder: Vec<String> = Vec::new();
        let mut x:i32 = 0;
        let mut y:i32 = 0;
        let mut maps: Vec<Array2<char>> = Vec::new();
        let loop_count = Arc::new(Mutex::new(0));

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

        let mut tiles = Array2::<char>::default((x as usize,y as usize));
        let mut x_pos = 0;
        let mut y_pos = 0;

        //fill array with values from file
        for (index_X, line) in temp_input_holder.iter().enumerate() {
            for (index_Y, ch) in line.chars().enumerate() {
                tiles[[index_X, index_Y]] = ch;
                if ch == '^' {
                    x_pos = index_X as i32;
                    y_pos = index_Y as i32;
                }
            }
        }

        let mut current_pos:(i32, i32) = (x_pos, y_pos);

        println!("tile[{:?},{:?}] = {:?}", x_pos, y_pos, tiles[[current_pos.0 as usize, current_pos.1 as usize]]);

        for (index_X, line) in temp_input_holder.iter().enumerate() {
            for (index_Y, ch) in line.chars().enumerate() {
                tiles[[index_X, index_Y]] = ch;
                if ch == '^' || ch == '#'{
                }
                else {
                    let mut modified_tiles = tiles.clone();
                    modified_tiles[[index_X, index_Y]] = '#';
                    maps.push(modified_tiles);
                }
            }
        }

        println!("Maps generated: {:?}", maps.len());

        let mut handles = vec![];

        for (index, map) in maps.into_iter().enumerate() {
            let loop_count = Arc::clone(&loop_count);
            let current_pos:(i32, i32) = (x_pos, y_pos);
            let handle = thread::spawn(move || {
                println!("Now executing map: {:?}", index);
                let overlap = execute_map(map, x, y, current_pos);
                if overlap {
                    let mut  count = loop_count.lock().unwrap();
                    *count += 1;
                }
            });
            handles.push(handle);
        }

        for handle in handles {
            handle.join().unwrap();
        }

        let final_loop_count = loop_count.lock().unwrap();

        println!("Loop Count: {:?}", final_loop_count);

    }

    fn execute_map(mut tiles: Array2<char>, x: i32, y: i32, mut current_pos: (i32, i32)) -> bool {
        let mut direction: (i32, i32) = (0,0);
        let mut rotation: usize = 0;
        let orientations:Vec<char> = vec!['^', '>', 'v', '<'];
        let mut in_map = true;
        let mut overlap = false;
        let mut travel_log: Vec<((i32,i32), (i32,i32))> = Vec::new();

        while in_map {
            match tiles[[current_pos.0  as usize, current_pos.1 as usize]] {
                '^' => {
                    direction = (-1,0);
                }
                'v' => {
                    direction = (1,0);
                }
                '<' => {
                    direction = (0,-1);
                }
                '>' => {
                    direction = (0,1);
                }
                _ => {
                    println!("Error: Target not found");
                    break;
                }
            }
            let mut blocked = false;
            while !blocked {

                let mut next_pos = (current_pos.0 + direction.0, current_pos.1 + direction.1);

                if next_pos.0 < 0 || next_pos.0 >= x  || next_pos.1 < 0 || next_pos.1 >= y {
                    tiles[[current_pos.0 as usize, current_pos.1 as usize]] = 'X';
                    in_map = false;
                    break;
                }

                if tiles[[next_pos.0 as usize , next_pos.1 as usize]] == '#' {
                    blocked = true;
                }
                else {
                    if travel_log.contains(&(next_pos, direction)) {
                        println!("Overlap Detected");
                        overlap = true;
                        break;
                    }
                    travel_log.push((current_pos, direction));
                    tiles[[current_pos.0 as usize, current_pos.1 as usize]] = 'X';
                    current_pos.0 += direction.0;
                    current_pos.1 += direction.1;
                    tiles[[current_pos.0 as usize, current_pos.1 as usize]] = orientations[rotation % 4];
                }
            }
            if !in_map || overlap {
                break;
            }
            rotation += 1;
            tiles[[current_pos.0 as usize, current_pos.1 as usize]] = orientations[rotation % 4];
        }

        let mut count = 0;
        for i in tiles.iter() {
            if *i == 'X' {
                count += 1;
            }
        }
        println!("Tiles Walked: {:?}", count);
        println!("Overlap: {:?}", overlap);
        overlap
    }
}