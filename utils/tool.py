def is_strIntNum(str = ''):
  try:
    int(str)
    return True
  except ValueError:
    pass
  return False