# -*- coding: utf-8 -*-

from django import forms


class EmailPostForm(forms.Form):
    """Форма для отправки сообщений на эл.почту"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
