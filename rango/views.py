from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {}
    context_dict["boldmessage"] = ["Crunchy, creamy, cookie, candy, cupcake!"]
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]

    response = render(request, "rango/index.html", context=context_dict)
    return response


def about(request):
    context_dict = {"message": "Funny man!"}

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]

    return render(request, "rango/about.html", context=context_dict)


def training(request):
    example_dict = {
        "second_picture_presentation": "Below presented to Rango and his Hot Baby. Let`s scroll together!"
    }
    return render(request, "rango/training.html", context=example_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict["pages"] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict["category"] = None
        context_dict["pages"] = None

    # Go render the response and return it to the client.
    return render(request, "rango/category.html", context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect("/rango/")
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases. # Render the form with error messages (if any).
    return render(request, "rango/add_category.html", {"form": form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect("/rango/")

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

            return redirect(
                reverse(
                    "rango:show_category",
                    kwargs={"category_name_slug": category_name_slug},
                )
            )

        else:
            print(form.errors)

    context_dict = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context=context_dict)


@login_required
def restricted(request):
    return render(request, "rango/restricted.html")


# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(
        request, "last_visit", str(datetime.now())
    )
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        # Update the last visit cookie now that we have updated the count
        request.session["last_visit"] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session["last_visit"] = last_visit_cookie

    # Update/set the visits cookie
    request.session["visits"] = visits
