from django import forms
from events.models import Participant,Event,Category


class MixinStyleForm:

    default_class = "border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5 m-2"

    def apply_styles(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update(
                    {
                        # "class": "w-full text-sm text-gray-900 bg-white rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 p-2.5",
                    }
                )
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update(
                    {
                        "class": "block text-sm text-white bg-blue-500 hover:bg-blue-700 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:border-transparent p-2.5",
                    }
                )
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                    }
                )
            elif isinstance(field.widget, (forms.Textarea, forms.TextInput)):
                field.widget.attrs.update(
                    {
                        "class": self.default_class+" w-full",
                    }
                )
            else :
                field.widget.attrs.update(
                    {
                        "class": self.default_class,
                        "placeholder": f"{field.label}",
                    }
                )


class EventModelForm(MixinStyleForm,forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category", "image", "participants"]
    
        widgets = {
            "date" : forms.SelectDateWidget(),
            "time": forms.TimeInput(attrs={'type': 'time'}),
            "category" : forms.Select(),
            # TODO : Image upload not working properly
            "image" : forms.ClearableFileInput(),
            "participants" : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

