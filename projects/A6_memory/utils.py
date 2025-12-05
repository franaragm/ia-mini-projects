# ======================================================
# UTILIDADES PARA MANEJO DE ESTADO Y MEMORIA
# ------------------------------------------------------
# Este archivo contiene funciones auxiliares utilizadas
# en varios puntos del módulo A6 Memory:
#
#   1. get_field:
#      Acceso seguro y unificado a atributos tanto en diccionarios
#      como en modelos Pydantic. Facilita trabajar con estados
#      mixtos dentro de LangGraph.
#
#   2. clean_memory_text:
#      Limpieza profunda del texto generado por el LLM para evitar
#      almacenar basura, ruido, vacíos o contenido no útil dentro
#      de ChromaDB.
#
# Ambas funciones son esenciales para la robustez del sistema de
# memoria y garantizan consistencia en los datos procesados.
# ======================================================


# ======================================================
# get_field
# ------------------------------------------------------
# Función auxiliar para acceder de manera segura a un
# atributo de un objeto que puede ser:
#
#   - Un dict normal: {"role": "user", "content": "..."}
#   - Un objeto Pydantic: Message(role="user", content="...")
#
# Esto es necesario porque LangGraph trabaja internamente
# con diccionarios, pero algunas partes del código usan
# modelos Pydantic. Esta función unifica el acceso sin
# necesidad de condicionales repetidos en cada uso.
#
# Parámetros:
#   obj : dict | Pydantic object
#       Objeto que contiene el valor a extraer.
#   key : str
#       Nombre de la clave o atributo a obtener.
#
# Retorna:
#   El valor asociado a `key`.
#   Si el atributo no existe, devuelve None.
#
# Ejemplos:
#   get_field({"role": "user"}, "role")        → "user"
#   get_field(obj=Message(role="x"), "role")   → "x"
#   get_field(obj=Message(...), "missing")     → None
# ------------------------------------------------------
def get_field(obj, key):
    # Si es un diccionario, usar .get() evita excepciones
    if isinstance(obj, dict):
        return obj.get(key)
    
    # Para objetos (como Pydantic), getattr devuelve None si no existe
    return getattr(obj, key, None)


# ======================================================
# clean_memory_text
# ------------------------------------------------------
# Función encargada de filtrar el texto generado por el
# LLM antes de guardarlo en ChromaDB.
#
# ¿Por qué es necesaria?
# - Los modelos suelen devolver:
#     • espacios invisibles
#     • saltos adicionales
#     • respuestas triviales ("ok", "sí", "vale")
#     • cadenas vacías disfrazadas
# - También usamos un guion "-" como indicador explícito
#   de "no guardar memoria".
#
# Esta función garantiza que SOLO se almacene información
# útil, limpia y consistente.
#
# Parámetro:
#   text : str
#       Texto devuelto por el LLM tras aplicar el prompt
#       de preparación de memoria.
#
# Retorna:
#   str → Texto limpio y válido para almacenar.
#   ""  → Si no debe guardarse nada (por regla o limpieza).
#
# Ejemplos:
#   clean_memory_text("9843")                   → "9843"
#   clean_memory_text("-")                      → ""
#   clean_memory_text("   ok   ")               → ""
#   clean_memory_text("Banco: BBVA")            → "Banco: BBVA"
#   clean_memory_text("\u200bcliente 123")      → "cliente 123"
# ------------------------------------------------------
def clean_memory_text(text: str) -> str:
    """
    Limpia texto devuelto por el LLM para evitar almacenar:
    - caracteres invisibles (zero-width, BOM, etc.)
    - cadenas vacías
    - marcador "-" usado para indicar "no guardar"
    - respuestas no informativas (ok, sí, vale…)
    """

    # Si viene None o vacío desde el LLM → no guardar
    if not text:
        return ""

    # ----------------------------------------
    # 1. Eliminar caracteres invisibles
    # ----------------------------------------
    # Algunos modelos incluyen caracteres Unicode que no se ven,
    # pero que podrían contaminar la base de memoria.
    invisible = [
        "\u200b",  # zero-width space
        "\ufeff",  # BOM
        "\u200e",  # LTR mark
        "\u200f",  # RTL mark
    ]
    for ch in invisible:
        text = text.replace(ch, "")

    # Quitar espacios y saltos extra
    text = text.strip()

    # ----------------------------------------
    # 2. Guion medio ("-") → señal explícita de NO guardar
    # ----------------------------------------
    if text == "-":
        return ""

    # ----------------------------------------
    # 3. Si queda vacío después de limpiar → descartar
    # ----------------------------------------
    if not text:
        return ""

    # ----------------------------------------
    # 4. Evitar respuestas triviales no informativas
    # ----------------------------------------
    # Estas respuestas suelen surgir cuando el usuario afirma algo,
    # agradece o hace comentarios no almacenables.
    non_informative = {
        "ok", "vale", "si", "sí", ".", "bien", "correcto",
        "entendido", "perfecto"
    }

    if text.lower() in non_informative:
        return ""

    # Si pasa todos los filtros, el texto es válido
    return text
