from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from apps.permissions.decorators import module_permission_required
from .models import Album, AudioTrack, Script
from .forms import AlbumForm, AudioTrackForm, ScriptForm


def album_list_view(request):
    """显示所有专辑的卡片网格"""
    albums = Album.objects.annotate(
        track_count=Count('tracks'),
        total_plays=Sum('tracks__play_count')
    ).order_by('-created_at')
    
    return render(request, 'himalaya/album_list.html', {
        'albums': albums
    })


def album_detail_view(request, pk):
    """显示专辑详情和曲目列表"""
    album = get_object_or_404(Album, pk=pk)
    tracks = album.tracks.order_by('order', 'id')
    
    total_plays = tracks.aggregate(total=Sum('play_count'))['total'] or 0
    
    return render(request, 'himalaya/album_detail.html', {
        'album': album,
        'tracks': tracks,
        'total_plays': total_plays
    })


@module_permission_required('himalaya')
def album_create_view(request):
    """创建专辑"""
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.created_by = request.user
            album.save()
            messages.success(request, '专辑创建成功！')
            return redirect('himalaya:album_detail', pk=album.pk)
    else:
        form = AlbumForm()
    
    return render(request, 'himalaya/album_form.html', {
        'form': form,
        'title': '创建专辑'
    })


@module_permission_required('himalaya')
def album_edit_view(request, pk):
    """编辑专辑"""
    album = get_object_or_404(Album, pk=pk)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, '专辑更新成功！')
            return redirect('himalaya:album_detail', pk=album.pk)
    else:
        form = AlbumForm(instance=album)
    
    return render(request, 'himalaya/album_form.html', {
        'form': form,
        'album': album,
        'title': '编辑专辑'
    })


@module_permission_required('himalaya')
def album_delete_view(request, pk):
    """删除专辑"""
    album = get_object_or_404(Album, pk=pk)
    
    if request.method == 'POST':
        album.delete()
        messages.success(request, '专辑删除成功！')
        return redirect('himalaya:album_list')
    
    return render(request, 'himalaya/album_delete_confirm.html', {
        'album': album
    })


@module_permission_required('himalaya')
def track_create_view(request, album_pk):
    """向专辑添加音频轨道"""
    album = get_object_or_404(Album, pk=album_pk)
    
    if request.method == 'POST':
        form = AudioTrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.album = album
            track.uploaded_by = request.user
            track.save()
            messages.success(request, '音频轨道添加成功！')
            return redirect('himalaya:album_detail', pk=album.pk)
    else:
        form = AudioTrackForm()
    
    return render(request, 'himalaya/track_form.html', {
        'form': form,
        'album': album,
        'title': f'向《{album.title}》添加音频'
    })


@module_permission_required('himalaya')
def track_edit_view(request, pk):
    """编辑音频轨道"""
    track = get_object_or_404(AudioTrack, pk=pk)
    
    if request.method == 'POST':
        form = AudioTrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, '音频轨道更新成功！')
            return redirect('himalaya:album_detail', pk=track.album.pk)
    else:
        form = AudioTrackForm(instance=track)
    
    return render(request, 'himalaya/track_form.html', {
        'form': form,
        'track': track,
        'album': track.album,
        'title': '编辑音频'
    })


@module_permission_required('himalaya')
def track_delete_view(request, pk):
    """删除音频轨道"""
    track = get_object_or_404(AudioTrack, pk=pk)
    album = track.album
    
    if request.method == 'POST':
        track.delete()
        messages.success(request, '音频轨道删除成功！')
        return redirect('himalaya:album_detail', pk=album.pk)
    
    return render(request, 'himalaya/track_delete_confirm.html', {
        'track': track
    })


def track_play_view(request, pk):
    """增加播放计数并重定向到音频URL"""
    track = get_object_or_404(AudioTrack, pk=pk)
    track.increment_play_count()
    return redirect(track.audio_url)


def script_view(request, pk):
    """查看音频轨道的文稿"""
    track = get_object_or_404(AudioTrack, pk=pk)
    
    try:
        script = track.script
    except Script.DoesNotExist:
        script = None
    
    return render(request, 'himalaya/script_view.html', {
        'track': track,
        'script': script
    })


@module_permission_required('himalaya')
def script_edit_view(request, pk):
    """创建或编辑文稿"""
    track = get_object_or_404(AudioTrack, pk=pk)
    
    try:
        script = track.script
    except Script.DoesNotExist:
        script = None
    
    if request.method == 'POST':
        form = ScriptForm(request.POST, instance=script)
        if form.is_valid():
            script = form.save(commit=False)
            script.track = track
            script.author = request.user
            script.save()
            messages.success(request, '文稿保存成功！')
            return redirect('himalaya:script_view', pk=track.pk)
    else:
        form = ScriptForm(instance=script)
    
    return render(request, 'himalaya/script_form.html', {
        'form': form,
        'track': track,
        'script': script
    })
