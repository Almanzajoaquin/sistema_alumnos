import requests
from bs4 import BeautifulSoup
import io

def scrape_educativo(palabra_clave):
    """
    Scraper educativo que busca información en sitios educativos
    Versión mejorada con múltiples fuentes y mejor manejo de errores
    """
    resultados = []
    
    # Fuente 1: Wikipedia (principal)
    try:
        url_wikipedia = f"https://es.wikipedia.org/wiki/{palabra_clave.replace(' ', '_')}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url_wikipedia, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer título
            titulo = soup.find('h1')
            titulo_texto = titulo.get_text().strip() if titulo else f"Búsqueda: {palabra_clave}"
            
            # Buscar contenido relevante
            contenido = ""
            
            # Intentar encontrar el primer párrafo significativo
            primeros_parrafos = soup.find_all('p', limit=5)
            for p in primeros_parrafos:
                texto = p.get_text().strip()
                if len(texto) > 50:  # Solo párrafos con contenido sustancial
                    contenido = texto
                    break
            
            # Si no encontramos contenido en párrafos, buscar en otras etiquetas
            if not contenido:
                div_content = soup.find('div', {'id': 'mw-content-text'})
                if div_content:
                    contenido = div_content.get_text()[:300] + '...'
            
            # Limpiar y formatear contenido
            if contenido:
                contenido = contenido.replace('\n', ' ').replace('\t', ' ')
                # Eliminar múltiples espacios
                while '  ' in contenido:
                    contenido = contenido.replace('  ', ' ')
                
                contenido = contenido[:250] + '...' if len(contenido) > 250 else contenido
            else:
                contenido = f"Información sobre '{palabra_clave}' en Wikipedia. Haz clic para ver más detalles."
            
            resultados.append({
                'titulo': titulo_texto,
                'contenido': contenido,
                'fuente': 'Wikipedia',
                'url': url_wikipedia
            })
        else:
            # Si Wikipedia no tiene página, buscar en la página de búsqueda
            resultados.append({
                'titulo': f'Búsqueda: {palabra_clave}',
                'contenido': f'No se encontró una página específica en Wikipedia. Puedes buscar "{palabra_clave}" en la Wikipedia.',
                'fuente': 'Wikipedia',
                'url': f'https://es.wikipedia.org/w/index.php?search={palabra_clave.replace(" ", "+")}'
            })
            
    except requests.exceptions.Timeout:
        resultados.append({
            'titulo': 'Error de tiempo de espera',
            'contenido': 'La búsqueda en Wikipedia tardó demasiado tiempo.',
            'fuente': 'Sistema',
            'url': '#'
        })
    except Exception as e:
        resultados.append({
            'titulo': 'Error en Wikipedia',
            'contenido': f'No se pudo obtener información de Wikipedia: {str(e)}',
            'fuente': 'Sistema',
            'url': '#'
        })
    
    # Fuente 2: Información educativa alternativa
    try:
        # Para búsquedas educativas, podemos agregar información contextual
        if any(palabra in palabra_clave.lower() for palabra in ['matemática', 'matematicas', 'math', 'algebra']):
            resultados.append({
                'titulo': 'Matemáticas Educativas',
                'contenido': 'Las matemáticas son una disciplina fundamental en la educación. Incluyen aritmética, álgebra, geometría y cálculo.',
                'fuente': 'Recurso Educativo',
                'url': 'https://es.khanacademy.org/math'
            })
        elif any(palabra in palabra_clave.lower() for palabra in ['historia', 'history', 'historial']):
            resultados.append({
                'titulo': 'Historia Universal',
                'contenido': 'La historia estudia los eventos del pasado que han dado forma a nuestra sociedad actual.',
                'fuente': 'Recurso Educativo',
                'url': 'https://historia.nationalgeographic.com.es/'
            })
        elif any(palabra in palabra_clave.lower() for palabra in ['ciencia', 'science', 'cientifico']):
            resultados.append({
                'titulo': 'Ciencias Naturales',
                'contenido': 'Las ciencias naturales estudian los fenómenos naturales y el mundo que nos rodea.',
                'fuente': 'Recurso Educativo',
                'url': 'https://www.exploratorium.edu/'
            })
        elif any(palabra in palabra_clave.lower() for palabra in ['programacion', 'programming', 'codigo']):
            resultados.append({
                'titulo': 'Programación',
                'contenido': 'La programación es el proceso de crear instrucciones para que las computadoras ejecuten tareas específicas.',
                'fuente': 'Recurso Educativo',
                'url': 'https://www.freecodecamp.org/'
            })
            
    except Exception as e:
        print(f"Error en fuente alternativa: {e}")
    
    # Si no hay resultados, agregar uno por defecto
    if not resultados:
        resultados.append({
            'titulo': f'Búsqueda: {palabra_clave}',
            'contenido': f'No se encontraron resultados específicos para "{palabra_clave}". Intenta con términos más específicos o verifica la ortografía.',
            'fuente': 'Sistema',
            'url': f'https://www.google.com/search?q={palabra_clave.replace(" ", "+")}+educación'
        })
    
    return resultados