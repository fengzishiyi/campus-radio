# Permissions App

权限管理应用，用于控制不同角色用户对各个模块的访问权限。

## 功能特性

- 基于角色的权限控制（RBAC）
- 支持三种角色：管理员（admin）、播音员（anchor）、喜马拉雅人员（himalaya）
- 灵活的模块权限配置
- 装饰器用于视图权限检查
- 模板标签用于前端权限显示

## 使用方法

### 1. 装饰器

#### @admin_required
检查用户是否为管理员：

```python
from apps.permissions.decorators import admin_required

@admin_required
def my_admin_view(request):
    # 只有管理员可以访问
    return render(request, 'admin_page.html')
```

#### @module_permission_required(module_name)
检查用户是否有编辑指定模块的权限：

```python
from apps.permissions.decorators import module_permission_required

@module_permission_required('news')
def edit_news(request):
    # 只有有news模块权限的用户可以访问
    return render(request, 'news_edit.html')
```

### 2. 模板标签

在模板中加载标签库：

```django
{% load perm_tags %}
```

#### {% can_edit "module_name" user %}
检查用户是否可以编辑指定模块：

```django
{% can_edit "news" request.user as can_edit_news %}
{% if can_edit_news %}
    <a href="{% url 'news:create' %}">创建新闻</a>
{% endif %}
```

#### {% is_admin user %}
检查用户是否为管理员：

```django
{% is_admin request.user as user_is_admin %}
{% if user_is_admin %}
    <a href="{% url 'permissions:config' %}">权限配置</a>
{% endif %}
```

### 3. 权限配置界面

管理员可以访问 `/admin/permissions/config/` 进行权限配置：

- 查看所有模块的权限设置
- 为每个模块勾选允许访问的角色
- 启用/禁用模块权限检查

## 默认权限配置

系统初始化时会创建以下默认权限：

| 模块标识 | 模块名称 | 允许的角色 |
|---------|---------|----------|
| news | 新闻管理 | admin, anchor |
| schedule | 节目编排 | admin, anchor |
| booking | 录音室预约 | admin, anchor, himalaya |
| himalaya | 喜马拉雅管理 | admin, himalaya |
| announcements | 公告管理 | admin |
| groups | 小组管理 | admin |
| user_management | 用户管理 | admin |

## API

### 模型方法

```python
module_perm = ModulePermission.objects.get(module_name='news')
can_edit = module_perm.can_edit(user)  # 返回 True/False
```

### 直接查询

```python
from apps.permissions.models import ModulePermission

# 获取指定模块权限
module = ModulePermission.objects.get(module_name='news')

# 检查用户权限
if module.can_edit(request.user):
    # 用户有权限
    pass
```

## 测试

运行测试：

```bash
python manage.py test apps.permissions
```

测试覆盖：
- 模型方法测试
- 装饰器测试
- 模板标签测试
- 默认权限创建测试
