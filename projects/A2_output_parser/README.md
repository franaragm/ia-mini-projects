# 🧩 Mini Proyecto A2 — Output Parser & Validación

En este mini proyecto aprendemos a **convertir la salida del modelo en datos estructurados y confiables**, usando dos herramientas clave:

- **Pydantic** para validar la estructura y tipos del JSON.
- **Manejo de errores de parseo** para evitar que la API falle cuando el modelo responde mal.

Este paso es fundamental porque a partir de ahora la IA no solo *responde*, sino que *nos dice qué acción tomar* de manera programática.

---

## 🎯 Objetivo

Queremos transformar un mensaje libre del usuario en un **objeto JSON estructurado**, donde la IA identifica:

| Campo | Descripción |
|------|-------------|
| `action` | Qué quiere hacer el usuario (ej. "create_task") |
| `title` | Texto relevante, si aplica |
| `due_date` | Fecha si aplica (YYYY-MM-DD) |

Ejemplo de entrada:

```json
{ "message": "Crea una tarea llamada Preparar informe para mañana" }
