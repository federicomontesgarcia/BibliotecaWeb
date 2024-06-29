from django.shortcuts import render, redirect

from django.conf import settings

from .forms import FormularioContacto

from django.core.mail import EmailMessage

# Create your views here.

def contacto(request):
    """Función para que el visitante en la web escriba una sugerencia o solicitud y sea enviada vía e-mail"""

    formulario_contacto = FormularioContacto()

    if request.method == "POST":
        formulario_contacto = FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            contenido = request.POST.get("contenido")

            email = EmailMessage("mensaje desde el aplicativo web Biblioteca",
                                 "El usuario con nombre {} con la dirección {} escribe lo siguiente:\n\n {}".format(nombre, email, contenido),
                                 settings.EMAIL_HOST_USER,["baudolino78@hotmail.com"],reply_to=[email])
            try:
                email.send()

                return redirect("/contacto/?valido")

            except:
                return redirect(("/contacto/?novalido"))

    return render(request, "contacto/contacto.html", {'miFormulario': formulario_contacto})