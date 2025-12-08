using System.Collections.Generic;
using UnityEditor.Experimental.GraphView;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PuzzleManager : MonoBehaviour
{

    public TextAsset demoFile;
    public TextAsset inputFile;
    public bool useDemoFile = true;
    private List<(Vector3 pos, GameObject box)> junctionBoxes = new();
    private List<(Vector3 boxA, Vector3 boxB, float distance)> distances = new();

    void Start()
    {
        Debug.Log("SceneManager started.");
        LoadBoxes();
        SetupScene();
        CalculateDistances();
        
        distances.Sort((a, b) => a.distance.CompareTo(b.distance));

        for (int i = 0; i < (useDemoFile ? 10 : 1000); i++)
        {
            var (boxAPos, boxBPos, distance) = distances[i];
            var boxA = junctionBoxes.Find(jb => jb.pos == boxAPos).box;
            var boxB = junctionBoxes.Find(jb => jb.pos == boxBPos).box;
            GroupBox(boxA, boxB);
            DrawLine(boxA, boxB);

        }
        
        GetLargestGroups();
    }

    void Update()
    {

    }
    
    void LoadBoxes()
    {
        string[] lines = (useDemoFile ? demoFile : inputFile).text.Split('\n');
        foreach (string line in lines)
        {
            string[] parts = line.Split(',');
            int x = int.Parse(parts[0]);
            int y = int.Parse(parts[1]);
            int z = int.Parse(parts[2]);
            junctionBoxes.Add((new Vector3(x, y, z), GameObject.CreatePrimitive(PrimitiveType.Cube)));
        }

        Debug.Log($"Loaded {junctionBoxes.Count} junction boxes.");
    }
    
    void SetupScene()
    {
        Debug.Log("Setting up scene...");
        var firstPos = junctionBoxes.GetEnumerator();
        firstPos.MoveNext();
        Bounds bounds = new Bounds(firstPos.Current.Item1, Vector3.zero);

        foreach (var junctionBox in junctionBoxes) bounds.Encapsulate(junctionBox.pos);

        float maxDimension = Mathf.Max(bounds.size.x, bounds.size.y, bounds.size.z);
        float visibleScale = Mathf.Max(maxDimension / 200f, 5f);

        foreach (var junctionBox in junctionBoxes)
        {
            junctionBox.box.transform.position = junctionBox.pos;
            junctionBox.box.transform.localScale = Vector3.one * visibleScale;
            
            var boxRenderer = junctionBox.box.GetComponent<Renderer>();
            boxRenderer.material = new Material(Shader.Find("Sprites/Default"));
            boxRenderer.material.color = Random.ColorHSV(0f, 1f, 0.8f, 1f, 0.8f, 1f);;
        }

        float maxDim = Mathf.Max(bounds.size.x, bounds.size.y, bounds.size.z);

        CameraOrbit orbit = Camera.main.gameObject.AddComponent<CameraOrbit>();

        orbit.target = bounds.center;
        orbit.distance = maxDim * 2.0f; 
        orbit.sensitivity = .05f;

        Camera.main.farClipPlane = maxDim * 10f;

        if (Camera.main.orthographic)
        {
            Camera.main.orthographicSize = maxDim * 0.6f;
        }
    }

    void CalculateDistances()
    {
        for (int i = 0; i < junctionBoxes.Count; i++)
        {
            for (int j = i + 1; j < junctionBoxes.Count; j++)
            {
                if (junctionBoxes[j].box.transform.position == junctionBoxes[i].box.transform.position) continue;
                float distance = Vector3.Distance(junctionBoxes[i].pos, junctionBoxes[j].pos);
                distances.Add((junctionBoxes[i].pos, junctionBoxes[j].pos, distance));
            }
        }
        
        Debug.Log($"Calculated distances between {junctionBoxes.Count} junction boxes.");
    }

    void GroupBox(GameObject cubeA, GameObject cubeB)
    {
        Transform parentA = cubeA.transform.parent;
        Transform parentB = cubeB.transform.parent;
        
        if (parentA == null && parentB == null)
        {
            GameObject newGroup = new GameObject("Circuit Group");
            
            cubeA.transform.SetParent(newGroup.transform);
            cubeB.transform.SetParent(newGroup.transform);
            UnifyGroupColor(newGroup.transform);
        }
        else if (parentA != null && parentB == null)
        {
            cubeB.transform.SetParent(parentA);
            UnifyGroupColor(parentA);
        }
        else if (parentA == null && parentB != null)
        {
            cubeA.transform.SetParent(parentB);
            UnifyGroupColor(parentB);
        }
        else if (parentA != parentB)
        {
            int countA = parentA.childCount;
            int countB = parentB.childCount;

            if (countA >= countB)
            {
                MergeGroups(mainGroup: parentA, groupToAbsorb: parentB);
            }
            else
            {
                MergeGroups(mainGroup: parentB, groupToAbsorb: parentA);
            }
        }
    }
    
    void MergeGroups(Transform mainGroup, Transform groupToAbsorb)
    {
        while (groupToAbsorb.childCount > 0)
        {
            Transform child = groupToAbsorb.GetChild(0);
            child.SetParent(mainGroup);
        }
        
        mainGroup.name = $"Circuit Group ({mainGroup.childCount} nodes)";
        
        DestroyImmediate(groupToAbsorb.gameObject);
        UnifyGroupColor(mainGroup);
    }

    void DrawLine(GameObject boxA, GameObject boxB)
    {
        GameObject wireObj = new GameObject("Wire");
        wireObj.transform.SetParent(boxA.transform.parent); 
        
        LineRenderer lr = wireObj.AddComponent<LineRenderer>();
    
        lr.positionCount = 2;
        lr.SetPosition(0, boxA.transform.position);
        lr.SetPosition(1, boxB.transform.position);
        
        float lineWidth = boxA.transform.localScale.x * 0.2f;
        
        lr.startWidth = lineWidth; 
        lr.endWidth = lineWidth;
        
        lr.material = boxA.GetComponent<Renderer>().material;
    }
    
    void GetLargestGroups()
    {
        GameObject[] allObjects = SceneManager.GetActiveScene().GetRootGameObjects();
        
        List<Transform> circuitGroups = new List<Transform>();
        
        foreach (var obj in allObjects)
        {
            if (obj.name.StartsWith("Circuit Group"))
            {
                circuitGroups.Add(obj.transform);
            }
        }
        
        circuitGroups.Sort((a, b) => GetBoxCount(b).CompareTo(GetBoxCount(a)));
        
        long multiplicationResult = 1; 
        
        for (int i = 0; i < 3; i++)
        {
            int count = GetBoxCount(circuitGroups[i]);
            Debug.Log($"Rank {i + 1}: '{circuitGroups[i].name}' with {count} boxes");
            
            multiplicationResult *= count;
        }
        
        Debug.Log($"Product of Top 3 sizes: {multiplicationResult}");
    }
    
    int GetBoxCount(Transform group)
    {
        int count = 0;
        foreach (Transform child in group)
        {
            if (child.name != "Wire") 
            {
                count++;
            }
        }
        return count;
    }
    
    void UnifyGroupColor(Transform group)
    {
        if (group.childCount == 0) return;
        
        Color masterColor = Color.white;
        foreach(Transform child in group) 
        {
            if (child.name != "Wire") 
            {
                masterColor = child.GetComponent<Renderer>().material.color;
                break;
            }
        }
        
        foreach (Transform child in group)
        {
            if (child.name != "Wire")
            {
                child.GetComponent<Renderer>().material.color = masterColor;
            }
            else 
            {
                LineRenderer lr = child.GetComponent<LineRenderer>();
                if (lr != null)
                {
                    lr.startColor = masterColor;
                    lr.endColor = masterColor;
                    lr.material.color = masterColor; 
                }
            }
        }
    }

}
