from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'parent', 'parent_name', 'category_type', 'user_id', 'children', 'created_at'
        ]
        read_only_fields = ['id', 'user_id', 'created_at', 'children', 'parent_name']

    def get_children(self, obj):
        # 재귀적으로 children 직렬화
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return [] 