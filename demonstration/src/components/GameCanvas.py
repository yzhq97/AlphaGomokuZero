#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import math
import src.config as config
from src.components.ChessCanvas import ChessCanvas
from src.model.Gomoku import Board
from src.model.MCTS_AlphaZero import MCTSPlayer
from src.model.PVN_11 import PolicyValueNet
from copy import deepcopy
import sys


class GameCanvas(ChessCanvas):

    def __init__(self, master, scene):
        ChessCanvas.__init__(self, master, config.N, scene.M)
        self.scene = scene
        self.N = config.N
        self.M = scene.M

        self.board = Board(self.N)

        self.colors = ["black", "white"]

        self.last_location = None

        self.ai_ready = False
        self.ai_probs = None
        # self.ai_prob_vis = [[None for _ in range(self.N)] for _ in range(self.N)]
        self.ai_location = None
        self.pvn = None
        self.ai = None

        self.think_path_is_shown = False
        self.ended = False
        self.ai_thinking = False

    def reset(self):
        self.board.init_board(0)
        self.ai_ready = False
        self.ai_location = None
        self.last_location = None
        ChessCanvas.reset(self)

    def init_ai(self, model_file, play_out):
        self.pvn = PolicyValueNet(self.N, self.N, model_file)
        self.ai = MCTSPlayer(self.pvn.policy_value_fn,
                             c_puct=5,
                             n_playout=play_out)

    def game_start(self):
        self.reset()
        self.init_ai(self.scene.model, config.PLAYOUT)
        self.human_order = self.scene.human_order
        self.ai_order = 1 - self.scene.human_order
        if self.ai_order == 0:
            self.scene.show_message("AI思考中")
            self.after(50, self.ai_move)
        else:
            self.scene.show_message("由您先开始")
            self.bind('<Button-1>', self.mouse_click)

    def place_location(self, location):
        current_player = self.board.get_current_player()

        if self.last_location is not None:
            self.delete_location(self.last_location)
            if current_player == 0:
                self.render_location(self.last_location, self.piece_size, 'white')
            else:
                self.render_location(self.last_location, self.piece_size, 'black')
        self.last_location = location

        if current_player == 0:
            self.render_location(location, self.piece_size, 'black', outline=config.PROB_COLOR, width=5.0)
        else:
            self.render_location(location, self.piece_size, 'white', outline=config.PROB_COLOR, width=5.0)

        self.board.do_location(location)

        current_player = self.board.get_current_player()
        if current_player == self.human_order:
            self.scene.show_message(u"这一轮由您走")
        else:
            self.scene.show_message(u"AI思考中")

        self.think_path_is_shown = False
        return self.board.game_end()

    def game_end(self, winner):
        if winner == -1:
            self.scene.show_message(u"游戏结束，平局")
        elif winner == self.human_order:
            self.scene.show_message(u"恭喜您获得了胜利！")
        else:
            self.scene.show_message(u"AI获得了胜利")
        self.scene.on_game_end(winner)
        self.unbind("<Button-1>")
        self.pvn.close()

    def mouse_click(self, event):
        if self.ai_thinking: return

        N, M = self.N, self.M

        human_location = None
        mouse_found = False
        for i in range(N):
            if mouse_found: break
            for j in range(N):
                square_distance = math.pow((event.x - self.chess_points[i][j].pixel_x), 2) \
                                  + math.pow((event.y - self.chess_points[i][j].pixel_y), 2)
                distance = square_distance ** 0.5
                human_location = (i, j)
                if (distance < self.M/2.0) and \
                        self.board.location_is_valid(human_location):
                    mouse_found = True
                    break

        if not mouse_found: return

        current_player = self.board.get_current_player()
        if current_player != self.human_order: return

        end, winner = self.place_location(human_location)
        if end: self.game_end(winner)
        else:
            self.after(50, self.ai_move)

    def ai_think(self):
        self.show_think_finish()

        self.unbind("<Button-1>")
        self.ai_thinking = True
        self.scene.show_message(u"AI思考中")
        if self.ai_ready:
            return

        ai_move, self.ai_probs, mcts_root = self.ai.get_action(self.board, temp=1e-6, return_prob=True)
        self.ai_location = Board.move_to_location(ai_move, self.N)

        self.scene.board = self.board
        self.scene.mcts_root = mcts_root

        self.ai_ready = True
        self.ai_thinking = False
        self.scene.show_think(self.scene.board, self.scene.mcts_root)
        self.bind('<Button-1>', self.mouse_click)

    def show_think_finish(self):
        self.scene.show_think_finish()

    def ai_move(self):
        if self.ended:
            return
        if self.board.current_player != self.ai_order:
            return
        if not self.ai_ready:
            self.ai_think()

        end, winner = self.place_location(self.ai_location)
        if end: self.game_end(winner)

        self.ai_ready = False











