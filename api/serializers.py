from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name',]

class FavoriteItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteItem
		fields = ['item','user',]

class FavoriteUserSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = FavoriteItem
		fields = ['user',]

class ItemListSerializer(serializers.ModelSerializer):
	added_by = UserSerializer()
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api-detail",
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	num_of_fave_users = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = [
			'image',
			'name',
			'description',
			'detail',
			'added_by',
			'num_of_fave_users',
			]

	def get_num_of_fave_users(self,obj):
		favorited = FavoriteItem.objects.filter(item=obj)
		return favorited.count()


class ItemDetailSerializer(serializers.ModelSerializer):
	list_of_fave_users = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = [
			'image',
			'name',
			'description',
			'list_of_fave_users',]

	def get_list_of_fave_users(self , obj):
		favorited = FavoriteItem.objects.filter(item=obj)
		users_list = FavoriteUserSerializer(favorited, many=True).data
		return users_list

