"""Test view for the `django-user-tags` app."""
from django.core.urlresolvers import reverse
from django.views.generic import FormView

from user_tags.tests.test_app.forms import DummyModelForm


class TestView(FormView):
    template_name = 'test_app/test_view.html'
    form_class = DummyModelForm

    def form_valid(self, form):
        form.save()
        return super(TestView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user_tags_test_view')
