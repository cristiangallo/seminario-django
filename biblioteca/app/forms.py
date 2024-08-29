
from django import forms
from .models import Socio


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
