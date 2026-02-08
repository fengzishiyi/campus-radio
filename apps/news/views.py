from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from apps.permissions.decorators import module_permission_required
from .models import NewsItem
from .forms import NewsItemForm


@login_required
def news_list_view(request):
    """新闻列表视图（带日期范围过滤）"""
    news_items = NewsItem.objects.all().select_related('reporter', 'reporter__profile')
    
    # 日期范围过滤
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        news_items = news_items.filter(date__gte=start_date)
    if end_date:
        news_items = news_items.filter(date__lte=end_date)
    
    context = {
        'news_items': news_items,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'news/list.html', context)


@login_required
def news_detail_view(request, pk):
    """新闻详情视图"""
    news_item = get_object_or_404(NewsItem.objects.select_related('reporter', 'reporter__profile'), pk=pk)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'news/detail.html', context)


@module_permission_required('news')
def news_create_view(request):
    """创建新闻视图"""
    if request.method == 'POST':
        form = NewsItemForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.reporter = request.user
            news_item.save()
            messages.success(request, '新闻创建成功！')
            return redirect('news:detail', pk=news_item.pk)
    else:
        form = NewsItemForm()
    
    context = {
        'form': form,
        'action': '创建',
    }
    return render(request, 'news/form.html', context)


@module_permission_required('news')
def news_edit_view(request, pk):
    """编辑新闻视图"""
    news_item = get_object_or_404(NewsItem, pk=pk)
    
    if request.method == 'POST':
        form = NewsItemForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, '新闻更新成功！')
            return redirect('news:detail', pk=news_item.pk)
    else:
        form = NewsItemForm(instance=news_item)
    
    context = {
        'form': form,
        'news_item': news_item,
        'action': '编辑',
    }
    return render(request, 'news/form.html', context)


@module_permission_required('news')
def news_delete_view(request, pk):
    """删除新闻视图"""
    news_item = get_object_or_404(NewsItem, pk=pk)
    
    if request.method == 'POST':
        news_item.delete()
        messages.success(request, '新闻删除成功！')
        return redirect('news:list')
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'news/delete_confirm.html', context)


@login_required
def news_stats_view(request):
    """统计视图"""
    # 总新闻数
    total_count = NewsItem.objects.count()
    
    # 最近6个月的月度统计
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_stats = (
        NewsItem.objects
        .filter(date__gte=six_months_ago)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # 格式化月度数据供图表使用
    monthly_labels = [stat['month'].strftime('%Y-%m') for stat in monthly_stats]
    monthly_data = [stat['count'] for stat in monthly_stats]
    
    # Top 10 播报员排行
    top_reporters = (
        NewsItem.objects
        .values('reporter__profile__real_name', 'reporter__username')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    
    reporter_labels = [
        reporter['reporter__profile__real_name'] or reporter['reporter__username'] 
        for reporter in top_reporters
    ]
    reporter_data = [reporter['count'] for reporter in top_reporters]
    
    context = {
        'total_count': total_count,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
        'reporter_labels': reporter_labels,
        'reporter_data': reporter_data,
    }
    return render(request, 'news/stats.html', context)
