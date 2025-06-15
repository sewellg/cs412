from django.db import models

# Create your models here.
class Voter(models.Model):
    '''store data from a single voter in newton'''

    first_name = models.TextField()
    last_name = models.TextField()
    residential_address_street_number = models.IntegerField()
    residential_address_street_name = models.TextField()
    residential_address_apartment_number = models.TextField()
    residential_address_zip_code = models.IntegerField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField()
    precint_number = models.IntegerField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()
    filename = '/Users/gsewe/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:

        fields = line.split(',')
        # show which value in each field
        try:
                voter = Voter(
                        first_name=fields[2],
                        last_name=fields[1],
                        residential_address_street_number=int(fields[3] or 0),
                        residential_address_street_name=fields[4],
                        residential_address_apartment_number=(fields[5] or 0),
                        residential_address_zip_code=int(fields[6] or 0),
                        date_of_birth=fields[7],
                        date_of_registration=fields[8],
                        party_affiliation=fields[9],
                        precint_number=int(fields[10] or 0),
                        v20state=fields[11].lower() == 'true',
                        v21town=fields[12].lower() == 'true',
                        v21primary=fields[13].lower() == 'true',
                        v22general=fields[14].lower() == 'true',
                        v23town=fields[15].lower() == 'true',
                        voter_score=int(fields[16] or 0)
                        )
                voter.save()
                print(f'Created voter: {voter}')
        except:
                print(f'skipped:{fields}')
    print(f'Done. Created {len(Voter.objects.all())} Voters.')