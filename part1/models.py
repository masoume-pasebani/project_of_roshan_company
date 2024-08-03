from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User




class News(models.Model):
    
    choice = [
    ('ECONOMIC', 'Economic'),
    ('SOCIAL', 'Social'),
    ('CULTURAL', 'Cultural'),
    ('SPORTS', 'Sports'),
    ('POLITICAL', 'Political'),
    ('OTHER', 'Other'),
]
    title = models.CharField(max_length = 150)
    text = models.TextField()
    tags = models.CharField(max_length= 150)
    source = models.TextField()
    category = models.CharField(max_length=10, choices=choice, default = 'OTHER'  )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['-id']  
        verbose_name = 'New'
        verbose_name_plural = 'News'

    