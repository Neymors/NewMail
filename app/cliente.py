# cliente.py (versión corregida)
import feedparser

def leer_feeds(urls):
    fuentes = []
    for url in urls:
        feed = feedparser.parse(url)
        articulos = []
        for entry in feed.entries:
            articulos.append({
                'title': entry.get('title'),
                'link': entry.get('link'),
                'summary': entry.get('summary', ''),
                'published': entry.get('published', '')
            })
        fuentes.append({
            'url': url,           # Agrega la URL de la fuente
            'entries': articulos  # Artículos agrupados
        })
    return fuentes