from django.db import models
from gyms.models import GymMember

# Create your models here.
class VisitLog(models.Model): # 출입관리
    visitlog_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    nfc_uid = models.CharField(max_length=30, null=True)
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    QR_fields = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.member} - {self.enter_time}"

    @property
    def is_checked_out(self):
        return self.exit_time is not None