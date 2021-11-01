class Modify:
    @classmethod
    def pretty(cls, item, title: str, sign=("=",), f_long=150):
        lt = (f_long - len(title)) // 2
        title = title.upper()
        mf = '\n<yellow>{0}{1}{0}</>\n'
        return f'{mf.format(sign[0] * lt, title)}{item}{mf.format(sign[-1] * lt, title)}'

    @classmethod
    def pretty_batch(cls, *items: list):
        return ''.join([cls.pretty(i[0], i[1]) for i in items])
