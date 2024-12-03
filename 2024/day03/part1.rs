pub mod part1{
    use std::fs;
    use std::io::BufRead;
    use regex::Regex;

    pub fn run() {
        let input = fs::read_to_string("./src/input.txt").expect("Error reading file");
        let re = Regex::new(r"(?:mul[(]\d+[,]\d+[)])").unwrap();


        let product:i32  = re.find_iter(&input).map(|m| m.as_str()).map(|m| m.strip_prefix("mul(").unwrap().strip_suffix(")").unwrap().split(",").map(|x| x.parse::<i32>().unwrap()).collect::<Vec<i32>>().iter().product::<i32>()).sum();
        println!("{}", product);

    }
}