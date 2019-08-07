#  _*_ coding: utf-8 _*_
'''
时间 : 2019/08/6--21:53
作者 : 'dwb'
'''
import requests, re ,json
from lxml import etree

class Bilibili:
    def __init__(self,av):
        self.av=av
        self.url = 'https://www.bilibili.com/video/av{}/'.format(av)
        # 哔哩哔哩弹幕url
        self.danmu_url= 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        self.oid=0

    def get_html(self,url):
        """发送请求,返回响应"""
        return requests.get(url,headers = self.headers).content.decode()

    def get_xml(self,oid):
        print(oid)
        # oid,设置弹幕请求url
        # 拼接弹幕url,调用函数,发送请求,获取结果
        danmu_xml = self.get_html(self.danmu_url.format(oid)).encode()  # 解析时说有问题,encode()转为byte型
        # print("*****")
        # print(danmu_xml)
        # 将获取到的xml类型转换为etree对象
        xml_etr_obj = etree.HTML(danmu_xml)
        # 获取弹幕列表
        self.danmu = xml_etr_obj.xpath('//d/text()')  # # 解析时
        self.p = xml_etr_obj.xpath('//d/@p')
        # 说有问题,获取结果是用encode()转为byte型

    def get_danmu_str(self, danmu,p,oid):
        """保存弹幕"""
        str='<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>106882099</chatid><mission>0</mission><maxlimit>500</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>'
        for i in range(len(danmu)):
            str += (' <d p="' + p[i] + '">' + danmu[i] + '</d>')
            # print(danmu_str)
            str += ("\n")
        str += ("</i>")
        return str
        # print('保存',str)
    def get_oid(self,av):
        html = self.get_html('https://api.bilibili.com/x/web-interface/view?aid='+av)
        self.oid = re.findall(r'"cid":(\d+),', html)[0]

    def new_save_danmu(self,str):
        """保存弹幕"""
        with open('./bilibili_video/{}/{}-{}.xml'.format(self.video_title,self.av,self.video_title), 'w',encoding="utf-8") as f:
            f.write(str)

    def retern_str(self):
        print(self.url)
        # 发送请求,获取结果
        bi_html = self.get_html(self.url)
        print('获取oid')
        self.get_oid(self.av)
        # self.oid = re.findall(r"/(\d+)-1-30080.m4s\?", bi_html)[0]
        # 请求xml的url并
        self.get_xml(self.oid)
        #保存弹幕
        str=self.get_danmu_str(self.danmu,self.p,self.oid)
        return str

    def get_title(self):
        html = self.get_html('https://api.bilibili.com/x/web-interface/view?aid='+self.av)
        print(html)
        self.video_title = re.findall(r'"part":"(.*?)"', html)[0]
        return self.video_title
        #data["title"].replace(" ", "_")

    def run(self):
        print(self.url)
        # 发送请求,获取结果
        bi_html = self.get_html(self.url)
        print('获取oid')
        self.get_oid(self.av)
        # self.oid = re.findall(r"/(\d+)-1-30080.m4s\?", bi_html)[0]
        # 请求xml的url并
        self.get_xml(self.oid)
        #保存弹幕
        str=self.get_danmu_str(self.danmu,self.p,self.oid)
        # print(str)
        self.new_save_danmu(str)  # 保存
        print('保存成功')

if __name__ == '__main__':
    av = '62263029'
    bili = Bilibili(av)
    bili.run()
'''
第一个参数是弹幕出现的时间以秒数为单位。 
第二个参数是弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕 
第三个参数是字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大 
第四个参数是字体的颜色以HTML颜色的十进制为准 
第五个参数是Unix格式的时间戳。基准时间为 1970-1-1 08:00:00 
第六个参数是弹幕池 0普通池 1字幕池 2特殊池【目前特殊池为高级弹幕专用】 
第七个参数是发送者的ID，用于“屏蔽此弹幕的发送者”功能 
第八个参数是弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。
'''