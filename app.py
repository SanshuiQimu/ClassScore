#!/usr/bin/env python3
"""
高一11班积分管理系统 - Flask应用
包含：积分查询、问题反馈、积分兑换、管理员后台
"""

from flask import Flask, render_template, jsonify, request, session
from functools import wraps
import json
import os
import hashlib
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# 数据存储文件
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

FEEDBACK_FILE = os.path.join(DATA_DIR, 'feedback.json')
EXCHANGE_FILE = os.path.join(DATA_DIR, 'exchange.json')
SCORE_CHANGES_FILE = os.path.join(DATA_DIR, 'score_changes.json')

# 管理员账号
ADMIN_USERNAME = "ssqm100716"
ADMIN_PASSWORD = "lkx123456."

# 积分数据
SCORE_DATA = {
    "5": {
        "陈晨": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "陈浩": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "陈嘉悦": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "陈文磊": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "陈奕兴": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "陈子菡": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "董煜": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":30,"累计得分":29},
        "段伟豪": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":-2,"3月月末加分":0,"累计得分":-3},
        "方道锐": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":-1},
        "何静怡": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "黄崇强": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "黄麒睿": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":30,"累计得分":29},
        "黄永俊": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "金礼胜": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":40,"累计得分":39},
        "金睿": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "李道旭": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "李佳妍": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":35,"累计得分":34},
        "李祉葶": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "林成旭": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "林嘉琦": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":-1},
        "林家宝": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "林可翔": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":40,"累计得分":39},
        "林志豪": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":20,"累计得分":23},
        "卢霖凯": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "吕明磊": {"原始积分":0,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":20,"累计得分":19},
        "缪佳宁": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "夏锴": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "夏贻恒": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "谢锡俊": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "杨成辉": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "杨嘉乐": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "叶彤": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "应天乐": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "尤圣晨": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "余鑫": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "张怀文": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "张紫懿": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "郑高翔": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "郑书杰": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "郑意佳": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "周欣悦": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "朱型权": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "朱子龙": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3},
        "朱紫贤": {"原始积分":0,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":3}
    },
    "6": {
        "陈晨": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "陈浩": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "陈嘉悦": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "陈文磊": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "陈奕兴": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "陈子菡": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "董煜": {"原始积分":29,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":28},
        "段伟豪": {"原始积分":-3,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":-4},
        "方道锐": {"原始积分":-1,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":-2},
        "何静怡": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "黄崇强": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "黄麒睿": {"原始积分":29,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":28},
        "黄永俊": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "金礼胜": {"原始积分":39,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":38},
        "金睿": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "李道旭": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "李佳妍": {"原始积分":34,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":33},
        "李祉葶": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "林成旭": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "林嘉琦": {"原始积分":-1,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":-2},
        "林家宝": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "林可翔": {"原始积分":39,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":38},
        "林志豪": {"原始积分":23,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":26},
        "卢霖凯": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "吕明磊": {"原始积分":19,"作业全勤积分":-1,"卫生与其他":0,"3月月末加分":0,"累计得分":18},
        "缪佳宁": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "夏锴": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "夏贻恒": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "谢锡俊": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "杨成辉": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "杨嘉乐": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "叶彤": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "应天乐": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "尤圣晨": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "余鑫": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "张怀文": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "张紫懿": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "郑高翔": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "郑书杰": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "郑意佳": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "周欣悦": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "朱型权": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "朱子龙": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6},
        "朱紫贤": {"原始积分":3,"作业全勤积分":3,"卫生与其他":0,"3月月末加分":0,"累计得分":6}
    },
    "15": {
        "陈晨": {"原始积分":117.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":8,"累计得分":131.5},
        "陈浩": {"原始积分":111,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-5,"累计得分":112},
        "陈嘉悦": {"原始积分":119.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":125.5},
        "陈文磊": {"原始积分":118,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":124},
        "陈奕兴": {"原始积分":59,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-1.5,"累计得分":63.5},
        "陈子菡": {"原始积分":76,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":82},
        "董煜": {"原始积分":209.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":215.5},
        "段伟豪": {"原始积分":40,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":46},
        "方道锐": {"原始积分":22.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":28.5},
        "何静怡": {"原始积分":130,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":136},
        "黄崇强": {"原始积分":92.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-5,"累计得分":93.5},
        "黄麒睿": {"原始积分":185.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":191.5},
        "黄永俊": {"原始积分":55.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":61.5},
        "金礼胜": {"原始积分":207.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":213.5},
        "金睿": {"原始积分":120,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":6.5,"累计得分":132.5},
        "李道旭": {"原始积分":106,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-5,"累计得分":107},
        "李佳妍": {"原始积分":210,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":216},
        "李祉葶": {"原始积分":162,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":168},
        "林成旭": {"原始积分":64,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":70},
        "林嘉琦": {"原始积分":32,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":38},
        "林家宝": {"原始积分":147,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":153},
        "林可翔": {"原始积分":236,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-5,"累计得分":237},
        "林志豪": {"原始积分":115,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-1.5,"累计得分":119.5},
        "卢霖凯": {"原始积分":202,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-1.5,"累计得分":206.5},
        "吕明磊": {"原始积分":35,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":41},
        "缪佳宁": {"原始积分":96.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":102.5},
        "夏锴": {"原始积分":79.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":85.5},
        "夏贻恒": {"原始积分":101.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":107.5},
        "谢锡俊": {"原始积分":134.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":140.5},
        "杨成辉": {"原始积分":87,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":93},
        "杨嘉乐": {"原始积分":97,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-5,"累计得分":98},
        "叶彤": {"原始积分":60.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":66.5},
        "应天乐": {"原始积分":95.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":101.5},
        "尤圣晨": {"原始积分":41.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":47.5},
        "余鑫": {"原始积分":152.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":158.5},
        "张怀文": {"原始积分":216.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":222.5},
        "张紫懿": {"原始积分":73.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":79.5},
        "郑高翔": {"原始积分":54,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":60},
        "郑书杰": {"原始积分":134.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":140.5},
        "郑意佳": {"原始积分":59.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":65.5},
        "周欣悦": {"原始积分":53.5,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":59.5},
        "朱型权": {"原始积分":129,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":-1.5,"累计得分":133.5},
        "朱子龙": {"原始积分":76,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":0,"累计得分":82},
        "朱紫贤": {"原始积分":153,"作业全勤积分":3,"礼立班积分":3,"卫生与其他":9,"累计得分":168}
    },
    "15": {"\u6797\u53ef\u7fd4": {"\u539f\u59cb\u79ef\u5206": 236.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 68.0, "\u7d2f\u8ba1\u5f97\u5206": 304.0}, "\u8463\u715c": {"\u539f\u59cb\u79ef\u5206": 209.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 94.0, "\u7d2f\u8ba1\u5f97\u5206": 303.5}, "\u5f20\u6000\u6587": {"\u539f\u59cb\u79ef\u5206": 216.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 53.0, "\u7d2f\u8ba1\u5f97\u5206": 269.5}, "\u91d1\u793c\u80dc": {"\u539f\u59cb\u79ef\u5206": 207.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u7d2f\u8ba1\u5f97\u5206": 250.5}, "\u674e\u4f73\u598d": {"\u539f\u59cb\u79ef\u5206": 210.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u7d2f\u8ba1\u5f97\u5206": 253.0}, "\u5362\u9716\u51ef": {"\u539f\u59cb\u79ef\u5206": 202.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u7d2f\u8ba1\u5f97\u5206": 245.0}, "\u9ec4\u9e92\u777f": {"\u539f\u59cb\u79ef\u5206": 185.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 52.0, "\u7d2f\u8ba1\u5f97\u5206": 237.5}, "\u8c22\u9521\u4fca": {"\u539f\u59cb\u79ef\u5206": 134.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 94.0, "\u7d2f\u8ba1\u5f97\u5206": 228.5}, "\u6797\u5bb6\u5b9d": {"\u539f\u59cb\u79ef\u5206": 147.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 96.0, "\u7d2f\u8ba1\u5f97\u5206": 243.0}, "\u674e\u7949\u8476": {"\u539f\u59cb\u79ef\u5206": 162.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 52.0, "\u7d2f\u8ba1\u5f97\u5206": 214.0}, "\u4f55\u9759\u6021": {"\u539f\u59cb\u79ef\u5206": 130.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 91.0, "\u7d2f\u8ba1\u5f97\u5206": 221.0}, "\u6731\u578b\u6743": {"\u539f\u59cb\u79ef\u5206": 129.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 68.0, "\u7d2f\u8ba1\u5f97\u5206": 197.0}, "\u90d1\u4e66\u6770": {"\u539f\u59cb\u79ef\u5206": 134.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 56.0, "\u7d2f\u8ba1\u5f97\u5206": 190.5}, "\u9648\u6d69": {"\u539f\u59cb\u79ef\u5206": 111.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u7d2f\u8ba1\u5f97\u5206": 144.0}, "\u4f59\u946b": {"\u539f\u59cb\u79ef\u5206": 152.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 176.5}, "\u6731\u7d2b\u8d24": {"\u539f\u59cb\u79ef\u5206": 153.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u7d2f\u8ba1\u5f97\u5206": 176.0}, "\u5e94\u5929\u4e50": {"\u539f\u59cb\u79ef\u5206": 95.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 93.0, "\u7d2f\u8ba1\u5f97\u5206": 188.5}, "\u91d1\u777f": {"\u539f\u59cb\u79ef\u5206": 120.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 67.0, "\u7d2f\u8ba1\u5f97\u5206": 187.0}, "\u9648\u5609\u60a6": {"\u539f\u59cb\u79ef\u5206": 119.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u7d2f\u8ba1\u5f97\u5206": 152.5}, "\u9648\u6587\u78ca": {"\u539f\u59cb\u79ef\u5206": 118.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 142.0}, "\u9648\u6668": {"\u539f\u59cb\u79ef\u5206": 117.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 22.0, "\u7d2f\u8ba1\u5f97\u5206": 139.5}, "\u6797\u5fd7\u8c6a": {"\u539f\u59cb\u79ef\u5206": 115.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 139.0}, "\u9648\u5b50\u83e1": {"\u539f\u59cb\u79ef\u5206": 76.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 66.0, "\u7d2f\u8ba1\u5f97\u5206": 142.0}, "\u590f\u8d3b\u6052": {"\u539f\u59cb\u79ef\u5206": 101.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 125.5}, "\u7f2a\u4f73\u5b81": {"\u539f\u59cb\u79ef\u5206": 96.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 116.5}, "\u674e\u9053\u65ed": {"\u539f\u59cb\u79ef\u5206": 106.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 130.0}, "\u9ec4\u5d07\u5f3a": {"\u539f\u59cb\u79ef\u5206": 92.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 34.0, "\u7d2f\u8ba1\u5f97\u5206": 126.5}, "\u9648\u5955\u5174": {"\u539f\u59cb\u79ef\u5206": 59.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 66.0, "\u7d2f\u8ba1\u5f97\u5206": 125.0}, "\u6768\u5609\u4e50": {"\u539f\u59cb\u79ef\u5206": 97.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 121.0}, "\u6768\u6210\u8f89": {"\u539f\u59cb\u79ef\u5206": 87.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u7d2f\u8ba1\u5f97\u5206": 110.0}, "\u5f20\u7d2b\u61ff": {"\u539f\u59cb\u79ef\u5206": 73.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u7d2f\u8ba1\u5f97\u5206": 106.5}, "\u590f\u9534": {"\u539f\u59cb\u79ef\u5206": 79.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 103.5}, "\u6731\u5b50\u9f99": {"\u539f\u59cb\u79ef\u5206": 76.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u9ec4\u6c38\u4fca": {"\u539f\u59cb\u79ef\u5206": 55.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 1.5, "\u671f\u672b\u52a0\u5206": 43.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u53f6\u5f64": {"\u539f\u59cb\u79ef\u5206": 60.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 6.5, "\u671f\u672b\u52a0\u5206": 33.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5c24\u5723\u6668": {"\u539f\u59cb\u79ef\u5206": 41.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 6.5, "\u671f\u672b\u52a0\u5206": 52.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6797\u6210\u65ed": {"\u539f\u59cb\u79ef\u5206": 64.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 13.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u90d1\u610f\u4f73": {"\u539f\u59cb\u79ef\u5206": 59.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 17.5, "\u671f\u672b\u52a0\u5206": 23.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5415\u660e\u78ca": {"\u539f\u59cb\u79ef\u5206": 35.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 22.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u90d1\u9ad8\u7fd4": {"\u539f\u59cb\u79ef\u5206": 54.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 23.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5468\u6b23\u60a6": {"\u539f\u59cb\u79ef\u5206": 53.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 24.5, "\u671f\u672b\u52a0\u5206": 22.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6bb5\u4f1f\u8c6a": {"\u539f\u59cb\u79ef\u5206": 40.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 36.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6797\u5609\u7426": {"\u539f\u59cb\u79ef\u5206": 32.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 46.0, "\u671f\u672b\u52a0\u5206": 22.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u65b9\u9053\u9510": {"\u539f\u59cb\u79ef\u5206": 22.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 22.5}},
    "16": {"\u6797\u53ef\u7fd4": {"\u539f\u59cb\u79ef\u5206": 236.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 68.0, "\u6708\u672b\u52a0\u5206": 40.0, "\u7d2f\u8ba1\u5f97\u5206": 344.0}, "\u8463\u715c": {"\u539f\u59cb\u79ef\u5206": 209.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 94.0, "\u6708\u672b\u52a0\u5206": 30.0, "\u7d2f\u8ba1\u5f97\u5206": 333.5}, "\u5f20\u6000\u6587": {"\u539f\u59cb\u79ef\u5206": 216.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 53.0, "\u6708\u672b\u52a0\u5206": 25.0, "\u7d2f\u8ba1\u5f97\u5206": 294.5}, "\u91d1\u793c\u80dc": {"\u539f\u59cb\u79ef\u5206": 207.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u6708\u672b\u52a0\u5206": 40.0, "\u7d2f\u8ba1\u5f97\u5206": 290.5}, "\u674e\u4f73\u598d": {"\u539f\u59cb\u79ef\u5206": 210.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u6708\u672b\u52a0\u5206": 35.0, "\u7d2f\u8ba1\u5f97\u5206": 288.0}, "\u5362\u9716\u51ef": {"\u539f\u59cb\u79ef\u5206": 202.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 265.0}, "\u9ec4\u9e92\u777f": {"\u539f\u59cb\u79ef\u5206": 185.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 52.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 257.5}, "\u8c22\u9521\u4fca": {"\u539f\u59cb\u79ef\u5206": 134.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 94.0, "\u6708\u672b\u52a0\u5206": 15.0, "\u7d2f\u8ba1\u5f97\u5206": 243.5}, "\u6797\u5bb6\u5b9d": {"\u539f\u59cb\u79ef\u5206": 147.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 96.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 243.0}, "\u674e\u7949\u8476": {"\u539f\u59cb\u79ef\u5206": 162.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 52.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 234.0}, "\u4f55\u9759\u6021": {"\u539f\u59cb\u79ef\u5206": 130.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 91.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 221.0}, "\u6731\u578b\u6743": {"\u539f\u59cb\u79ef\u5206": 129.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 68.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 217.0}, "\u90d1\u4e66\u6770": {"\u539f\u59cb\u79ef\u5206": 134.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 56.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 210.5}, "\u9648\u6d69": {"\u539f\u59cb\u79ef\u5206": 111.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u6708\u672b\u52a0\u5206": 60.0, "\u7d2f\u8ba1\u5f97\u5206": 204.0}, "\u4f59\u946b": {"\u539f\u59cb\u79ef\u5206": 152.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 27.5, "\u7d2f\u8ba1\u5f97\u5206": 204.0}, "\u6731\u7d2b\u8d24": {"\u539f\u59cb\u79ef\u5206": 153.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 196.0}, "\u5e94\u5929\u4e50": {"\u539f\u59cb\u79ef\u5206": 95.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 93.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 188.5}, "\u91d1\u777f": {"\u539f\u59cb\u79ef\u5206": 120.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 67.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 187.0}, "\u9648\u5609\u60a6": {"\u539f\u59cb\u79ef\u5206": 119.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 172.5}, "\u9648\u6587\u78ca": {"\u539f\u59cb\u79ef\u5206": 118.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 162.0}, "\u9648\u6668": {"\u539f\u59cb\u79ef\u5206": 117.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 22.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 159.5}, "\u6797\u5fd7\u8c6a": {"\u539f\u59cb\u79ef\u5206": 115.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 159.0}, "\u9648\u5b50\u83e1": {"\u539f\u59cb\u79ef\u5206": 76.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 66.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 142.0}, "\u590f\u8d3b\u6052": {"\u539f\u59cb\u79ef\u5206": 101.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 15.0, "\u7d2f\u8ba1\u5f97\u5206": 140.5}, "\u7f2a\u4f73\u5b81": {"\u539f\u59cb\u79ef\u5206": 96.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 20.0, "\u6708\u672b\u52a0\u5206": 20.0, "\u7d2f\u8ba1\u5f97\u5206": 136.5}, "\u674e\u9053\u65ed": {"\u539f\u59cb\u79ef\u5206": 106.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 130.0}, "\u9ec4\u5d07\u5f3a": {"\u539f\u59cb\u79ef\u5206": 92.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 34.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 126.5}, "\u9648\u5955\u5174": {"\u539f\u59cb\u79ef\u5206": 59.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 66.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 125.0}, "\u6768\u5609\u4e50": {"\u539f\u59cb\u79ef\u5206": 97.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 121.0}, "\u6768\u6210\u8f89": {"\u539f\u59cb\u79ef\u5206": 87.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 110.0}, "\u5f20\u7d2b\u61ff": {"\u539f\u59cb\u79ef\u5206": 73.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 33.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 106.5}, "\u590f\u9534": {"\u539f\u59cb\u79ef\u5206": 79.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 103.5}, "\u6731\u5b50\u9f99": {"\u539f\u59cb\u79ef\u5206": 76.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u9ec4\u6c38\u4fca": {"\u539f\u59cb\u79ef\u5206": 55.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 1.5, "\u671f\u672b\u52a0\u5206": 43.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u53f6\u5f64": {"\u539f\u59cb\u79ef\u5206": 60.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 6.5, "\u671f\u672b\u52a0\u5206": 33.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5c24\u5723\u6668": {"\u539f\u59cb\u79ef\u5206": 41.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 6.5, "\u671f\u672b\u52a0\u5206": 52.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6797\u6210\u65ed": {"\u539f\u59cb\u79ef\u5206": 64.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 13.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u90d1\u610f\u4f73": {"\u539f\u59cb\u79ef\u5206": 59.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 17.5, "\u671f\u672b\u52a0\u5206": 23.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5415\u660e\u78ca": {"\u539f\u59cb\u79ef\u5206": 35.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 22.0, "\u671f\u672b\u52a0\u5206": 43.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u90d1\u9ad8\u7fd4": {"\u539f\u59cb\u79ef\u5206": 54.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 23.0, "\u671f\u672b\u52a0\u5206": 23.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u5468\u6b23\u60a6": {"\u539f\u59cb\u79ef\u5206": 53.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 24.5, "\u671f\u672b\u52a0\u5206": 22.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6bb5\u4f1f\u8c6a": {"\u539f\u59cb\u79ef\u5206": 40.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 36.0, "\u671f\u672b\u52a0\u5206": 24.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u6797\u5609\u7426": {"\u539f\u59cb\u79ef\u5206": 32.0, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 46.0, "\u671f\u672b\u52a0\u5206": 22.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 100.0}, "\u65b9\u9053\u9510": {"\u539f\u59cb\u79ef\u5206": 22.5, "\u73ed\u7ea7\u79ef\u5206\u8865\u507f\u673a\u5236": 0.0, "\u671f\u672b\u52a0\u5206": 0.0, "\u6708\u672b\u52a0\u5206": 0.0, "\u7d2f\u8ba1\u5f97\u5206": 22.5}}
}

# 动态积分变动存储
score_changes = {}

def load_data(filepath):
    """加载JSON数据"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(filepath, data):
    """保存JSON数据"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def admin_required(f):
    """管理员权限检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({"error": "需要管理员权限"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/score/<week>/<name>')
def get_score(week, name):
    """获取指定周次和姓名的积分"""
    if week not in SCORE_DATA:
        return jsonify({"error": "周次不存在"}), 404
    
    if name not in SCORE_DATA[week]:
        return jsonify({"error": "姓名不存在"}), 404
    
    # 合并动态积分变动 - 从文件实时读取
    data = SCORE_DATA[week][name].copy()
    changes = load_data(SCORE_CHANGES_FILE)
    total_change = sum(c.get('change', 0) for c in changes if c.get('name') == name)
    data['累计得分'] = data.get('累计得分', 0) + total_change
    
    return jsonify({
        "week": week,
        "name": name,
        "data": data
    })

@app.route('/api/score/<week>')
def get_week_scores(week):
    """获取指定周次的所有积分"""
    if week not in SCORE_DATA:
        return jsonify({"error": "周次不存在"}), 404
    
    # 合并动态积分变动 - 从文件实时读取
    data = SCORE_DATA[week].copy()
    changes = load_data(SCORE_CHANGES_FILE)
    
    # 计算每个学生的总变动
    student_changes = {}
    for c in changes:
        name = c.get('name')
        if name:
            student_changes[name] = student_changes.get(name, 0) + c.get('change', 0)
    
    for name in data:
        if name in student_changes:
            data[name]['累计得分'] = data[name].get('累计得分', 0) + student_changes[name]
    
    return jsonify({
        "week": week,
        "data": data
    })

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交问题反馈"""
    data = request.json
    if not data or not data.get('content'):
        return jsonify({"error": "问题内容不能为空"}), 400
    
    feedback = {
        "id": hashlib.md5(f"{time.time()}{data.get('name','')}".encode()).hexdigest()[:16],
        "content": data.get('content'),
        "name": data.get('name', '匿名'),
        "timestamp": datetime.now().isoformat(),
        "ip": request.remote_addr
    }
    
    feedbacks = load_data(FEEDBACK_FILE)
    feedbacks.append(feedback)
    save_data(FEEDBACK_FILE, feedbacks)
    
    return jsonify({"success": True, "message": "提交成功"})

@app.route('/api/exchange', methods=['POST'])
def submit_exchange():
    """提交积分兑换"""
    data = request.json
    if not data or not data.get('item_name') or not data.get('price') or not data.get('name'):
        return jsonify({"error": "必填项不能为空"}), 400
    
    try:
        price = float(data.get('price', 0))
        points_needed = price * 3
    except:
        return jsonify({"error": "价格格式错误"}), 400
    
    exchange = {
        "id": hashlib.md5(f"{time.time()}{data.get('name','')}".encode()).hexdigest()[:16],
        "item_link": data.get('item_link', '无'),
        "item_name": data.get('item_name'),
        "price": price,
        "points_needed": points_needed,
        "name": data.get('name'),
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
        "ip": request.remote_addr
    }
    
    exchanges = load_data(EXCHANGE_FILE)
    exchanges.append(exchange)
    save_data(EXCHANGE_FILE, exchanges)
    
    return jsonify({"success": True, "message": "提交成功", "points_needed": points_needed})

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.json
    if not data:
        return jsonify({"error": "请求数据不能为空"}), 400
    
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({"success": True, "message": "登录成功"})
    
    return jsonify({"error": "账号或密码错误"}), 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    """管理员登出"""
    session.pop('is_admin', None)
    return jsonify({"success": True})

@app.route('/api/admin/feedback')
@admin_required
def get_feedback():
    """获取所有问题反馈（管理员）"""
    feedbacks = load_data(FEEDBACK_FILE)
    return jsonify(feedbacks)

@app.route('/api/admin/exchange')
@admin_required
def get_exchange():
    """获取所有积分兑换（管理员）"""
    exchanges = load_data(EXCHANGE_FILE)
    return jsonify(exchanges)

@app.route('/api/admin/score-changes')
@admin_required
def get_score_changes():
    """获取所有积分变动记录（管理员）"""
    changes = load_data(SCORE_CHANGES_FILE)
    return jsonify(changes)

@app.route('/api/admin/score-change', methods=['POST'])
@admin_required
def admin_score_change():
    """管理员修改积分"""
    data = request.json
    if not data or not data.get('name') or data.get('change') is None:
        return jsonify({"error": "必填项不能为空"}), 400
    
    name = data.get('name')
    change = float(data.get('change'))
    reason = data.get('reason', '')
    
    # 记录积分变动
    change_record = {
        "id": hashlib.md5(f"{time.time()}{name}".encode()).hexdigest()[:16],
        "name": name,
        "change": change,
        "reason": reason,
        "timestamp": datetime.now().isoformat(),
        "admin": session.get('is_admin', False)
    }
    
    changes = load_data(SCORE_CHANGES_FILE)
    changes.append(change_record)
    save_data(SCORE_CHANGES_FILE, changes)
    
    return jsonify({"success": True, "message": "积分修改成功"})


@app.route('/api/student/total-score/<name>')
def get_student_total_score(name):
    """获取学生总分和所有记录"""
    # 获取最新一周的原始积分
    latest_week = max(SCORE_DATA.keys(), key=lambda x: int(x))
    base_data = SCORE_DATA[latest_week].get(name, {}).copy()
    
    if not base_data:
        return jsonify({"error": "学生不存在"}), 404
    
    base_score = base_data.get('累计得分', 0)
    
    # 加载所有积分变动记录
    changes = load_data(SCORE_CHANGES_FILE)
    student_changes = [c for c in changes if c.get('name') == name]
    
    # 计算动态积分变动总和
    dynamic_change = sum(c.get('change', 0) for c in student_changes)
    
    # 加载所有兑换记录
    exchanges = load_data(EXCHANGE_FILE)
    student_exchanges = [e for e in exchanges if e.get('name') == name]
    
    # 计算已通过兑换消耗的积分
    exchange_deduction = sum(
        e.get('points_needed', 0) 
        for e in student_exchanges 
        if e.get('status') == 'approved'
    )
    
    # 最终总分
    total_score = base_score + dynamic_change - exchange_deduction
    
    # 构建记录列表
    records = []
    
    # 添加积分变动记录
    for change in sorted(student_changes, key=lambda x: x.get('timestamp', ''), reverse=True):
        records.append({
            "type": "score_change",
            "title": "积分变动" if change.get('change', 0) > 0 else "积分扣除",
            "change": change.get('change', 0),
            "reason": change.get('reason', '无原因'),
            "timestamp": change.get('timestamp', ''),
            "status": "已完成"
        })
    
    # 添加兑换记录
    for exchange in sorted(student_exchanges, key=lambda x: x.get('timestamp', ''), reverse=True):
        status = exchange.get('status', 'pending')
        status_text = {
            'pending': '审核中',
            'approved': '已通过',
            'rejected': '已驳回'
        }.get(status, '未知')
        
        records.append({
            "type": "exchange",
            "title": f"积分兑换：{exchange.get('item_name', '未知商品')}",
            "change": -exchange.get('points_needed', 0),
            "reason": f"价格：¥{exchange.get('price', 0)}",
            "timestamp": exchange.get('timestamp', ''),
            "status": status_text,
            "status_code": status
        })
    
    # 按时间排序
    records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        "name": name,
        "base_score": base_score,
        "dynamic_change": dynamic_change,
        "exchange_deduction": exchange_deduction,
        "total_score": total_score,
        "records": records
    })

@app.route('/api/admin/exchange/<exchange_id>/approve', methods=['POST'])
@admin_required
def approve_exchange(exchange_id):
    """同意积分兑换"""
    exchanges = load_data(EXCHANGE_FILE)
    exchange = None
    for e in exchanges:
        if e.get('id') == exchange_id:
            exchange = e
            break
    
    if not exchange:
        return jsonify({"error": "兑换记录不存在"}), 404
    
    if exchange.get('status') == 'approved':
        return jsonify({"error": "该兑换已处理"}), 400
    
    name = exchange.get('name')
    points_needed = exchange.get('points_needed', 0)
    
    # 扣除积分
    change_record = {
        "id": hashlib.md5(f"{time.time()}{name}".encode()).hexdigest()[:16],
        "name": name,
        "change": -points_needed,
        "reason": f"积分兑换：{exchange.get('item_name')}",
        "timestamp": datetime.now().isoformat(),
        "admin": True,
        "exchange_id": exchange_id
    }
    
    changes = load_data(SCORE_CHANGES_FILE)
    changes.append(change_record)
    save_data(SCORE_CHANGES_FILE, changes)
    
    # 更新兑换状态
    exchange['status'] = 'approved'
    exchange['approved_at'] = datetime.now().isoformat()
    save_data(EXCHANGE_FILE, exchanges)
    
    return jsonify({"success": True, "message": "兑换已同意"})

@app.route('/api/admin/exchange/<exchange_id>/reject', methods=['POST'])
@admin_required
def reject_exchange(exchange_id):
    """驳回积分兑换"""
    data = request.json or {}
    reject_reason = data.get('reason', '无原因')
    
    exchanges = load_data(EXCHANGE_FILE)
    exchange = None
    for e in exchanges:
        if e.get('id') == exchange_id:
            exchange = e
            break
    
    if not exchange:
        return jsonify({"error": "兑换记录不存在"}), 404
    
    if exchange.get('status') == 'rejected':
        return jsonify({"error": "该兑换已驳回"}), 400
    
    # 更新兑换状态
    exchange['status'] = 'rejected'
    exchange['reject_reason'] = reject_reason
    exchange['rejected_at'] = datetime.now().isoformat()
    save_data(EXCHANGE_FILE, exchanges)
    
    return jsonify({"success": True, "message": "兑换已驳回"})

@app.route('/api/my-exchanges/<name>')
def get_my_exchanges(name):
    """获取用户的兑换记录（用于显示驳回提示）"""
    exchanges = load_data(EXCHANGE_FILE)
    my_exchanges = [e for e in exchanges if e.get('name') == name and e.get('status') == 'rejected']
    # 清除已查看的标记
    for e in my_exchanges:
        if not e.get('viewed'):
            e['viewed'] = True
    save_data(EXCHANGE_FILE, exchanges)
    return jsonify(my_exchanges)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
