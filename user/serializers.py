from rest_framework import serializers
from user.models import User, UserType, Hobby, HobbyUser

from django.contrib.auth.hashers import make_password

class HobbySerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, obj):
        # user list excluding currently logged-in user
        users = list(obj.users.all())[1:]
        return [user.fullname for user in users]

    class Meta:
        model = Hobby
        fields = ("name", "users")

class UserSerializer(serializers.ModelSerializer):
    hobbies = HobbySerializer(source="hobby_set", read_only=True, many=True)

    def validate(self, data):
        # http_method = self.context.get("request").method
        # if http_method == "POST":
        # validate email type
        if not data.get("email").endswith("@gmail.com"):
            raise serializers.ValidationError(
                detail={"error": "You must register with a google account."}
            )

        # validate user type
        try:
            user_type = self.context.get("user_type", '')
            user_type_instance = UserType.objects.get(user_type=user_type)
            data['user_type'] = user_type_instance
        
        except UserType.DoesNotExist:
            raise serializers.ValidationError(
                detail={'error': "Please select a valid user type."}
            )

        return data
    
    def create(self, validated_data):
        hashed_pw = make_password(self.context.get('password',''))
        validated_data['password'] = hashed_pw

        new_user = User(**validated_data)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            # instance.email = validated_data.get('email', instance.email)
            # instance.fullname = validated_data.get('fullname', instance.fullname)
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'email', 'fullname', 'user_type', 'join_date', 'hobbies')