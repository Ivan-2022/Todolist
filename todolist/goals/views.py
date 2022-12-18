from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import Category, Goal, Comment, Board
from .permissions import BoardPermissions, CategoryPermissions, GoalPermissions, CommentPermissions
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardSerializer, BoardListSerializer, BoardCreateSerializer


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]  # проверить нужен ли IsAuthenticated
    serializer_class = BoardListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class GoalCategoryCreateView(CreateAPIView):
    model = Category
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = Category
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "board"]

    def get_queryset(self):
        return Category.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = GoalCategorySerializer
    permission_classes = [CategoryPermissions]

    def get_queryset(self):
        return Category.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.goals.update(status=Goal.Status.archived)
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created", "due_date", "priority"]
    ordering = ["title", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    permission_classes = [CommentPermissions]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user=self.request.user)
