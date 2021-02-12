from django.urls import path
from .views import InvoiceListView, createInvoice, generate_PDF, view_PDF,product_delete_view


app_name = 'invoice'
urlpatterns = [
    path('', InvoiceListView.as_view(), name="invoice-list"),
    path('create/', createInvoice, name="invoice-create"),
    path('invoice-detail/<id>', view_PDF, name='invoice-detail'),
    path('invoice-download/<id>', generate_PDF, name='invoice-download'),
    path('<int:id>/delete/', product_delete_view, name='invoice_delete'),


]
