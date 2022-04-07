class Iterator():
    """Класс для итераций цикла боя"""
    __inst = None                                          
    def __new__(cls, lg = None):
        if(cls.__inst == None): 
            cls.__inst = super().__new__(cls)
            cls.__inst.__iteration = []
        return cls.__inst 
    
    def __getIt(self):
        if(len(self.__iteration) == 0):
            return False    
        if(next(self.__iteration[-1]) == False):       
            self.__iteration.pop(-1)  
            try:
                self.__getIt()
            except:
                pass                
        return True
        
    def __setIt(self, it): 
        self.__iteration.append(it)
        self.__getIt()

    iteration = property(__getIt, __setIt)
   
class Parameters:
    """Класс для параметров боя"""
    __inst = None                                          
    def __new__(cls, lg = None):
        if(cls.__inst == None): 
            cls.__inst = super().__new__(cls)
            cls.__inst.__init()
        return cls.__inst        
        
    def __init(self):                                           
        self.__size = {"width": 10, "height": 12}                                      
        self.__fleet = {"4":1, "3":2, "2":3, "1":4} 
        try:
            self.__strings = self.__loadStrings(self.__setLanguage()) 
            self.__interface = self.__setInterface()
        except:
            self.__interface = None
                        
    @property
    def interface(self):
        return self.__interface

    def __setInterface(self):                                        #TODO сделать правильно
        print(self.getString("InputInterface"), end=": ")
        res = input().upper()
        if(res == "CMD"):
            return "CMD"
        return "TK"
    
    def __setLanguage(self):  
        print("Выберете язык игры / Choose the language of the game [RUS] / ENG", end=": ")
        res = input().upper()
        if(res == "ENG"):
            return "ENG"
        return "RUS"
        
    def isOK(self):
        return (self.interface != None)
      
    def __loadStrings(self, lg):
        lang = {"RUS": 1, "ENG": 2}
        lang = lang[lg]
        f = open("src\data.dat")
        res = {"None": ""}
        for ln in f:
            temp = ln.split(";")
            temp = list(map(lambda s: s.strip(), temp))
            res[temp[0]] = temp[lang]
        return res  
        
    def getSea(self):
        for h in range(self.__size["height"]):
            for w in range(self.__size["width"]):
                yield [h, w]
    
    def getSeaArray(self):
        temp = [None]*self.__size["height"]
        return list(map(lambda s: [None]*self.__size["width"], temp))
    
    def getFleet(self):
        for el in self.__fleet:
            for sh in range(self.__fleet[el]):
                yield int(el)
    
    def getCoordinate(self, h, w):
        return self.__getY(h) + self.__getX(w)
    
    def __getX(self, w):
        return str(w+1)
    
    def __getY(self, h):
        return chr(h + ord("A"))
    
    def getXCoordinates(self):
        return map(self.__getX, range(self.__size["width"]))
    
    def getYCoordinates(self):
        return map(self.__getY, range(self.__size["height"])) 
     
    def getString(self, ind):
        return self.__strings[ind]