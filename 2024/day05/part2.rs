pub mod part2{
    use std::fs::File;
    use std::io;
    use std::io::BufRead;

    pub(crate) fn run() {
        let input = File::open("./src/input.txt").expect("Cannot open file");
        let buf_reader = io::BufReader::new(input);

        let mut rules:Vec<(i32,i32)> = Vec::new();
        let mut updates:Vec<Vec<i32>> = Vec::new();

        for line in buf_reader.lines() {
            let line = line.unwrap();
            if line.contains('|'){
                let mut parts = line.split("|");
                let mut rule_part1 = parts.next().unwrap().trim().parse::<i32>().unwrap();
                let mut rule_part2 = parts.next().unwrap().trim().parse::<i32>().unwrap();
                rules.push((rule_part1, rule_part2));
            }
            else if line.contains(',') {
                let mut parts = line.split(",");
                let mut update:Vec<i32> = Vec::new();
                for part in parts {
                    update.push(part.trim().parse::<i32>().unwrap());
                }
                updates.push(update);
            }
        }

        for (index, rule) in rules.iter().enumerate() {
            println!("Rule {}: {:?}", index + 1, rule);
        }

        for (index, update) in updates.iter().enumerate() {
            println!("Update {}: {:?}", index + 1, update);
        }

        let mut sorted_updates:Vec<Vec<i32>> = Vec::new();

        for (index, update) in updates.iter().enumerate() {
            println!("Update {}: {:?}", index + 1, update);
            let sorted_result = order_update(rules.clone(), update.clone());
            if sorted_result.1 {
                println!("Sorted update {}: {:?}", index, sorted_result.0);
                sorted_updates.push(sorted_result.0);
            }
            else {
                println!("Update is already sorted");
            }
            println!("---------")
        }

        let mut total = 0;

        for (index, update) in sorted_updates.iter().enumerate() {
            println!("update {}: {:?}", index +1 , update);
            println!("Middle value of update {}: {}", index + 1, update[update.len() / 2]);
            total += update[update.len() / 2];
            println!("total: {}", total);
            println!("---------");
        }

        println!("Total: {}", total);
    }

    fn order_update(rules:Vec<(i32,i32)>, mut update:Vec<i32>) -> (Vec<i32>, bool) {
        let mut sorted = false;
        let mut adjusted = false;
        while !sorted {
            sorted = true;
            for rule in &rules {
                if update.contains(&rule.0) && update.contains(&rule.1) {
                    let index_a = update.iter().position(|&x| x == rule.0).unwrap();
                    let index_b = update.iter().position(|&x| x == rule.1).unwrap();

                    if index_a > index_b {
                        println!("using rule: {:?}", rule);
                        update.swap(index_a, index_b);
                        sorted = false;
                        adjusted = true;
                    }
                }
            }
        }
        (update, adjusted)
    }
}