from django import forms
from .widgets import MyDataSetWidget


class ModelChoiceField(forms.ModelChoiceField):

    def __init__(self, queryset, *, label_text=None, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 blank=False, **kwargs):
        self.label_text = label_text
        super(ModelChoiceField, self).__init__(queryset,
                                               empty_label=empty_label,
                                               required=required,
                                               widget=widget,
                                               label=label,
                                               initial=initial,
                                               help_text=help_text,
                                               to_field_name=to_field_name,
                                               limit_choices_to=limit_choices_to,
                                               blank=blank
                                               , **kwargs)

    # The original writing method must be written on the object__ str__  Method. After the method is rewritten, the system will automatically display the field set by the user
    def label_from_instance(self, obj):
        return getattr(obj, self.label_text)
