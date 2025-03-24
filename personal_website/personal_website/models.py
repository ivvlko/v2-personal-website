from django.db import models
from .utils import process_youtube_link


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    images = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True)

    def __str__(self):
        return self.title


class PortfolioItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    video = models.FileField(upload_to='portfolio_videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=[("programming", "Programming"),
                                                        ("stocks", "Stocks"),
                                                        ("workouts", "Workouts"),
                                                        ("history", "History"),
                                                        ("politics", "Politics"), ])

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.video_url:
            self.video_url = process_youtube_link(self.video_url)
        super().save(*args, **kwargs)


class ProgrammingItem(PortfolioItem):
    repo_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)


class CodeSnippet(models.Model):
    programming_item = models.ForeignKey(ProgrammingItem, on_delete=models.CASCADE, related_name="snippets")
    language = models.CharField(max_length=50000, choices=[("python", "Python"),
                                                           ("javascript", "JavaScript"),
                                                           ("jupyter", "Jupyter")])
    code = models.TextField()
    description = models.TextField(blank=True, null=True)


class StockItem(PortfolioItem):
    external_link = models.URLField()


class HistoryItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)


class WorkoutItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)


class PoliticsItem(PortfolioItem):
    text_content = models.TextField(blank=True, null=True)

