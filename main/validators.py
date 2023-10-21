from rest_framework import serializers

class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is not None and not tmp_val.startswith('https://youtube.com'):
            raise serializers.ValidationError("The URL must be 'https://www.youtube.com/'")

