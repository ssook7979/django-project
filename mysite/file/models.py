from django.db import models
from board2.models import Post, Comment
from members.models import CustomUser

def get_upload_to(instance, filename):
    return 'upload/{0}/%Y%m%d/{1}'.format(instance.post.id, filename)

ON_WRITING = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

class File(models.Model):
    on_writing = models.CharField(max_length=1, choices=ON_WRITING, default='Y')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, default=None, null=True, blank=True)
    file = models.FileField(upload_to='upload/%Y%m%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
