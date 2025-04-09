from django.forms.widgets import Widget
from django.utils.safestring import mark_safe

class CustomDateTimeWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        # Aquí pegas tu HTML personalizado.
        html = f"""
        <div class="custom-datetime">
            <input type="date" name="{name}" value="{value or ''}"  />
        </div>
        """
        return mark_safe(html)