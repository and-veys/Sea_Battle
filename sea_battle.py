# Морской бой
import random
from src.parameters import Parameters, Iterator

if(Parameters().interface == "TK"):
    from src.interface_tkinter import Interface
else:
    from src.interface_cmd import Interface
   

def main():
    """Основная функция"""  
    if(Parameters().isOK()):
        try:            
            Iterator().iteration = Game().start()
            Interface().start()            
            print("\n" + Parameters().getString("Bye"))
        except KeyboardInterrupt:
            print("\n\n" + Parameters().getString("ctrlC"))
    else:
        print("\nStart error ...error ...error")

class Game:
    """Класс игры"""   
    def __init__(self):
        self.__human = Human()
        self.__ai = AI()
        self.__ai.info = None
        self.__human.enemy = self.__ai
        self.__ai.enemy = self.__human 
        Interface(self)

    def start(self):
        while(True):            
            Interface().paint()            
            for pl in self.players:             
                Iterator().iteration = pl.setFleet()
                if(pl.name == "Human"):
                    yield True
            Interface().paint()                
            temp = True
            while(temp):                                    
                for pl in self.players: 
                    Iterator().iteration = pl.playerShoot()
                    if(pl.name == "Human"):
                        yield True
                    if(pl.isWin()):  
                        temp = False
                        break
                        
            Interface().paint()            
            if(Interface().isEnd()):
                yield True
            if(not Interface().result):                
                self.__newGame()
            else:
                yield False

    def __newGame(self):
        for pl in self.players:                
            pl.newGame() 
            
        
    @property 
    def players(self):
        return self.__human, self.__ai
        
class Player:
    """Общий класс игрока"""   
    __info = None
    def __init__(self, nm):
        self.__sea = {}
        self.__fleet = Fleet()
        self.__name = nm
        self.__enemy = None 
        self.__cells = {}
        for cd in Parameters().getSea():
            self.__sea[Parameters().getCoordinate(*cd)] = Cell(*cd)
        for cl in self.__sea:
            self.__sea[cl].init(self.__sea)
            
    def getStatus(self):
        for st in self.__sea.values():
            yield st.getStatus(self.name == "AI")           
        
    def setShip(self, sh, cd = None): 
        while(cd == None):
            temp = self.generateShipCoordinate()
            if(sh.length == 1):
                temp.pop(-1) 
            if(sh.setShip(temp, self.__sea)):
                return True
        return sh.setShip(cd, self.__sea) 

    def generateShipCoordinate(self):
        cd = self.generateShootCoordinate()             
        return [cd, self.generateShipCourse(cd)]
           
    def generateShootCoordinate(self):   
        cells = list(filter(lambda s: self.__sea[s].shoot == False, self.__sea))                
        return random.choice(cells)
    
    def generateShipCourse(self, cd):
        return random.choice(self.__sea[cd].getCourses()) 

    def resetShoots(self):
        for cl in self.__sea.values():
            cl.shoot = False
       
    def __setEnemy(self, en):
        self.__enemy = en
    def __getEnemy(self):
        return self.__enemy
    enemy = property(__getEnemy, __setEnemy)
    
    @property
    def name(self):
        return self.__name
        
    @property
    def fleet(self):
        return self.__fleet.getShips()
    
    @property
    def sea(self):
        return self.__sea 
        
    def __getInfo(self):
        if(Player.__info == None):
            return ""
        if(type(Player.__info) == str):
            return Parameters().getString(Player.__info)
        if(len(Player.__info) == 1):
            return ""
        kol = 6   
        fun  = lambda s: ("" if s[0]==None else "'{}' ".format(s[0])) + Parameters().getString(s[1])
        info = Player.__info.copy()
        if(len(info) > kol):
            info = list(map(fun, [info[0]] + info[len(info) - kol + 1:]))  
            info.insert(1, "...")
        else:
            info = map(fun, info)
        return " >> ".join(info) 
   

    def __setInfo(self, info):
        if(type(info) == list):
            Player.__info.append(info)
        else:
            Player.__info = info   
            
    def __delInfo(self):
        Player.__info = [[None, self.name]]
        
    info = property(__getInfo, __setInfo, __delInfo)
    
    def enemyShoot(self, cd):
        if(cd == None):
            cd = self.generateShootCoordinate() 
        try:
            temp = self.__sea[cd].setShoot()            
        except:
            self.info = [cd, "ErrShoot"]
            return True    
        self.info = [cd, temp]
        if(temp == "miss"):
            return False
        if(self.__fleet.hit(temp)):
            self.info = [None, "win"]
            return False            
        return True
    
    def getLastTurn(self):
        temp = Player.__info[-1]  
        return temp[0], temp[1]
        
    def isWin(self):
        cd, sh = self.getLastTurn()
        return sh == "win"
    
    def newGame(self):
        for cl in self.__sea.values():
            cl.shoot = False
            cl.ship = None                
        self.__fleet = Fleet()  
        self.info = None
                

class Human(Player):
    """Класс игрока-человека"""
    def __init__(self):
        super().__init__("Human")
           
    def setFleet(self):        
        fleet = self.fleet
        sh = next(fleet)
        while(sh):
            if(Interface().setShipCoordinate(sh.length)):
                yield True
            if(Interface().setShipCourse(sh.length)):
                yield True
            if(self.setShip(sh, Interface().result)): 
                sh = next(fleet)
                self.info = None
            else:
                self.info = "ErrShip"
            Interface().paint() 
        self.resetShoots()
        yield False
    
    def playerShoot(self):
        del self.info
        temp = True
        while(temp):            
            if(Interface().setShoot()):
                yield True
            temp  = self.enemy.enemyShoot(Interface().result)
            Interface().paint()
        yield False        

class AI(Player):
    """Класс игрока-Компьютера"""
    def __init__(self):
        super().__init__("AI")
        self.__shoots = None
        
    def setFleet(self): 
        fleet = self.fleet
        sh = next(fleet)
        while(sh):
            if(self.setShip(sh)): 
                sh = next(fleet)
        self.resetShoots()  
        yield False  
           
    def playerShoot(self):
        del self.info
        temp = True
        while(temp):
            temp = self.enemy.enemyShoot(self.__getShoot())
            self.__setShoot()
        Interface().paint()
        yield False       
 
    def __getShoot(self):  
        if(self.__shoots == None):
            return None           
        while(len(self.__shoots[0]) == 1):
            self.__shoots.pop(0)        
        return self.__shoots[0].pop(1)
        
    def __setShoot(self):
        cd, sh = self.getLastTurn()   
        if(sh == "kill" or sh == "win"):
            self.__shoots = None
            return           
        if(self.__shoots == None):
            if(sh == "hit"):
                self.__shoots = list(map(lambda s: self.enemy.sea[cd].getNextCells(s), "UDRL"))
        else:
            if(sh == "miss"):
                self.__shoots.pop(0)    
          
class Cell:
    """Класс, описывающий ячейку поля"""
    def __init__(self, h, w):
        param = Parameters()
        self.__ship = None
        self.__shoot = False
        self.__data = [h, w]
        self.__index = param.getCoordinate(h, w)
        self.__neighbors = {
                "U": param.getCoordinate(h-1, w),
                "D": param.getCoordinate(h+1, w),
                "L": param.getCoordinate(h, w-1),
                "R": param.getCoordinate(h, w+1),
                "UL": param.getCoordinate(h-1, w-1),
                "UR": param.getCoordinate(h+1, w-1),
                "DL": param.getCoordinate(h-1, w+1),
                "DR": param.getCoordinate(h+1, w+1)}
    
    def init(self, sea):
        for i in list(self.__neighbors.keys()):
            cl = sea.get(self.__neighbors[i])
            if(cl == None):
                del self.__neighbors[i]
            else:
                self.__neighbors[i] = cl
                
    def setData(self, dt):
        self.__data = dt
    
    def getStatus(self, hide):
        res = ("Sea" if self.__ship == None else "Ship")
        if(self.__shoot):
            res += "Shoot"
        if(res == "Ship" and hide):
            res = "Sea"
        return self.__data, res, self
        
    def __setShoot(self, sh):
        self.__shoot = sh    
    def __getShoot(self):
        return self.__shoot
    shoot = property(__getShoot, __setShoot)
    
    def __setShip(self, sh):
        self.__ship = sh
    def __getShip(self):
        return self.__ship
    ship = property(__getShip, __setShip)      
    
    def getCourses(self):  
        return list(filter(lambda s: len(s) == 1, self.__neighbors.keys()))
   
    def getNextCell(self, ng):
        return self.__neighbors[ng]
    
    def getNextCells(self, ng):        
        temp = self
        res = [ng]
        try:
            while(True):
                temp = temp.getNextCell(ng)
                if(temp.shoot):
                    break
                res.append(temp.__index)
        except:
            pass
        return res            
    
    def setAroundShoots(self):
        self.shoot = True
        for cl in self.__neighbors.values():
            cl.shoot = True
    
    def setShoot(self):
        if(self.shoot):
            return "was"
        self.shoot = True
        if(self.ship == None):
            return "miss"
        if(self.ship.hit()):
            return "kill"
        return "hit"
    
    def getCoordinates(self, dt):
        if(len(dt) == 1):
            return [self.__index]
        temp = self.getCourses()
        for cl in temp:
            if(self.__neighbors[cl] is dt[1]):
                return [self.__index, cl]
        return ["-1"]
    
class Fleet:
    """Класс для флота кораблей"""
    def __init__(self):    
        self.__ships = []
        self.__decks = 0
        for ln in Parameters().getFleet():
            self.__decks += ln
            self.__ships.append(Ship(ln))
    
    def getShips(self):
        for sh in self.__ships:
            yield sh
        yield False
    
    def hit(self, temp):
        if(temp == "hit" or temp == "kill"):
            self.__decks -= 1
        return (self.__decks == 0)
    
class Ship:
    """Класс, описывающий корабль"""
    def __init__(self, d):    
        self.__decks = [None]*d 
        self.__shoot = d            
    
    @property
    def length(self):
        return len(self.__decks)
    
    def setShip(self, cd, sea):
        if(len(cd) != (1 if self.length == 1 else 2)):
            return False
        
        try:           
            self.__decks[0] = sea[cd[0]]
            for i in range(self.length - 1): 
                self.__decks[i+1] = self.__decks[i].getNextCell(cd[1])           
            for cl in self.__decks:
                if(cl.shoot):
                    return False
        except:
            return False  
        for cl in self.__decks:
            cl.ship = self
        self.__setAroundShoots()
        return True 
        
    def __setAroundShoots(self):
        for cl in self.__decks:
            cl.setAroundShoots()
    
    def hit(self):
        self.__shoot -= 1
        if (self.__shoot == 0):
            self.__setAroundShoots()
            return True
        return False 
      
main()