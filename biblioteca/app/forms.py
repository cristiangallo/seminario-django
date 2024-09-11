
from django import forms
from .models import Socio, Libro


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        # fields = '__all__'
        exclude = []

    def clean(self):
        return self.cleaned_data

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        return telefono

    def clean_celular(self):
        import re
        import phonenumbers
        telefono = self.cleaned_data.get('telefono')
        celular = self.cleaned_data.get('celular')
        if not telefono and not celular:
            raise forms.ValidationError("Debe informar un telefono o un celular")

        if celular:
            try:
                celular = "".join(re.findall(r'[0-9]+', celular))
                celular = phonenumbers.parse(celular, "AR")
                if not phonenumbers.is_valid_number(celular):
                    raise forms.ValidationError('El celular ingresado no es válido.')
                celular = phonenumbers.format_number(celular, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            except phonenumbers.NumberParseException:
                raise forms.ValidationError('El celular ingresado no es válido.')

        return celular


class BuscadorForm(forms.Form):
    libro = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Nombre del libro*",
                'required': "required",
                # 'data-validation-required-message': "Please enter your name."
            }))
    nro_doc_socio = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "DNI socio*",
                # 'required': "required",
                # 'data-validation-required-message': "Please enter your name."
            }))

    def buscar_libros(self):
        texto = self.cleaned_data.get("libro")
        nro_doc_socio = self.cleaned_data.get("nro_doc_socio")
        resultado_busqueda = Libro.objects.filter(titulo__icontains=texto)

        return resultado_busqueda


class LibroForm(forms.ModelForm):
    ISBN = forms.CharField(
        max_length=100, required=True, label='ISBN', widget=forms.TextInput(
            attrs={'readonly': 'readonly', 'class': 'form-control'}))

    class Meta:
        model = Libro
        exclude = []

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(LibroForm, self).__init__(*args, **kwargs)
        if instance.pk:
            self.fields['ISBN'] = forms.CharField(
                initial=instance.isbn(), required=False, label='ISBN', widget=forms.TextInput(
                    attrs={'class': 'form-control', 'readonly': 'readonly'}))
        elif instance is None or instance.pk is None:
            self.fields['ISBN'] = forms.CharField(
                required=True, label='ISBN', widget=forms.TextInput(
                    attrs={'class': 'form-control'}))

        fields_order = ['ISBN'] + list(self.fields.keys())
        self.fields = {field: self.fields[field] for field in fields_order}

    def clean_ISBN(self):
        import re
        ISBN = self.cleaned_data.get('ISBN')
        ISBN = "".join(re.findall(r'[0-9]+', ISBN))
        if len(ISBN) != 13 or not ISBN.isdigit():
            raise forms.ValidationError(f'El ISBN debe contener exactamente 13 dígitos. "{ISBN}" no es válido.')
        return ISBN

    def save(self, commit=True):
        instance = super(LibroForm, self).save(commit=False)
        # if not instance.pk:
        ISBN = self.cleaned_data.get('ISBN')
        self.instance.pk = ISBN
        libro = super(LibroForm, self).save(commit=True)
        return libro