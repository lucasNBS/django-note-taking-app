from django import forms

class InputField(forms.TextInput):
  template_name = 'widgets/input.html'

  def __init__(self, label=None, small=None, type="text", **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.small = small
    self.type = type

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["small"] = self.small
    context["widget"]["type"] = self.type
    return context

class Textarea(forms.Textarea):
  template_name = 'widgets/textarea.html'

  def __init__(self, label=None, **kwargs):
    super().__init__(**kwargs)
    self.label = label

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    return context

class SelectMultiple(forms.SelectMultiple):
  template_name = 'widgets/select_multiple.html'

  def __init__(self, label=None, initial_value=None, **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.initial_value = initial_value

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["value"] = self.initial_value
    return context
  
class Select(forms.Select):
  template_name = 'widgets/select.html'

  def __init__(self, label=None, initial_value=None, **kwargs):
    super().__init__(**kwargs)
    self.label = label
    self.initial_value = initial_value

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    context["widget"]["value"] = self.initial_value
    return context