from django import forms
from django.forms import formset_factory


class CheckboxForm(forms.Form):
    box = forms.BooleanField()
    box.widget.attrs['class'] = 'form-check-input'


class CheckBoxSet:
    def __init__(self, extra):
        self.article_formset = formset_factory(CheckboxForm, extra=extra)
        self.formset = self.article_formset()
