
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

# Create your views here.
def review(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews':reviews,
    }
    return render(request, 'reviews/review.html', context)

def review_create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.save()
        return redirect('reviews:review')
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form,
    }
    return render(request, 'reviews/review_create.html',context)