from django import forms
from .models import Author, Quote, Tag


# Форма для створення/редагування автора
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author # вказуємо модель, з якою працюємо
        # перелік полів, які будемо використовувати у формі
        fields = ["fullname", "born_date", "born_location", "description"] 
        # вказуємо, як виглядатимуть поля форми
        widgets = {
            "fullname": forms.TextInput(attrs={"required": True, "maxlength": "150"}),  
        }


# Форма для створення/редагування цитати
class QuoteForm(forms.ModelForm):
    # дозволимо вводити теги рядком "tag1, tag2, tag3"
    tags_csv = forms.CharField(
        required=False, help_text="Separated by commas: tag1, tag2, ..."
    )
    
    # вказуємо, що це форма для моделі Quote
    class Meta:
        model = Quote
        fields = ["text", "author", "tags_csv"]
        widgets = {"text": forms.Textarea(attrs={"required": True}),}

    # перевизначаємо метод save, щоб обробити теги
    # і зберегти їх у відповідному полі ManyToMany
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
