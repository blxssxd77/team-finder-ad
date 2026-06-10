import random
import re
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_COLORS = [
    '#6B7280', '#4B5563', '#5B6B7A', '#4A5568',
    '#718096', '#2D3748', '#64748B', '#475569',
]

PHONE_PATTERN = re.compile(r'^(8\d{10}|\+7\d{10})$')


def normalize_phone(phone):
    phone = phone.strip()
    if phone.startswith('8') and len(phone) == 11:
        return '+7' + phone[1:]
    return phone


def validate_phone(phone):
    return bool(PHONE_PATTERN.match(phone.strip()))


def generate_avatar(name):
    letter = name[0].upper() if name else '?'
    color = random.choice(AVATAR_COLORS)
    size = 200
    image = Image.new('RGB', (size, size), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('arial.ttf', 100)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    x = (size - (bbox[2] - bbox[0])) // 2
    y = (size - (bbox[3] - bbox[1])) // 2 - 10
    draw.text((x, y), letter, fill='white', font=font)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{letter}.png')
