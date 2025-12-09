using NUnit.Framework;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Tilemaps;

public class PuzzleManager : MonoBehaviour
{

    public TextAsset inputFile;
    public TextAsset demoFile;
    public bool useDemoFile = true;
    public List<(int, int)> redTileLocs = new ();
    public RectInt bestRect;


    void Start()
    {
        Debug.Log("Puzzle Manager started.");
        string[] lines = (useDemoFile ? demoFile : inputFile).text.Split('\n');
        foreach (string line in lines)
        {
            Debug.Log(line);
            string[] parts = line.Split(',');
            int x = int.Parse(parts[0]);
            int y = int.Parse(parts[1]);
            redTileLocs.Add((x, y));
        }
        Debug.Log($"Loaded {redTileLocs.Count} red tile locations.");


        long biggestArea = 0;
        Vector2Int bestCorner1 = Vector2Int.zero;
        Vector2Int bestCorner2 = Vector2Int.zero;

        for (int i = 0; i < redTileLocs.Count; i++)
        {
            for (int j = i + 1; j < redTileLocs.Count; j++)
            {
                var (x1, y1) = redTileLocs[i];
                var (x2, y2) = redTileLocs[j];

                long width = Mathf.Abs(x2 - x1) + 1;
                long height = Mathf.Abs(y2 - y1) + 1;
                long area = width * height;

                if (area > biggestArea)
                {
                    biggestArea = area;
                    bestCorner1 = new Vector2Int(x1, y1);
                    bestCorner2 = new Vector2Int(x2, y2);
                }
            }
        }

        Debug.Log($"Biggest area: {biggestArea} between {bestCorner1} and {bestCorner2}");

        bestRect = new RectInt
        (
            Mathf.Min(bestCorner1.x, bestCorner2.x),
            Mathf.Min(bestCorner1.y, bestCorner2.y),
            Mathf.Abs(bestCorner2.x - bestCorner1.x) + 1,
            Mathf.Abs(bestCorner2.y - bestCorner1.y) + 1
        );

    }


    void Update()
    {
        
    }

    private void OnDrawGizmos()
    {
        Gizmos.color = new Color(0, 1, 0, 0.3f);
        Gizmos.DrawCube(new Vector3(bestRect.center.x, bestRect.center.y, 0), new Vector3(bestRect.width, bestRect.height, 1));

        Gizmos.color = Color.green;
        Gizmos.DrawWireCube(new Vector3(bestRect.center.x, bestRect.center.y, 0), new Vector3(bestRect.width, bestRect.height, 1));



        Gizmos.color = Color.red;
        Debug.Log($"Drawing {redTileLocs.Count} red tile locations.");
        foreach (var (x, y) in redTileLocs)
        {
            Gizmos.DrawCube(new Vector3(x, y, 0), Vector3.one * 100);
        }
    }
}
