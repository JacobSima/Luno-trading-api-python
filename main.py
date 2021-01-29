import time
from datetime import datetime
from collections import deque
from decouple import config
from luno_python.client import Client

# use your own KEY_ID and SECRETfrom .env file to be created on the root of the project
KEY_ID = config('KEY_ID')  
SECRET = config('SECRET')
queue = deque([0,0])

def result_process(result):
  queue_result = 0
  dtn = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  last_trade = float(result.get('last_trade'))
  queue.append(last_trade)
  queue.popleft()
  old_last_trade = float(queue[0])
  last_last_trade = float(queue[1])

  if old_last_trade == 0:
    queue_result = old_last_trade
  else:
    queue_result = ((last_last_trade - old_last_trade)/(old_last_trade))*100

  queue_result = '{:+.2f}%'.format(queue_result)
  print(f'{dtn} - Last trade {last_trade} : ({queue_result})')

def main():
  while True:
    c = Client(api_key_id=KEY_ID, api_key_secret=SECRET)
    try:
      res = c.get_ticker(pair='ETHZAR')
      result_process(res)
      time.sleep(10)
    except Exception as e:
      print(e)
    

if __name__ == '__main__':
  main()









