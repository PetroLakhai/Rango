from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse

from rango.bing_search import run_query
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page


def index(request):
    """The method render index (main) page."""
    category_list: QuerySet = Category.objects.order_by("-likes")[:5]
    page_list: QuerySet = Page.objects.order_by("-views")[:5]

    context_dict = {}
    context_dict["boldmessage"] = ["Green text, green text, green text!"]
    context_dict["categories"] = category_list
    context_dict["pages"] = page_list

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]

    response = render(request, "rango/index.html", context=context_dict)
    return response


def about(request):
    """The method render about page."""
    context_dict = {"message": "Funny man!"}

    visitor_cookie_handler(request)
    context_dict["visits"] = request.session["visits"]
    return render(request, "rango/about.html", context=context_dict)


def training(request):
    """The method render training page."""
    example_dict = {
        "second_picture_presentation": "Below presented to Rango and his Hot Baby. Let`s scroll together!"
    }
    return render(request, "rango/training.html", context=example_dict)


def show_category(request, category_name_slug):
    """The method render category page."""
    context_dict = {}

    try:
        category: Category = Category.objects.get(slug=category_name_slug)
        pages: Page = Page.objects.filter(category=category)

        context_dict["pages"] = pages
        context_dict["category"] = category

    except Category.DoesNotExist:
        context_dict["category"] = None
        context_dict["pages"] = None

    return render(request, "rango/category.html", context=context_dict)


@login_required
def add_category(request):
    """The method render add_category page, if user registered."""
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/rango/")
        else:
            print(form.errors)
    return render(request, "rango/add_category.html", {"form": form})


@login_required
def add_page(request, category_name_slug: str):
    """The method render add_page page, if user registered."""
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

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
    """The method render restricted page, if user registered."""
    return render(request, "rango/restricted.html")


def _get_server_side_cookie(request, cookie: str, default_val=None) -> int:
    """The method collect cookie data. It is helper method for method visitor_cookie_handler."""
    val: int = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    """The method collect data about user`s quantity of website visits and last time when user visit website."""
    visits = int(_get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie: str = _get_server_side_cookie(
        request, "last_visit", str(datetime.now())
    )
    last_visit_time: datetime = datetime.strptime(
        last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S"
    )

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie
    request.session["visits"] = visits


def search(request):
    result_list = []
    query = ""

    if request.method == "POST":
        query = request.POST["query"].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(
        request,
        "rango/search.html",
        context={"result_list": result_list, "query": query},
    )
