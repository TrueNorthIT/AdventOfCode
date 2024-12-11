namespace day11
{
    internal class Program
    {
        static IDictionary<string, Stone[]> stringAnswers = new Dictionary<string, Stone[]>();
        static IDictionary<long, Stone> longAnswers = new Dictionary<long, Stone>();

        static void Main()
        {
            var stones = File.ReadAllLines("inputtest.txt").First().Split(' ').Select(s => new Stone(s)).ToArray();
            for (int i = 0; i < 75; i++)
            {
                stones = Blink(stones).ToArray();
                Console.WriteLine("{1:HH:mm:ss} Blinked {0:00} times", i, DateTime.Now);
            }
            Console.WriteLine(stones.Count());
        }

        static IEnumerable<Stone> Blink(IEnumerable<Stone> stones)
        {
            return stones.SelectMany(s =>
            {
                if (s.IsZero) return [new Stone(1L, "1", false) ];
                else if ((s.AsString.Length & 1) == 0)
                {
                    if (stringAnswers.TryGetValue(s.AsString, out var answer))
                    {
                        return answer.Select(a => a.Clone());
                    }
                    else
                    {
                        answer = [
                            new Stone(s.AsString.Substring(0, s.AsString.Length / 2), false),
                        new Stone(s.AsString.Substring(s.AsString.Length / 2))
                        ];
                        stringAnswers[s.AsString] = answer;
                        return answer;
                    }
                }
                else if (longAnswers.TryGetValue(s.AsLong, out var longAnswer)) return [longAnswer.Clone()];
                
                var newLongAnswer = new Stone((s.AsLong << 11) - (s.AsLong << 5 ) + (s.AsLong << 3 ));
                longAnswers[s.AsLong] = newLongAnswer;
                return [newLongAnswer];
            });
        }

        private class Stone
        {
            private long? asLong;
            private string asString;
            private bool? isZero;

            public Stone(long asLong)
            {
                this.asLong = asLong;
            }

            public Stone(string asString)
            {
                var firstNonZeroDigit = findFirstNonZeroDigit(asString);
                if (firstNonZeroDigit >= 0)
                {
                    this.asString = asString.Substring(firstNonZeroDigit);
                    this.isZero = false;
                }
                else
                {
                    this.asString = "0";
                    this.asLong = 0;
                    this.isZero = true;
                }
            }

            public Stone(string asString, bool isZero)
            {
                this.isZero = isZero;
                if (isZero)
                {
                    this.asString = "0";
                    this.asLong = 0L;
                }
                else
                {
                    this.asString = asString.Substring(findFirstNonZeroDigit(asString));
                }
            }

            public Stone(long asLong, string asString, bool isZero)
            {
                this.asLong = asLong;
                this.asString = asString;
                this.isZero = isZero;
            }

            private Stone(long? asLong, string asString, bool? isZero)
            {
                this.asLong = asLong;
                this.asString = asString;
                this.isZero = isZero;
            }

            static int findFirstNonZeroDigit(string numAsString)
            {
                for (int i = 0; i < numAsString.Length; i++)
                {
                    if (numAsString[i] != '0') return i;
                }
                return -1;
            }

            public long AsLong
            {
                get
                {
                    if (!asLong.HasValue) asLong = long.Parse(asString);
                    return asLong.Value;
                }
            }

            public string AsString
            {
                get
                {
                    if (asString == null) asString = asLong.ToString();
                    return asString;
                }
            }

            public bool IsZero
            {
                get
                {
                    if (!isZero.HasValue) isZero = AsLong == 0;
                    return isZero.Value;
                }
            }

            public Stone Clone()
            {
                return new Stone(this.asLong, this.asString, this.isZero);
            }
        }
    }
}
