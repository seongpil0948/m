# self 는 클래스 그자체
class sp:
    def __init__(self, *args, **kwargs):
        if 'sp' in args:
            self.name = 'sp'
        elif 'seongpil' in kwargs:
            self.name = kwargs.pop('seongpil', None) 
        self.stock += 1
        print(f"calling init stock is {self.stock}")
    def myname(self):
        print(f'my name is {self.name} in class sp')
    
    def __del__(self):
        print(f"calling __Del__({self})")


class sp_wife(sp):
    def __init__(self):
        super().__init__()
        self.stock += 1
        print(f"calling init stock is {self.stock}")    
    def myname(self):
        print(f'overriden my name is {self.name}')

    def __del__(self):
        print(f"calling __Del__({self})")        


class spchild(sp, sp_wife):
    def __init__(self):
        super(self, sp).__init__(['sp', 'sp_wife', 'sp_child'], {'seongpil': 1})
        self.stock += 1
        print(f"calling init stock is {self.stock}")
    
    def myname(self):
        super(self, sp_wife).myname()

    def hi(self):
        print(f' my name is {self.name} place of {__name__}') # class name

    def __del__(self):
        print(f"calling __Del__({self})")


pil = sp({'seongpil'})
