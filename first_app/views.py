from django.http import HttpResponse,HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic.base import View

from django.contrib.auth.models import User

from first_app.models import Person

from first_app.locator import convert_adres, haversine, coord_to_adr

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from first_app.forms import LocForm

from first_app import locator
from django.shortcuts import render, get_object_or_404, render_to_response



import re




class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
        pass


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)
        pass


class UserRegistrationForm(FormView):
    form_class = UserCreationForm
    template_name = "accounts/registration.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
#        login(self.request, self.user)
        return super(UserRegistrationForm, self).form_valid(form)
        pass



method_decorator(login_required)
def UserProfile(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':

        if request.POST['coords'] == 'no coords':
            on_ip_loc = locator.vichisly_po_ip('195.222.85.234')
            fex = locator.create_locations_table(on_ip_loc)
            return HttpResponseRedirect("/accounts/{}".format(id))
            pass


        else:

            client_loc = request.POST['coords'].split(',')

            accuracy = float(client_loc[2])
            lat = float(client_loc[0])
            lon = float(client_loc[1])
            places = locator.create_locations_table({'lat':lat, 'lon':lon}, 0.01)



            list_of_addr = [coord_to_adr(re.findall(r'[\d\.\d]+',place[1])[1:]) for place in places]

            return render(request, 'accounts/profile.html',{'places':list_of_addr})
            pass
    else:
        

        return render(request, 'accounts/profile.html')
        pass
