from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet


class Tags(models.Model):
    name = models.CharField(max_length=50)
    objects = models.Manager()


class Profiles(models.Model):
    image = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = models.Manager()


class HotQuestions(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().order_by('-likes_count')


class NewQuestions(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().order_by('-id')


class TagQuestions(models.Manager):
    def get_queryset(self, tag) -> QuerySet:
        return super().get_queryset().filter(tags__exact=tag)


class Questions(models.Model):
    objects = models.Manager()
    hot_questions = HotQuestions()
    new_questions = NewQuestions()
    tag_questions = TagQuestions()
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    likes_count = models.IntegerField(default=0)
    asker = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    answers_count = models.IntegerField(default=0)


class Answers(models.Model):
    text = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    objects = models.Manager()


class QuestionLikes(models.Model):
    action = models.IntegerField(default=0)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE,
                                 related_name='question_likes', blank=True)

    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)


class AnswerLikes(models.Model):
    action = models.IntegerField(default=0)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='answer_likes',
                               blank=True)
    user = models.ForeignKey(Profiles, on_delete=models.CASCADE)


def new_user(user_info):
    user_new = User.objects.create_user(username=user_info['username'], first_name=user_info['first_name'],
                                        email=user_info['email'], password=user_info['password'])
    profile = Profiles(user=user_new)
    profile.save()
    return user_new


def new_question(new_quest, user):
    tags_ = new_quest['tags_'].split(' ')
    user_ = User.objects.get(username=user.username)
    new_quest = Questions(asker=user_, title=new_quest['title'], text=new_quest['text'])
    new_quest.save()
    for tag in tags_:
        try:
            tag_ = Tags.objects.get(name=tag)
        except Tags.DoesNotExist:
            tag_ = Tags(name=tag)
            tag_.save()
        new_quest.tags.add(tag_)
    new_quest.save()
    return new_quest.pk
