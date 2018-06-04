# coding: utf-8
import vlc
from encode import *
import requests

# 获取歌曲ID 对应的mp3 url
_URL_GET_MP3 = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='


# 通过歌曲 ID获取 mp3地址
def res_get_mp3(music_id):
    first_param = "{\"ids\":\"[%d]\",\"br\":128000,\"csrf_token\":\"\"}" % int(
        music_id)
    params = get_params(first_param)
    return get_json(_URL_GET_MP3, params, get_encSecKey())


class playerAction(object):
    def __init__(self, table):
        self.table = table

    #播放音乐
    def replay(self):
        try:
            self.player.release()
        except Exception as e:
            # print('ignore ==========>'+ str(e))
            pass

        music_id = self.table.get_current_music_id()
        print('开始播放音乐%s' % self.table.get_current_music_name())
        music_url = res_get_mp3(music_id)["data"][0].get("url")
        self.player = vlc.MediaPlayer(music_url)
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.SongFinished)
        self.player.play()

    #暂停音乐
    def pause(self):
        self.player.pause()

    #开始音乐
    def play(self):
        print('开始播放音乐%s' % self.table.get_current_music_name())
        self.player.play()

    #下载音乐
    def download(self):
        music_id = self.table.get_current_music_id()
        music_url = res_get_mp3(music_id)["data"][0].get("url")
        music = requests.get(music_url)
        name = sys.path[0] + "/download/%s.mp3" % music_id
        with open(name, "wb+") as code:
            code.write(music.content)
            print('下载结束')
    
    def SongFinished(self, event):
        del self.player
        print("歌曲结束, 开始下一首")
        self.table.update('down')
        self.replay()