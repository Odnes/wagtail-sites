import json
import os

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from wagtail.models import Page, Orderable, Collection
from wagtail.images import get_image_model
from wagtail.documents.models import Document
from blog.models import BlogPage
from bs4 import BeautifulSoup

# field > block > type. A RichTextField contains a single RichText object. A Streamfield contains multiple Streamblock objects.
# check chatGPTs answer of how to populate a Streamfield via StreamValue
from wagtail.rich_text import RichText

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('arg1', type=str, help='A positional argument')

        # Named (optional) arguments
        parser.add_argument('--img_dir', type=str, help='Used to import images and image directories into wagtail')

    def handle(self, *arg, **kwargs):
        if 'img_dir' in kwargs:
            img_dir = kwargs['img_dir']
            # Import the image files into wagtail (don't forget to run django's collectstatic first)
            self.import_images(img_dir)

      # Grab articles' html
       # with open('tk5n4_content.json') as f:
       #     d = json.load(f)

       #     test_html = d[2]['data'][30]['introtext'] + d[2]['data'][30]['fulltext']
       #     soup = BeautifulSoup(test_html, 'html.parser')
       #     for tag in soup.descendants:
       #         if tag.name == "img":
       #             if 'style' in tag.attrs and tag.attrs['style'].find('float') != -1:
       #                 print(tag.attrs['style'])
       #                 img_name = tag.attrs['src'].split("images/")[-1]
       #                 img_path = f"original_images/{img_name}"
       #                 print(img_path)
       #                 image = Image.objects.filter(file="original_images/zagori.png").first() # use get() instead of filter if sure it should return a single object
       #     parent_page = Page.objects.get(title="Αρχική")
       #     print(image.title)
#
#            blog_page = BlogPage(
#                title="My Blog Post",
#                slug="my-blog-post",
#            )
#
#            blog_page.body.append(('paragraph', RichText("<p>And they all lived happily ever after.</p>")))
#
#            parent_page.add_child(instance=blog_page)
#            blog_page.save_revision().publish()
            # Use beautifulsoup to parse html and:
            # if <img>:
                # if <a> partent has float: left or float: right:  (?)
                    # if gallery_open:
                        # gallery_open = false
                #  block.block_type == 'image'
                # else:
                    # if !gallery_open:
                        # gallery_open
                    # block.block_type == "gallery"
# - Only difference between regular images and gallery images is that regular images have have parent <a> with "float" set.
# - Therefore, custom logic needs to be implemented for conditionally starting and finishing a new gallery.

# Done already, manually. Should implement it at some point.
            # replace all images/FOLDER_NAME/FILE_NAME
            # with /media/original_images/FOLDER_NAME/FILE_NAME

    def import_images(self, img_dir):
        # Traverse the directory and process files
        for root, dirs, files in os.walk(img_dir):
            relative_path = os.path.relpath(root, img_dir)
            print(root)
            print(relative_path, str(type(relative_path)))
            # why does this need relative path? perhaps because it mirrors directories in urls, which ideally are relative?
            collection = self._get_or_create_collection(relative_path)
            for filename in files:
                if self._is_image_file(filename):
                    pass
                    #self._create_wagtail_image(os.path.join(root, filename), filename, collection)

# Creates a collection tree for each directory path provided
# TODO: start trying to build the tree from the collection corresponding to the current
#  relative path, not from the root collection
    def _get_or_create_collection(self, relative_path):
        current_collection = Collection.get_first_root_node()
    # can't filter by name and parent, because parent is not known within the method.
    # should perhaps extract the walking logic from the function?
    #        current_collection = Collection.objects.filter(name=part,).first()
        print(current_collection.get_parent())
       #TODO check comment above. breakpoint()
        if current_collection is None:
            root_collection = Collection.add_root(name="Root")
            current_collection = root_collection
            print("Root collection created")
        else:
            print("Root collection already exists")

        path_parts = relative_path.split('/')
        for part in path_parts:
                try:
                    current_collection = current_collection.get_children().get(name=part)
                except Collection.DoesNotExist:
                     current_collection.add_child(name=part)
                     current_collection = current_collection.get_children().get(name=part)
                print("Current node:" + current_collection.name)

        # the wagtail database.
        # Method of Django's QuerySet API, filters for, and if empty, creates a collection.
#          root_collection = Collection.objects.filter(name=relative_path.split('/')[-2])
#          print("Parent detected: " + str(root_collection))
#          collection = Collection.objects.get_or_create(name=relative_path.split('/')[-1])[0]
#          current_collection = root_collection
#          while relative_path != current_collection + name
#          current_collection = Collection.objects.get_or_create(name=part, path=current_collection)

              #        current_collection = Collection.objects.create( name=part, path=current_collection)
#          return current_collection



    def _is_image_file(self, filename):
           # Check if the file is an image based on its extension
           return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

    def _create_wagtail_image(self, file_path, filename, collection):
        Image = get_image_model()
        with open(file_path, 'rb') as f:
            #TODO if not Image.objects.filter(File.objects.name == filename):
            wagtail_image = Image.objects.create(
                title=filename,
                file=File(f, name=filename),
                collection=collection
            )
        self.stdout.write(f'Created Wagtail Image: {wagtail_image.title} in collection {collection.name}')
