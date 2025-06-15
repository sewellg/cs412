from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import *
from . models import Voter
# Create your views here.

class VoterListView(ListView):
    '''view to display newton voters'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
            
        # start with entire queryset
        voters = super().get_queryset().order_by('last_name')

        # filter voters by these field(s):
        if 'pa' in self.request.GET:
            party_affiliation = self.request.GET['pa']
            if party_affiliation:
                voters = voters.filter(party_affiliation=party_affiliation)
        if 'mindob' in self.request.GET:
            mindob = self.request.GET['mindob']
            if mindob:
                voters = voters.filter(date_of_birth__year__gte=mindob)
        if 'maxdob' in self.request.GET:
            maxdob = self.request.GET['maxdob']
            if maxdob:
                voters = voters.filter(date_of_birth__year__lte=maxdob)
        if 'vs' in self.request.GET:
            vs = self.request.GET['vs']
            if vs:
                voters = voters.filter(voter_score__gte=vs)
        # election participation checkboxes — only filter if checkbox is present in request
        if '20se' in self.request.GET:
            voters = voters.filter(v20state=True)
        if '21te' in self.request.GET:
            voters = voters.filter(v21town=True)
        if '21pe' in self.request.GET:
            voters = voters.filter(v21primary=True)
        if '22ge' in self.request.GET:
            voters = voters.filter(v22general=True)
        if '23te' in self.request.GET:
            voters = voters.filter(v23town=True)
        return voters
    
class VoterDetailView(DetailView):
    '''view to display a single voter'''

    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'

