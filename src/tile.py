import textures

# 16 different possible tiles
# 1  | all open
# 2  | top open
# 3  | right open
# 4  | bottom open
# 5  | left open
# 6  | top and bottom open
# 7  | left and right open
# 8  | top and right open
# 9  | right and bottom open
# 10 | bottom and left open
# 11 | left and top open
# 12 | top closed
# 13 | right closed
# 14 | bottom closed
# 15 | left closed
# 16 | all closed

class Tiles:
    def __init__(self, textures : textures[16]):
        self.textures = textures
        pass

    def get_1(self) -> textures:
        return self.textures[0]

    def get_2(self) -> textures:
        return self.textures[1]

    def get_3(self) -> textures:
        return self.textures[2]

    def get_4(self) -> textures:
        return self.textures[3]

    def get_5(self) -> textures:
        return self.textures[4]

    def get_6(self) -> textures:
        return self.textures[5]

    def get_7(self) -> textures:
        return self.textures[6]

    def get_8(self) -> textures:
        return self.textures[7]

    def get_9(self) -> textures:
        return self.textures[8]

    def get_10(self) -> textures:
        return self.textures[9]

    def get_11(self) -> textures:
        return self.textures[10]

    def get_12(self) -> textures:
        return self.textures[11]

    def get_13(self) -> textures:
        return self.textures[12]

    def get_14(self) -> textures:
        return self.textures[13]

    def get_15(self) -> textures:
        return self.textures[14]

    def get_16(self) -> textures:
        return self.textures[15]

