from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def validate_stroke(value):
    stroke_names = ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']
    if value not in stroke_names:
        raise ValidationError(f"{value} is not a valid stroke")

def validate_distance(value):
    if value < 50:
        raise ValidationError(f"Ensure this value is greater than or equal to 50.")
        
def validate_record_date(value):
    if value > timezone.now():
        raise ValidationError("Can't set record in the future.")

class SwimRecord(models.Model):
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    team_name = models.CharField(max_length=50,null=False)
    relay = models.BooleanField(null=False)
    stroke = models.CharField(max_length=50, null=False, validators=[validate_stroke])
    distance = models.IntegerField(validators=[validate_distance])
    record_date = models.DateTimeField(validators=[validate_record_date])
    record_broken_date = models.DateTimeField()

    def clean(self):
        super().clean()
        if (self.record_broken_date is not None) and (self.record_broken_date < self.record_date):
            raise ValidationError({'record_broken_date': "Can't break record before record was set."})

