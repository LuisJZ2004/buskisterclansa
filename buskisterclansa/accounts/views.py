from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import View

# This app
from .forms import CustomUserCreationForm

class SingInView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home_path")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="accounts:login_path")
        else:
            print(dict(form.errors))
            return render(
                request=request,
                template_name="accounts/sign_in.html",
                context={
                    'form': form,
                    'errors': dict(form.errors),
                }
            )
            
    def get(self, request):
        return render(
            request=request,
            template_name="accounts/sign_in.html",
            context= {
                'form': CustomUserCreationForm()
            }
        )

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        # In the default LoginView it doesn't return the errors if any, so I send them if the form is not valid
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))
