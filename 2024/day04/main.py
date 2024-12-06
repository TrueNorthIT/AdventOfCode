from math import pi, sqrt, atan, cos, sin

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

class PotentialMatch:
    def __init__(self, x_point: Point, m_point, x_max: int, y_max: int):
        self.x_point = x_point
        self.m_point = m_point
        self.x_max = x_max
        self.y_max = y_max
        a_point = Point(self.m_point.x + self.m_point.x - self.x_point.x, self.m_point.y + self.m_point.y - self.x_point.y)
        if a_point.x > self.x_max or a_point.x < 0 or a_point.y > self.y_max or a_point.y < 0:
            self.a_point = None
        else:
            self.a_point = a_point
        s_point = Point(self.m_point.x + 2*(self.m_point.x - self.x_point.x), self.m_point.y + 2* (self.m_point.y - self.x_point.y))
        if s_point.x > self.x_max or s_point.x < 0 or s_point.y > self.y_max or s_point.y < 0:
            self.s_point = None
        else:
            self.s_point = s_point
    
    def __str__(self):
        return "X:{0}  M:{1}  A:{2}  S{3}".format(self.x_point, self.m_point, self.a_point, self.s_point)


class Part2PotentialMatch:
    def __init__(self, m1_point, a_point: Point, x_max: int, y_max: int):
        self.m1_point = m1_point
        self.a_point = a_point
        self.x_max = x_max
        self.y_max = y_max
        x_delta = self.a_point.x - self.m1_point.x
        y_delta = self.a_point.y - self.m1_point.y
        s1_point = Point(self.a_point.x + x_delta, self.a_point.y + y_delta)
        if s1_point.x > self.x_max or s1_point.x < 0 or s1_point.y > self.y_max or s1_point.y < 0:
            self.s1_point = None
        else:
            self.s1_point = s1_point
        tan_delta = y_delta / x_delta
        xors1_point = Point(self.a_point.x + (cos(atan(tan_delta)+(pi/2)) * sqrt(2)), self.a_point.y + (sin(atan(tan_delta)+(pi/2)) * sqrt(2)))
        if xors1_point.x > self.x_max or xors1_point.x < 0 or xors1_point.y > self.y_max or xors1_point.y < 0:
            self.xors1_point = None
        else:
            self.xors1_point = xors1_point
        xors2_point = Point(self.a_point.x + (cos(atan(tan_delta)+(3*pi/2)) * sqrt(2)), self.a_point.y + (sin(atan(tan_delta)+(3*pi/2)) * sqrt(2)))
        if xors2_point.x > self.x_max or xors2_point.x < 0 or xors2_point.y > self.y_max or xors2_point.y < 0:
            self.xors2_point = None
        else:
            self.xors2_point = xors2_point
    
class Checker:
    def __init__(self, filename: str):
        self.lines = [line.strip() for line in open(filename, 'r')]
        self.x_max = len(self.lines[0])-1
        self.y_max = len(self.lines)-1

    def part1(self) -> int:
        count = 0
        for line_index,line in enumerate(self.lines):
            for x_point in (Point(x_x_index, line_index) for x_x_index,char in enumerate(line) if char == 'X'):
                possible_matches = [PotentialMatch(x_point, m_point, self.x_max, self.y_max) for m_point in self.adjacent_points(x_point) if self.is_legal(m_point) and self.lines[m_point.y][m_point.x] == "M"]
                count += len([True for potential_match in possible_matches if 
                              potential_match.a_point is not None and self.lines[potential_match.a_point.y][potential_match.a_point.x] == "A"
                              and potential_match.s_point is not None and self.lines[potential_match.s_point.y][potential_match.s_point.x] == "S"
                              ])
        return count
            

    def adjacent_points(self, start: Point) -> list[Point]:
        return [point for point in [
            Point(start.x-1, start.y-1), 
            Point(start.x, start.y-1),
            Point(start.x+1, start.y-1),
            Point(start.x-1, start.y), 
            Point(start.x+1, start.y),
            Point(start.x-1, start.y+1), 
            Point(start.x, start.y+1),
            Point(start.x+1, start.y+1)
        ] if self.is_legal(point)]

    def is_legal(self, point: Point) -> bool:
        return point.x >= 0 and point.x <= self.x_max and point.y >= 0 and point.y <= self.y_max

    def part2(self) -> int:
        count = 0
        for line_index,line in enumerate(self.lines[1:-1], 1):
            for a_point in (Point(m_a_index, line_index) for m_a_index,char in enumerate(line[1:-1], 1) if char == 'A'):
                up_left = self.lines[a_point.y-1][a_point.x-1]
                up_right = self.lines[a_point.y-1][a_point.x+1]
                down_left = self.lines[a_point.y+1][a_point.x-1]
                down_right = self.lines[a_point.y+1][a_point.x+1]

                if ((up_left == "M" and down_right == "S") or (up_left == "S" and down_right == "M") \
                    and \
                    (up_right == "M" and down_left == "S") or (up_right == "S" and down_left == "M")):
                    count+=1

        return count



print(Checker('inputtest.txt').part2())
