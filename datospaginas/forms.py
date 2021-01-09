#encoding:utf-8
from django import forms


class ContactoForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput, label = "Nombre Completo")
    email = forms.EmailField(label = "Correo")
    telefono = forms.CharField(widget = forms.TextInput, label = "Telefono")
    comments = forms.CharField(widget = forms.Textarea, label = "Comentarios")