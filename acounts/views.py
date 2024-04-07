from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import CreateView
from acounts.forms import UserRegisterForm, ProfileForm

# Create your views here.


class LogoutViewWithGet(LogoutView):

    http_method_names = LogoutView.http_method_names + ['get']

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
    

class RegisterView(CreateView):
    form_class = UserRegisterForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request, self.object) # type: ignore
        return reverse_lazy('Project_list')

@login_required # type: ignore
def edit_profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    else:
        form = ProfileForm(instance = request.user)
        return render(request, 'profile.html', {
            'form':form
        })