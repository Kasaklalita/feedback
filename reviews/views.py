from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from .models import Review
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView
# Create your views here.

# View as a class

class ReviewView(CreateView):
    model = Review
    # fields = '__all__'
    form_class = ReviewForm
    template_name = 'reviews/review.html'
    success_url = '/thank-you'

# class ReviewView(FormView):
#     form_class = ReviewForm
#     template_name = 'reviews/review.html'
#     success_url = '/thank-you'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

    # def get(self, request):
    #     form = ReviewForm()
    #     return render(request, "reviews/review.html", {
    #         "form": form
    #     })

    # def post(self, request):
    #     form = ReviewForm(request.POST) # instance = existing_model - updating the database
    #     if form.is_valid():
    #         form.save() # Saving to the database
    #         return HttpResponseRedirect("/thank-you")
    #     return render(request, "reviews/review.html", {
    #         "form": form
    #     })

# View as a method
# def review(request):
#     if request.method == 'POST':
#         # existing_model = Review.objects.get(pk = 1)
#         form = ReviewForm(request.POST) # instance = existing_model - updating the database
#         if form.is_valid():
#             form.save() # Saving to the database
#             # review = Review(user_name = form.cleaned_data['user_name'],
#             #     review_text = form.cleaned_data['review_text'],
#             #     rating = form.cleaned_data['rating'])
#             # review.save()
#             return HttpResponseRedirect("/thank-you")
#     else:
#         form = ReviewForm()
#
#     return render(request, "reviews/review.html", {
#         "form": form
#     })

class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'This works!'
        return context

class ReviewsListView(ListView):
    template_name = 'reviews/review_list.html'
    model = Review
    context_object_name = 'reviews'

    # def get_queryset(self): # вывод некоторых
    #     base_query = super().get_queryset()
    #     data = base_query.filter(pk = 1)
    #     return data

    def get_context_data(self, **kwargs): # Вывод всех элементов
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        context['reviews'] = reviews
        return context

class SingleReviewView(DetailView):
    template_name = 'reviews/single_review.html'
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_review = self.object
        request = self.request
        favorite_id = request.session.get('favorite_review') # Безопасно
        # favorite_id = request.session['favorite_review']
        context['is_favorite'] = favorite_id == str(loaded_review.id)
        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     review_id = kwargs['id']
    #     selected_review = Review.objects.get(pk = review_id)
    #     context['review'] = selected_review
    #     return context

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("/reviews/" + review_id)
