import re

def clear_space_back(datas):
  result = []
  for data in datas:
    data = data.strip()
    if data != '':
      result.append(data)
  return result

def clear_html(datas):
  result = []
  for data in datas:
    result.append(re.sub('<[^>]+>','',data))
  return result