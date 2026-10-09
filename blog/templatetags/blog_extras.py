from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Safely replace or add query parameters in URLs (useful for pagination with search query).
    Example: {% url_replace page=page_obj.next_page_number %}
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter
def format_post_content(text):
    """
    Format blog post content:
    Preserves existing HTML tags if present, or wraps plain text in paragraph tags
    and formats blockquotes and code snippets.
    """
    if not text:
        return ""
    # If the text already has substantial HTML tags like <p>, <div>, <h2>, render safe
    if bool(re.search(r'<(p|div|h[1-6]|ul|ol|table|blockquote|pre)', text, re.IGNORECASE)):
        return mark_safe(text)

    # Otherwise convert plain text paragraphs (split by double newlines)
    paragraphs = text.strip().split('\n\n')
    formatted = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        # Convert single newlines inside paragraph to <br>
        p_clean = p_clean.replace('\n', '<br>')
        formatted.append(f"<p>{p_clean}</p>")
    return mark_safe('\n'.join(formatted))


@register.filter
def reading_badge(minutes):
    """Returns a friendly reading time string."""
    if minutes <= 1:
        return "1 min read"
    return f"{minutes} min read"
