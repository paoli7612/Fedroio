from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Pawn(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=512, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='childs')
    slug = models.SlugField(max_length=512, unique=True, blank=True)
    image = models.ImageField(upload_to='pawn_images/', null=True, blank=True)  # Add this line
    number = models.PositiveIntegerField(null=True, blank=True)
    hide = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def url(self):
        return reverse('pawn', kwargs={'slug': self.slug})
    
    def parent_url(self):
        if self.parent:
            return self.parent.url()
        else:
            return reverse('pawns')
        
    def breadcrumb(self):
        if self.parent:
            return self.parent.breadcrumb() + [self]
        else:
            return [self]
        
    def all_questions(self):
        questions = list(self.questions.all())
        for child in self.childs.all():
            questions_child = child.all_questions()
            if questions_child:
                questions += questions_child
        return questions