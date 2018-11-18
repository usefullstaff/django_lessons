from django.http import HttpResponse,HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic.base import View

from django.contrib.auth.models import User

from first_app.models import Person

from first_app.locator import convert_adres, haversine

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from first_app.forms import LocForm

from first_app import locator
from django.shortcuts import render, get_object_or_404, render_to_response

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

        form =  LocForm(request.POST)

        if form.is_valid():
            if request.POST['coords'] == 'no coords':
                on_ip_loc = locator.vichisly_po_ip('195.222.85.234')
                fex = locator.create_locations_table(on_ip_loc)


            else:

                client_loc = request.POST['coords'].split(',')

                accuracy = float(client_loc[2])
                lat = float(client_loc[0])
                lon = float(client_loc[1])
                fex = locator.create_locations_table({'lat':lat, 'lon':lon})
               



            full_location = '{},{},{},{}'.format(form.cleaned_data['country'], 
                                        form.cleaned_data['city'], 
                                        form.cleaned_data['street'], 
                                        form.cleaned_data['building'])
            
            point_coords = convert_adres(full_location)

            home_coords = '{},{},{},{}'.format(user.person.home_country,
                                                user.person.home_city,
                                                user.person.home_street,
                                                user.person.home_building,)
            
            home = convert_adres(home_coords)


            dlina = haversine(float(home['latitude']), float(home['longitude']), point_coords['latitude'], point_coords['longitude'])
    
            return HttpResponseRedirect("/accounts/{}".format(id))
    else:
        
        
        form = LocForm()
        return render(request, 'accounts/profile.html', { 'form': form})
        pass

