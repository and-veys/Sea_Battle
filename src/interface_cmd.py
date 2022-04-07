import os
from .parameters import Parameters, Iterator
class Interface:
    """Класс для работы в CMD"""
    __inst = None                                           
    def __new__(cls, gm = None):
        if(cls.__inst == None): 
            cls.__inst = super().__new__(cls)
            cls.__inst.__init(gm)
        return cls.__inst  
        
    def __init(self, gm):
        self.__game = gm
        self.__result = None       
        self.__cell = {        
                "Cell":         " {:2}",
                "Ship":         " \u25A0 ",
                "Sea":          " \u00B7 ",
                "ShipShoot":    " X ",
                "SeaShoot":     " \u25CF "}  
        self.__continue = "Y"
        
    def start(self): 
        while(Iterator().iteration):
            pass 
        
    def paint(self):
        os.system("cls")         
        param = Parameters()
        players = self.__game.players
        xC = "".join(map(lambda s: self.__cell["Cell"].format(s), param.getXCoordinates()))
        yC = [""]*2 + list(param.getYCoordinates()) + [""]
        yC = list(map(lambda s: self.__cell["Cell"].format(s), yC))       
        res = [""]*len(yC)        
        for pl in players:
            m = param.getSeaArray()
            for cd in pl.getStatus(): 
                m[cd[0][0]][cd[0][1]] = self.__cell[cd[1]]                
            m = map(lambda s: "".join(s), m)                
            m = [self.__centerText(param.getString(pl.name), len(xC)), xC] + list(m) + [xC]
            for i in range(len(yC)):
                res[i] += yC[i] + m[i] 
        for i in range(len(yC)):
            res[i] += yC[i] + "\n"
        print(*res, sep = "")
        print(players[0].info)        
           
    def __centerText(self, s, ln):
        res = (ln - len(s))//2          
        res = " "*res + s 
        return res + " "*(ln-len(res))
                
    def isEnd(self):
        print(Parameters().getString("InputContinue").format(self.__continue), end = ": ")
        self.__result = (self.__continue != input().upper())
        return False
    
    @property
    def result(self):
        return self.__result
            
    def setShipCoordinate(self, decks):        
        param = Parameters()
        if(decks == 1):                    
            print(param.getString("InputShip1"))
            print(param.getString("InputDeck1"), end=": ") 
        else:
            print(param.getString("InputShip"))        
            print(param.getString("InputDeck").format(decks), end=": ")        
        self.__inputCoordinate(True) 
        return False
    
    def setShipCourse(self, decks):
        return False    
    
    def __inputCoordinate(self, spl):
        self.__result = input().upper()
        if(self.__result == ""):
            self.__result = None
        elif(spl):
            self.__result = self.__result.split()
          
    def setShoot(self):        
        print(Parameters().getString("InputShoot"), end = ": ") 
        self.__inputCoordinate(False)
        return False            
