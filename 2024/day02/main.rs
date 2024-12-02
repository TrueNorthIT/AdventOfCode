mod part1;
mod part2;

use std::io::{stdin, stdout, Write};

fn main() {

    let mut input = String::new();

    print!("Enter the part you want to run (1 or 2): ");
    let _ = stdout().flush();
    stdin().read_line(&mut input).expect("Did not enter a correct string");

    let input: i32 = input.trim().parse().unwrap();

    if input == 1 {
        part1::part1::run();
    }
    else if input == 2 {
        part2::part2::run();
    }
    else {
        println!("Invalid input");
    }
}