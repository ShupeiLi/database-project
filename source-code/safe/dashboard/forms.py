# -*- coding: utf-8 -*-

from django import forms
from register.models import NewUser


class OrderSubmitForm(forms.Form):
    """
    Ref: Seller submits an order.
    """
    ono = forms.fields.IntegerField()
    dtrans_choices = (('plane', '航空运输'), ('train', '铁道运输'), ('truck', '公路运输'))
    dtrans = forms.fields.ChoiceField(choices=dtrans_choices, widget=forms.widgets.select)
    
