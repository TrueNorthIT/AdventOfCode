var initialSecretNumbers = File.ReadAllLines("input.txt").Select(long.Parse).ToArray();

const int L = 2000;
long p1Ans = 0;
List<List<long>> prices = new List<List<long>>();
foreach (var num in initialSecretNumbers)
{
    long curr = num;
    var currentPrices = new List<long>();
    for (int i = 0; i < L; i++)
    {
        currentPrices.Add(curr % 10);
        curr = (curr ^ (curr * 64)) % 16777216;
        curr = (curr ^ (curr / 32)) % 16777216;
        curr = (curr ^ (curr * 2048)) % 16777216;
    }
    prices.Add(currentPrices);
    p1Ans += curr;
}

Console.WriteLine($"Part 1: {p1Ans}");

//we compute the best for all the possible keys for all the sequences
var allSequences = prices.Select(sequences).ToList();
Console.WriteLine($"Generated: {allSequences.Count} sequences");

//flatten this to get all possible keys that match anything
var allCandidates = allSequences.SelectMany(kvp => kvp.Keys).Distinct().ToList();
Console.WriteLine($"Generated: {allCandidates.Count} candidates");

//and now loop through and get the best for each monkey for these
long max = int.MinValue;
foreach ((long p0, long p1, long p2, long p3) candidate in allCandidates)
{
    var bananas = allSequences.Select(dict => dict.ContainsKey(candidate) ? dict[candidate] : 0).Sum();
    max = Math.Max(max, bananas);
}
Console.WriteLine($"Part 2: {max}");

Dictionary<(long p0, long p1, long p2, long p3), long> sequences(List<long> prices)
{
    var results = new Dictionary<(long p0, long p1, long p2, long p3), long>();
    for (int i = 4; i < 2000; i++)
    {
        var key = (prices[i - 3] - prices[i - 4],
                        prices[i - 2] - prices[i - 3],
                        prices[i - 1] - prices[i - 2],
                        prices[i] - prices[i - 1]);

        if (!results.ContainsKey(key))
            results.Add(key, prices[i]);
    }
    return results;
}
