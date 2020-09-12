# # Write to Json
# from stock.core.data import Market
# from stock.models import Company
# all_codes = list({i.code: i for i in Company.objects.all()}.keys())
# for code in all_codes:
#   a = Market('2019-01-01', '2019-03-01', code)
#   c = a.get_daily_price 
#   n = a.get_corp_info 
#   c.to_json(f"datas/json/{n['code']}.json", orient='table')

# # Read from Json in datas/
import pandas as pd
import numpy as np
import os

json_path = './stock/core/data/json'
all_codes = os.listdir(json_path)
def return_dfs (num_of_companys=1, curr=0):
  if curr > 4:
    exit()
  else:
    tries = curr

  codes = np.random.choice(all_codes, num_of_companys)
  dfs = {}
  for code in codes:
    # return {code: pd.read_json(f'datas/{code}.json', orient='table')}
    try:
      dfs[code] = pd.read_json(os.path.join(json_path, code) , orient='table')
    except ValueError:
        tries += 1
        print(f"{code} is in valid")
        os.remove(os.path.join(json_path, code))
        return return_dfs(num_of_companys, tries)
  return dfs
