import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

# Función para scrapear una página web y devolver su contenido como lista de Document
def scrape_webpage(url: str) -> list[Document]:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    # Parseamos el contenido HTML, soup contiene el árbol DOM completo
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extraemos texto visible, obtenemos los tags no deseados y los eliminamos de soup
    # tag representa cada etiqueta no deseada encontrada y es un apuntador a la misma en el árbol DOM que contiene soup
    # tag no es un objeto independiente, por lo que al eliminarlo de soup, se elimina del árbol DOM original
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose() # Elimina etiquetas no deseadas

    # Obtenemos el texto limpio del árbol DOM modificado
    # retorna texto del dom sin tags HTML y separado por saltos de línea
    text = soup.get_text(separator="\n")
    # retorna una lista de líneas limpias sin espacios en blanco ni líneas vacías
    clean_lines = [line.strip() for line in text.splitlines() if line.strip()]
    # unimos las líneas limpias en un solo string separado por saltos de línea
    clean_text = "\n".join(clean_lines)

    # Retornamos el contenido como una lista con un solo Document
    return [Document(page_content=clean_text, metadata={"source": url})]
