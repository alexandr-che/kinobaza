from django import forms

from movies.models import StarRating, Rating, Comment


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


class CommentForm(forms.ModelForm):
    comment = forms.Textarea()

    class Meta:
        model = Comment
        fields = ('comment',)
