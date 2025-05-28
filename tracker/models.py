from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    BODY_TYPE_CHOICES = [
        ('thin', 'Thin'),
        ('medium', 'Medium'),
        ('fat', 'Fat'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField(null=True, blank=True)
    body_type = models.CharField(max_length=10, choices=BODY_TYPE_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def calculate_bmi(self):
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)

    def assign_body_type(self):
        self.bmi = self.calculate_bmi()
        if self.bmi < 18.5:
            self.body_type = 'thin'
        elif 18.5 <= self.bmi < 25:
            self.body_type = 'medium'
        else:
            self.body_type = 'fat'

    @classmethod
    def find_profile(cls, user):
        """Utility method to find a profile across all databases"""
        for db in ['default', 'thin', 'medium', 'fat']:
            try:
                return cls.objects.using(db).get(user=user)
            except cls.DoesNotExist:
                continue
        return None

    def save(self, *args, **kwargs):
        # Calculate BMI and body type
        self.assign_body_type()
        
        # Determine target database
        using_db = {
            'thin': 'thin',
            'medium': 'medium', 
            'fat': 'fat'
        }.get(self.body_type, 'default')
        
        # Save ONLY to the target database
        kwargs['using'] = using_db
        super().save(*args, **kwargs)
        
        # Don't try to save to default DB - let the router handle reads