from datetime import datetime
from rest_framework import serializers
from main import models


class PollSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    description = serializers.CharField()

    def create(self, validated_data):
        instance = models.Poll(**validated_data)
        try:
            instance.save()
        except Exception as e:
            return e
        return 0

    def update(self, instance, validated_data):
        validated_datetime = datetime.fromisoformat(validated_data.get('start_date'))
        # костыль, но исключает проблемы с разными
        # isoformat, и сверяет по разному (проблема с Z и +00.00)
        if instance.start_date.date() != validated_datetime.date() or \
                instance.start_date.time() != validated_datetime.time():
            return 'start_date cannot be changed'
        instance.name = validated_data.get('name')
        instance.end_date = validated_data.get('end_date')
        instance.description = validated_data.get('description')
        try:
            instance.save()
        except Exception as e:
            return e
        return 0


class QuestionSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=15)
    question = serializers.CharField()
    answers = serializers.JSONField()  # []

    def create(self, validated_data):
        poll = models.Poll.objects.all().get(name=validated_data.pop('poll_name'))
        instance = models.Question(poll=poll, **validated_data)
        try:
            instance.save()
        except Exception as e:
            return e
        return 0

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type')
        instance.question = validated_data.get('question')
        instance.answers = validated_data.get('answers')
        try:
            instance.save()
        except Exception as e:
            return e
        return 0


class CUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    competed_polls = serializers.JSONField()  # { poll_id : { question: [answers] } }

    def create(self, validated_data):
        instance = models.CUser(**validated_data)
        try:
            instance.save()
        except Exception as e:
            return e
        return 0

    def update(self, instance, validated_data):
        instance.competed_polls = validated_data.get('competed_polls')
        try:
            instance.save()
        except Exception as e:
            return e
        return 0
