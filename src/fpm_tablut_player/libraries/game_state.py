import numpy as np
import copy

from fpm_tablut_player.utils import DebugUtils, GameUtils


Uscite=[(0,1),(0,2),(0,6),(0,7),(1,0),(1,8),(2,0),(2,8),(6,0),(6,8),(7,0),(7,8),(8,1),(8,2),(8,6),(8,7)]
Throne=[(4,4)]
Accampamenti=[(0,3),(0,4),(0,5),(1,4),(3,0),(3,8),(4,0),(4,1),(4,7),(4,8),(5,0),(5,8),(7,4),(8,3),(8,4),(8,5)]

class GameState:
    state:[[]]
    turn: str
    BlackNumber:int
    WhiteNumber:int
    WhiteList:list
    BlackList:list
    King:tuple
    FinalDeaths:list

    def createFromServerState(self,stateFromServer):
        #Load the state and the turn (asking them to the server). If King is not initialized, or black pawn are zero, it return FALSE
        self.turn = GameUtils.turnToString(stateFromServer["turn"])
        self.state = np.array(stateFromServer["board"],dtype=object)
        self.BlackNumber=0
        self.WhiteNumber=0
        self.WhiteList=[]
        self.BlackList=[]
        for i in range(0, len(self.state)):
            for j in range(len(self.state[i,:])):
                if self.state[i,j]=="BLACK":
                    self.BlackNumber=self.BlackNumber+1
                    self.BlackList.append((i,j))
                if self.state[i,j]=="WHITE":
                    self.WhiteNumber=self.WhiteNumber+1
                    self.WhiteList.append((i,j))
                if self.state[i,j]=="KING":
                    self.King=((i,j))
        try:
            #print("King position -> ",self.King)
            self.King
        except:
            raise Exception("king not found")
        if self.BlackNumber==0 or self.BlackList==[]:
            raise Exception("no Black pawns on the board")
        
        return self
            


    def getAllPointOnBoard(self) ->list:
        
        #return all the pawns on the board
        PointList=[]
        PointList.append(self.King)
        PointList=PointList + self.WhiteList + self.BlackList
        return PointList

    def isPoint(self,point_coord) -> object:
        #return False if in the position of the state is Empty, otherwise return All the pawns(list)
        
        PointList=self.getAllPointOnBoard()
        for index in range(len(PointList)):
            if PointList[index]==point_coord:
                return PointList
        return False

    def getTheMostNear(self,point_coord) ->object: 
        #return, giving a real pawn coordinate, the first (x,y) in each direction where he can't go
        PointList=self.isPoint(point_coord)
        
        if  PointList==False:
            #print("The point considered: ",point_coord," is not a pawn")
            DebugUtils.error("The point considered: {} is not a pawn",[point_coord])
            return False
        else:
            PointList=PointList+Throne
            if point_coord not in Accampamenti:
                #the black paws in the camp can move in the camp tull they are in the camp
                PointList=PointList+Accampamenti
            ovest,est,nord,sud=100,100,100,100
            x=point_coord[0]
            y=point_coord[1]
            nord_coord,sud_coord,est_coord,ovest_coord =None,None,None,None

            for e in PointList:
                if e[0]==x and e[1] != y:#se la x  uguale e non la y sono tutti i punti sulla x diversi da se stesso
                    #DebugUtils.info("point_coord: {} una pedina sull'asse x: {}   è uguale la x",[(x,y),e])

                    if e[1]<y:
                        #punto sulla x prima di coord
                        ovest_find=y-e[1]
                        ovest=(min(ovest,ovest_find))
                    if e[1]>y:
                        est_find=e[1]-y
                        est=(min(est,est_find))
                if e[1]==y and e[0] != x:
                    #se la x  uguale e non la x sono tutti i punti sulla x diversi da se stesso
                    #DebugUtils.info("point_coord: {} una pedina sull'asse y: {}   è uguale la y",[(x,y),e])

                    if e[0]<x:
                        #punto sulla x prima di coord
                        nord_find=x-e[0]
                        nord=(min(nord,nord_find))
                    if e[0]>x:
                        
                        sud_find=e[0]-x
                        sud=(min(sud,sud_find))
            if nord==100:
                nord=-1
                nord_coord=(-1,y)
            else:
                nord_coord=(x-nord,y)
            if est==100:
                est=-1
                est_coord=(x,9)
            else:
                est_coord=(x,y+est)
            if sud==100:
                sud=-1
                sud_coord=(9,y)
            else:
                sud_coord=(sud+x,y)
            if ovest==100:
                ovest=-1
                ovest_coord=(x,-1)
            else:
                ovest_coord=(x,y-ovest)
            #DebugUtils.info("\nDISTANZE: -> NORD: {} SUD: {} OVEST: {} EST: {}",[nord,sud,ovest,est])
            #DebugUtils.info("TUPLA POS : ->NORD: {} SUD: {} OVEST: {} EST: {}\n",[nord_coord,sud_coord,ovest_coord,est_coord])
                
            point= {
                "point_coord":(x,y),
                "est": est_coord, #massima distanza percorribile
                "ovest":ovest_coord,#massima distanza percorribile
                "nord":nord_coord,#massima distanza percorribile
                "sud":sud_coord,#massima distanza percorribile}
            }

            point_dist= {
                "point_coord":(x,y),
                "est": est, #massima distanza percorribile
                "ovest":ovest,#massima distanza percorribile
                "nord":nord,#massima distanza percorribile
                "sud":sud,#massima distanza percorribile}
            }

            return point,point_dist
        return None

    def getMoveFromCoord(self,point_coord) -> object:
        #giving a real coordinate, return the list of possible (x,y) where the pawn can go
        ListOfReachableCoord=[]
        ListOfReachableCoordFinal=[]
        DictOfNeighbour=self.getTheMostNear(point_coord)[0]
        if DictOfNeighbour:
            point_coord=DictOfNeighbour["point_coord"]
            #print("getMoveFromCoord: point_coord -> ",point_coord)
            for key in DictOfNeighbour:
                value=DictOfNeighbour[key]
                #print(key, '->', value)
                if key!="point_coord":
                    if value != None:
                        if key=="sud":
                            #print(key, '->',value)#
                            for i in range(point_coord[0]+1,value[0]):
                                #print("\ti: ",i," -> ", (i,value[1]))
                                ListOfReachableCoord.append(("s",i,value[1]))
                                ListOfReachableCoordFinal.append({'from':point_coord,'to':(i,value[1])})
                        if key=="nord":
                            #print(key, '->',value)
                            for i in range(value[0]+1,point_coord[0]):
                                #print("\ti",i," -> ", (i,value[1]))
                                ListOfReachableCoord.append(("n",i,value[1]))
                                ListOfReachableCoordFinal.append({'from':point_coord,'to':(i,value[1])})
                        if key=="est":
                            #print(key, '->',value)
                            for i in range(point_coord[1]+1,value[1]):
                                #print("\ti",i," -> ", (value[0],i))
                                ListOfReachableCoord.append(("e",value[0],i))
                                ListOfReachableCoordFinal.append({'from':point_coord,'to':(value[0],i)})
                        if key=="ovest":
                            #print(key, '->',value)
                            for i in range(value[1]+1,point_coord[1]):
                                #print("\ti",i," -> ", (value[0],i))
                                ListOfReachableCoord.append(("o",value[0],i))
                                ListOfReachableCoordFinal.append({'from':point_coord,'to':(value[0],i)})
            #print("\nLista -->: ",ListOfReachableCoord)
            #print("Lista -->: ",ListOfReachableCoordFinal,"\n")
                                            
            return ListOfReachableCoordFinal
        DebugUtils.error("Error in GameState.getMostNear, probably the point_considered is EMPTY",[])
        return False


    def getPossibleMoves(self,turn) ->list:
        #giving turn, white or black, return the list of all possible moves for white or black pawns
        Moves=[]
        if turn=="white":
            for point in self.WhiteList:
                a=self.getMoveFromCoord(point)
                Moves.append(a)
        else:
            for point in self.BlackList:
                b=self.getMoveFromCoord(point)
                Moves.append(b)
        JsonMoves=[]
        for i in Moves:
            for j in i:
                JsonMoves.append(j)

        #DebugUtils.info("GET POSSIBLE MOVES FROM {}\n{}",[turn,JsonMoves])
        return JsonMoves


    def changeTurn(self) -> str:  
        if self.turn=="white":
            self.turn="black"
        else:
            self.turn="white"
        return self.turn

    def deletePawn(self,point_coord):
        if point_coord==(4,4):
            self.state[(4,4)]="THRONE"
        else:
            self.state[point_coord]="EMPTY"
    
    def movePawnFromTo(self,starting_coord,ending_coord):
        #change the board moving the pawn
        replace=self.state[starting_coord]
        if replace not in {"WHITE","BLACK","KING"}:
            DebugUtils.error("I'm not taking a pawn",[])
            return self
        
        if starting_coord==(4,4):
            self.state[starting_coord]="THRONE"
        else:
            self.state[starting_coord]="EMPTY"

        if self.state[ending_coord]=="EMPTY" or self.state[ending_coord]=="THRONE" :
            self.state[ending_coord]=replace
        else:
            DebugUtils.error("I'm moving a pawn on another pawn",[])
        #print("MovePawnFromTo: From ",starting_coord,"to: ",ending_coord,". It's a ",replace," pawn")
        #print(starting_coord," -> ",self.state[starting_coord],"\n",ending_coord," -> ",self.state[ending_coord],"\n")#,self.state,"\n")
        return self


    def getDist1(self,point_coord) ->list:
            x=point_coord[0]
            y=point_coord[1]
            nord,est,ovest,sud=-1,-1,-1,-1
            if (x+1 < 9) and (self.state[(x+1,y)]=="WHITE" or self.state[(x+1,y)]=="BLACK" or self.state[(x+1,y)]=="KING"):
                sud=1
            if (x-1 >= 0) and (self.state[(x-1,y)]=="WHITE" or self.state[(x-1,y)]=="BLACK" or self.state[(x-1,y)]=="KING"):
                nord=1
            if (y+1 < 9) and (self.state[(x,y+1)]=="WHITE" or self.state[(x,y+1)]=="BLACK" or self.state[(x,y+1)]=="KING"):
                est=1
            if (y-1 >= 0) and (self.state[(x,y-1)]=="WHITE" or self.state[(x,y-1)]=="BLACK" or self.state[(x,y-1)]=="KING"):
                ovest=1
            
            point= {
                "point_coord":(x,y),
                "est": (x,y+1), #massima distanza percorribile
                "ovest":(x,y-1),#massima distanza percorribile
                "nord":(x-1,y),#massima distanza percorribile
                "sud":(x+1,y),#massima distanza percorribile}
            }

            point_dist= {
                "point_coord":(x,y),
                "est": est, #massima distanza percorribile
                "ovest":ovest,#massima distanza percorribile
                "nord":nord,#massima distanza percorribile
                "sud":sud,#massima distanza percorribile}
            }
            #print(point,point_dist)
            return point,point_dist

    def Enemy(self,turn) ->set:
        turno=turn.upper()

        if turno=="WHITE" or turno=="KING":
            return {"BLACK"}
        else:
            return {"WHITE","KING"}


    def Killed(self,coord,pawn_color,pos) ->list:
        #print("Killed function: ",coord)
        if self.state[coord] in pawn_color: #{"WHITE,"KING"}     {"BLACK"}
            MustBeKilled=[]
            pawn_considered=self.state[coord]
            if pawn_considered=="KING":
                King=coord
                #print("I'm considering King",King)
                dic=self.getDist1(coord)[0]
                #print("AAAAAAAAAAAAAAAAAAA",dic)
                #print("BBBBBBBBBBBBBBBBBBB",dic["nord"])
                nord=[self.state[(dic["nord"])]]
                est=[self.state[(dic["est"])]]
                ovest=[self.state[(dic["ovest"])]]
                sud=[self.state[(dic["sud"])]]

                list_King=[]
                list_King=nord+est+ovest+sud
                #print("\nlistKing: ",list_King)
                count=0
                for e in list_King:
                    if e=="BLACK":
                        count=count+1
                if count==3 and ("THRONE" in list_King  or "EMPTY"==self.state[(4,4)]):
                    #print("cacca1")
                    self.deletePawn(coord)
                    MustBeKilled.append(King)
                elif count==4 and King==(4,4):
                    #print("cacca2")
                    self.deletePawn(coord)
                    MustBeKilled.append(King)
                else:

                    est=self.state[(coord[0],coord[1]+1)]
                    ovest=self.state[(coord[0],coord[1]-1)]
                    nord=self.state[(coord[0]-1,coord[1])]
                    sud=self.state[(coord[0]+1,coord[1])]

                    if count==2 and ( (est==ovest and est=="BLACK") or (nord==sud and nord=="BLACK") ) and ("THRONE" not in list_King  )and (King not in [(4,4),(4,3),(3,4),(4,5),(5,4)]):
                        self.deletePawn(coord)
                        MustBeKilled.append(King)                    

            else:
                if pos=="est" and coord[1]+1 < 9:
                    on_the_opposite_side=self.state[(coord[0],coord[1]+1)]  
                    enemy=self.Enemy(pawn_considered)
                    #print("\ton the opposite side",(coord[0],coord[1]+1)," -> ",on_the_opposite_side,". His enemy is ",enemy)
                    if (on_the_opposite_side in enemy) or ((coord[0],coord[1]+1) in Throne+Accampamenti ):
                        self.deletePawn(coord)
                        MustBeKilled.append(coord)   
                if pos=="ovest" and coord[1]-1 > -1:
                    on_the_opposite_side=self.state[(coord[0],coord[1]-1)]
                    enemy=self.Enemy(pawn_considered)
                    #print("\ton the opposite side",(coord[0],coord[1]-1)," -> ",on_the_opposite_side,". His enemy is ",enemy)
                    if (on_the_opposite_side in enemy) or ((coord[0],coord[1]-1) in Throne+Accampamenti ):
                        self.deletePawn(coord)
                        MustBeKilled.append(coord)        
                if pos=="nord" and coord[0]-1 < -1:
                    on_the_opposite_side=self.state[(coord[0]-1,coord[1])]
                    enemy=self.Enemy(pawn_considered)
                    #print("\ton the opposite side",(coord[0]-1,coord[1])," -> ",on_the_opposite_side,". His enemy is ",enemy)
                    if (on_the_opposite_side in enemy) or ((coord[0]-1,coord[1]) in Throne+Accampamenti ):
                        self.deletePawn(coord)
                        MustBeKilled.append(coord)   
                if pos=="sud" and coord[0]+1 < 9:
                    on_the_opposite_side=self.state[(coord[0]+1,coord[1])]
                    enemy=self.Enemy(pawn_considered)
                    #print("\ton the opposite side",(coord[0]+1,coord[1])," -> ",on_the_opposite_side,". His enemy is ",enemy)
                    if (on_the_opposite_side in enemy) or ((coord[0]+1,coord[1]) in Throne+Accampamenti ):
                        self.deletePawn(coord)
                        MustBeKilled.append(coord)   
            return MustBeKilled
        else:
            DebugUtils.error("Killed error",[])
            return []

    def computeKill(self,move):
        self.FinalDeaths=[]
        #print("computekill: ",self.turn.upper()," turn")
        starting_coord=move["from"]
        ending_coord=move["to"]
        self.movePawnFromTo(starting_coord,ending_coord)
        #print("\ndopo che mi sono mosso\n",self.state)

        if self.state[ending_coord]!=self.turn.upper():
            DebugUtils.error("Error on moving a pawn of the enemy lead",[])
            return self

        enemy=self.Enemy(self.turn)
        #print("computekill change turn : ",self.turn.upper()," turn")
        dic=self.getDist1(ending_coord)
        #print("dic ->",dic)
        DictOfNeighbour=dic[0]
        DictOfNeighbourDist=dic[1]

        #if ending_coord==DictOfNeighbourDist["point_coord"]:
        #    print("it's working")

        CanBeKilled=[]
        if DictOfNeighbourDist["nord"]==1 and self.state[(DictOfNeighbour["nord"])]in enemy:
            CanBeKilled.append(DictOfNeighbour["nord"])
        if DictOfNeighbourDist["sud"]==1 and self.state[(DictOfNeighbour["sud"])]in enemy:
            CanBeKilled.append(DictOfNeighbour["sud"])
        if DictOfNeighbourDist["ovest"]==1 and self.state[(DictOfNeighbour["ovest"])]in enemy:
            CanBeKilled.append(DictOfNeighbour["ovest"])
        if DictOfNeighbourDist["est"]==1 and self.state[(DictOfNeighbour["est"])]in enemy:
            CanBeKilled.append(DictOfNeighbour["est"])
        #print("\nnord of ending_coord -> ",self.state[(DictOfNeighbour["nord"])],"\nsud of ending_coord -> ",self.state[(DictOfNeighbour["sud"])],"\novest of ending_coord -> ",self.state[(DictOfNeighbour["ovest"])],"\nest of ending_coord -> ",self.state[(DictOfNeighbour["est"])])

        killed_nord,killed_est,killed_ovest,killed_sud=[],[],[],[]
        #print("befor killing ",killed_nord,killed_est,killed_ovest,killed_sud)
        for e in CanBeKilled:#nemici nell'intorno di distanza 1
            #print("\nfrom: ",ending_coord,"CanBeKilled List: ",e)
            #check if e die
            if ending_coord[0]==e[0]:#x
                #print("initial coordingate x",ending_coord,"pawn to check kill",e)
                if e[1]>ending_coord[1]:
                    #print("est initial coordingate x:",ending_coord," -> ",e,"\n")
                    killed_est=self.Killed(e,enemy,"est")
                else:
                    #print("ovest initial coordingate x:",ending_coord," -> ",e,"\n")
                    killed_ovest=self.Killed(e,enemy,"ovest")
            elif ending_coord[1]==e[1]:##nord sud
                #print("initial coordingate y:nord or sud:",ending_coord,"pawn to check kill",e)
                if e[0]>ending_coord[0]:
                    #print("sud initial coordingate y:",ending_coord," -> ",e,"\n")
                    killed_sud=self.Killed(e,enemy,"sud")
                else:
                    #print("nord initial coordingate y:",ending_coord," -> ",e,"\n")
                    killed_nord=self.Killed(e,enemy,"nord")

            
            
        
        #print("after killing",killed_nord,killed_est,killed_ovest,killed_sud)
        FinalDeaths=killed_nord+killed_est+killed_ovest+killed_sud
        self.changeTurn()
        self.FinalDeaths=FinalDeaths
        #print("FINALDEATH: ",self.FinalDeaths)
        #print("\ndopo che ho ucciso\n",self.state,"\n")
        return self



    def getKilled(self,initialGameState,moves)->list:
        TempGameState=GameState().createFromMoves(initialGameState,moves)
        return TempGameState.FinalDeaths
        
        
    def createFromMoves(self,initialGameState,moves):
        endingGameState=copy.deepcopy(initialGameState)
        for move in moves:
            #print("mossa. ->",move)
       
            endingGameState=endingGameState.computeKill(move)#turno bianco= turno nero.uccidi

        internalState={}
        internalState["board"]=endingGameState.state
        internalState["turn"] = endingGameState.turn

        #killed=endingGameState.FinalDeaths
        endingGameState=GameState().createFromServerState(internalState)
        #endingGameState.FinalDeaths=killed
        return endingGameState



    def __init__(self):
        self.state=[]
        self.turn=None

  


# GameState1=GameState()
# """
# state=[["EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY","BLACK","BLACK"],
#        ["EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY","BLACK","BLACK"],
#        ["BLACK","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY","BLACK","BLACK"],
#        ["BLACK","BLACK","EMPTY","EMPTY","KING","EMPTY","WHITE","EMPTY","EMPTY"],
#        ["BLACK","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","WHITE","BLACK","BLACK"],
#        ["EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","WHITE","BLACK","BLACK"],
#        ["EMPTY","WHITE","WHITE","EMPTY","EMPTY","EMPTY","WHITE","BLACK","BLACK"],
#        ["EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","WHITE","BLACK","BLACK"],
#        ]
# """
# state=[["EMPTY","WHITE","EMPTY","BLACK","BLACK","BLACK","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","BLACK","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["BLACK","EMPTY","BLACK","EMPTY","BLACK","BLACK","EMPTY","EMPTY","BLACK"],
#        ["BLACK","KING","BLACK","EMPTY","THRONE","BLACK","WHITE","BLACK","BLACK"],
#        ["BLACK","WHITE","BLACK","BLACK","BLACK","EMPTY","EMPTY","EMPTY","BLACK"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","BLACK","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","BLACK","BLACK","BLACK","EMPTY","EMPTY","EMPTY"],
#        ]
# """
# state=[["EMPTY","EMPTY","EMPTY","BLACK","BLACK","BLACK","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","BLACK","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["BLACK","EMPTY","EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","BLACK"],
#        ["BLACK","BLACK","WHITE","WHITE","KING","WHITE","WHITE","BLACK","BLACK"],
#        ["BLACK","EMPTY","EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","BLACK"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","WHITE","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","EMPTY","BLACK","EMPTY","EMPTY","EMPTY","EMPTY"],
#        ["EMPTY","EMPTY","EMPTY","BLACK","BLACK","BLACK","EMPTY","EMPTY","EMPTY"],
#        ]
# """
# turno="white"
# print("response from server is ok: --> ",GameState1.createFromServer({"board":state,"turn":turno}))
# print(GameState1.state)
# print(GameState1.BlackNumber)
# print(GameState1.WhiteNumber)
# print(GameState1.turn)

# point_King=(4,1)
# #print(GameState1.getPossibleMoves(point_King))
# #print(GameState1.WhiteList)
# #print(GameState1.state[(4,4)])
# print("-----------")
# a=GameState1.getMoveFromCoord(point_King)
# #for i in a:
# #    print(i)


# print("\\\\\\")
# allMoves=GameState1.getPossibleMoves(turno)

# print("\n\n\n\n\n\n\n")
# print("\n\n")
# actions=0
# for i in allMoves:
#     print(i)
#     actions+=1
# print(actions)
# print("-----------")
# print("\n\n\n\n\n\n\n")
# #print(GameState1.computeKill({'from': (0, 3), 'to': (3, 3)}))



# print("\nprima\n",GameState1.state)
# GameState2=GameState()
# GameState3=GameState2.createFromMoves(GameState1,[{'from': (0, 1), 'to': (3, 1)},{'from': (0, 3), 'to': (0, 1)},{'from': (4, 6), 'to': (3, 6)}])
# #print("GameState3",GameState3)
# #print("dopo",GameState1.state)
# #print("dopo3",GameState3.state)
# #print(GameState3.FinalDeaths)
# #print(GameState1.FinalDeaths)
# print("\ndopo\n",GameState3.state)
# print(GameState3.state[point_King])

# ##GameState4=GameState().createFromServer(state,turno)
# #print(GameState4.state[(0,1)])
