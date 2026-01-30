from django import forms
from events.models import Participant,Event,Category


class MixinStyleForm:
    def apply_styles(self):
        pass


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

