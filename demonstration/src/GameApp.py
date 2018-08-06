#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import tkinter as tk
import sys
import os
import pickle
import src.config as config
from src.WelcomeScene import WelcomeScene
from src.IdleScene import IdleScene
from src.OrderSelectionScene import OrderSelectionScene
from src.GameScene import GameScene
from src.ThinkScene import ThinkScene
from src.play_data import PlayData

class GameApp:
    def __init__(self, master, win2):
        self.root = master
        self.win2 = win2

        self.root.configure(background=config.BGCOLOR)
        self.win2.configure(background=config.BGCOLOR)
        # self.scn_width = self.root.winfo_screenwidth()
        # self.scn_height = self.root.winfo_screenheight()
        self.scn_width = 1920
        self.scn_height = 1080

        self.root.geometry('%dx%d%+d+%d' % (self.scn_width, self.scn_height, 0, 0))
        # self.win2.geometry('%dx%d%+d+%d' % (self.scn_width, self.scn_height, 0, -self.scn_height))
        self.win2.geometry('%dx%d%+d+%d' % (self.scn_width, self.scn_height, 0, 0))
        # self.root.attributes("-fullscreen", True)
        # self.win2.attributes("-fullscreen", True)

        self.model = None
        self.human_order = None

        self.play_data_file = os.path.join('.', 'static', 'play_data.pkl')
        self.play_data = None
        self.init_data_file()

        self.board = None
        self.mcts_root = None

        self.welcome_scene = WelcomeScene(self.root, self)
        self.idle_scene = IdleScene(self.win2, self)
        self.order_selection_scene = OrderSelectionScene(self.root, self)
        self.game_scene = GameScene(self.root, self)
        self.think_scene = ThinkScene(self.win2, self, None, None)

        self.welcome_scene.pack()
        self.idle_scene.pack()
        self.root.bind("<Escape>", self.exit)

    def on_select_difficulty_finish(self):
        self.welcome_scene.pack_forget()
        self.order_selection_scene.pack()

    def on_select_order_finish(self):
        self.order_selection_scene.pack_forget()
        self.game_scene.start_game(self.model, self.human_order)
        self.game_scene.pack()

    def show_think(self):
        if self.board is None: return
        self.idle_scene.pack_forget()
        self.think_scene.board = self.board
        self.think_scene.mcts_root = self.mcts_root
        self.think_scene.show()
        # self.game_scene.pack_forget()
        self.think_scene.pack()

    def show_think_finish(self):
        del self.board
        del self.mcts_root
        # self.think_scene.pack_forget()
        # del self.think_scene
        # self.game_scene.pack()

    def on_game_exit(self):
        self.game_scene.pack_forget()
        self.think_scene.pack_forget()
        self.think_scene.reset()
        self.idle_scene.pack()
        self.welcome_scene.pack()

    def on_game_end(self, winner):
        self.save_data(winner)

    def exit(self, arg):
        sys.exit(0)

    def new_data_file(self):
        self.play_data = PlayData()
        with open(self.play_data_file, 'wb') as output:
            pickle.dump(self.play_data, output, pickle.HIGHEST_PROTOCOL)


    def init_data_file(self):
        if os.path.isfile(self.play_data_file):
            with open(self.play_data_file, 'rb') as input:
                self.play_data = pickle.load(input)
        else:
            self.new_data_file()

    def save_data(self, winner):
        if self.model == config.MODEL_EASY:
            if self.human_order == 1:
                if winner == 1 - self.human_order:
                    self.play_data.easy_black_win += 1
                elif winner == self.human_order:
                    self.play_data.easy_black_lose += 1
                else:
                    self.play_data.easy_black_draw += 1
            else:
                if winner == 1 - self.human_order:
                    self.play_data.easy_white_win += 1
                elif winner == self.human_order:
                    self.play_data.easy_white_lose += 1
                else:
                    self.play_data.easy_white_draw += 1
        if self.model == config.MODEL_MED:
            if self.human_order == 1:
                if winner == 1 - self.human_order:
                    self.play_data.medium_black_win += 1
                elif winner == self.human_order:
                    self.play_data.medium_black_lose += 1
                else:
                    self.play_data.medium_black_draw += 1
            else:
                if winner == 1 - self.human_order:
                    self.play_data.medium_white_win += 1
                elif winner == self.human_order:
                    self.play_data.medium_white_lose += 1
                else:
                    self.play_data.medium_white_draw += 1
        if self.model == config.MODEL_HARD:
            if self.human_order == 1:
                if winner == 1 - self.human_order:
                    self.play_data.hard_black_win += 1
                elif winner == self.human_order:
                    self.play_data.hard_black_lose += 1
                else:
                    self.play_data.hard_black_draw += 1
            else:
                if winner == 1 - self.human_order:
                    self.play_data.hard_white_win += 1
                elif winner == self.human_order:
                    self.play_data.hard_white_lose += 1
                else:
                    self.play_data.hard_white_draw += 1

        self.welcome_scene.show_play_data()
        with open(self.play_data_file, 'wb') as output:
            pickle.dump(self.play_data, output)


