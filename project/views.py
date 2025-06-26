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
    template_name = 'project/login.html'
    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('profile', kwargs={'pk': profile.pk})
    
class MasterListView(ListView):
    '''view to display all squishmallows'''

    template_name = 'project/squishmallows.html'
    model = Squishmallow
    context_object_name = 'squishmallows'
    paginate_by = 52

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(species__icontains=q)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
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
    model = Profile
    template_name = 'project/collection.html'
    context_object_name = 'profile'

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Profile, pk=pk)
        else:
            return get_object_or_404(Profile, user=self.request.user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        collection = profile.get_collection()

        # Avoid losing attached photos by decorating the list directly
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
        context = super().get_context_data(**kwargs)

        if 'new_user_form' not in context:
            context['new_user_form'] = UserCreationForm()

        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            new_user = user_form.save()
            login(self.request, new_user)

            empty_collection = Collection.objects.create(user=new_user)
            form.instance.user = new_user
            form.instance.collection = empty_collection

            return super().form_valid(form)

        # Pass user_form with errors into context
        return self.render_to_response(
            self.get_context_data(form=form, new_user_form=user_form)
        )


    
class AddSquishView(View):
    '''view to add squish to collection'''
    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def dispatch(self, request, *args, **kwargs):
        squish_id = kwargs.get('squish_id')
        squish = get_object_or_404(Squishmallow, pk=squish_id)
        profile = Profile.objects.get(user=request.user)
        profile.add_squish(squish)
        return redirect('collection', pk=profile.pk)

class CreateListingView(CreateView):
    '''view to handle listing creation'''

    form_class = CreateListingForm
    template_name = 'project/create_listing.html'

    def get_initial(self):
        initial = super().get_initial()
        squish_id = self.request.GET.get('squish_id')
        if squish_id:
            try:
                squish = Squishmallow.objects.get(id=squish_id)
                initial['squishmallow'] = squish
            except Squishmallow.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.owner = profile
        listing = form.save()
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # pass current user to the form
        return kwargs
    
class ConfirmPurchaseView(LoginRequiredMixin, View):
    '''confirm user wants to purchase and then add squish to collection'''

    template_name = 'project/confirm_purchase.html'
    context_object_name = 'listing'

    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        return render(request, self.template_name, {'listing': listing})

    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        profile = Profile.objects.get(user=self.request.user)
        profile.add_squish(listing.squishmallow)  # your method from earlier
        listing.delete()  # Optional: remove listing after purchase
        return redirect('collection', pk=profile.pk)
    
class CreateSquishPhotoView(CreateView):
    '''create a photo for a squish'''

    form_class = CreateSquishPhotoForm
    template_name = 'project/create_photo.html'

    def get_initial(self):
        initial = super().get_initial()
        squish_id = self.request.GET.get('squish_id')
        if squish_id:
            try: 
                squish = Squishmallow.objects.get(id=squish_id)
                initial['squish'] = squish
            except Squishmallow.DoesNotExist:
                pass
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  
        return kwargs
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile

        squish_id = self.request.GET.get('squish_id')
        if squish_id:
            try:
                form.instance.squish = Squishmallow.objects.get(id=squish_id)
            except Squishmallow.DoesNotExist:
                form.add_error('squish', 'Squishmallow not found')
                return self.form_invalid(form)
        photo = form.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        profile = Profile.objects.get(user=self.request.user)
        return reverse('collection', kwargs={'pk':profile.pk})
    
    
class ShowProfileListingsView(DetailView):
    model = Profile
    template_name = 'project/profile_listings.html'
    context_object_name = 'profile'

    def get_object(self, queryset = ...):
        pk = self.kwargs.get('pk')
        if pk:
            return get_object_or_404(Profile, pk=pk)
        else:
            return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        listings = profile.get_listings()


        context['listings'] = listings
        return context
class DeleteProfileView(LoginRequiredMixin, DeleteView):
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
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        '''handle form to update profile'''
        user = self.request.user
        form.instance.user = user

        return super().form_valid(form)