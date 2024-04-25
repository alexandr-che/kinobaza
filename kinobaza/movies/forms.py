from django import forms

from movies.models import StarRating, Rating


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=StarRating.objects.all(),
        widget=forms.RadioSelect(),
        required=False,
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('rate',)
