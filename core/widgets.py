from django import forms

class InputField(forms.TextInput):
  template_name = 'widgets/input.html'

  def __init__(self, label=None, **kwargs):
    super().__init__(**kwargs)
    self.label = label

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["label"] = self.label
    print(context)
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