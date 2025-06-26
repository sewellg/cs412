from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from .models import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models.query import QuerySet
from .forms import *
from django.db.models import Q


# Create your views here.
class HomepageView(TemplateView):
    '''view to display home page'''
    template_name = 'project/welcome.html'

class ShowProfileView(DetailView):
    '''view class to show a singular profile'''

    model = Profile
    template_name = 'project/profile.html'
    context_object_name = 'profile'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        '''returns specified object, in this case: current user'''
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Profile, pk=pk)
        else:
            return get_object_or_404(Profile, user=self.request.user)
        
    def get_context_data(self, **kwargs):
        '''adds context data and ensures user has correct badges'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        profile.check_badges()

        return context
        
class ShowAllProfilesView(ListView):
    '''class to show all profiles'''
    model = Profile
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles'        
    
class CustomLoginView(LoginView):
    '''view for logging in'''
    template_name = 'project/login.html'
    def get_success_url(self):
        '''when successfully logged in, bring to their profile'''
        profile = Profile.objects.get(user=self.request.user)
        return reverse('profile', kwargs={'pk': profile.pk})
    
class MasterListView(ListView):
    '''view to display all squishmallows'''

    template_name = 'project/squishmallows.html'
    model = Squishmallow
    context_object_name = 'squishmallows'
    paginate_by = 52

    def get_queryset(self):
        '''defines a queryset, allowing users to search for squishmallows by name or species'''
        queryset = super().get_queryset()
        q = self.request.GET.get('q') # if there is a search being done
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(species__icontains=q) # search for the search value in either the name or species
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        '''adds the context data for the masterlist'''
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context
    
class ListingsView(ListView):
    '''view to display all listings'''

    template_name = 'project/listings.html'
    model = Listing
    context_object_name = 'listings'
    paginate_by = 25

class ShowListingView(DetailView):
    '''show one listing'''

    model = Listing
    template_name = 'project/show_listing.html'
    context_object_name = 'listing'

class CollectionView(DetailView):
    '''show a profile's collection'''
    model = Profile
    template_name = 'project/collection.html'
    context_object_name = 'profile'

    def get_object(self):
        '''get the specific profile whose collection is being viewed'''
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Profile, pk=pk) # returns 404 if no profile found
        else:
            return get_object_or_404(Profile, user=self.request.user)
        
    def get_context_data(self, **kwargs):
        '''adds context data for collections'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        collection = profile.get_collection()

        # avoid losing attached photos by decorating the list of squishmallows directly with the photos
        squish_list = list(collection.squishmallows.all())
        for squish in squish_list:
            squish.photos = SquishPhoto.objects.filter(squish=squish, profile=profile)

        context['squishmallows'] = squish_list
        return context
        
    

class CreateProfileView(CreateView):
    '''view to handle creation of new profile'''

    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'

    def get_context_data(self, **kwargs):
        '''gets context data for creating a profile'''
        context = super().get_context_data(**kwargs)

        if 'new_user_form' not in context:
            context['new_user_form'] = UserCreationForm() # if a new user form doesn't exist, make one

        return context

    def form_valid(self, form):
        '''checking to see if the form is valid'''
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            new_user = user_form.save() 
            login(self.request, new_user) # if valid, login the new user

            empty_collection = Collection.objects.create(user=new_user) # initialize an empty collection for them
            form.instance.user = new_user
            form.instance.collection = empty_collection

            return super().form_valid(form)

        # pass user_form with errors into context
        return self.render_to_response(
            self.get_context_data(form=form, new_user_form=user_form)
        )


    
class AddSquishView(View):
    '''view to add squish to collection'''
    def get_object(self):
        '''get current user'''
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def dispatch(self, request, *args, **kwargs):
        '''takes in a request and returns a response'''
        squish_id = kwargs.get('squish_id')
        squish = get_object_or_404(Squishmallow, pk=squish_id) # get requested squish
        profile = Profile.objects.get(user=request.user) # get user's profile
        profile.add_squish(squish) # adds the requested squishmallow into user's profile
        return redirect('collection', pk=profile.pk) # redirect them to their collection

class CreateListingView(CreateView):
    '''view to handle listing creation'''

    form_class = CreateListingForm
    template_name = 'project/create_listing.html'

    def get_initial(self):
        '''if the user clicked "add a listing" from a specific squish, set that squish as the desired listing squish'''
        initial = super().get_initial()
        squish_id = self.request.GET.get('squish_id') # get squish the user clicked from
        if squish_id:
            try:
                squish = Squishmallow.objects.get(id=squish_id)
                initial['squishmallow'] = squish # initialize the squishmallow field in listing to be the desired squish
            except Squishmallow.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        '''determines if form is valid'''
        profile = Profile.objects.get(user=self.request.user) # get the current user
        form.instance.owner = profile # set the owner of the new listing to be current user
        listing = form.save()
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        '''retrieves kwargs to pass to the form'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass current user to the form
        return kwargs
    
class ConfirmPurchaseView(LoginRequiredMixin, View):
    '''confirm user wants to purchase and then add squish to collection'''

    template_name = 'project/confirm_purchase.html'
    context_object_name = 'listing'

    def get(self, request, pk):
        '''retrieve info on which squish was clicked'''
        listing = get_object_or_404(Listing, pk=pk)
        return render(request, self.template_name, {'listing': listing})

    def post(self, request, pk):
        '''add this squish to user's collection'''
        listing = get_object_or_404(Listing, pk=pk)
        profile = Profile.objects.get(user=self.request.user)
        profile.add_squish(listing.squishmallow)  # add squish to collection
        listing.delete()  # remove listing after purchase
        return redirect('collection', pk=profile.pk) # redirect to collection
    
class CreateSquishPhotoView(CreateView):
    '''create a photo for a squish'''

    form_class = CreateSquishPhotoForm
    template_name = 'project/create_photo.html'

    def get_initial(self):
        '''initialize the squish field in squishphoto to the squish the user clicked on'''
        initial = super().get_initial()
        squish_id = self.request.GET.get('squish_id') # get requested squish
        if squish_id:
            try: 
                squish = Squishmallow.objects.get(id=squish_id)
                initial['squish'] = squish # initialize field to requested squish
            except Squishmallow.DoesNotExist:
                pass
        return initial
    
    def get_form_kwargs(self):
        '''get kwargs from request and pass to form'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        '''ensure form is valid'''
        profile = Profile.objects.get(user=self.request.user) # get current user's profile and set it as the squishphoto's profile
        form.instance.profile = profile

        squish_id = self.request.GET.get('squish_id') # obtain id of current requested squish
        if squish_id:
            try:
                form.instance.squish = Squishmallow.objects.get(id=squish_id) # set the squish field in the squishphoto model to requested squish
            except Squishmallow.DoesNotExist:
                form.add_error('squish', 'Squishmallow not found') # error message if squish not found
                return self.form_invalid(form)
        photo = form.save() # save the photo

        return super().form_valid(form)
    
    def get_success_url(self):
        '''reroute to the user's collection upon successful addition of a squishmallow photo'''
        profile = Profile.objects.get(user=self.request.user)
        return reverse('collection', kwargs={'pk':profile.pk})
    
    
class ShowProfileListingsView(DetailView):
    '''show a profile's listings'''
    model = Profile
    template_name = 'project/profile_listings.html'
    context_object_name = 'profile'

    def get_object(self, queryset = ...):
        '''find a given profile'''
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Profile, pk=pk)
        else:
            return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        '''add context data for view'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        listings = profile.get_listings() # retrieve only the listings from a given profile

        context['listings'] = listings
        return context
    
class DeleteProfileView(LoginRequiredMixin, DeleteView):
    '''delete a profile'''
    model = Profile
    template_name = 'project/delete_profile.html'
    context_object_name = 'profile'

    def get_success_url(self):
        '''directs user to url upon submitting'''
        pk = self.kwargs['pk']
        return reverse('login')
    
    def form_valid(self, form):
        '''handle form submission to delete profile'''
        user = self.request.user
        return super().form_valid(form)
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''updates logged in profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile.html'

    def get_object(self):
        '''gets logged in profile'''
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        '''handle form to update profile'''
        user = self.request.user
        form.instance.user = user

        return super().form_valid(form)