# 校园广播站管理系统

一个基于 Django 5.0 的现代化校园广播站管理系统框架，采用 Tailwind CSS 构建优雅的用户界面。

## 项目简介

这是一个全新的、干净的 Django 项目框架，专为校园广播站管理系统设计。项目提供了基础的配置和结构，您可以在此基础上快速开发自己的应用。

### 特性

- ✨ 基于 Django 5.0 最新版本
- 🎨 使用 Tailwind CSS CDN，无需复杂配置
- 📁 清晰的项目结构，易于维护
- 🔧 预配置的开发环境
- 📝 详细的中文文档
- 🚀 开箱即用的基础功能

## 技术栈

- **后端框架**: Django 5.0
- **数据库**: SQLite（开发环境）
- **前端框架**: Tailwind CSS
- **Python 版本**: 3.8+
- **其他依赖**: 
  - python-dotenv（环境变量管理）
  - Pillow（图片处理）

## 项目结构

```
campus-radio/
├── config/                 # Django 配置目录
│   ├── __init__.py
│   ├── settings.py        # 项目设置
│   ├── urls.py            # 主路由配置
│   ├── views.py           # 基础视图
│   ├── wsgi.py            # WSGI 配置
│   └── asgi.py            # ASGI 配置
├── apps/                   # 应用目录
│   └── __init__.py        # 用于存放各个应用
├── templates/              # 模板目录
│   ├── base.html          # 基础模板
│   ├── home.html          # 首页模板
│   └── registration/      # 认证相关模板
│       ├── login.html     # 登录页面
│       └── register.html  # 注册页面
├── static/                 # 静态文件目录
│   ├── css/
│   │   └── style.css      # 自定义样式
│   ├── js/
│   │   └── main.js        # 自定义脚本
│   └── images/            # 图片资源
├── media/                  # 媒体文件目录（用户上传）
├── .gitignore             # Git 忽略文件
├── .env.example           # 环境变量示例
├── manage.py              # Django 管理脚本
├── requirements.txt       # Python 依赖
└── README.md              # 项目说明文档
```

## 快速开始

### 环境准备

1. **安装 Python**
   
   确保您的系统已安装 Python 3.8 或更高版本：
   ```bash
   python --version
   ```

2. **克隆项目**
   
   ```bash
   git clone <repository-url>
   cd campus-radio
   ```

3. **创建虚拟环境**
   
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，设置您的配置：
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

   > **提示**: 可以使用以下 Python 命令生成一个安全的 SECRET_KEY：
   > ```python
   > from django.core.management.utils import get_random_secret_key
   > print(get_random_secret_key())
   > ```

### 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 创建超级用户

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

### 运行开发服务器

```bash
python manage.py runserver
```

现在您可以访问：
- **首页**: http://127.0.0.1:8000/
- **管理后台**: http://127.0.0.1:8000/admin/

## 如何添加新应用

### 1. 创建应用

在 `apps/` 目录下创建新应用：

```bash
python manage.py startapp your_app apps/your_app
```

### 2. 注册应用

在 `config/settings.py` 的 `INSTALLED_APPS` 中添加：

```python
INSTALLED_APPS = [
    # ...
    'apps.your_app',
]
```

### 3. 创建模型

在 `apps/your_app/models.py` 中定义数据模型：

```python
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "您的模型"
        verbose_name_plural = "您的模型"
    
    def __str__(self):
        return self.name
```

### 4. 创建并运行迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 注册到管理后台

在 `apps/your_app/admin.py` 中：

```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
```

### 6. 创建视图

在 `apps/your_app/views.py` 中：

```python
from django.shortcuts import render
from .models import YourModel

def your_view(request):
    items = YourModel.objects.all()
    return render(request, 'your_app/your_template.html', {'items': items})
```

### 7. 配置 URL

创建 `apps/your_app/urls.py`：

```python
from django.urls import path
from . import views

app_name = 'your_app'

urlpatterns = [
    path('', views.your_view, name='index'),
]
```

在 `config/urls.py` 中包含应用路由：

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('your-app/', include('apps.your_app.urls')),
]
```

## 开发指南

### 创建模型

模型定义在各应用的 `models.py` 中：

```python
from django.db import models
from django.contrib.auth.models import User

class Example(models.Model):
    # 字段类型
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "示例"
        verbose_name_plural = "示例"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

### 创建视图

#### 函数视图

```python
from django.shortcuts import render, get_object_or_404
from .models import Example

def example_list(request):
    examples = Example.objects.filter(is_active=True)
    return render(request, 'your_app/list.html', {'examples': examples})

def example_detail(request, pk):
    example = get_object_or_404(Example, pk=pk)
    return render(request, 'your_app/detail.html', {'example': example})
```

#### 类视图

```python
from django.views.generic import ListView, DetailView
from .models import Example

class ExampleListView(ListView):
    model = Example
    template_name = 'your_app/list.html'
    context_object_name = 'examples'
    paginate_by = 10
    
    def get_queryset(self):
        return Example.objects.filter(is_active=True)

class ExampleDetailView(DetailView):
    model = Example
    template_name = 'your_app/detail.html'
    context_object_name = 'example'
```

### 创建模板

模板使用 Django 模板语言和 Tailwind CSS：

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}页面标题{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">{{ title }}</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for item in items %}
        <div class="bg-white shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-2">{{ item.title }}</h2>
            <p class="text-gray-600">{{ item.content|truncatewords:20 }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

### 配置路由

在应用的 `urls.py` 中：

```python
from django.urls import path
from . import views

app_name = 'your_app'

urlpatterns = [
    path('', views.ExampleListView.as_view(), name='list'),
    path('<int:pk>/', views.ExampleDetailView.as_view(), name='detail'),
]
```

## 常用命令

### 开发服务器

```bash
# 启动开发服务器
python manage.py runserver

# 指定端口
python manage.py runserver 8080

# 指定 IP 和端口
python manage.py runserver 0.0.0.0:8000
```

### 数据库操作

```bash
# 创建迁移文件
python manage.py makemigrations

# 查看迁移 SQL
python manage.py sqlmigrate app_name 0001

# 执行迁移
python manage.py migrate

# 回滚迁移
python manage.py migrate app_name 0001
```

### 用户管理

```bash
# 创建超级用户
python manage.py createsuperuser

# 修改用户密码
python manage.py changepassword username
```

### Shell 操作

```bash
# 进入 Django Shell
python manage.py shell

# 进入增强版 Shell（需要安装 IPython）
pip install ipython
python manage.py shell
```

### 静态文件

```bash
# 收集静态文件（生产环境）
python manage.py collectstatic

# 清除静态文件
python manage.py collectstatic --clear
```

### 其他命令

```bash
# 检查项目问题
python manage.py check

# 显示已安装的应用
python manage.py showmigrations

# 清空数据库（谨慎使用）
python manage.py flush
```

## 项目规范建议

### 代码风格

- 遵循 PEP 8 Python 代码规范
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 模型、视图、URL 等分离，保持代码整洁

### 命名约定

- **应用名称**: 使用小写字母和下划线，如 `user_management`
- **模型名称**: 使用单数形式，首字母大写，如 `Article`
- **视图函数**: 使用小写字母和下划线，如 `article_list`
- **URL 名称**: 使用小写字母和连字符，如 `article-list`
- **模板文件**: 使用小写字母和下划线，如 `article_list.html`

### 数据库设计

- 合理使用外键关系
- 添加适当的索引提升查询性能
- 使用 `verbose_name` 提供字段说明
- 使用 `help_text` 提供字段帮助信息

### 安全建议

- 不要在代码中硬编码敏感信息
- 使用环境变量存储密钥和配置
- 生产环境设置 `DEBUG = False`
- 配置合适的 `ALLOWED_HOSTS`
- 定期更新依赖包

### Git 使用

- 编写清晰的提交信息
- 经常提交，小步快跑
- 使用分支进行功能开发
- 不要提交敏感文件（已在 .gitignore 中配置）

## 常见问题

### 1. 如何生成新的 SECRET_KEY？

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. 如何更改数据库？

编辑 `config/settings.py` 中的 `DATABASES` 配置。例如使用 PostgreSQL：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. 如何部署到生产环境？

1. 设置 `DEBUG = False`
2. 配置 `ALLOWED_HOSTS`
3. 使用生产级数据库（PostgreSQL、MySQL 等）
4. 配置静态文件服务
5. 使用 WSGI 服务器（如 Gunicorn）
6. 配置 HTTPS

### 4. 如何使用自定义用户模型？

在项目初期，创建自定义用户模型：

```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 添加自定义字段
    pass
```

在 `settings.py` 中配置：

```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

## 资源链接

- [Django 官方文档](https://docs.djangoproject.com/)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**祝您开发愉快！** 🚀
