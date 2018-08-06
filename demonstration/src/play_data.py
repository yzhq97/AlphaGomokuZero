#author: Zhuoqian Yang yzhq97@buaa.edu.cn

class PlayData:
    def __init__(self):
        self.easy_black_win = 0
        self.easy_black_draw = 0
        self.easy_black_lose = 0
        self.easy_white_win = 0
        self.easy_white_draw = 0
        self.easy_white_lose = 0
        self.medium_black_win = 0
        self.medium_black_draw = 0
        self.medium_black_lose = 0
        self.medium_white_win = 0
        self.medium_white_draw = 0
        self.medium_white_lose = 0
        self.hard_black_win = 0
        self.hard_black_draw = 0
        self.hard_black_lose = 0
        self.hard_white_win = 0
        self.hard_white_draw = 0
        self.hard_white_lose = 0

    def easy_black_winrate(self):
        all = self.easy_black_win + self.easy_black_lose
        if all == 0: return 0.0
        else: return 1.0 * self.easy_black_win / all

    def easy_white_winrate(self):
        all = self.easy_white_win + self.easy_white_lose
        if all == 0: return 0.0
        else: return 1.0 * self.easy_white_win / all

    def medium_black_winrate(self):
        all = self.medium_black_win + self.medium_black_lose
        if all == 0:
            return 0.0
        else:
            return 1.0 * self.medium_black_win / all

    def medium_white_winrate(self):
        all = self.medium_white_win + self.medium_white_draw + self.medium_white_lose
        if all == 0:
            return 0.0
        else:
            return 1.0 * self.medium_white_win / all

    def hard_black_winrate(self):
        all = self.hard_black_win + self.hard_black_draw + self.hard_black_lose
        if all == 0:
            return 0.0
        else:
            return 1.0 * self.hard_black_win / all

    def hard_white_winrate(self):
        all = self.hard_white_win + self.hard_white_draw + self.hard_white_lose
        if all == 0:
            return 0.0
        else:
            return 1.0 * self.hard_white_win / all

