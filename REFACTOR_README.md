# 校园广播站管理系统 UI/UX 重构说明

## 概述

本次重构将系统从报纸复古风格全面升级为现代化的 GitHub 网页风格，合并了多个功能模块，新增了迷你播放器等实用功能。

## 主要变更

### 1. 🎨 UI 风格变更

**从报纸风格到 GitHub 风格：**

- ✅ 删除了 `static/css/newspaper.css` 的报纸风格
- ✅ 新增了 `static/css/style.css`，采用 GitHub 设计语言
- ✅ 使用现代化无衬线字体栈
- ✅ GitHub 风格的圆角卡片、边框、按钮
- ✅ 简洁的顶部导航栏（深色背景）
- ✅ 现代化的配色方案（蓝色主题 `#0969da`）

**颜色系统：**
- 主色调：`#0969da` (GitHub 蓝)
- 成功：`#1a7f37` (绿色)
- 警告：`#9a6700` (黄色)
- 危险：`#d1242f` (红色)
- 背景：`#ffffff`, `#f6f8fa`
- 边框：`#d0d7de`

### 2. 📋 导航结构简化

**新的三板块导航：**
1. **头版** (`/`) - 首页，合并了公告功能
2. **录音室** (`/studio/`) - 合并了排班和预约功能
3. **喜马拉雅** (`/himalaya/`) - 保持不变

**移除的独立入口：**
- 公告（已合并到首页）
- 排班（已合并到录音室）

**保留的旧 URL（向后兼容）：**
- `/broadcast/` - 重定向到 `/studio/`
- `/booking/` - 重定向到 `/studio/`
- `/announcements/` - 仍可访问完整公告列表

### 3. 🏠 首页重构

**新首页布局：**

1. **信息栏**（顶部）
   - 今日日期
   - 天气信息
   - 今日录音室预约数量

2. **公告区域**（主体区域）
   - 占据页面最大视觉面积
   - GitHub 风格卡片展示
   - 紧急公告用红色边框高亮
   - 显示公告类型标签（紧急、活动、排班变更、通知）

3. **两栏布局**（底部）
   - 左栏：今日录音室时间轴（8:00-22:00）
   - 右栏：今日广播歌单和节目安排

### 4. 🎙️ 录音室模块（合并功能）

**主要功能页面：**

#### 日历视图 (`/studio/`)
- FullCalendar 月历展示
- 同时显示排班和预约信息
- 不同颜色区分：
  - 蓝色：已排班
  - 绿色：预约
  - 红色：直播日
- 点击日期进入日详情页

#### 日详情页 (`/studio/<date>/`)

合并了三个功能区：

**1. 节目安排**
- 添加节目（节目名称 + 时间段）
- 查看和删除已有节目

**2. 歌曲管理**
- 添加歌曲（歌名 + 歌手）
- 上传音频文件（MP3等格式）
- 查看已上传歌曲
- 删除歌曲

**3. 预约管理**
- 创建录音室预约
- 查看当天所有预约
- 时间轴可视化（8:00-22:00）
- 预约状态显示（待确认、已确认、已完成）

**直播功能：**
- 固定时间：16:00-18:00
- 可一键开启/关闭直播标记
- 直播在时间轴上显示为特殊标记（📡）

**取消的批量功能：**
- ❌ 批量创建一周排班
- ❌ 从分组填充
- ❌ 复制前一天排班

（这些功能的URL已删除，简化了操作流程）

### 5. 🎵 迷你播放器

**位置：** 固定在页面底部

**功能：**
- 播放/暂停
- 上一曲/下一曲
- 进度条控制
- 音量控制
- 显示歌曲名和歌手

**播放列表：**
- 自动加载今日歌单（从 `/studio/api/today-playlist/` 获取）
- 只播放已上传音频文件的歌曲
- 支持自动播放下一曲

**每日清理：**
- 使用 Django management command
- 运行命令：`python manage.py cleanup_daily_songs`
- 建议在每天 23:00 通过 cron 或任务调度器自动运行
- 清理当天上传的所有音频文件

### 6. 📊 数据模型变更

**DailySchedule 模型新增字段：**
```python
is_live = models.BooleanField(
    '是否直播', 
    default=False, 
    help_text='16:00-18:00直播标记'
)
```

**Song 模型新增字段：**
```python
audio_file = models.FileField(
    '音频文件', 
    upload_to='daily_songs/%Y/%m/%d/', 
    blank=True, 
    null=True, 
    help_text='上传的MP3等音频文件'
)
```

**数据库迁移：**
```bash
python manage.py migrate schedule 0002_add_live_and_audio
```

## 技术栈

- **前端框架：** Tailwind CSS (CDN)
- **交互：** HTMX
- **日历：** FullCalendar 6.1.10
- **音频播放：** HTML5 Audio API
- **后端：** Django 6.0
- **数据库：** SQLite (开发环境)

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 配置媒体文件

确保 `settings.py` 中配置了 MEDIA 设置：

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

在 `urls.py` 中已包含媒体文件的静态服务（开发环境）。

### 4. 配置定时任务（可选）

**使用 cron (Linux/Mac):**

```bash
# 编辑 crontab
crontab -e

# 添加每天 23:00 清理歌曲的任务
0 23 * * * cd /path/to/campus-radio && /path/to/venv/bin/python manage.py cleanup_daily_songs
```

**使用 Windows 任务计划程序:**

创建每天 23:00 运行的任务，执行：
```
python manage.py cleanup_daily_songs
```

## URL 路由映射

### 新 URL 结构

| 功能 | 新 URL | 说明 |
|-----|--------|------|
| 首页 | `/` | 头版，包含公告、今日安排 |
| 录音室日历 | `/studio/` | 月历视图 |
| 日详情 | `/studio/<date>/` | 合并的日详情页 |
| 添加节目 | `/studio/<date>/add-program/` | POST |
| 添加歌曲 | `/studio/<date>/add-song/` | POST |
| 上传歌曲 | `/studio/<date>/upload-song/` | POST (multipart) |
| 创建预约 | `/studio/<date>/add-booking/` | 跳转到预约表单 |
| 切换直播 | `/studio/<date>/toggle-live/` | POST |
| 今日歌单API | `/studio/api/today-playlist/` | JSON |
| 日历事件API | `/studio/api/events/` | JSON (FullCalendar) |
| 喜马拉雅 | `/himalaya/` | 保持不变 |

### 兼容性 URL（保留）

| 旧 URL | 说明 |
|--------|------|
| `/broadcast/` | 排班模块（保留向后兼容） |
| `/booking/` | 预约模块（保留向后兼容） |
| `/announcements/` | 公告列表 |

## API 端点

### 今日歌单 API

**URL:** `/studio/api/today-playlist/`

**方法:** GET

**返回格式:**
```json
{
  "songs": [
    {
      "id": 1,
      "title": "歌曲名",
      "artist": "歌手",
      "audio_url": "/media/daily_songs/2026/02/10/song.mp3"
    }
  ]
}
```

### 日历事件 API

**URL:** `/studio/api/events/`

**方法:** GET

**参数:**
- `start`: 开始日期 (ISO 8601)
- `end`: 结束日期 (ISO 8601)

**返回格式:**
```json
[
  {
    "title": "已排班 - 张三",
    "start": "2026-02-10",
    "url": "/studio/2026-02-10/",
    "color": "#0969da"
  }
]
```

## 权限控制

权限系统保持不变，使用装饰器：

- `@login_required` - 需要登录
- `@module_permission_required('schedule')` - 需要排班模块权限

## 文件上传

**支持的音频格式：**
- MP3
- WAV
- OGG
- M4A

**上传路径：**
- `media/daily_songs/YYYY/MM/DD/`

**自动清理：**
- 每天 23:00 删除当天上传的所有音频文件

## 常见问题

### Q: 如何切换回旧的报纸风格？

A: 编辑 `templates/base.html`，将：
```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```
改为：
```html
<link rel="stylesheet" href="{% static 'css/newspaper.css' %}">
```

### Q: 迷你播放器不显示？

A: 检查：
1. 是否有今日歌单数据
2. 歌曲是否上传了音频文件
3. 浏览器控制台是否有 JavaScript 错误

### Q: 批量排班功能去哪了？

A: 为简化操作流程，移除了批量排班功能。现在通过日历逐日添加排班信息。

### Q: 如何访问分组管理？

A: 访问 `/studio/groups/`

## 升级注意事项

### 从旧版本升级

1. **备份数据库：**
   ```bash
   cp db.sqlite3 db.sqlite3.backup
   ```

2. **运行迁移：**
   ```bash
   python manage.py migrate
   ```

3. **更新静态文件：**
   ```bash
   python manage.py collectstatic --no-input
   ```

4. **创建 media 目录：**
   ```bash
   mkdir -p media/daily_songs
   ```

### 已知兼容性问题

- 旧的 `/broadcast/calendar/<date>/` URL 需要手动更新为 `/studio/<date>/`
- 模板中硬编码的 URL 需要更新

## 维护和监控

### 日志位置

- Django 日志：控制台输出
- 音频文件上传错误：检查 Django DEBUG 页面

### 存储空间监控

由于音频文件每天自动清理，理论上不会占用过多空间。但建议：

1. 监控 `media/daily_songs/` 目录大小
2. 确保清理任务正常运行
3. 设置备份策略（如需要）

## 截图

（建议添加实际截图）

1. 首页 - 公告主体展示
2. 录音室日历 - FullCalendar 视图
3. 日详情页 - 三栏布局
4. 迷你播放器 - 底部固定

## 贡献者

- UI/UX 设计：GitHub Copilot
- 开发实现：GitHub Copilot
- 需求提供：@fengzishiyi

## 更新日志

### v2.0.0 (2026-02-10)

- 🎨 全面重构为 GitHub 风格 UI
- 🔀 合并排班和预约模块为"录音室"
- 🏠 首页合并公告展示
- 🎵 新增迷你播放器
- 📤 支持歌曲音频文件上传
- 📡 新增直播标记功能
- 🗑️ 自动清理每日歌曲文件
- ♻️ 简化导航结构为三板块

---

**文档最后更新：** 2026-02-10
