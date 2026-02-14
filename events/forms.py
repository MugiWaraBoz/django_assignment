from django import forms
from events.models import Event,Category
from django.contrib.auth.models import User



class MixinStyleForm:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styles()

    default_class = "border border-slate-700/40 bg-slate-800/50 backdrop-blur-sm text-slate-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-3 m-2 focus:bg-slate-800/70 transition-colors"

    def apply_styles(self):
        for field_name, field in self.fields.items():

            for field_name, field in self.fields.items():
                # Base classes applied to most fields
                base_class = self.default_class

                # 1. Special case: first_name field (custom width)
                if field_name == "first_name" or field_name == "last_name":
                    field.widget.attrs.update({
                        "class": f"{base_class} w-full lg:w-2/5"
                    })

                # 2. Multi-select checkboxes
                elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({
                        "class": "flex flex-col gap-2"  # nicely spaced stacked checkboxes
                    })

                # 3. File input
                elif isinstance(field.widget, forms.ClearableFileInput):
                    field.widget.attrs.update({
                        "class": (
                            "block text-sm text-white bg-gradient-to-r from-blue-500/70 "
                            "to-indigo-500/70 hover:from-blue-600/90 hover:to-indigo-600/90 "
                            "backdrop-blur-sm rounded-lg border border-slate-700/40 cursor-pointer "
                            "focus:outline-none focus:border-transparent p-2.5 transition-all duration-200 shadow-md"
                        )
                    })

                # 4. Time input
                elif isinstance(field.widget, forms.TimeInput):
                    field.widget.attrs.update({
                        "class": base_class
                    })

                # 5. Standard text inputs
                elif isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput, forms.Textarea)):
                    field.widget.attrs.update({
                        "class": f"{base_class} w-full"
                    })

                # 6. Fallback for any other field types
                else:
                    field.widget.attrs.update({
                        "class": base_class,
                        "placeholder": field.label  # auto placeholder from label
                    })



class EventModelForm(MixinStyleForm,forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "time", "location", "category", "image"]
    
        widgets = {
            "date" : forms.SelectDateWidget(),
            "time": forms.TimeInput(attrs={'type': 'time'}),
            "category" : forms.Select(),
            # TODO : Image upload not working properly
            "image" : forms.ClearableFileInput(),
        }

            
