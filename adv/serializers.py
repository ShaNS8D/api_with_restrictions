from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from adv.models import Adv


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Adv
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )
        # read_only_fields = ['creator']

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        
        if self.context['request'].method == 'POST':
            if Adv.objects.filter(status='OPEN', creator=self.context["request"].user).count() >= 10:
                raise ValidationError('Лимит 10 открытых объвлений')
        
        if self.context['request'].method == 'PATCH':
            if Adv.objects.filter(status='OPEN', creator=self.context["request"].user).count() >= 10 and data.get('status') == 'OPEN':
                raise ValidationError('У Вас уже есть 10 открытых объвлений')

        return data

