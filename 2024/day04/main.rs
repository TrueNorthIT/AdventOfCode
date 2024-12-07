use std::fs::File;
use std::io;
use std::io::BufRead;
use ndarray::{array, Array2, Ix2, IxDyn};

fn main() {
    let input = File::open("./src/test.txt").expect("Cannot open file");
    let buf_reader = io::BufReader::new(input);
    let mut temp_input_holder: Vec<String> = Vec::new();
    let mut x:i32 = 0;
    let mut y:i32 = 0;

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

    for (index_X, _) in wordsearch.rows().into_iter().enumerate() {
        for (index_Y, ch) in wordsearch.row(index_X).iter().enumerate() {

            if *ch == 'X' {

            }

        }
    }
}
