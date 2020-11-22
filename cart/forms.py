from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20 + 1)]


class ItemQuantityUpdateForm(forms.Form):
    quantity = forms.TypedChoiceField(label="Количество",
                                      choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
