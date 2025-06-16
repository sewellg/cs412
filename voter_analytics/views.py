from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import *
from . models import Voter

import math
import plotly
import plotly.graph_objs as go
from collections import Counter
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        voter = context['voter']

        unaff = len(Voter.objects.filter(party_affiliation = 'U '))

        print(f'unaffiliated={unaff}')


        return context
    
class VoterGraphView(ListView):
    '''shows graphs about voter data'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'graph'

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

    def get_context_data(self, **kwargs):
        '''provide context variables for template'''
        context = super().get_context_data(**kwargs)

        voters = self.get_queryset()

        # create pie chart of party affiliations
        unaff = len(voters.filter(party_affiliation = 'U '))
        dem = len(voters.filter(party_affiliation = 'D '))
        rep = len(voters.filter(party_affiliation='R '))

        # plotly graph object
        x1 = ['Unaffiliated', 'Democratic', 'Republican']
        y1 = [unaff, dem, rep]

        # generate pie chart
        fig1 = go.Pie(labels = x1, values = y1)
        title_text1 = 'Voters by Party Affiliation'

        # graph as html div
        graph1_div_splits = plotly.offline.plot({"data": [fig1],
                                                "layout_title_text": title_text1},
                                                auto_open=False,
                                                output_type="div")

        # create bar chart of voters by age
        years = []
        
        for voter in voters:
            years.append(voter.date_of_birth.year)

        year_counts = Counter(years) # count the number of times each year appears

        sorted_year_counts = dict(sorted(year_counts.items())) #sort into a dict for plotting

        x2 = list(sorted_year_counts.keys())
        y2 = list(sorted_year_counts.values())


        # generate bar chart
        fig2 = go.Bar(x=x2, y=y2)
        title_text2 = 'Voters by Year of Birth'

        # graph as html div
        graph2_div_splits = plotly.offline.plot({"data": [fig2],
                                                "layout_title_text": title_text2},
                                                auto_open=False,
                                                output_type="div")
        
        # create bar chart of voters by age
        
        v20state = 0
        v21town = 0
        v21primary = 0
        v22general = 0
        v23town = 0

        for voter in voters:
            if voter.v20state == True:
                v20state += 1
            if voter.v21town == True:
                v21town += 1
            if voter.v21primary == True:
                v21primary += 1
            if voter.v22general == True:
                v22general += 1
            if voter.v23town == True:
                v23town += 1



        x3 = ["'20 State", "'21 Town", "'21 Primary", "'22 General", "'23 Town"]
        y3 = [v20state, v21town, v21primary, v22general, v23town]


        # generate bar chart
        fig3 = go.Bar(x=x3, y=y3)
        title_text3 = 'Voters by Election'

        # graph as html div
        graph3_div_splits = plotly.offline.plot({"data": [fig3],
                                                "layout_title_text": title_text3},
                                                auto_open=False,
                                                output_type="div")
        
        context['graph1_div_splits'] = graph1_div_splits
        context['graph2_div_splits'] = graph2_div_splits
        context['graph3_div_splits'] = graph3_div_splits


        return context