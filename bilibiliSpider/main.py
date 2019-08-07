#  _*_ coding: utf-8 _*_
'''
地址 : https://github.com/qq843399535/bilibiliSpider
时间 : 2019/08/6--21:53
作者 : 'dwb'
'''
import Niconvert
import bilibili_spider
import bilibili_video_download_v2

#Bilibili
class testAss:
    def __init__(self,av):
        self.input = ""
        self.resolution = "1920:1080"
        self.font_name = "微软雅黑"
        self.font_size = 32
        self.line_count = 8
        self.bottom_margin = 0
        self.shift = 0
        self.av = av
        self.video_title=''
    def get_ass(self):
        b=bilibili_spider.Bilibili(self.av)
        self.video_title=b.get_title()
        self.input = b.retern_str()
        # with open("./{}.xml".format(oid), 'r', encoding='utf-8') as file:
        #     input=file.read()
        ass_str = Niconvert.xmlToAss.convert(self.input, self.resolution, self.font_name, self.font_size, self.line_count, self.bottom_margin, self.shift)
        url='./bilibili_video/'+self.video_title+'/av'+self.av+'-'+self.video_title+'.ass'
        with open(url, 'w', encoding="utf_8_sig") as f:
            # print(type(danmu))
            f.write(ass_str)#.encode(encoding='UTF-8').decode(encoding="Unicode")


if __name__ == '__main__':
    # av号
    av = '62119074'
    test = testAss(av)
    #从coookie中获取SESSDATA，为空只能下载360p
    SESSDATA = ''
    bilibili_video_download_v2.run(av,SESSDATA)
    print("******************************B站弹幕下载******************************")
    test.get_ass()
