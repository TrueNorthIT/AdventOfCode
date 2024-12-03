pub mod part2{
    use std::fs;
    use std::io::BufRead;
    use regex::Regex;

    pub fn run() {
        let input = fs::read_to_string("./src/input.txt").expect("Error reading file");
        let re = Regex::new(r"(mul[(]\d+,\d+[)])|(do[(][)])|(don't[(][)])").unwrap();
        let mut enabled = true;
        let mut total = 0;

        re.find_iter(&input).map(|m| m.as_str()).for_each(|m| {
            match m {
                "do()" => {
                    enabled = true;
                    println!("do() found, enabling instructions...")
                },
                "don't()" => {
                    enabled = false;
                    println!("don't() found, disabling instructions...")
                },
                _ => {
                    if enabled {
                        let values = m.strip_prefix("mul(").unwrap().strip_suffix(")").unwrap().split(",").map(|x| x.parse::<i32>().unwrap()).collect::<Vec<i32>>();
                        println!("{}", values.iter().product::<i32>());
                        total += values.iter().product::<i32>();
                    }
                }
            }
        });

        println!("Total: {}", total);
    }
}