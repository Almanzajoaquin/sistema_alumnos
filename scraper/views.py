from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from .scraper import scrape_educativo  # Esta línea está bien
from django.conf import settings

@login_required
def scraper_view(request):
    resultados = []
    palabra_clave = ""
    
    if request.method == 'POST':
        palabra_clave = request.POST.get('palabra_clave', '').strip()
        
        if palabra_clave:
            if len(palabra_clave) < 2:
                messages.warning(request, 'Por favor ingrese una palabra clave más específica (mínimo 2 caracteres).')
            else:
                resultados = scrape_educativo(palabra_clave)
                if not resultados or (len(resultados) == 1 and 'error' in resultados[0].get('titulo', '').lower()):
                    messages.warning(request, 'No se encontraron resultados relevantes para la búsqueda. Intente con otros términos.')
                else:
                    messages.success(request, f'Se encontraron {len(resultados)} resultado(s) para "{palabra_clave}"')
        else:
            messages.error(request, 'Por favor ingrese una palabra clave.')
    
    return render(request, 'scraper/scraper.html', {
        'resultados': resultados,
        'palabra_clave': palabra_clave
    })

@login_required
def enviar_resultados_email(request):
    if request.method == 'POST':
        palabra_clave = request.POST.get('palabra_clave', '')
        resultados = scrape_educativo(palabra_clave)
        
        if resultados:
            try:
                # Crear tabla HTML
                tabla_html = """
                <table border="1" style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                    <thead>
                        <tr style="background-color: #2c3e50; color: white;">
                            <th style="padding: 12px; text-align: left;">Título</th>
                            <th style="padding: 12px; text-align: left;">Contenido</th>
                            <th style="padding: 12px; text-align: left;">Fuente</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for resultado in resultados:
                    tabla_html += f"""
                    <tr>
                        <td style="padding: 10px; border: 1px solid #ddd;">
                            <strong>{resultado['titulo']}</strong>
                        </td>
                        <td style="padding: 10px; border: 1px solid #ddd;">
                            {resultado['contenido']}
                        </td>
                        <td style="padding: 10px; border: 1px solid #ddd;">
                            {resultado['fuente']}
                        </td>
                    </tr>
                    """
                
                tabla_html += "</tbody></table>"
                
                # Enviar email
                email = EmailMessage(
                    f'Resultados de búsqueda: {palabra_clave}',
                    f'',
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                )
                
                email.content_subtype = "html"
                email.body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <div style="max-width: 800px; margin: 0 auto;">
                        <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                            Resultados de Búsqueda Educativa
                        </h2>
                        
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="color: #2c3e50; margin-top: 0;">
                                Término buscado: <span style="color: #e74c3c;">{palabra_clave}</span>
                            </h3>
                            <p>Se encontraron <strong>{len(resultados)} resultado(s)</strong></p>
                        </div>
                        
                        {tabla_html}
                        
                        <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-radius: 5px;">
                            <p style="margin: 0;">
                                <strong>Sugerencia:</strong> Para mejores resultados, usa términos específicos y verifica la ortografía.
                            </p>
                        </div>
                        
                        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                            <p>Saludos cordiales,<br>
                            <strong>Sistema de Scraping Educativo</strong></p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                email.send()
                
                messages.success(request, f'Resultados enviados exitosamente a {request.user.email}')
                
            except Exception as e:
                messages.error(request, f'Error al enviar el email: {str(e)}')
        else:
            messages.warning(request, 'No hay resultados para enviar.')
    
    return redirect('scraper')