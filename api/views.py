from django.shortcuts import redirect

# Create your views here.
def root_redirect(request):
    return redirect('api/v1/')