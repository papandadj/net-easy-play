import numpy as np
import pandas as pd
import os.path
import time
import itertools
FILEURL = './data.csv'

if os.path.isfile(FILEURL):
    df = pd.read_csv(FILEURL)
else:
    print("初始化数据库")
    df = pd.DataFrame(columns=['name', 'music_id', 'current', 'time'])


def to_str(input_list):
    return [str(i) if len(str(i)) != 1 else '0' + str(i) for i in input_list]

# return 2018.05.29格式时间
def get_time():
    now_time = time.localtime()
    return '.'.join(to_str([now_time.tm_year, now_time.tm_mon, now_time.tm_mday, now_time.tm_hour, now_time.tm_min, now_time.tm_sec]))


class db(object):
    def __init__(self):
        self.df = df

    '''
        name{list}:歌曲名称
        music_id{list}：歌曲名称对应的music_id
        name 跟music_id 对应
    '''
    def insert(self, name, music_id, current=0):
        now_time=get_time()
        current = list(itertools.repeat(current,len(name)))
        now_time = list(itertools.repeat(now_time,len(name)))
        data_bulk = np.vstack((name, music_id, current, now_time)).T
        #获取当前的播放位置
        try:
            current_position = self.df.loc[self.df['current']==1].index.tolist()[0]
        except:
            current_position = -1
        self.df = self.df.head(current_position +1)
        insert_bulk = pd.DataFrame(data_bulk, columns=['name', 'music_id', 'current', 'time'])
        self.df = self.df.append(insert_bulk, ignore_index=True)
        self.df.drop_duplicates(subset='music_id', keep='last', inplace=True)
        self.df = self.df.reset_index(drop=True)

    '''
        保存文件表格到文件
    '''
    def save(self):
        self.df.to_csv(FILEURL, index=False)

    '''
        action{string}: 更新表格中current的位置
            up:向上
            down:向下
    '''
    def update(self, action):
        if action=='up':
            current_position = self.df.loc[self.df['current']==1].index.tolist()[0]
            if current_position == 0:
                pass
            else:
                self.df['current'] = 0
                aim_position = current_position-1
                self.df.at[aim_position,"current"]=1

        if action=='down':
            try:
                current_position = self.df.loc[self.df['current']==1].index.tolist()[0]
            except:
                current_position = -1
            if current_position >= (self.df.shape[0] - 1):
                pass
            else:
                self.df['current'] = 0
                aim_position = current_position+1
                self.df.at[aim_position,"current"]=1

    '''
        获取当前正在播放的歌曲 id
    '''
    def get_current_music_id(self):
        return self.df.loc[self.df['current']==1, "music_id"]._values[0]
       
    '''
        获取当前正在播放的歌曲名称
    ''' 
    def get_current_music_name(self):
        return self.df.loc[self.df['current']==1, "name"]._values[0]