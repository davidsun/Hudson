from django.db import models

class HudsonModel(models.Model) :
    class Meta :
        abstract = True

    def save(self, *args, **kwargs) :
        self.full_clean()
        super(HudsonModel, self).save(*args, **kwargs)
