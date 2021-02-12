from django.db import models
from django.urls import reverse
from distributed_counter import DistributedCounter
import datetime


# Create your models here.
class Invoice(models.Model):
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default="this is a default message.")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    Contract_Agreement_Num = models.CharField(max_length=100,null=True, blank=True)
    remark = models.DecimalField(max_digits=9, decimal_places=2,null=True, blank=True)
    grand_total = models.CharField(max_length=100,null=True, blank=True)
    words = models.CharField(max_length=100,null=True, blank=True)
    number=models.IntegerField(max_length=100,null=True)

    def __str__(self):
        return str(self.customer)

    def get_status(self):
        return self.status

   # def get_absoulte_url(self):
    #    return reverse('invoice-list', kwargs={"id": self.id})

    # def save(self, *args, **kwargs):
    # if not self.id:
    #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
    # return super(Invoice, self).save(*args, **kwargs)


class LineItem(models.Model):
    customer = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    #serial = models.IntegerField(default=lambda: Invoice.objects.latest('id').serial + 1,null=True)
    service = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField()
    unit = models.TextField(max_length=100, null=True, blank=True)
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.customer)

