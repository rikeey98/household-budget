from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q
from .models import Category  # type: ignore
from .serializers import CategorySerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()  # type: ignore
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(user=user)  # type: ignore
        parent_id = self.request.query_params.get('parent_id')
        category_type = self.request.query_params.get('category_type')
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        if category_type:
            queryset = queryset.filter(category_type=category_type)
        return queryset.order_by('parent_id', 'name')

    def create(self, request, *args, **kwargs):
        print('==== [DEBUG] 카테고리 생성 요청 ====', flush=True)
        print('request.data:', request.data, flush=True)
        print('user:', request.user, flush=True)
        data = request.data.copy()
        # data['user'] = request.user.id  # user 필드는 serializer.save에서 할당
        parent_id = data.get('parent')
        name = data.get('name')
        category_type = data.get('category_type')
        print('parent_id:', parent_id, 'name:', name, 'category_type:', category_type, flush=True)
        # 동일 부모, 동일 이름, 동일 사용자 중복 체크
        qs = Category.objects.filter(user=request.user, name=name, parent_id=parent_id)  # type: ignore
        print('중복 체크 결과 exists:', qs.exists(), flush=True)
        if qs.exists():
            print('중복 분류 존재: 400 반환', flush=True)
            return Response({'detail': '동일한 이름의 분류가 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # parent_id 유효성 체크
        if parent_id:
            try:
                parent = Category.objects.get(id=parent_id, user=request.user)  # type: ignore
                if parent.category_type != category_type:
                    print('상위 분류 타입 불일치: 400 반환', flush=True)
                    return Response({'detail': '상위 분류와 분류 타입이 일치해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            except Category.DoesNotExist:  # type: ignore
                print('상위 분류 없음: 400 반환', flush=True)
                return Response({'detail': '상위 분류가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print('serializer.is_valid() 에러:', serializer.errors, flush=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer, user=request.user)
        print('카테고리 생성 성공', flush=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, user=None):
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def tree(self, request):
        user = request.user
        category_type = request.query_params.get('category_type')
        qs = Category.objects.filter(user=user, parent=None)  # type: ignore
        if category_type:
            qs = qs.filter(category_type=category_type)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        user = request.user
        q = request.query_params.get('q', '')
        category_type = request.query_params.get('category_type')
        qs = Category.objects.filter(user=user)  # type: ignore
        if category_type:
            qs = qs.filter(category_type=category_type)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(parent__name__icontains=q))
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        user = request.user
        # 소유권 검증
        if instance.user != user:
            return Response({'detail': '본인 소유의 분류만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        # 이름 중복 체크 (동일 부모, 동일 이름, 동일 사용자)
        name = data.get('name', instance.name)
        parent_id = data.get('parent', instance.parent_id)
        qs = Category.objects.filter(user=user, name=name, parent_id=parent_id).exclude(id=instance.id)  # type: ignore
        if qs.exists():
            return Response({'detail': '동일한 이름의 분류가 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # parent 변경 시 순환참조 방지
        if parent_id:
            if int(parent_id) == instance.id:
                return Response({'detail': '자기 자신을 상위 분류로 설정할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            # 상위 분류가 자신의 하위(자식)인지 확인 (순환참조 방지)
            def is_descendant(child, target_id):
                if child.id == int(target_id):
                    return True
                for c in child.children.all():
                    if is_descendant(c, target_id):
                        return True
                return False
            parent = Category.objects.filter(id=parent_id, user=user).first()  # type: ignore
            if parent and is_descendant(instance, parent.id):
                return Response({'detail': '순환참조는 허용되지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            # 타입 일치 확인
            category_type = data.get('category_type', instance.category_type)
            if parent and parent.category_type != category_type:
                return Response({'detail': '상위 분류와 분류 타입이 일치해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # PATCH도 동일 검증 적용
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # 소유권 검증
        if instance.user != user:
            return Response({'detail': '본인 소유의 분류만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
        cascade = request.query_params.get('cascade', 'false').lower() == 'true'
        if instance.children.exists():
            if not cascade:
                return Response({'detail': '하위(자식) 분류가 존재하여 삭제할 수 없습니다. 연쇄 삭제하려면 ?cascade=true를 사용하세요.'}, status=status.HTTP_400_BAD_REQUEST)
            # 연쇄 삭제
            def delete_children(cat):
                for child in cat.children.all():
                    delete_children(child)
                    child.delete()
            delete_children(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# urls.py에서 router.register('')로 연결 필요
