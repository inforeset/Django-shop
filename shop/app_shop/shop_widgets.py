from itertools import chain

from django.db.models import BLANK_CHOICE_DASH
from django.forms import CheckboxInput, NumberInput, TextInput, HiddenInput
from django.utils.encoding import force_str
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django_filters.widgets import LinkWidget, RangeWidget


class ShopLinkWidget(LinkWidget):

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if not hasattr(self, "data"):
            self.data = {}
        if value is None:
            value = ""
        output = []
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        return mark_safe("\n".join(output))

    def option_string(self):
        link = '<a%(attrs)s %(classes)s id="%(id)s" href="?%(query_string)s">%(label)s</a>'
        return link

    def render_options(self, choices, selected_choices, name):
        selected_choices = set(force_str(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if not option_value.startswith("-"):
                if isinstance(option_label, (list, tuple)):
                    for option in option_label:
                        output.append(self.render_option(name, selected_choices, *option))
                else:
                    output.append(
                        self.render_option(
                            name, selected_choices, option_value, option_label
                        )
                    )
        return "\n".join(output)

    def render_option(self, name, selected_choices, option_value, option_label):
        option_value = force_str(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = "All"
        data = self.data.copy()
        classes = 'class="Sort-sortBy'
        if (option_value in selected_choices) or ('' in selected_choices and option_value == 'price'):
            data[name] = f'-{option_value}'
            classes = f'{classes} Sort-sortBy_inc"'
        else:
            data[name] = option_value
        if '' not in selected_choices:
            if option_value in selected_choices or f'-{option_value}' in selected_choices:
                if option_label.startswith('-'):
                    classes = f'{classes} Sort-sortBy_inc"'
                else:
                    classes = f'{classes} Sort-sortBy_dec"'
            else:
                classes = f'{classes}"'

        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
            "attrs": "",
            "classes": classes,
            "query_string": url,
            "label": force_str(option_label),
            "id": data[name]
        }


class ShopCheckboxInput(CheckboxInput):
    def value_from_datadict(self, data, files, name):
        if name not in data:
            # A missing value means False because HTML form submission does not
            # send results for unselected checkboxes.
            return None
        value = data.get(name)
        # Translate true and false strings to boolean values.
        values = {"true": True, "false": False}
        if isinstance(value, str):
            value = values.get(value.lower(), value)
        return bool(value)
