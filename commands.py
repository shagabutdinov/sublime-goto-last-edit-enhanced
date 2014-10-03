import sublime
import sublime_plugin

class History():
  def __init__(self):
    self.index = 0
    self.max = 0

  def increment(self):
    self.max += 1
    self.index = self.max

class Collection():
  def __init__(self):
    self.list = {}
    self.index = 0

  def get(self, view):
    id = view.id()
    if id not in self.list:
      self.list[id] = History()

    return self.list[id]

collection = Collection()

class GotoLastEditEnhanced(sublime_plugin.TextCommand):
  def run(self, edit, backward = False):
    history = collection.get(self.view)
    history_range = reversed(range(0, history.index + 1))
    if backward:
      history_range = range(history.index, history.max + 1)

    for index in history_range:
      regions = self.view.get_regions('goto_last_edit_' + str(index))
      if self.is_regions_equal(regions, self.view.sel()):
        continue

      if len(regions) > 0:
        self.view.sel().clear()
        self.view.sel().add_all(regions)
        self.view.show(regions[0])
        history.index = index
        break

  def is_regions_equal(self, regions_1, regions_2):
    if len(regions_1) != len(regions_2):
      return False

    for index, region_1 in enumerate(regions_1):
      region_2 = regions_2[index]
      if region_2.a != region_1.a or region_2.b != region_1.b:
        return False

    return True

class Listener(sublime_plugin.EventListener):
  def on_modified(self, view):
    history = collection.get(view)
    history.increment()
    view.add_regions('goto_last_edit_' + str(history.index), view.sel())