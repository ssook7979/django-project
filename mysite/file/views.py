from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import File
from .forms import FileForm
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class BasicUploadView(View):
    def get(self, request):
        file_list = File.objects.filter(owner=self.request.user, on_writing='Y')
        return render(self.request, 'file/upload.html', {'file_list':file_list,})

    @method_decorator(login_required)
    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            file.owner = self.request.user
            file.save()
            data = {'is_valid':True, 'name':file.file.name, 'url':file.file.url}
        else:
            data = {'is_valid':False}
        return JsonResponse(data)

class FileDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, photo_id):
        try:
            file = File.objects.get(id=photo_id)
        except File.DoesNotExist:
            data = {'success':False}
            return JsonResponse(data)
        
        if file.owner  == self.request.user:
            file.delete()
            data = {'success':True}
            return JsonResponse(data)
        else:
            return HttpResponse('wrong_path')
        
