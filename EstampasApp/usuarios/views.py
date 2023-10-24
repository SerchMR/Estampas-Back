from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from .models import Cliente
from .models import Artista
from .models import Admin
import json
from django.http import HttpResponse
# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'GET':
        response_data = {
        "mensaje": "Login exitoso.",
        "redireccion": "/usuario"
        }
        # Convertir el diccionario a formato JSON
        json_response = json.dumps(response_data)

        # Crear una respuesta JSON
        response = HttpResponse(json_response, content_type='application/json')

        # Redirigir al usuario a la URL especificada en el diccionario JSON
        response['Location'] = response_data["redireccion"]
        try:
            usuarioObtenido = Usuario.objects.filter(usuario=request.GET.get('usuario'))
            print(usuarioObtenido)
        except Usuario.DoesNotExist:
            usuarioObtenido = None
        #caso cliente
        if request.GET.get('rol') == 'cliente':
            try:
                cliente = Cliente.objects.filter(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Usuario.DoesNotExist:
                cliente = None
            if  usuarioObtenido is not None and cliente is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como cliente')
        #caso Artista
        if request.GET.get('rol') == 'artista':
            try:
                artista = Artista.objects.filter(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Usuario.DoesNotExist:
                artista = None
            if  usuarioObtenido is not None and artista is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como artista')
        #caso admin
        if request.GET.get('rol') == 'admin':
            try:
                admin = Admin.objects.filter(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Usuario.DoesNotExist:
                admin = None
            if  usuarioObtenido is not None and admin is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como admin')
        else:
            return HttpResponse('Metodo no GET')

@csrf_exempt
def registro(request):
    nuevo_artista = None
    nuevo_cliente = None
    nuevo_usuario = None
    if request.method == 'GET':

        contador = 0
        for key, value in request.GET.items():
            contador+=1

        #registro usuario        
        print(request.GET.get('tipoid'))
        print(request.GET.get('numid'))
        
        nuevo_usuario = Usuario(tipoid=request.GET.get('tipoid'), numid=request.GET.get('numid'),
                                        nombre=request.GET.get('nombre'), apellido=request.GET.get('apellido')
                                        , genero=request.GET.get('genero'), correo=request.GET.get('correo'),
                                        usuario=request.GET.get('usuario'), contrasena=request.GET.get('contrasena'))
        print(nuevo_usuario)
        nuevo_usuario.save()
        print("se creo usuario")
        #print(Usuario.objects.get())
        

        #registro cliente
        if request.GET.get('rol')=='cliente' and request.GET.get('direccion', None) is not None:
            nuevo_cliente = Cliente (numidusuario = Usuario.objects.get(numid =request.GET.get('numid')),
                                      tipoidusuario = request.GET.get('tipoid'),
                                        direccion =request.GET.get('direccion'))
            nuevo_cliente.save()
            print("se creo cliente")
            return HttpResponse('Cliente creado')
        elif(request.GET.get('rol')=='artista'):    #registro artista
            nuevo_artista = Artista (tipoidusuario = request.GET.get('tipoid'), numidusuario = Usuario.objects.get(numid =request.GET.get('numid')), utilidad = 0, numventas =0)
            nuevo_artista.save()
            print("se creo artista")
        #if (contador == 9):
        #    nuevo_usuario = Usuario(tipoID=request.GET.get('tipoid'), numID=request.GET.get('numid'),
        #                                nombre=request.GET.get('nombre'), apellido=request.GET.get('apellidp')
        #                                , genero=request.GET.get('genero'), correo=request.GET.get('correo'),
        #                                usuario=request.GET.get('usuario'), contrasena=request.GET.get('contrasena'))
        #    nuevo_usuario.save()
        #    print("se creo artista")
        #else:
        #    return HttpResponse('Faltaron datos')
        response_data = {
        "mensaje": "Registro exitoso.",
        "redireccion": "/api/login"
        }

        # Convertir el diccionario a formato JSON
        json_response = json.dumps(response_data)

        # Crear una respuesta JSON
        response = HttpResponse(json_response, content_type='application/json')

        # Redirigir al usuario a la URL especificada en el diccionario JSON
        response['Location'] = response_data["redireccion"]
        
        return response
    else:
        return HttpResponse('fallo en el registro')