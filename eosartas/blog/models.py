from datetime import date

from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.blocks import RawHTMLBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index

class HomePage(Page):
#    parent_page_types = [] # uncomment to henceforth hide this model from admin options
    pass


class IndexPage(Page):
#    parent_page_types = [] # uncomment to henceforth hide this model from admin options
    subpage_types = ['blog.BlogPage']


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    parent_page_types = ['blog.IndexPage']

    date = models.DateField("Post date", default=date.today)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    intro = StreamField([
        ('heading', blocks.CharBlock(form_classname="")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
        ('gallery', blocks.StreamBlock([('image', ImageChooserBlock()),
                                        #('video', EmbedBlock())
                                       ])
        ),
        ('raw_html', RawHTMLBlock()),
    ])

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock()),
        ('gallery', blocks.StreamBlock([('image', ImageChooserBlock()),
                                        #('video', EmbedBlock())
                                       ])
        ),
        ('raw_html', RawHTMLBlock()),
    ], blank=True)


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Blog information"),
            FieldPanel('intro'),
            FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [ # Inherit search_fields from Page
           index.SearchField('body')
       ]


@register_snippet
class Menu(ClusterableModel):
    label = models.CharField(max_length=100)

    panels = [
        FieldPanel('label'),
        InlinePanel('submenu_items', label="Menu items"),
    ]

    def __str__(self):
        return self.label


class MenuItem(Orderable):
    root = ParentalKey("blog.Menu", related_name="submenu_items", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    has_dropdown = models.BooleanField(default=False)
    url = models.CharField(max_length=255, blank=True)
    submenus = StreamField([
        ('submenu_item', blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('url', blocks.CharBlock()),
        ])
        )
    ], blank=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('url'),
        FieldPanel('has_dropdown'),
        FieldPanel('submenus'),
    ]
