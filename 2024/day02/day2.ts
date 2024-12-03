import fs from "fs";


async function getRawData(filename: string): Promise<number[][]> {
    const data = await fs.promises.readFile(filename, "utf-8");
    
    const lines = data.split("\n");

    const sets: number[][] = [];

    lines.forEach((line) => {
        const nums = line.replace("\r", "").split(" ").map((num) => {
            var n = num.trim();
            return parseInt(n);
        });
        if (nums.filter((num) => isNaN(num)).length === 0) {
            sets.push(nums);
        } else {
            sets.push([]);
        }
    });

    return sets;
}

function isCorrectData(data: number[]): boolean {
    const isDescending = data[0] > data[1];

    for (var i = 0; i < data.length - 1; i++){
        if (Math.abs(data[i + 1] - data[i]) > 3) { 
            console.log(data)
            return false;
        }

        if (isDescending && data[i] <= data[i + 1]) {
            console.log(data)
            return false;
        } else if (!isDescending && data[i] >= data[i + 1]) {
            console.log(data)
            return false;
        }

    }

    console.log(data, "CORRECT")
    return true;
}

function isCorrectDataWithDamper(data: number[]): boolean {
    const isDescending = data[0] > data[1];

    for (var i = 0; i < data.length - 1; i++){
        if (Math.abs(data[i + 1] - data[i]) > 3) { 
            console.log("----------------------------")
            console.log(data)
            return isCorrectData(data.filter((v, index) => index != i))
                || isCorrectData(data.filter((v, index) => index != i + 1));
        }

        if (isDescending && data[i] <= data[i + 1]) {
            console.log("----------------------------")
            console.log(data)
            return isCorrectData(data.filter((v, index) => index != i))
                || isCorrectData(data.filter((v, index) => index != i + 1));
        } else if (!isDescending && data[i] >= data[i + 1]) {
            console.log("----------------------------")
            console.log(data)
            return isCorrectData(data.filter((v, index) => index != i))
                || isCorrectData(data.filter((v, index) => index != i + 1));
        }

    }

    return true;
}


async function main() {
    const sets = await getRawData("./2024/day02/day2.txt");

    const invalidSets = sets.filter(set => !isCorrectData(set));
    const test = invalidSets.filter(isCorrectDataWithDamper);

    const damperedSets = sets.filter(isCorrectDataWithDamper);

    console.log(sets.length, test.length, damperedSets.length);
}

main();