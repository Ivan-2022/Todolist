from django.urls import path

from views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalCreateView, GoalListView, \
    GoalView, GoalCommentCreateView, GoalCommentListView, GoalCommentView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='category_create'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='category'),
    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal'),
    path('goal_comment/create', GoalCommentCreateView.as_view(), name='comment_create'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comment_list'),
    path('goal_comment/<pk>', GoalCommentView.as_view(), name='comment'),
]
