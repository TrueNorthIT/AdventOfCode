use std::fs::File;
use std::io::{Read};
use std::path::Path;
use regex::{Captures, Match, Matches, Regex};
use regex::bytes::CaptureMatches;

fn read_input(filename: &str) -> String {
    let path = Path::new(filename);
    let display = path.display();
    let mut file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why),
        Ok (file) => file,
    };
    let mut input = String::new();
    file.read_to_string(&mut input).expect("couldn't read input file");
    return input;
}

fn part_1(input: &str) -> i32 {
    let mult_regex = Regex::new(r"mul\((?<d1>\d{1,3}),(?<d2>\d{1,3})\)").unwrap();
    let ans: i32 = mult_regex.captures_iter(input).map(|c| &c["d1"].parse::<i32>().unwrap() * &c["d2"].parse::<i32>().unwrap()).sum();
    
    ans
}

fn main() {
    let input = read_input("day03/input.txt");
    println!("Part 1: {}", part_1("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"));
}