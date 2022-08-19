from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from rango.bing_search import run_query
from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, UserProfile


class IndexView(View):
    def get(self, request):
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


# def index(request):
#     """The method render index (main) page."""
#     category_list: QuerySet = Category.objects.order_by("-likes")[:5]
#     page_list: QuerySet = Page.objects.order_by("-views")[:5]
#
#     context_dict = {}
#     context_dict["boldmessage"] = ["Green text, green text, green text!"]
#     context_dict["categories"] = category_list
#     context_dict["pages"] = page_list
#
#     visitor_cookie_handler(request)
#     context_dict["visits"] = request.session["visits"]
#
#     response = render(request, "rango/index.html", context=context_dict)
#     return response


class AboutView(View):
    def get(self, request):
        context_dict = {}
        visitor_cookie_handler(request)
        context_dict["visits"] = request.session["visits"]
        return render(request, "rango/about.html", context_dict)


class TrainingView(View):
    def get(self, request):
        example_dict = {
            "second_picture_presentation": "Below presented to Rango and his Hot Baby. Let`s scroll together!"
        }
        return render(request, "rango/training.html", context=example_dict)


class ShowCategoryView(View):
    def get(self, request, category_name_slug):
        """The method render category page."""
        context_dict = {}

        try:
            category: Category = Category.objects.get(slug=category_name_slug)
            pages: Page = Page.objects.filter(category=category).order_by("-views")

            context_dict["pages"] = pages
            context_dict["category"] = category

        except Category.DoesNotExist:
            context_dict["category"] = None
            context_dict["pages"] = None

        return render(request, "rango/category.html", context=context_dict)


# def show_category(request, category_name_slug):
#     """The method render category page."""
#     context_dict = {}
#
#     try:
#         category: Category = Category.objects.get(slug=category_name_slug)
#         pages: Page = Page.objects.filter(category=category).order_by("-views")
#
#         context_dict["pages"] = pages
#         context_dict["category"] = category
#
#     except Category.DoesNotExist:
#         context_dict["category"] = None
#         context_dict["pages"] = None
#
#     return render(request, "rango/category.html", context=context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, "rango/add_category.html", {"form": form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("rango:index"))
        else:
            print(form.errors)
        return render(request, "rango/add_category.html", {"form": form})


# @login_required
# def add_category(request):
#     """The method render add_category page, if user registered."""
#     form = CategoryForm()
#
#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect("/rango/")
#         else:
#             print(form.errors)
#     return render(request, "rango/add_category.html", {"form": form})


class AddPageView(View):
    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None

        if category is None:
            return redirect("/rango/")

        form = PageForm()

        context_dict = {"form": form, "category": category}
        return render(request, "rango/add_page.html", context=context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
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


# @login_required
# def add_page(request, category_name_slug: str):
#     """The method render add_page page, if user registered."""
#     try:
#         category = Category.objects.get(slug=category_name_slug)
#     except Category.DoesNotExist:
#         category = None
#
#     if category is None:
#         return redirect("/rango/")
#
#     form = PageForm()
#
#     if request.method == "POST":
#         form = PageForm(request.POST)
#
#         if form.is_valid():
#             if category:
#                 page = form.save(commit=False)
#                 page.category = category
#                 page.views = 0
#                 page.save()
#
#             return redirect(
#                 reverse(
#                     "rango:show_category",
#                     kwargs={"category_name_slug": category_name_slug},
#                 )
#             )
#
#         else:
#             print(form.errors)
#     context_dict = {"form": form, "category": category}
#     return render(request, "rango/add_page.html", context=context_dict)


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):

        """The method render restricted page, if user registered."""
        return render(request, "rango/restricted.html")


# @login_required
# def restricted(request):
#     """The method render restricted page, if user registered."""
#     return render(request, "rango/restricted.html")


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


class SearchView(View):
    def post(self, request):
        result_list = []

        if request.method == "POST":
            query = request.POST["query"].strip()
            if query:
                # Run our Bing function to get the results list!
                result_list = run_query(query)

        pages = Page.objects.all()
        search_results = []
        for page in pages:
            if query.lower() in page.title.lower():
                search_results.append(page)
        return render(
            request,
            "rango/category.html",
            {"result_list": result_list, "search_results": search_results},
        )


# def search(request):
#     result_list = []
#
#     if request.method == "POST":
#         query = request.POST["query"].strip()
#         if query:
#             # Run our Bing function to get the results list!
#             result_list = run_query(query)
#
#     pages = Page.objects.all()
#     search_results = []
#     for page in pages:
#         if query.lower() in page.title.lower():
#             search_results.append(page)
#     return render(request, "rango/category.html", {"result_list": result_list, "search_results": search_results})


class GoToUrlView(View):
    def get(self, request):
        if request.method == "GET":
            page_id = request.GET.get("page_id")
            try:
                page = Page.objects.filter(id=page_id).first()
            except Page.DoesNotExist:
                return redirect(reverse("rango:index"))

            page.views = page.views + 1
            page.save()
            page_url = page.url

            return redirect(page_url)

        return redirect(reverse("index"))


# def goto_url(request):
#     if request.method == "GET":
#         page_id = request.GET.get("page_id")
#         try:
#             page = Page.objects.filter(id=page_id).first()
#         except Page.DoesNotExist:
#             return redirect(reverse('rango:index'))
#
#         page.views = page.views + 1
#         page.save()
#         page_url = page.url
#
#         return redirect(page_url)
#
#     return redirect(reverse("index"))


class ProfileRegistrationView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()

        context_dict = {"form": form}
        return render(request, "rango/profile_registration.html", context_dict)

    @method_decorator(login_required)
    def post(self, request):
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit=False)
                user_profile = UserProfile.objects.get(user__id=request.user.id)
                user_profile.website = form.cleaned_data["website"]
                user_profile.picture = form.cleaned_data["picture"]
                user_profile.save()
                return redirect("/rango/")
            else:
                print(form.errors)
        context_dict = {"form": form}
        return render(request, "rango/profile_registration.html", context_dict)


# @login_required
# def profile_registration(request):
#     form = UserProfileForm()
#
#     if request.method == "POST":
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save(commit=False)
#             user_profile = UserProfile.objects.get(user__id=request.user.id)
#             user_profile.website = form.cleaned_data["website"]
#             user_profile.picture = form.cleaned_data["picture"]
#             user_profile.save()
#             return redirect("/rango/")
#         else:
#             print(form.errors)
#     context_dict = {'form': form}
#     return render(request, "rango/profile_registration.html", context_dict)
