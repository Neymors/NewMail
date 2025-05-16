import requests
import json

API_KEY = "AIzaSyB8Dp1tP5jScVPGBxR4kfzt80814rRb1kM"
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def resumir_noticias(noticias_api):
    """
    Resume las noticias agrupadas por fuente.
    Devuelve una lista de diccionarios con 'url' y 'resumen'.
    """
    resultados = []

    for fuente in noticias_api:
        url_fuente = fuente.get("url", "Desconocido")
        entradas = fuente.get("entries", [])
        if not entradas:
            continue

        textos = []
        for entrada in entradas:
            titulo = entrada.get('title', 'Sin título')
            descripcion = entrada.get('description', 'Sin descripción')
            textos.append(f"Título: {titulo}\nResumen: {descripcion}")

        texto_completo = "\n\n".join(textos)
        payload = _crear_payload(texto_completo)
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        resumen_texto = _procesar_respuesta(response)

        resultados.append({
            "url": url_fuente,
            "resumen": resumen_texto
        })

    return resultados

def _crear_payload(texto_completo):
    """
    Crea el payload para la solicitud POST a la API.
    """
    return {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Resumí claramente estas noticias:\n\n{texto_completo}"
                    }
                ]
            }
        ]
    }

def _procesar_respuesta(response):
    """
    Procesa la respuesta de la API y devuelve el texto del resumen o un mensaje de error.
    """
    if response.status_code == 200:
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error al generar resumen: {response.status_code} - {response.text}"
