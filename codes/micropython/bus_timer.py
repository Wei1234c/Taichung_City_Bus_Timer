import urequests as requests
import gc
gc.collect()


def split_text(text):
    text = text.split('@')[0] 
    length = len(text)
    start = 0
    end = 0
    
    while end < length - 1 and end >= 0:
        start = text.find('|', end)
        end = text.find('|', start + 1)

        part = text[start + 1:end]
        yield part.split(',')
        
        start = end  
        
        
def get_ETA(schedules, bus_stop_code):
    for schedule in schedules:
        if schedule[2] == bus_stop_code + '_': 
            return schedule[:-1]
        
        
def get_minutes_left(schedule):
    minutes_left = schedule[0].replace('_', '')
    if minutes_left.isdigit() and int(minutes_left) >= 0:
        return minutes_left
    

def query_minutes_left(route_id, route_direction, bus_stop_code):
    
    base_url = 'http://citybus.taichung.gov.tw/ibus/RealRoute/aspx/RealRoute.ashx?Lang=Cht&BusType=0&Data=' + route_id + '_,' + route_direction
    # url_bus_stops = base_url + '&Type=GetStop'  # 站牌名稱 編號 座標
    url_schedules = base_url + '&Type=GetFreshData'  # 站牌編號 到站時刻 

    schedules = requests.get(url_schedules).text
    schedules = split_text(schedules)
    schedule = get_ETA(schedules, bus_stop_code)
    print(schedule)

    return get_minutes_left(schedule)