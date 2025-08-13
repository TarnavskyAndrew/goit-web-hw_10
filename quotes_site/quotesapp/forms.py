from django import forms
from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        widgets = {
            "fullname": forms.TextInput(attrs={"required": True, "maxlength": "150"}),
        }


class QuoteForm(forms.ModelForm):
    # дозволимо вводити теги рядком "tag1, tag2, tag3"
    tags_csv = forms.CharField(
        required=False, help_text="Separated by commas: tag1, tag2, ..."
    )

    class Meta:
        model = Quote
        fields = ["text", "author", "tags_csv"]
        widgets = {"text": forms.Textarea(attrs={"required": True}),}

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # обрабка tags_csv
        tags_csv = self.cleaned_data.get("tags_csv") or ""
        if tags_csv:
            names = [t.strip() for t in tags_csv.split(",") if t.strip()]
            from .models import Tag

            tags = []
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.set(tags)
        return instance
