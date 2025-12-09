import * as fs from 'fs';
import memoize from 'memoize';

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    toCacheKey() {
        return `${this.x},${this.y}`;
    }
}

class Range {
    constructor(min, max, other) {
        this.min = min;
        this.max = max;
        this.other = other;
    }
    isIn(value, other) {
        return value >= this.min && value <= this.max && this.other === other;
    }
}

const points = fs.readFileSync('input.txt','utf8').split('\r\n').map(line => {const parts =line.split(','); return new Point(parseInt(parts[0]), parseInt(parts[1]));});
console.log(part2());

function part2() {
    const maxX = Math.max(...points.map(p => p.x));
    const maxY = Math.max(...points.map(p => p.y));
    console.log(`Max X: ${maxX}, Max Y: ${maxY}`);
    let horizontalLinesBuilder = [];
    let verticalLinesBuilder = [];
    for (let index = 1; index < points.length; index++) {
        const lastPoint = points[index - 1];
        const point = points[index];
        joinPoints(lastPoint, point);
    }
    joinPoints(points[points.length - 1], points[0]);
    const horizontalLines = {};
    const verticalLines = {};
    for (let hLineIndex = 0; hLineIndex < horizontalLinesBuilder.length; hLineIndex++) {
        if (Object.hasOwnProperty(horizontalLines, horizontalLinesBuilder[hLineIndex].other)) {
            horizontalLines[horizontalLinesBuilder[hLineIndex].other].push(horizontalLinesBuilder[hLineIndex]);
        } else {
            horizontalLines[horizontalLinesBuilder[hLineIndex].other] = [horizontalLinesBuilder[hLineIndex]];
        }
    }
    for (let vLineIndex = 0; vLineIndex < verticalLinesBuilder.length; vLineIndex++) {
        if (Object.hasOwnProperty(verticalLines, verticalLinesBuilder[vLineIndex].other)) {
            verticalLines[verticalLinesBuilder[vLineIndex].other].push(verticalLinesBuilder[vLineIndex]);
        } else {
            verticalLines[verticalLinesBuilder[vLineIndex].other] = [verticalLinesBuilder[vLineIndex]];
        }
    }
    console.log('Finished drawing red/green lines');
    let memoizedIsPointBoundedAbove = memoize(isPointBoundedAbove, {cacheKey: (args) => args[0].toCacheKey()});
    let memoizedIsPointBoundedBelow = memoize(isPointBoundedBelow, {cacheKey: (args) => args[0].toCacheKey()});
    let memoizedIsPointBoundedLeft = memoize(isPointBoundedLeft, {cacheKey: (args) => args[0].toCacheKey()});
    let memoizedIsPointBoundedRight = memoize(isPointBoundedRight, {cacheKey: (args) => args[0].toCacheKey()});

    let isAreaBounded = (point1, point2) => {
        const bottomEdge = Math.min(point1.y, point2.y);
        const topEdge = Math.max(point1.y, point2.y);
        const leftEdge = Math.min(point1.x, point2.x);
        const rightEdge = Math.max(point1.x, point2.x);
        for (let y = bottomEdge; y <= topEdge; y++) {
            if (!memoizedIsPointBoundedLeft(new Point(leftEdge, y))) return false;
            if (!memoizedIsPointBoundedRight(new Point(rightEdge, y))) return false;
        }
        for (let x = leftEdge; x <= rightEdge; x++) {
            if (!memoizedIsPointBoundedAbove(new Point(x, topEdge))) return false;
            if (!memoizedIsPointBoundedBelow(new Point(x, bottomEdge))) return false;
        }
        return true;
    }

    let maxArea = 0;
    let possibleAreas = points.length * (points.length - 1) / 2;
    let done = 0;
    for (let index = 0; index < points.length; index++) {
        const point1 = points[index];
        for (let index2 = index + 1; index2 < points.length; index2++) {
            done++;
            const point2 = points[index2];
            const area = (Math.abs(point1.x - point2.x) + 1) * (Math.abs(point1.y - point2.y) + 1);
            if (area > maxArea && isAreaBounded(point1, point2)) {
                maxArea = area;
            }
            console.log(`Done ${done}/${possibleAreas}. Max Area so far: ${maxArea}`);
        }
    }
    return maxArea;

    function isPointBoundedAbove(point) {
        let found = false;
        for (let y=point.y; y<=maxY; y++) {
            if (horizontalLines[y]?.some(range => range.isIn(point.x, y))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        return true;
    }

    function isPointBoundedBelow(point) {
        let found = false;
        for (let y=point.y; y>=0; y--) {
            if (horizontalLines[y]?.some(range => range.isIn(point.x, y))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        return true;
    }

    function isPointBoundedRight(point) {
        let found = false;
        for (let x=point.x; x<=maxX; x++) {
            if (verticalLines[x]?.some(range => range.isIn(point.y, x))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        return true;
    }

    function isPointBoundedLeft(point) {
        let found = false;
        for (let x=point.x; x>=0; x--) {
            if (verticalLines[x]?.some(range => range.isIn(point.y, x))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        return true;
    }

    function isPointInside(point) {
        let found = false;
        for (let x=point.x; x>=0; x--) {
            if (verticalLines.some(range => range.isIn(point.y, x))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        for (let x=point.x; x<=maxX; x++) {
            if (verticalLines.some(range => range.isIn(point.y, x))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        for (let y=point.y; y>=0; y--) {
            if (horizontalLines.some(range => range.isIn(point.x, y))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        for (let y=point.y; y<=maxY; y++) {
            if (horizontalLines.some(range => range.isIn(point.x, y))) {
                found = true;
                break;
            }
        }
        if (!found) return false;
        return true;
    }

    function joinPoints(lastPoint, point) {
        if (lastPoint.x === point.x) {
            verticalLinesBuilder.push(new Range(Math.min(lastPoint.y, point.y, lastPoint.x), Math.max(lastPoint.y, point.y), lastPoint.x));
        } else {
            horizontalLinesBuilder.push(new Range(Math.min(lastPoint.x, point.x, lastPoint.y), Math.max(lastPoint.x, point.x), lastPoint.y));
        }
    }
}

function part1() {
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
    return maxArea;
}
