from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import YoutubeLinkValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.URLField(validators=[YoutubeLinkValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_lessons_info(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializer(lessons, many=True).data
