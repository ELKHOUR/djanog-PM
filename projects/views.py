
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from . import models
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = models.Project
    template_name = 'project/list.html'
    paginate_by = 6

    def get_queryset(self):
        
        query_set = super().get_queryset()
        where = {'user_id': self.request.user}
        q = self.request.GET.get('q', None)
        if q :
            where['title__icontains'] = q # type: ignore
        return query_set.filter(**where)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'project/create.html'
    success_url = reverse_lazy('Project_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectUpdateForm
    template_name = 'project/update.html'
    success_url = reverse_lazy('Project_list')

    def test_func(self):
        return super().get_object().user_id == self.request.user.id  # type: ignore

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.id]) # type: ignore
    


class ProjectDeleteView(LoginRequiredMixin, DeleteView , UserPassesTestMixin):
    model = models.Project
    template_name = 'project/delete.html'
    success_url = reverse_lazy('Project_list')

    def test_func(self):
        return super().get_object().user_id == self.request.user.id   # type: ignore


class TaskCreateView(LoginRequiredMixin, CreateView, UserPassesTestMixin):
    model = models.Task
    fields = ['project', 'description']
    http_method_names = ['post']


    def test_func(self):
        project_id = self.request.POST.get('project', '')
        return models.Project.objects.get(pk=project_id).user_id == self.request.user.id

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id]) # type: ignore





class TaskUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = models.Task
    fields = ['is_completed']
    http_method_names = ['post']

    def test_func(self):
        return super().get_object().project.user_id == self.request.user.id   # type: ignore

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id]) # type: ignore



class TaskDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = models.Task

    def test_func(self):
        return super().get_object().project.user_id == self.request.user.id   # type: ignore

    def get_success_url(self):
        return reverse('Project_update', args=[self.object.project.id]) # type: ignore