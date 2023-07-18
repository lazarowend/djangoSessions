from django.shortcuts import render, redirect
from .models import Usuario
from hashlib import sha256
from django.http import HttpResponse


def login(request):
    status = request.GET.get('status')
    return render(request, 'usuarios/login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'usuarios/cadastro.html', {'status': status})


def valida_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            return redirect('/auth/cadastro/?status=1')
        
        if len(senha) < 8:
            return redirect('/auth/cadastro/?status=2')
        
        usuario = Usuario.objects.filter(email=email)
        if len(usuario) > 0:
            return redirect('/auth/cadastro/?status=3')

        try:
            senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(
                nome=nome,
                senha=senha,
                email=email
            )
            usuario.save()
            return redirect('/auth/cadastro/?status=0')
        except:
            return redirect('/auth/cadastro/?status=4')


def valida_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario.objects.filter(email=email).filter(senha=senha)

        if len(usuario) == 0:
            return redirect('/auth/login/?status=1')
        
        # request.session['status'] = {'logado': True, 'usuario.id': usuario[0].id}
        request.session['logado'] = True
        request.session['usuario.id'] = usuario[0].id
        return redirect('/plataforma/home')



def sair(request):
    try:
        del request.session['logado']
        return redirect('/auth/login')
    except KeyError:
        return redirect('/auth/login/?status=3')
    # return HttpResponse(request.session.get_expiry_date())
    # flush apaga tudo
    # clear mantem a variavel na memoria
    # request.session.flush() --- ideal para logout
    # return redirect('/auth/login')