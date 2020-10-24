from django.db import models
from django.conf import settings


class Report(models.Model):
    '''User generated reports containing posts that match a rule'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField('report title', max_length=70)
    rule = models.CharField('the rule by which records are selected',
                            max_length=100)
    created_at = models.DateTimeField('creation date', auto_now_add=True)
    start_date = models.DateField('period start date', blank=True, null=True)
    end_date = models.DateField('period end date', blank=True, null=True)
    is_completed = models.BooleanField('completeness of creating report',
                                       default=False)

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    '''
    If tags are created for the report
    then at least one tag must be in the post
    '''
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name='tags')
    name = models.CharField('tag name', max_length=30)

    def __str__(self):
        return f'{self.name}'


class Source(models.Model):
    '''Name of the post's source'''
    name = models.CharField('source name', max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'sources'


class Post(models.Model):
    '''Post satisfying the report rule'''
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name='posts')
    post_id = models.CharField('post id in source', max_length=150)
    author_id = models.CharField('author id in source', max_length=150)
    url = models.URLField('post url in source')
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    text = models.TextField('post text', db_index=True)
    likes = models.PositiveIntegerField('post likes count')
    comments = models.PositiveIntegerField('post comments count')
    reposts = models.PositiveIntegerField('post reposts count')
    views = models.PositiveIntegerField('post views count')
    pub_date = models.DateTimeField('post publication date')

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return f'{self.text[:30]}'


class PostImage(models.Model):
    '''Attached image of post'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='images')
    url = models.URLField('url of attached image')

    class Meta:
        db_table = 'post_images'


class CategoryAbstract(models.Model):
    '''Absctract class for category of posts'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.post.text[:30]}'


class Favorite(CategoryAbstract):
    '''Favorite posts in report'''

    class Meta:
        db_table = 'favorites'


class Archive(CategoryAbstract):
    '''Archive posts in report'''

    class Meta:
        db_table = 'archive'
        verbose_name_plural = 'archive'


class Spam(CategoryAbstract):
    '''Spam posts in report'''

    class Meta:
        db_table = 'spam'
        verbose_name_plural = 'spam'
