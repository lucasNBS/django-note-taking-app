from .models import Folders

def is_general_folder(folder):
  return folder.id == Folders.objects.filter(title="General").first().id