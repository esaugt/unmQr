from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, LoginForm, BloqueForm, SitioForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse_lazy
from sitios.models import Bloque, Sitio
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('administrador')  # Redirecciona a la página de inicio después del inicio de sesión exitoso
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_cnfrm')  # Redirecciona a la página de inicio de sesión después del registro exitoso
    else:
        form = UserRegistrationForm()

    return render(request, 'registrarse.html', {'form': form})

def recuperar(request):
    return render(request, 'recuperar.html')

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def registro_cnfrm(request):
    return render(request, 'registrado.html')

@login_required
def administrador(request):
    bloques = Bloque.objects.all()
    return render(request, 'administrador.html', {'bloques': bloques})

@login_required
def ver_sitios(request, bloque_id):
    bloque = get_object_or_404(Bloque, id=bloque_id)
    sitios = Sitio.objects.filter(bloque=bloque)
    return render(request, 'sitios.html', {'bloque': bloque, 'sitios': sitios})


@login_required
def editar_bloque(request, bloque_id):
    bloque = get_object_or_404(Bloque, id=bloque_id)
    if request.method == 'POST':
        form = BloqueForm(request.POST, instance=bloque)
        if form.is_valid():
            form.save()
            return redirect('administrador')
    else:
        form = BloqueForm(instance=bloque)
    return render(request, 'editar_bloque.html', {'form': form})

@login_required
def editar_sitio(request, sitio_id):
    sitio = get_object_or_404(Sitio, id=sitio_id)

    if request.method == 'POST':
        form = SitioForm(request.POST, instance=sitio)
        if form.is_valid():
            form.save()
            return redirect('ver_sitios', bloque_id=sitio.bloque.id)
    else:
        form = SitioForm(instance=sitio)

    return render(request, 'editar_sitio.html', {'form': form, 'sitio': sitio})

class MyPasswordResetView(PasswordResetView):
    template_name = 'reestablecer/reset_recuperar.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'reestablecer/password_reset_email.html'
    subject_template_name = 'reestablecer/password_reset_subject.txt'

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reestablecer/reset_enviado.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'reestablecer/reset_nueva.html'
    success_url = reverse_lazy('password_reset_complete')

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'reestablecer/reset_confirmacion.html'


##subirimagen
from django.core.exceptions import ValidationError

@login_required
def editar_bloque(request, bloque_id):
    bloque = get_object_or_404(Bloque, id=bloque_id)
    if request.method == 'POST':
        form = BloqueForm(request.POST, request.FILES, instance=bloque)
        if form.is_valid():
            # Save the form and handle the image
            form.save()
            return redirect('administrador')
    else:
        form = BloqueForm(instance=bloque)
    return render(request, 'editar_bloque.html', {'form': form})
