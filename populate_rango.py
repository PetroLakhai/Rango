import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django

django.setup()

from rango.models import Category, Page


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {
            "title": "Official Python Tutorial",
            "url": "http://docs.python.org/3/tutorial/",
            "views": 1,
        },
        {
            "title": "How to Think like a Computer Scientist",
            "url": "http://www.greenteapress.com/thinkpython/",
            "views": 2,
        },
        {
            "title": "Learn Python in 10 Minutes",
            "url": "http://www.korokithakis.net/tutorials/python/",
            "views": 3,
        },
    ]

    django_pages = [
        {
            "title": "Official Django Tutorial",
            "url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/",
            "views": 4,
        },
        {"title": "Django Rocks", "url": "http://www.djangorocks.com/", "views": 5},
        {
            "title": "How to Tango with Django",
            "url": "http://www.tangowithdjango.com/",
            "views": 6,
        },
    ]

    go_pages = [
        {
            "title": "Official Go Documentation",
            "url": "https://go.dev/doc/",
            "views": 3,
        },
        {
            "title": "Go Wikipedia",
            "url": "https://shorturl.at/ayzKX",
            "views": 5,
        },
    ]

    other_pages = [
        {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/", "views": 7},
        {"title": "Flask", "url": "http://flask.pocoo.org", "views": 8},
    ]

    categories = {
        "Python": {"pages": python_pages, "views": 128, "likes": 64},
        "Django": {"pages": django_pages, "views": 128, "likes": 32},
        "Other Frameworks": {"pages": other_pages, "views": 128, "likes": 16},
        "Pascal": {"pages": [], "views": 10, "likes": 5},
        "Perl": {"pages": [], "views": 9, "likes": 4},
        "Prolog": {"pages": [], "views": 8, "likes": 3},
        "PostScript": {"pages": [], "views": 7, "likes": 2},
        "Programing": {"pages": [], "views": 6, "likes": 1},
        "Go": {"pages": go_pages, "views": 3, "likes": 2},
    }

    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat_key, cat_data in categories.items():
        category = add_cat(cat_key, views=cat_data["views"], likes=cat_data["likes"])
        for page in cat_data["pages"]:
            add_page(category, page["title"], page["url"], page["views"])

    # Print out the categories we have added.
    for category in Category.objects.all():
        for page in Page.objects.filter(category=category):
            print(f"- {category}: {page}")


def add_page(cat, title, url, views):
    page = Page.objects.get_or_create(category=cat, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page


def add_cat(name, views, likes):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category


# Start execution here!
if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()
