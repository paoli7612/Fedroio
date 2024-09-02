from django.contrib import admin
from .models import Pawn, Sentence, Question

# Register your models here.
admin.site.register(Pawn)
admin.site.register(Sentence)
admin.site.register(Question)