def is_chinese(char):
    code_point = ord(char)
    return (0x4E00 <= code_point <= 0x9FFF) or \
           (0x3400 <= code_point <= 0x4DBF) or \
           (0x20000 <= code_point <= 0x2A6DF) or \
           (0x2A700 <= code_point <= 0x2B73F) or \
           (0x2B740 <= code_point <= 0x2B81F) or \
           (0x2B820 <= code_point <= 0x2CEAF) or \
           (0x2CEB0 <= code_point <= 0x2EBEF)
