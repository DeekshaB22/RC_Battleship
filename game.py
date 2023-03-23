import socket
import copy
import errno
import time
import os
import pickle
from colorama import Fore,Style

GAME_PORT = 6005
HEADERSIZE = 10

# participating clients must use this port for game communication


############## GAME LOGIC ##############

################## PLAYER FUNCTIONS ##################

# pl_grid={'A': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'B': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'C': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'D': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'E': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'F': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'G': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'H': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'I': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'J': [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']}
pl_grid={1: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 2: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 3: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 4: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 5: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 6: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 7: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 8: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 9: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 10: [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']}
opp_grid={}
lost_playergrid={}

def lost_plgrid(gridy):
  for i in range (10):
    for j in range (10):
        # if gridy[chr(c+i)][j] == "#":
        if gridy[i+1][j] == "#":           
          gridy[i+1][j]= "X"
            
def player_grid():
    global pl_grid
    c = 65  
    print(f"  ", end='')
    for j in range(10):
        print(f"  {j+1} ", end='')    
    print("\n  ", (10*4)*"-")
      
    for i in range(10):
        print(f"{chr(c+i)} ", end='')
        for j in range(10):
            # if pl_grid[chr(c+i)][j] == "#":
            if pl_grid[i+1][j] == "#":  
              # print(Fore.GREEN+f"| {pl_grid[chr(c+i)][j]} ", end='')  
              print(Fore.GREEN+f"| {pl_grid[i+1][j]} ", end='')
            # elif pl_grid[chr(c+i)][j] == "X":
            elif pl_grid[i+1][j] == "X":
              # print(Fore.RED+f"| {pl_grid[chr(c+i)][j]} ", end='')
              print(Fore.RED+f"| {pl_grid[i+1][j]} ", end='')
            else:
              # print(Style.RESET_ALL+f"| {pl_grid[chr(c+i)][j]} ", end='')
              print(Style.RESET_ALL+f"| {pl_grid[i+1][j]} ", end='')                   
        print(Style.RESET_ALL+"| ")
        print(Style.RESET_ALL+"  ", (10*4)*"-")
    print(Style.RESET_ALL+"\n")   

def update_playergrid(move,row,col):
  pl_grid[row][col-1]=move

def mark_ships(crd):
  if crd[0]==crd[2]:
    for i in range (crd[1],crd[3]+1):
      update_playergrid("#",crd[0],i)
  elif crd[1]==crd[3]:
    # for i in range (ord(crd[0]),ord(crd[2])+1):
    for i in range (crd[0],crd[2]+1):
      # update_playergrid("#",chr(i),crd[1])
      update_playergrid("#",i,crd[1])

  else:
    print("error")
  os.system('cls')   
  print("Your grid:\n")
  player_grid()  

def print_grids():
  os.system('cls')   
  print("Your grid:\n")
  player_grid() 
  print("Opponent's grid:\n")
  oppo_grid() 
   
########## SHIPS ###########

def twoship():
  as2x, as2y,ae2x,ae2y= input("2 block ship A:").split()
  crd2A= [ord(as2x)-64, int(as2y),ord(ae2x)-64,int(ae2y)]
  mark_ships(crd2A)
  bs2x,bs2y,be2x,be2y= input("2 block ship B:").split()
  crd2B=[ord(bs2x)-64,int(bs2y),ord(be2x)-64,int(be2y)]
  mark_ships(crd2B)

  global coord_2
  coord_2= [crd2A,crd2B]

def threeship(): 
  as3x, as3y,ae3x,ae3y= input("3 block ship A:").split()
  crd3A= [ord(as3x)-64, int(as3y),ord(ae3x)-64,int(ae3y)]
  mark_ships(crd3A)
  bs3x,bs3y,be3x,be3y= input("3 block ship B:").split()
  crd3B=[ord(bs3x)-64,int(bs3y),ord(be3x)-64,int(be3y)]
  mark_ships(crd3B)
  cs3x,cs3y,ce3x,ce3y= input("3 block ship C:").split()
  crd3C=[ord(cs3x)-64,int(cs3y),ord(ce3x)-64,int(ce3y)]
  mark_ships(crd3C)

  global coord_3
  coord_3= [crd3A,crd3B,crd3C]

def fourship():
  as4x, as4y,ae4x,ae4y= input("4 block ship A:").split()
  crd4A= [ord(as4x)-64, int(as4y),ord(ae4x)-64,int(ae4y)]
  mark_ships(crd4A)

  global coord_4
  coord_4= [crd4A]   

def fiveship():
  as5x, as5y,ae5x,ae5y= input("5 block ship A:").split()
  crd5= [ord(as5x)-64, int(as5y),ord(ae5x)-64,int(ae5y)]
  mark_ships(crd5)

  global coord_5
  coord_5= [crd5]

#######################################################################

def attack_on_pl (opp_move):
  if pl_grid[opp_move[0]][opp_move[1]] == "#":
    update_playergrid("X",opp_move[0],opp_move[1])
  else:
    update_playergrid("*",opp_move[0],opp_move[1])
     
  
def set_grid():
  print("Your grid:\n")
  player_grid()
  print("Enter ship coordinates:\n")
  # twoship()
  # threeship()
  fourship()
  # fiveship()
  global lost_playergrid
  lost_playergrid= copy.deepcopy(pl_grid)
  lost_plgrid(lost_playergrid)

def lose(grid):
  flag=0
  global lost_playergrid
  for i in 10:
    for j in 10:
       if grid[i][j]== "X":
          if lost_playergrid[i][j]=="X":
             continue
          else:
             flag==1
    if flag==1:
      return False
      break            
  print("Opponent won")
  return True
##################### OPPONENT FUNCTIONS #############################

opp_grid={}
lost_oppgrid={}

def oppo_grid():
    global opp_grid
    c = 65  
    print(f"  ", end='')
    for j in range(10):
        print(f"  {j+1} ", end='')    
    print("\n  ", (10*4)*"-")
      
    for i in range(10):
        print(f"{chr(c+i)} ", end='')
        for j in range(10):
            if opp_grid[i+1][j] == "X":
              print(Fore.RED+f"| {opp_grid[i+1][j]} ", end='')
            else:
              print(Style.RESET_ALL+f"| {opp_grid[i+1][j]} ", end='')              
        print(Style.RESET_ALL+"| ")
        print(Style.RESET_ALL+"  ", (10*4)*"-")
    print(Style.RESET_ALL+"\n")

def update_oppgrid(move,row,col):
  opp_grid[row][col-1]=move  

def lost_oppogrid(grid):
   for i in (65,75):
      for j in range (10):
         if grid[i+1][j]== "#":
            grid[i+1][j]= "X"

def attack_on_opp(pl_move):
  print(pl_move)
  global opp_grid
  if opp_grid[pl_move[0]][pl_move[1]] == "#":
    update_oppgrid("X",pl_move[0],pl_move[1])
    print_grids()
  else:
    update_oppgrid("*",pl_move[0],pl_move[1])
    print_grids()

def win(grid):
  flag=0
  for i in 10:
    for j in 10:
       if grid[i][j]== "X":
          if lost_oppgrid[i][j]=="X":
             continue
          else:
             flag==1
    if flag==1:
       return False
       break  
  print("You won")
  return True


############## EXPORTED FUNCTIONS ##############

def game_server(after_connect):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as accepter_socket:
      accepter_socket.bind(('', GAME_PORT))
      accepter_socket.listen(1)

      # non-blocking to allow keyboard interupts (^c)
      accepter_socket.setblocking(False)
      while True:
        try:
          game_socket, addr = accepter_socket.accept()
        except socket.error as e:
          if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
            time.sleep(0.1)
            continue
        break

      game_socket.setblocking(True)
      with game_socket:
        after_connect()
        set_grid()

        msg = pickle.dumps(pl_grid)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        game_socket.send(msg)
      
        full_msg = b''
        new_msg = True
        msg = game_socket.recv(1024)
        if new_msg:
          msglen = int(msg[:HEADERSIZE])
          new_msg = False

        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
          opp_grid=pickle.loads(full_msg[HEADERSIZE:])
          new_msg = True
          full_msg = b""
        
        print("Game started")

        while True:
          print("Opponents turn")

          full_msg = b''
          new_msg = True
          msg = game_socket.recv(1024)
          if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

          full_msg += msg

          if len(full_msg)-HEADERSIZE == msglen:
            opp_move=pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b""        
          # opp_move = game_socket.recv(1024)
          print(opp_move)
          if not opp_move:
            break
          attack_on_pl(opp_move)
          if lose(pl_grid):
            break
          print("Your turn")
          pl_move = [int(x) for x in input("Enter coordinates to strike: ").split()] 
          attack_on_opp(pl_move)
          game_socket.send(pl_move.encode())
          if win(opp_grid):
            break

        print_grids()
        print("game ended")

def game_client(opponent):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as game_socket:
      game_socket.connect((opponent, GAME_PORT))
      
      set_grid()
      
      full_msg = b''
      new_msg = True
      msg = game_socket.recv(1024)
      if new_msg:
        msglen = int(msg[:HEADERSIZE])
        new_msg = False

      full_msg += msg

      if len(full_msg)-HEADERSIZE == msglen:
        opp_grid=pickle.loads(full_msg[HEADERSIZE:])
        new_msg = True
        full_msg = b""

      msg = pickle.dumps(pl_grid)
      msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
      game_socket.send(msg)

      print('Game Started')

      while True:
        print("Your turn")
        x,y =input("Enter coordinates to strike: ").split()
        pl_move=[ord(x)-64,int(y)]
        print(pl_move[0],pl_move[1])
        attack_on_opp(pl_move)

        msg = pickle.dumps(pl_grid)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        game_socket.send(msg)  
        print("move sent")       
        if win(opp_grid):
            break
      
        print("Opponents turn")
        opp_move = game_socket.recv(1024).decode()
        if not opp_move:
          break
        attack_on_pl(opp_move)
        if lose(pl_grid):
            break
        
      print_grids()
      print("game ended")
