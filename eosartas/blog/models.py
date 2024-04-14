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
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index

class HomePage(Page):
#    parent_page_types = [] # uncomment to henceforth hide this model from admin options
    pass

class BlogTagIndexPage(Page):
#    parent_page_types = [] # uncomment to henceforth hide this model from admin options

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogIndexPage(Page):
#    parent_page_types = [] # uncomment to henceforth hide this model from admin options
    subpage_types = ['blog.BlogPage']


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    parent_page_types = ['blog.BlogIndexPage']


    date = models.DateField("Post date", default=date.today)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('gallery', blocks.StreamBlock([('image', ImageChooserBlock()),
                                        ('video', ImageChooserBlock())
                                       ])
        ),             
    ])


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags')
        ], heading="Blog information"),
            FieldPanel('body'),
      # Might use later for sidebar related articles tab
      #  MultiFieldPanel(
      #      [InlinePanel("carousel_images", label="Image")],
      #      heading="Carousel Images",
      #  ),
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
