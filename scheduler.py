import time
import schedule
import downloader

def download_data(t):
    #Don't run if on the weekend
    downloader.download()

schedule.every().day.at("03:00").do(download_data, 'Loading data')
while True:
    schedule.run_pending()
    print('Waiting to get data')
    time.sleep(60) # wait one minute