import utime

def sync_time_by_rtc():
    import ntptime
    ntptime.settime()
        
def get_current_time_tuple():
    # 获取当前UTC时间
    current_utc_time = utime.time()

    # 东八区偏移量为8小时（8 * 3600秒）
    #utc_offset = 8 * 3600

    # 计算东八区的本地时间
    eastern_time = current_utc_time

    # 将UTC时间转换为元组
    local_time_tuple = utime.localtime(eastern_time)
    return local_time_tuple
    
def get_current_time():
    time_tuple = get_current_time_tuple()
    # 获取当前小时和分钟
    current_hour = time_tuple[3]
    current_minute = time_tuple[4]
    current_second = time_tuple[5]
    return f"{current_hour:02}:{current_minute:02}:{current_second:02}"
    
def get_current_date():
    time_tuple = get_current_time_tuple()
    # 获取当前小时和分钟
    current_year = time_tuple[0]
    current_month = time_tuple[1]
    current_day = time_tuple[2]
    return f"{current_year}-{current_month:02}-{current_day:02}"
