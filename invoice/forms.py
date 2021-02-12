from django import forms
from django.forms import formset_factory
from .models import Invoice


class InvoiceForm(forms.Form):
    # fields = ['customer', 'message']
    customer = forms.CharField(
        label='Customer',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer/Company Name',
            'rows': 1
        })
    )
    customer_email = forms.CharField(
        label='Customer Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'customer@company.com',
            'rows': 1
        })
    )
    billing_address = forms.CharField(
        label='Billing Address',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '',
            'rows': 1
        })
    )
    message = forms.CharField(
        label='Contact_info',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact_info',
            'rows': 1
        })
    )
    remark = forms.CharField(
        label='tax',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tax',
            'rows': 1
        })
    )

    Contract_Agreement_Num = forms.CharField(
        label='Contract_Agreement_Num',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'customer_agreement',
            'rows': 1
        })
    )



class LineItemForm(forms.Form):
    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Service Name'
        })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Book Name here',
            "rows": 1
        })
    )
    unit = forms.CharField(
        label='unit',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Unit',
            "rows": 1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        })  # quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate $',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )


LineItemFormset = formset_factory(LineItemForm, extra=1)