import tkinter
from .parameters import Parameters, Iterator


class Label(tkinter.Frame):
    """Класс ячейки с текстом"""
    def __init__(self, wnd, g = "SystemButtonFace"):      
        super().__init__(master = wnd, bg = g)
        
    def init(self, txt = ""):   
        self.__cell = tkinter.Label(text = txt, width = 2, height = 1, master = self, font = "Arial 14 bold", bg = self["bg"])
        self.__cell.pack(padx = 2, pady = 2)
    @property
    def cell(self):
        return self.__cell
        
class Cell(Label):
    """Класс игровой ячейки"""
    __colors = None
    def __init__(self, wnd): 
        self.__index = None
        super().__init__(wnd, Cell.__colors["Sea"])  
      
    def init(self, cl, hd):
        super().init()
        self.__index = cl 
        if(hd):
            self.cell.bind("<Button-1>", self.__shoot) 
        else:
            self.cell.bind("<Button-1>", self.__fleet) 
            
    def __shoot(self, event):
        self.__setBuffer("SHOOT")             
    
    def __fleet(self, event):
        self.__setBuffer("FLEET")
           
    def __setBuffer(self, mes):
        if(Interface().isEvent(mes)):
            Interface().result = self.__index
            self.paint("Ship")
            Iterator().iteration   
    def paint(self, col):
        self.cell["bg"] = Cell.__colors[col]
    
    def setColors(col):
        Cell.__colors = col

class Interface:
    """Класс для работы в TKinter"""
    __inst = None                                          
    def __new__(cls, gm = None):
        if(cls.__inst == None): 
            cls.__inst = super().__new__(cls)
            cls.__inst.__init(gm)
        return cls.__inst  
        
    def __init(self, gm):
        self.__game = gm
        self.__result = None   
        self.__window = None
        self.__label_1 = None
        self.__label_2 = None
        Cell.setColors({        
                "Ship":         "lightgreen",
                "Sea":          "blue",
                "ShipShoot":    "red",
                "SeaShoot":     "white"}
                )         
        param = Parameters()     
        xC = list(param.getXCoordinates())
        yC = [""]*2 + list(param.getYCoordinates()) + [""]

        self.__window = tkinter.Tk()  
        self.__window.title(param.getString("Title"))
        self.__window.resizable(width = False, height = False)         
        wnd = tkinter.Frame(self.__window, relief = tkinter.RIDGE, borderwidth = 5)   
        for pl in self.__game.players:       
            temp = self.__getLabel(wnd, yC, tkinter.TOP)
            temp.pack(side = tkinter.LEFT)
            temp = self.__getSea(wnd, xC, pl)
            temp.pack(side = tkinter.LEFT)
        temp = self.__getLabel(wnd, yC, tkinter.TOP)
        temp.pack(side = tkinter.RIGHT)  
        wnd.pack(padx = 10, pady = 10)
        
        wnd = tkinter.Frame(self.__window)
        self.__label_1 = tkinter.Label(wnd, font = "Arial 12", relief = tkinter.RIDGE, borderwidth = 5, anchor = "w", padx = 10, pady = 5)
        self.__label_1.grid(row = 0, column = 0, sticky = "ew")
        self.__label_2 = tkinter.Label(wnd, font = "Arial 12", relief = tkinter.RIDGE, borderwidth = 5, anchor = "w", padx = 10, pady = 5)
        self.__label_2.grid(row = 1, column = 0, sticky = "ew", pady = (3, 0))
        button = tkinter.Button(wnd, text = "<<   >>", width = 10, font = "Arial 12 bold")
        button.grid(row = 0, column = 1, rowspan = 2, sticky = "nsew", padx = (10, 0), pady = 10) 
        button.bind("<Button-1>", self.__button) 
        wnd.columnconfigure(0, weight = 1)
        wnd.pack(fill = tkinter.X, padx = 10, pady = (0, 10)) 
    
    def __button(self, event):
        if(len(self.__result) == 1):
            self.result = "button"
            Iterator().iteration  
    
    def __getLabel(self, par, arr, sd):
        wnd = tkinter.Frame(par)
        for el in arr:
            temp = Label(wnd)
            temp.init(el)
            temp.pack(padx = 1, pady = 1, side = sd)
        return wnd
    
    def __getSea(self, par, xC, pl):   
        wnd = tkinter.Frame(par)
        temp = tkinter.Label(wnd, text = Parameters().getString(pl.name), font = "Arial 14 bold", fg = "green")
        temp.pack(pady = 3)
        temp = self.__getLabel(wnd, xC, tkinter.LEFT)
        temp.pack()
        w = tkinter.Frame(wnd)        
        for cd in pl.getStatus():
            temp = Cell(w)
            temp.init(cd[2], pl.name == "AI")
            temp.grid(row = cd[0][0], column = cd[0][1], padx = 1, pady = 1)
            cd[2].setData(temp)
        w.pack()        
        temp = self.__getLabel(wnd, xC, tkinter.LEFT)
        temp.pack()
        return wnd       
    
    def paint(self):
        for pl in self.__game.players:
            for cd in pl.getStatus():
                cd[0].paint(cd[1])  
        self.paintText()
        
    def  paintText(self):
        self.__label_1["text"] = self.__game.players[0].info
   
    def __getResult(self):
        if(type(self.__result[-1]) == str):
            return None
        ind = self.__result.pop(0)
        temp = self.__result[0].getCoordinates(self.__result)
        if(ind == "SHOOT"):
            return temp[0]
        return temp   
    def __setResult(self, res):   
        self.__result.append(res)    
    def __delResult(self):
        self.__result = []
    result = property(__getResult, __setResult, __delResult)
    
    def isEvent(self, mes):
        return self.__result[0] == mes    
    
    def setShipCoordinate(self, decks): 
        del self.result
        self.result = "FLEET" 
        param = Parameters()
        self.paintText()
        if(decks == 1):                    
            self.__label_2["text"] = param.getString("InputShip1_TK") 
        else:
            self.__label_2["text"] = param.getString("InputShip_TK").format(decks) 
        return True
        
    def setShipCourse(self, decks):
        if(decks == 1 or type(self.__result[-1]) == str):
            return False
        self.__game.players[0].info = None
        self.paintText()    
        self.__label_2["text"] = Parameters().getString("InputCourse_TK")      
        return True   
    
    def setShoot(self): 
        del self.result
        self.result = "SHOOT"                 
        self.__label_2["text"] = Parameters().getString("InputShoot_TK")        
        return True
    
    def isEnd(self):
        del self.result
        self.result = "END" 
        self.__label_2["text"] = Parameters().getString("InputContinue_TK")
        return True
    
    def start(self):
        self.__window.mainloop()