from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from app.forms import ReadOnlyForm

class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You are not logged in!')
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

class SuperuserPermissionsOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# class ReadOnlyMixin(UserPassesTestMixin):
#     def test_func(self):
#         return not self.request.user.is_superuser  # Пользователи, не являющиеся суперпользователями, могут видеть форму, но не редактировать

class RegularUserReadOnlyFormMixin(FormMixin):
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if not self.request.user.is_superuser:
            for field in form.fields:
                form.fields[field].disabled = True
        return form
        # if not self.request.user.is_superuser:
        #     return ReadOnlyForm
        # else:
        #     return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['read_only'] = True
        return context