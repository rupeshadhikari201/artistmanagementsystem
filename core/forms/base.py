from django import forms
from django.utils.safestring import mark_safe
from core.utils.tailwind_classes import TAILWIND_CLASSES, ERROR_CLASSES, LABEL_CLASSES

class TailwindForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # apply styles
        self.apply_widget_styles()
        self.apply_label_styles()
        
    def apply_widget_styles(self):
        
        for name, field in self.fields.items():
            widget = field.widget 
            
            if isinstance(widget, forms.TextInput):
                css = TAILWIND_CLASSES['input']
            
            elif isinstance(widget, forms.EmailField):
                css = TAILWIND_CLASSES['input']
                
            elif isinstance(widget, forms.PasswordInput):
                css = TAILWIND_CLASSES['input']
                
            elif isinstance(widget, forms.Textarea):
                css = TAILWIND_CLASSES['textarea']
                
            elif isinstance(widget, forms.Select):
                css = TAILWIND_CLASSES['select']
            
            elif isinstance(widget, forms.SelectMultiple):
                css = TAILWIND_CLASSES["multi_select"]

            elif isinstance(widget, forms.CheckboxInput):
                css = TAILWIND_CLASSES["checkbox"]

            elif isinstance(widget, forms.RadioSelect):
                css = TAILWIND_CLASSES["radio"]

            else:
                css = TAILWIND_CLASSES["input"]
                
            widget.attrs['class'] = f"{widget.attrs.get('class','')}{css}".strip()
            
    
    def apply_label_styles(self):
        
        for name, field in self.fields.items():
            field.label_suffix = ""
            
            if field.required:
                field.widget.attrs['data-label-class'] = LABEL_CLASSES['required']
            else:
                field.widget.attrs['data-label-class'] = LABEL_CLASSES['default']
                