import re

from django import forms

from .constants import GITHUB_URL_ERROR_MESSAGE

GITHUB_PATTERN = re.compile(r'^https?://(www\.)?github\.com/', re.IGNORECASE)


def validate_github_url(url):
    if url and not GITHUB_PATTERN.match(url):
        raise forms.ValidationError(GITHUB_URL_ERROR_MESSAGE)
    return url
