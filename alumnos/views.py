from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from .models import Alumno
from .forms import AlumnoForm
from django.conf import settings
from django.http import HttpResponse

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, 'Alumno creado exitosamente.')
            return redirect('dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/alumno_form.html', {'form': form})

def generar_pdf_alumno(alumno):
    """Genera un PDF profesional con los datos del alumno"""
    buffer = io.BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch)
    styles = getSampleStyleSheet()
    
    # Crear estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Centrado
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    normal_style = styles['Normal']
    
    # Contenido del PDF
    content = []
    
    # Título
    content.append(Paragraph("SISTEMA DE GESTIÓN DE ALUMNOS", title_style))
    content.append(Spacer(1, 0.2*inch))
    
    # Información del alumno
    content.append(Paragraph("INFORMACIÓN DEL ALUMNO", heading_style))
    
    # Datos en formato tabla
    datos = [
        ["<b>Nombre:</b>", f"{alumno.nombre} {alumno.apellido}"],
        ["<b>Email:</b>", alumno.email],
        ["<b>Edad:</b>", f"{alumno.edad} años"],
        ["<b>Carrera:</b>", alumno.carrera],
        ["<b>Estado:</b>", alumno.get_estado_display()],
        ["<b>Fecha de Registro:</b>", alumno.fecha_creacion.strftime("%d/%m/%Y %H:%M")],
        ["<b>Registrado por:</b>", alumno.usuario.username],
    ]
    
    # Crear tabla
    table_data = []
    for label, value in datos:
        table_data.append([
            Paragraph(label, normal_style),
            Paragraph(value, normal_style)
        ])
    
    table = Table(table_data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('BACKGROUND', (1, 0), (1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    content.append(Paragraph(f"<i>Generado automáticamente el {alumno.fecha_creacion.strftime('%d/%m/%Y')}</i>", 
                        ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.gray)))
    
    # Construir PDF
    doc.build(content)
    buffer.seek(0)
    return buffer

@login_required
def enviar_pdf_email(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    
    try:
        # Generar PDF
        pdf_buffer = generar_pdf_alumno(alumno)
        
        # Crear email con HTML más profesional
        email_subject = f'Reporte de Alumno - {alumno.nombre} {alumno.apellido}'
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #2c3e50;">Reporte de Alumno Generado</h2>
            <p>Hola <strong>{request.user.username}</strong>,</p>
            <p>Se ha generado el reporte PDF del alumno <strong>{alumno.nombre} {alumno.apellido}</strong>.</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
                <h3 style="color: #2c3e50; margin-top: 0;">Resumen del Alumno:</h3>
                <ul>
                    <li><strong>Nombre:</strong> {alumno.nombre} {alumno.apellido}</li>
                    <li><strong>Email:</strong> {alumno.email}</li>
                    <li><strong>Edad:</strong> {alumno.edad} años</li>
                    <li><strong>Carrera:</strong> {alumno.carrera}</li>
                    <li><strong>Estado:</strong> {alumno.get_estado_display()}</li>
                </ul>
            </div>
            
            <p>El archivo PDF adjunto contiene toda la información detallada.</p>
            <p>Saludos cordiales,<br>
            <strong>Sistema de Gestión de Alumnos</strong></p>
            
            <hr style="border: none; border-top: 1px solid #eee;">
            <p style="color: #7f8c8d; font-size: 12px;">
                Este email fue generado automáticamente. Por favor no responder.
            </p>
        </body>
        </html>
        """
        
        # Crear y enviar email
        email = EmailMessage(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],  # Enviar al usuario logueado
            # ['docente@gmail.com'],  # Puedes agregar el email del docente aquí
        )
        
        email.content_subtype = "html"
        
        # Adjuntar PDF
        email.attach(
            f'reporte_alumno_{alumno.nombre}_{alumno.apellido}.pdf',
            pdf_buffer.getvalue(),
            'application/pdf'
        )
        
        # Enviar email
        email.send()
        
        messages.success(request, f'✅ PDF enviado exitosamente a {request.user.email}')
    
    except Exception as e:
        messages.error(request, f'❌ Error al enviar el PDF: {str(e)}')
        # Para debugging, puedes imprimir el error
        print(f"Error enviando email: {str(e)}")
    
    return redirect('dashboard')