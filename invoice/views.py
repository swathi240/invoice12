from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm
from django.db import transaction
from sequences import Sequence
from sequences import get_next_value,get_last_value
import pdfkit


class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices": invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')


def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                                             customer_email=form.data["customer_email"],
                                             billing_address=form.data["billing_address"],
                                             date=form.data["date"],
                                             due_date=form.data["due_date"],
                                             message=form.data["message"],
                                             Contract_Agreement_Num=form.data["Contract_Agreement_Num"],
                                             remark=form.data["remark"],
                                             grand_total=0,
                                             words=0
                                             )
            # invoice.save()

        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                unit = form.cleaned_data.get('unit')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')

                if service and description and unit and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount

                    LineItem(customer=invoice,
                             service=service,
                             description=description,
                             unit=unit,
                             quantity=quantity,
                             rate=rate,
                             amount=amount).save()

            invoice.total_amount = total
            invoice.remark = float(total) * 0.18
            invoice.grand_total = int(float(invoice.remark) + float(invoice.total_amount))
            invoice.words = num1words(invoice.grand_total)
            invoice.words = invoice.words.title()
            invoice.save()

            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def invoicenum():
    invoice=Invoice.objects.create(number=0)
    def post(self, request):

            invoice_ids = request.POST.getlist("invoice_id")
            invoice_ids = list(map(int, invoice_ids))
            invoices = Invoice.objects.filter(id__in=invoice_ids)

            for i in invoices:
                invoice.number = i + 1
                invoice.number = request.POST.getlist("invoice.number")
            return redirect('invoice:invoice-list')


def product_delete_view(request, id):
    obj = Invoice.objects.get(id=id)
    # obj1= LineItem.objects.get(id=id)
    # post request
    if request.method == "POST":
        # confirming delete
        obj.delete()
        # obj1.delete()

        return redirect('../../')
    context = {
        "object": obj,
        # "object1":obj1
    }
    return render(request, "invoice/invoice_delete.html", context)



def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "ABC AUTOMATION",
            "address": "XYZ address",
            "address1": "Bangalore ,Karnataka",
            "phone": "+91 9999999999,+91 111111111",
            "email": "swathi@gmail.com",
            "contact": "Gahgdad",

        },
        "account": "ACCOUNT DETAILS",
        "bank": "MY BANK",
        "add": " Bengaluru,",
        "add1": "Karnatak",
        "ifsc": "IFSC:xxxxxxxxx",
        "acc": "Account_No:1111111111111",
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,

        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "Contract_Agreement_Num": invoice.Contract_Agreement_Num,
        "remark": invoice.remark,
        "grand_total": invoice.grand_total,
        "words": invoice.words,
        "lineitem": lineitem,
    }
    return render(request, 'invoice/pdf_template.html', context)




def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    path_wkthmltopdf = "C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False,
                          configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


def num1words(num):
    num = int(num)
    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num1words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot == 0 else ' ' + num1words(num % pivot))


def change_status(request):
    return redirect('invoice:invoice-list')


def view_404(request, *args, **kwargs):
    return redirect('invoice:invoice-list')
