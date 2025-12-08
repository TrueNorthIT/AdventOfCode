using System.Collections.Generic;
using UnityEngine;
using static UnityEditor.MaterialProperty;

public class JunctionBox
{
    public int groupId;
    public GameObject cube;
    public JunctionBox(int id, GameObject _cube)
    {
        groupId = id;
        cube = _cube;
    }
}

public class PuzzleManager : MonoBehaviour
{

    public TextAsset demoFile;
    public TextAsset inputFile;
    public bool useDemoFile = true;
    public List<(Vector3, JunctionBox)> junctionBoxes = new List<(Vector3, JunctionBox)>();

    void Start()
    {
        Debug.Log("SceneManager started.");
        string[] lines = (useDemoFile ? demoFile : inputFile).text.Split('\n');
        foreach (string line in lines)
        {
            string[] parts = line.Split(',');
            junctionBoxes.Add((new Vector3(int.Parse(parts[0]), int.Parse(parts[1]), int.Parse(parts[2])), new JunctionBox(0, null)));
        }

        Debug.Log($"Loaded {junctionBoxes.Count} junction boxes.");

        var firstPos = junctionBoxes.GetEnumerator();
        firstPos.MoveNext();
        Bounds bounds = new Bounds(firstPos.Current, Vector3.zero);

        foreach (var box in junctionBoxes) bounds.Encapsulate(pos);

        float maxDimension = Mathf.Max(bounds.size.x, bounds.size.y, bounds.size.z);
        float visibleScale = Mathf.Max(maxDimension / 200f, 5f);

        foreach (var box in junctionBoxes)
        {
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.transform.position = box.Key;
            cube.transform.localScale = Vector3.one * visibleScale;

            // Make them bright pink so you can't miss them
            var renderer = cube.GetComponent<Renderer>();
            renderer.material = new Material(Shader.Find("Sprites/Default"));
            renderer.material.color = Color.magenta;

            box.Value.cube = cube;
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

        List<(Vector3, Vector3, int)> distances = new List<(Vector3, Vector3, int)>();

        for (int i = 0; i < junctionBoxes.Count; i++)
        {
           for (int j = 0; j < junctionBoxes.Count; j++)
            {
                if (i == j) continue;
            }
        }
    }

    void Update()
    {

    }

}
