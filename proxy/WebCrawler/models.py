from django.db import models

# Create your models here.
class ProxyMessage(models.Model):
    IP = models.CharField(max_length=17)
    Port = models.CharField(max_length=7,verbose_name="端口")
    Area = models.CharField(max_length=7,verbose_name="区域")
    Address = models.CharField(verbose_name="地址",max_length=30,blank=True,null=True)
    Type = models.CharField(max_length=10,verbose_name="代理类型")
    
    def __str__(self):
        return self.IP

    class Meta:
        verbose_name = u"IP统计"
        verbose_name_plural = u"IP统计"