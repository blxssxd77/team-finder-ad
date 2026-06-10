import re

from django import forms

from .models import Project

GITHUB_PATTERN = re.compile(r'^https?://(www\.)?github\.com/', re.IGNORECASE)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'github_url', 'status')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'github_url': 'Ссылка на GitHub',
            'status': 'Статус',
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url', '')
        if url and not GITHUB_PATTERN.match(url):
            raise forms.ValidationError('Ссылка должна вести на github.com')
        return url
