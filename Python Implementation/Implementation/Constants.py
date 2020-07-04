def Nb():
    # The number of 32-bit words in the state array
    return 4

def Nk():
    # The number of 32-bit words in the cipher key
    return 4
    # IE, 128-bit keys only are supported

def Nr():
    # The number of rounds of scrambling to be applied to each 128-bit group of words
    return Nk() + 6