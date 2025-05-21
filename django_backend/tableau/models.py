from django.db import models


class RatingsChoices(models.IntegerChoices):
    DISLIKE = 0, "dislike"
    LIKE = 1, "like"


RATING_CHOICES = ((0, "dislike"), (1, "like"))


class TestModel(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RatingsModel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255, null=True, blank=True)

    # 0 = dislike, 1 = like
    rating = models.IntegerField(
        default=RatingsChoices.DISLIKE, choices=RatingsChoices.choices
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # INVALIDATE EXISTING RATINGS
        ratings = RatingsModel.objects.filter(user=self.user, item=self.item).exclude(
            id=self.id
        )

        ratings.update(is_active=False)


class ContentMetaDataModel(models.Model):
    """
    Model to store mocked metadata for Tableau items.
    """

    id = models.AutoField(primary_key=True)
    luid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    parent_luid = models.CharField(max_length=255, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    hide_from_users = models.TextField(null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
