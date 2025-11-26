from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Enviar correo de bienvenida mejorado
            try:
                email_subject = 'Bienvenido al Sistema de Gestión de Alumnos'
                email_body = f"""
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #2c3e50;">¡Bienvenido {user.username}!</h2>
                    <p>Nos alegra darte la bienvenida al <strong>Sistema de Gestión de Alumnos</strong>.</p>
                    
                    <div style="background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #27ae60; margin-top: 0;">Tu cuenta ha sido creada exitosamente</h3>
                        <p><strong>Usuario:</strong> {user.username}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                    </div>
                    
                    <p>Ahora puedes:</p>
                    <ul>
                        <li>Gestionar alumnos en tu dashboard</li>
                        <li>Generar reportes en PDF</li>
                        <li>Enviar información por correo</li>
                        <li>Usar nuestro scraper educativo</li>
                    </ul>
                    
                    <p>¡Comienza explorando todas las funcionalidades!</p>
                    
                    <p>Saludos cordiales,<br>
                    <strong>Equipo del Sistema de Gestión de Alumnos</strong></p>
                    
                    <hr style="border: none; border-top: 1px solid #eee;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        Este es un email automático, por favor no responder.
                    </p>
                </body>
                </html>
                """
                
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
                email.content_subtype = "html"
                email.send()
                
                messages.success(request, '✅ ¡Registro exitoso! Se ha enviado un correo de bienvenida.')
                
            except Exception as e:
                messages.success(request, '✅ ¡Registro exitoso! (No se pudo enviar el correo de bienvenida)')
                print(f"Error enviando email de bienvenida: {str(e)}")
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'usuarios/login.html', {'form': form})