#author: Zhuoqian Yang yzhq97@buaa.edu.cn

class CrossPoint:

    def __init__(self, x, y, M):
        self.x = x
        self.y = y
        self.pixel_x = M + M * self.x
        self.pixel_y = M + M * self.y