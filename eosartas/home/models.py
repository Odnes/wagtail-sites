from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class HomePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
            FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [ # Inherit search_fields from Page
           index.SearchField('body')
       ]
