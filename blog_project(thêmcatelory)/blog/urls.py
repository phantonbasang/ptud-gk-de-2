from django.urls import path
from .views import CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete,TaskCreate,TaskDelete,TaskDetail,TaskList,TaskUpdate,bulk_delete_tasks,CustomLoginView,logout_view,RegisterPage,change_password,bulk_update_tasks,profile_view


urlpatterns = [
    path('', TaskList.as_view(), name="task"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', RegisterPage.as_view(), name="register"),
    path('task/<int:pk>/', TaskDetail.as_view(), name="tasks-detail"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="tasks-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="tasks-delete"),
    path('bulk-delete/', bulk_delete_tasks, name="bulk-delete"),
    path('bulk-update/', bulk_update_tasks, name="bulk-update"),
    path('change-password/', change_password, name='change_password'),
    path('profile/', profile_view, name='profile'),
    
    # Category management URLs
    path('categories/', CategoryList.as_view(), name='categories'),
    path('category/create/', CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),
]