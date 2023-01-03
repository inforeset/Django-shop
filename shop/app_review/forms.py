from django import forms
from django.forms import ModelForm

from .models import Review


class ReviewForm(ModelForm):
    text = forms.CharField(max_length=300, required=True, widget=forms.Textarea(attrs={'class': 'form-textarea',
                                                                                       'data-validate': 'require',
                                                                                       'placeholder': 'Отзыв'}))

    class Meta:
        model = Review
        fields = ('text',)
