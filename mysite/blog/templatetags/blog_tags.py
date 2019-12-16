# -*- coding: utf-8 -*-
"""Модуль для собственных тегов"""

from django import template
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Тег возвращает количество опубликованных статей"""
    return Post.published.count()
