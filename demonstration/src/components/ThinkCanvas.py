import src.config as config
from src.model.Gomoku import Board
from src.components.ChessCanvas import ChessCanvas
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

class ThinkCanvas(ChessCanvas):

    def __init__(self, master=None, N=8, M=48):
        self.master = master
        ChessCanvas.__init__(self, master, N, M)

        self.colors = ["black", "white"]

        self.value_node = None
        self.board = None
        self.node = None
        self.order = None
        self.location = None
        self.current_player = None

    def reset(self):
        self.board = None
        self.node = None
        self.order = None
        self.location = None
        self.current_player = None
        ChessCanvas.reset(self)

    def recover_state(self, state):
        for (move, player) in state.items():
            location = Board.move_to_location(move, self.N)
            self.render_location(location, self.M/3.0, self.colors[player])

    def place_location(self, location, r, color, outline=None, text=None, text_color=None, width=2.0):
        self.render_location(location, r, color, outline, text, text_color, width)

    def data_check(self, mcts_root, level, order):
        move, node = None, mcts_root
        for i in range(2 * level):
            if node.is_leaf():
                return False
            move, node = node.max_next(1)

        best_moves = node.max_next(3)
        if order >= len(best_moves):
            return False
        # tgt_move, tgt_node = best_moves[order]

        # human_moves = tgt_node.max_next(3)
        # visits_sum = 0
        # for tup in human_moves:
        #     move, node = tup
        #     visits_sum += node.n_visits
        # if visits_sum == 0:
        #     return False

        return True


    def show_think(self, board, mcts_root, level, order):
        self.reset()

        if not self.data_check(mcts_root, level, order):
            return

        self.recover_state(board.states)
        self.current_player = board.get_current_player()

        move, node = None, mcts_root
        for i in range(2 * level):
            move, node = node.max_next(1)
            location = Board.move_to_location(move, self.N)
            r = self.M/3.0
            color = self.colors[self.current_player]
            text = "%d"%(i+1)
            self.place_location(location, r, color, text=text, text_color=config.PROB_COLOR)
            self.current_player = 1 - self.current_player

        best_moves = node.max_next(3)
        if order >= len(best_moves):
            self.clear()
            return
        tgt_move, tgt_node = best_moves[order]
        tgt_location = Board.move_to_location(tgt_move, self.N)
        tgt_color = self.colors[self.current_player]
        text = "%d" % (level * 2 + 1)
        self.place_location(tgt_location, self.M/3.0, outline=config.CURR_COLOR, color=tgt_color, text=text, text_color=config.CURR_COLOR)
        self.current_player = 1 - self.current_player

        human_moves = tgt_node.max_next(3)
        visits_sum = 0
        for tup in human_moves:
            move, node = tup
            visits_sum += node.n_visits
        if visits_sum == 0:
            return
        else:
            for tup in human_moves:
                move, node = tup
                location = Board.move_to_location(move, self.N)
                r = 1.2 * (self.M/3.0) * (0.4 + 0.6*(node.n_visits/visits_sum))
                self.place_location(location, r, color=config.PROB_COLOR)







