import pandas as pd

class RowCombiner:
  _item = None

  def combine(self, new_item):
    if new_item is None:
      return
    elif self._item is None:
      self._item = new_item
    else:
      self._item = self.__combine(self._item, new_item)

  def get(self):
    return self._item

  def __combine(self, all_items, new_item):
    cols_to_use = new_item.columns.difference(all_items.columns)
    return all_items.join(new_item[cols_to_use])
