from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
# Create your views here.

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect("/thank-you")
        # entered_username = request.POST['username']
        # if entered_username == "" and len(entered_username) >= 100:
        #     return render(request, "reviews/review.html", {
        #         "has_error": True
        #     })

    form = ReviewForm()

    return render(request, "reviews/review.html", {
        "form": form
    })

def thank_you(request):
    return render(request, "reviews/thank_you.html")
