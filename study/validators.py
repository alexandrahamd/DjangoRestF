from rest_framework import serializers


class LessonLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value)
        link_video = value.get('link_video')
        print(link_video)
        if not link_video.startswith('https://www.youtube'):
            message = 'Ссылка должна быть только на youtube'
            raise serializers.ValidationError(message)
