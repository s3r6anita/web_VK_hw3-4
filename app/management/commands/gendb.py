from django.core.management.base import BaseCommand
from app.models import *
from faker import Faker
import random


class Command(BaseCommand):
    help = 'it is a command to generate data'
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='it is a start number of records')

    def handle(self, **options):

        ratio = options['ratio']
        # self.create_users(ratio)
        # print('users done')
        # self.create_questions(ratio)
        # print('questions done')
        # self.create_answers(ratio)
        # print('answers done')
        # self.create_tags(ratio)
        # print('tags done')
        # self.create_likes(ratio)
        # print('likes done')
        self.create_questions_tags(ratio)
        print('tags to question done')

    def create_users(self, ratio):
        usernames = []
        while len(usernames) <= ratio:
            new_usernames = [self.fake.user_name() for _ in range(ratio)]
            usernames += new_usernames
            usernames = list(set(usernames))
        users = [User(password=self.fake.password(), username=usernames[i], email=self.fake.email()) for i in
                 range(ratio)]
        for user in users:
            user.save()

        profile = [Profiles(user=users[i]) for i in range(len(users))]
        Profiles.objects.bulk_create(profile)

    def create_questions(self, ratio):
        ask_ratio = ratio - 1
        ratio = ratio * 10
        users = User.objects.all()
        print('number of users generated:')
        print(len(users))
        question = [Questions(asker=users[self.fake.random_int(min=1, max=ask_ratio)],
                              title=self.fake.sentence(nb_words=4),
                              text=self.fake.text()) for _ in range(ratio)]
        Questions.objects.bulk_create(question)

    def create_answers(self, ratio):
        questions = Questions.objects.all()
        users = User.objects.all()
        print('num questions:')
        print(len(questions))
        question_with_id = {}
        for question in questions:
            question_with_id[question.id] = question

        users_ratio = len(users) - 1
        ratio = ratio * 100
        answers = [
            Answers(text=self.fake.text(), question=questions[self.fake.random_int(min=1, max=len(questions) - 1)],
                    user=users[self.fake.random_int(min=1, max=users_ratio)], is_correct=self.fake.pybool())
            for _ in range(ratio)]
        print('answers generated')
        Answers.objects.bulk_create(answers)
        print('answers inserted')
        answers = Answers.objects.all()
        for answer in answers:
            question_with_id[answer.question.id].answers_count += 1
            question_with_id[answer.question.id].save()

    def create_tags(self, ratio):
        words = []
        while len(words) < ratio:
            new_words = [self.fake.word() for _ in range(ratio)]
            words += new_words
            new_words = [self.fake.first_name() for _ in range(ratio)]
            words += new_words
            new_words = [self.fake.last_name() for _ in range(ratio)]
            words += new_words
            words = list(set(words))
            print(len(words))

        tag = [Tags(name=words[i]) for i in range(ratio)]
        Tags.objects.bulk_create(tag)

    def create_likes(self, ratio):
        users = Profiles.objects.all()
        questions_ = Questions.objects.all()
        answers_ = Answers.objects.all()
        question_ratio = len(questions_) - 1
        like_ratio = ratio * 200
        answer_ratio = len(answers_) - 1
        question_dict = {}
        for question in questions_:
            question_dict[question.id] = question

        answer_dict = {}
        for answer in answers_:
            answer_dict[answer.id] = answer

        for i in range(len(questions_)):
            questions_[i].likes_ratio = 0
        print('question likes zero')

        for i in range(len(answers_)):
            answers_[i].likes_ratio = 0
        print('answer likes zero')
        # поменять цмфру
        for i in range(500):
            like = [
                QuestionLikes(action=random.randint(-1, 1),
                              question=questions_[random.randint(1, question_ratio)],
                              user=users[random.randint(1, ratio - 1)]) for _ in range(like_ratio // 1002)]
            QuestionLikes.objects.bulk_create(like)
            print(f'done {i} likes for questions')
            for likee in like:
                question = question_dict[likee.question.id]
                question.likes_count += likee.action
                question.save()
            like.clear()
        for i in range(500, 1000):
            like = [AnswerLikes(action=random.randint(-1, 1), user=users[random.randint(1, ratio - 1)],
                                answer=answers_[random.randint(1, answer_ratio)]) for _ in range(like_ratio // 1002)]
            AnswerLikes.objects.bulk_create(like)
            print(f'done {i} likes for answers')
            for likee in like:
                answer = answer_dict[likee.answer.id]
                answer.likes_count += likee.action
                answer.save()

    def create_questions_tags(self, ratio):
        questions_ = Questions.objects.all()
        tags_ = Tags.objects.all()
        for question in questions_:
            for i in range(random.randint(0, 3)):
                question.tags.add(tags_[random.randint(1, ratio - 1)])
            question.save()
