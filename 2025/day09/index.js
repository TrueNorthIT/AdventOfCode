import * as fs from 'fs';

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

const points = fs.readFileSync('input.txt','utf8').split('\r\n').map(line => {const parts =line.split(','); return new Point(parseInt(parts[0]), parseInt(parts[1]));});
let maxArea = 0;
for (let index = 0; index < points.length; index++) {
    const point1 = points[index];
    for (let index2 = index + 1; index2 < points.length; index2++) {
        const point2 = points[index2];
        const area = (Math.abs(point1.x - point2.x) + 1) * (Math.abs(point1.y - point2.y) + 1);
        if (area > maxArea) {
            maxArea = area;
        }
    }
}
console.log(maxArea);