import json

from django.core.management.base import BaseCommand
from wagtail.models import Page, Orderable

class Command(BaseCommand):
    def handle(self, *arg, **kwargs):
        with open('tk5n4_content.json') as f:
            d = json.load(f)
            print(d[2]['data'][30]['title'] + d[2]['data'][30]['introtext'] + d[2]['data'][30]['fulltext'])

            parent_page = Page.objects.get(title="Νεμέρτσικα").specific
            # replace all images/FOLDER_NAME/FILE_NAME
            # with /media/original_images/FOLDER_NAME/FILE_NAME

            # Use beautifulsoup to parse html and:
            # if <img>:
                # if float: left or float: right:  (?)
                #  block.block_type == 'image'
                # else:
                    # block.block_type == "gallery"

            # automatically load json lines into wagtail
