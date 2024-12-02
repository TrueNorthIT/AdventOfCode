import fs from "fs";

async function getData(): Promise<{set1: number[], set2: number[]}> {
    const data = await fs.promises.readFile("./2024/day01/day1.txt", "utf-8");
    
    const lines = data.split("\n");

    const sets: {set1: number[], set2: number[]} = {set1: new Array(), set2: new Array()};

    lines.forEach((line) => {
        const nums = line.replace("\r", "").split("   ").map((num) => {
            var n = num.trim();
            return parseInt(n);
        });
        if (!isNaN(nums[0]) && !isNaN(nums[1])) {
            sets.set1.push(nums[0]);
            sets.set2.push(nums[1]);
        }
    });

    return sets;
}

function getDifference(set1: number[], set2: number[]): number {
    const sortedSet1 = set1.sort();
    const sortedSet2 = set2.sort();

    var distance = 0;

    for (let i = 0; i < sortedSet1.length; i++) {
        distance += Math.abs(sortedSet1[i] - sortedSet2[i]);
    }

    return distance;
}

function getSimilarity(set1: number[], set2: number[]): number {
    var similarity = 0;

    for (const num of set1) {
        const timesAppeared = set2.filter((n) => n === num).length;

        similarity += timesAppeared * num;
    }

    return similarity;
}

async function main() {
    const {set1, set2} = await getData();

    console.log(getDifference(set1, set2));
    console.log(getSimilarity(set1, set2))
}

main();

