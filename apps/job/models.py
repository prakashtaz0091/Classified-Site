from django.db import models

class JobCategory(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('industry', 'Industry'),
        ('popular', 'Popular'),
        ('new', 'New'),
        ('featured', 'Featured'),
        # Add other categories as needed
    ]

    name = models.CharField(max_length=255, unique=True)
    image = models.FileField(upload_to='job_category_images/', blank=True, null=True)
    available_jobs = models.PositiveIntegerField(default=0)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPE_CHOICES, default='industry',blank=True,null=True)

    class Meta:
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'

    def __str__(self):
        return self.name



class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    image=models.FileField(upload_to='job_category_images/',blank=True,null=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    category=models.ForeignKey(JobCategory,on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50, choices=[('full-time', 'Full Time'), ('part-time', 'Part Time'), ('contract', 'Contract')], default='full-time')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-posted_date'] 
        
        
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"
    