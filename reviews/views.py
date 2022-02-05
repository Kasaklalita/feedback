from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from .models import Review
from django.views import View
from django.views.generic.base import TemplateView
# Create your views here.

# View as a class
class ReviewView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, "reviews/review.html", {
            "form": form
        })

    def post(self, request):
        form = ReviewForm(request.POST) # instance = existing_model - updating the database
        if form.is_valid():
            form.save() # Saving to the database
            return HttpResponseRedirect("/thank-you")
        return render(request, "reviews/review.html", {
            "form": form
        })

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

class ReviewsListView(TemplateView):
    template_name = 'reviews/review_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.all()
        context['reviews'] = reviews
        return context

class SingleReviewView(TemplateView):
    template_name = 'reviews/single_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_id = kwargs['id']
        selected_review = Review.objects.get(pk = review_id)
        context['review'] = selected_review
        return context
