#!/usr/bin/python3
# coding: utf-8
from encode import *
from data import db
from player import playerAction

#import db
table = db()

#import player
player = playerAction(table)

# 线程循环
loop = True

# 获取歌曲ID url
_URL_GET_ID = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='


# 通过歌手或者歌曲获取歌曲ID列表
def res_get_id(song):
    first_param = "{\"s\":\"%s\",\"type\":\"1\",\"offset\":\"0\",\"total\":\"true\",\"limit\":\"90\",\"csrf_token\":\"\"}" % str(
        song)
    params = get_params(first_param)
    return get_json(_URL_GET_ID, params, get_encSecKey())

while loop:
    action = input('请输入操作:')
    action = action.split(' ',1)
    if(action[0] == 'search'):
        try:
            music_id_list = res_get_id(action[1])['result']["songs"]
            music_name = []
            music_id = []
            if len(music_id_list) < 10:
                for index, value in enumerate(music_id_list):
                    music_name.append(music_id_list[index].get('name'))
                    music_id.append(music_id_list[index].get('id'))
            else:
                for index in range(10):
                    music_name.append(music_id_list[index].get('name'))
                    music_id.append(music_id_list[index].get('id'))
            table.insert(music_name, music_id)
            table.update('down')
            player.replay()
        except:
            print("获取歌曲失败")
            # sys.exit()
            pass

    elif action[0] == 'pause':
        player.pause()

    elif action[0] == 'play':
        player.play()

    elif action[0] == 'download':
        player.download()

    elif action[0] == 'down':
        table.update('down')
        player.replay()

    elif action[0] == 'up':
        table.update('up')
        player.replay()
