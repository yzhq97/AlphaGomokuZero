#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import os

N = 11
PLAYOUT = 500
MODEL_EASY = os.path.join(".", "mdl", "gomoku_11x11_2000.model")
MODEL_MED  = os.path.join(".", "mdl", "gomoku_11x11_3000.model")
MODEL_HARD = os.path.join(".", "mdl", "gomoku_11x11_5000.model")

BGCOLOR = "#fdf6E3"
PROB_COLOR = "#64b5f6"
CURR_COLOR = "#ff5252"
FONTFAMILY = "微软雅黑"

THINK_DESC = u"屏幕中展示了AI在接下来三轮的外推中，对它认为最好的三种走法的外推情况。红色的棋子是AI当前评估的走法，蓝色的点是AI认为您会下棋的位置，大小表示概率。\n\n"+\
             u"AI的思考方式：AI先用神经网络分析棋局，然后对未来可能的情况进行外推。AI在外推时会选择最佳的走法，同时假设对手也会选择最佳的走法。"
