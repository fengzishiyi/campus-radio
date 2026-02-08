from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ModulePermission
from .forms import ModulePermissionForm
from .decorators import admin_required


@admin_required
def permissions_config_view(request):
    """View and update module permissions"""
    modules = ModulePermission.objects.all().order_by('module_name')
    
    if request.method == 'POST':
        # Process form submissions
        for module in modules:
            form = ModulePermissionForm(request.POST, instance=module, prefix=str(module.id))
            if form.is_valid():
                form.save()
        
        messages.success(request, '权限配置已更新')
        return redirect('permissions:config')
    
    # Create forms for each module
    module_forms = []
    for module in modules:
        form = ModulePermissionForm(instance=module, prefix=str(module.id))
        module_forms.append({
            'module': module,
            'form': form
        })
    
    return render(request, 'permissions/config.html', {
        'module_forms': module_forms
    })
