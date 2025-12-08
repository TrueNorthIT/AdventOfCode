using UnityEngine;
using UnityEngine.InputSystem;

public class CameraOrbit : MonoBehaviour
{
    public Vector3 target;
    public float distance = 50f;
    public float sensitivity = 0.000005f;

    private float x = 0f;
    private float y = 0f;

    void Start()
    {
        Vector3 angles = transform.eulerAngles;
        x = angles.y;
        y = angles.x;
    }

    void LateUpdate()
    {
        if (Mouse.current == null) return;

        if (Mouse.current.leftButton.isPressed)
        {
            Vector2 delta = Mouse.current.delta.ReadValue();

            x += delta.x * sensitivity;
            y -= delta.y * sensitivity;
        }

        y = Mathf.Clamp(y, -89f, 89f);

        Quaternion rotation = Quaternion.Euler(y, x, 0);
        Vector3 position = rotation * new Vector3(0.0f, 0.0f, -distance) + target;

        transform.rotation = rotation;
        transform.position = position;
    }
}