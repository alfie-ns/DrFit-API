from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from response.response_handlers.get_initial_plan import get_initial_plan


class UserProfile(models.Model):
    # Choices
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    GOAL_CHOICES = [
        ('bulk', 'Bulk'),
        ('lose_weight', 'Lose weight'),
        ('healthy_happiness', 'Healthy happiness'),
        ('improve_posture', 'Improve posture'),
        ('stress_reduction', 'Stress reduction'),
        ('improve_flexibility', 'Improve flexibility'),
        ('improve_endurance', 'Improve endurance'),
        ('six_pack', 'Six Pack'),
    ]

    DETERMINATION_LEVEL_CHOICES = [
        ('casual', 'Casual'),
        ('determined', 'Determined'),
        ('very_determined', 'Very Determined'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise, desk job)'),
        ('lightly_active', 'Lightly Active (light exercise/sports 1-3 days/wk)'),
        ('moderately_active', 'Moderately Active (moderate exercise/sports 6-7 days/wk)'),
        ('very_active', 'Very Active (hard exercise every day, or 2x/day)'),
        ('extra_active', 'Extra Active (hard exercise 2+ hrs/day, training for marathon, triathlon, etc.)'),
    ]

    BMR_TYPE_CHOICES = [
        ('mifflin_st_jeor', 'Mifflin-St Jeor'),
        ('harris_benedict', 'Harris-Benedict'),
        ('katch_mcardle', 'Katch-McArdle'),
    ]
    

    # Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=6, choices = GENDER_CHOICES, null=False, blank=False)
    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    goal = models.CharField(max_length=20, choices = GOAL_CHOICES, null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices = ACTIVITY_LEVEL_CHOICES, null=True, blank=True)
    determination_level = models.CharField(max_length=20, choices = DETERMINATION_LEVEL_CHOICES, null=True, blank=True)
    bmr_type = models.CharField(max_length=20, choices = BMR_TYPE_CHOICES, null=True, blank=True)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    initial_plan = models.JSONField(null=True, blank=True)

    # Methods
    def __str__(self):
        return self.user.username
    
    def clean(self):
        # Validate choices
        if self.gender not in dict(UserProfile.GENDER_CHOICES):
            raise ValidationError({
                "gender": "Invalid choice. Valid options are: " + ', '.join([f"{t[0]} ({t[1]})" for t in UserProfile.GENDER_CHOICES])
            })
        elif self.goal not in dict(UserProfile.GOAL_CHOICES):
            raise ValidationError({
                "goal": "Invalid choice. Valid options are: " + ', '.join([f"{t[0]} ({t[1]})" for t in UserProfile.GOAL_CHOICES])
            })
        elif self.activity_level not in dict(UserProfile.ACTIVITY_LEVEL_CHOICES):
            raise ValidationError({
                "activity_level": "Invalid choice. Valid options are: " + ', '.join([f"{t[0]} ({t[1]})" for t in UserProfile.ACTIVITY_LEVEL_CHOICES])
            })
        elif self.determination_level not in dict(UserProfile.DETERMINATION_LEVEL_CHOICES):
            raise ValidationError({
                "determination_level": "Invalid choice. Valid options are: " + ', '.join([f"{t[0]} ({t[1]})" for t in UserProfile.DETERMINATION_LEVEL_CHOICES])
            })
        elif self.bmr_type not in dict(UserProfile.BMR_TYPE_CHOICES):
            raise ValidationError({
                "bmr_type": "Invalid choice. Valid options are: " + ', '.join([f"{t[0]} ({t[1]})" for t in UserProfile.BMR_TYPE_CHOICES])
            })
        elif self.age is not None and self.age < 0:
            raise ValidationError({
                "age": "Age cannot be negative."
            })
        elif self.weight is not None and self.weight < 0:
            raise ValidationError({
                "weight": "Weight cannot be negative."
            })
        elif self.height is not None and self.height < 0:
            raise ValidationError({
                "height": "Height cannot be negative."
            })

# Send welcome email on user create function  
@receiver(post_save, sender=UserProfile)
def send_welcome_email_on_user_create(sender, instance, created, **kwargs):
    print("ENTERED SEND_WELCOME_EMAIL FUNCTION")
    if created:
        user = User.objects.get(username=instance)
        user_profile = UserProfile.objects.get(user=user)
        # Send welcome email
        send_mail(
        'Welcome to drFit!',  # subject
        f"""Hi {user_profile.name},\n\n Welcome to drFit! We are excited to have you onboard.""",  # message
        'alfiemnurse@example.com',  # from
        [instance.user.email],  # recipient list
        fail_silently=False
    )
        
# Put initial plan function here?  
@receiver(post_save, sender=UserProfile)
def send_initialplan_on_user_create(sender, instance, created, **kwargs):
    if created:
        initial_plan = get_initial_plan(instance) # Get initial plan

        instance.initial_plan = initial_plan # Set initial plan
        instance.save() # Save initial plan
        
        # Send initial plan
        send_mail(
            'Your initial plan',  # subject
            f'Hi {instance.user.username},\n\n Here is your initial plan: {initial_plan}',  # message
            'alfiemnurse@gmail.com',  # from email
            [instance.user.email],  # recipient list
        )