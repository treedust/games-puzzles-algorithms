# iterative sliding-tile specific algorithm     rbh 2016
# under construction

from random import shuffle
from time import sleep, time
from sys import stdin

class Tile:
  """a simple sliding tile class"""

  def __init__(self):
    self.state = []
    self.made_slide = True
    for line in stdin:
      for elem in line.split():
        self.state.append(int(elem))
    # rows, cols are 1st 2 elements of list, so pop them
    self.r, self.c = self.state.pop(0), self.state.pop(0)
    # state now holds contents of tile in row-major order
    
    assert(self.r>=2 and self.c>=2)
    for s in self.state: assert(s>=0 and s < self.r*self.c)
    ndx_min = self.state.index(min(self.state))
    assert(self.state[ndx_min] == 0)

    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.c, self.c
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down

  def bound_check(self,coords,move):
    psn = self.psn_of(coords)
    tmp_mv = psn+move
    tmp_coords = self.coords(tmp_mv)
    if (tmp_coords[0] >= self.r or tmp_coords[1] >= self.c):
      print(">>>column or row move NOT valid<<<")
      return 0
    elif ( tmp_coords[0] == coords[0] and tmp_coords[1] != coords[1] ): #row move check
      #print("VALID row move")
      return 1
    elif ( tmp_coords[0] != coords[0] and tmp_coords[1] == coords[1] ): #column move check
      #print("VALID column move")
      return 1
    else:
      return 0

  def slide(self,shift):
    # slide a tile   shift is from blank's perspective
    b_dx = self.state.index(0) # index of blank
    o_dx = b_dx + shift        # index of other tile
    self.made_slide = False
    if o_dx < self.r*self.c:
      self.state[b_dx], self.state[o_dx] = self.state[o_dx], self.state[b_dx]
      self.made_slide = True
    self.showpretty()

  def coords(self,psn):
    if psn <= -1:
      return None
    return psn // self.c, psn % self.c
  
  def psn_of(self, coord):
    if coord is None:
      return -1
    return coord[1] + self.c*coord[0]

  def is_UL(self, a_c, b_c): return a_c[0] <= b_c[0] and a_c[1] <= b_c[1]

  def mv_blank(self,psn,direction): # blank to psn, try direction first
    #sleep(.5)
    #print('  blank to', psn,'direction',direction,'\n')
    y_crds = self.coords(psn)
    if y_crds is None:
      return
    print('>>>>slides')
    while True:
      b_dx = self.state.index(0)
      if (b_dx == psn) or (self.made_slide is False): return
      b_crds = self.coords(b_dx)
      if direction==self.LF or direction==self.RT:
        if   b_crds[1] > y_crds[1]: self.slide(self.LF)
        elif b_crds[1] < y_crds[1]: self.slide(self.RT)
        elif b_crds[0] < y_crds[0]: self.slide(self.DN)
        else:                       self.slide(self.UP)
      else: 
        if   b_crds[0] > y_crds[0]: self.slide(self.UP)
        elif b_crds[0] < y_crds[0]: self.slide(self.DN)
        elif b_crds[1] > y_crds[1]: self.slide(self.LF)
        else:                       self.slide(self.RT)

  def blank_ok(self,bc,tc): # blank is left of or above t
    return bc[0]==tc[0] and bc[1]==tc[1]-1 \
        or bc[1]==tc[1] and bc[0]==tc[0]-1

  def showpretty(self):      
    #print(self.rows, self.cols, self.state.index(0), self.shifts)
    count, outstring = 0, ''
    for x in self.state:
      count += 1
      if x==0: outstring   += '   '
      elif x<10: outstring += ' ' + str(x) + ' '
      else: outstring      +=       str(x) + ' '
      if count%self.c == 0: outstring += '\n'
    print(outstring)
    sleep(.5)

  def tst_mv(self):
    r = list(range(self.r*self.c))
    shuffle(r)
    for j in r:
      if j%2==0:
        self.mv_blank(j, self.UP)
      else:
        self.mv_blank(j, self.LF)

  def tst_iter(self):
    #for j in range(10):
    #  print('\ntst',j,'\n')
    #  shuffle(self.state)
    #  sleep(.5)
    #  self.itersolve()
    #self.state = [11,10, 9, 2,1,13, 7, 5,15, 0, 8,14,3,12, 6, 4]
    self.itersolve()

  def mv_tile(self,t,xlcn): # move tile t to destination xlcn
    def delta_c(ac,bc): return (bc[0]-ac[0],bc[1]-ac[1])

    def init():
      xc = self.coords(xlcn) # destination
      t_index = self.state.index(t)
      tc = self.coords(t_index)
      print('xlcn', xlcn, ' t_index', t_index,'\n')
      bc = self.coords(self.state.index(0))
      delta = delta_c(tc,xc) # coord delta from tile to dest
      #print('                  delta ',delta)
      #sleep(.5)
      abv = -1
      if tc[0] > 0: # if has above tile
        abv = self.psn_of((tc[0]-1,tc[1])) # above tile
      lf = -1
      if tc[1] > 0: # if has left tile
        lf  = self.psn_of((tc[0],tc[1]-1)) # left of tile
      rt = -1
      if tc[1] < self.r-1: # if has right tile
        rt  = self.psn_of((tc[0],tc[1]+1)) # right of tile
      return xc, t_index, tc, bc, delta, abv, lf, rt

    # assume tiles 1.. t-1 already in psn
    #print('\nmv_tile',t,xlcn,'\n')
    self.showpretty()
    sleep(1)
    while True:
      dst_coords, t_index, t_coords, blank_coords, delta, abv_t, left_t, right_t = init()
      print('blank_coords',blank_coords,' t_coords',t_coords,' dst_coords',dst_coords,' abv_t',abv_t,' left_t',left_t,' right_t',right_t)
      if t_index == xlcn or (self.made_slide is False): return
      if t_coords[1] < dst_coords[1]: # tile left of destination
        print('tile left dest')
        assert(t_coords[0] > dst_coords[0]) # then tile must also be below
        if t_coords[0]==dst_coords[0]+1: # tile at topmost position
          print('case A')
          if blank_coords[0]<t_coords[0]:
            print('-slide DN')
            self.slide(self.DN)
          self.mv_blank(right_t,self.RT)
          print('-slide LF')
          self.slide(self.LF)
        elif (blank_coords[1]<t_coords[1] or            # blank left of tile
          blank_coords[1]==t_coords[1] and blank_coords[0]<t_coords[0]): # blank above
          print('case B  abv_t',abv_t)
          self.mv_blank(abv_t,self.UP)
          print('-slide DN')
          self.slide(self.DN)
        else: 
          print('case C')
          self.mv_blank(right_t,self.UP)
          print('-slide LF')
          self.slide(self.LF)
      # tile not left of destination
      elif t_coords[1]==dst_coords[1]: # tile below dst (tile and dst are in same column)
        #print('tile below dest')
        print(t_coords,dst_coords)
        if t_coords[0]==dst_coords[0]+1: # title is directly below dst
          print('case D')
          #print('tile immediately below dst')
          if blank_coords[0]==t_coords[0] and blank_coords[1]<t_coords[1] and blank_coords[0]<self.r-1:
            # blank is same row as title and left of column and blank is not in final row
            print('-slide DN')
            self.slide(self.DN)
          if blank_coords[0]>=t_coords[0] and blank_coords[1]<=t_coords[1] and blank_coords[1]<self.c-1:
            # blank is under or same row as tile and left of or same column and not in final column
            self.mv_blank(right_t,self.RT)
          self.mv_blank(abv_t,self.UP)
          print('-slide DN')
          self.slide(self.DN)
          #print('why not stop here')
        else: # tile is not directly below dst
          print('case E')
          if blank_coords[0]>t_coords[0] and blank_coords[1]==t_coords[1] and blank_coords[1]<self.c-1:
            # blank is under tile and blank is same column as tile
            print('-side RT')
            self.slide(self.RT)
          self.mv_blank(abv_t,self.UP)
          print('-slide DN')
          self.slide(self.DN)
      # tile not left or below
      elif blank_coords[0]>t_coords[0] or blank_coords[0]-blank_coords[1] > t_coords[0]-t_coords[1]:
        # blank below tile or below UL-to-BR diagonal thru tile
        #print('tile other dest')
        print('case F')
        self.mv_blank(left_t, self.LF)
        print('-slide RT')
        self.slide(self.RT)
      elif t_coords[0] == dst_coords[0]: # tile same row as destination
        #print('tile other dest')
        print('case G')
        if blank_coords[0] == t_coords[0] and blank_coords[1] > t_coords[1]: #blank same row and right
          print('-slide DN')
          self.slide(self.DN)
        self.mv_blank(left_t, self.LF)
        print('-slide RT')
        self.slide(self.RT)
      else:
        #print('tile other dest')
        print('case H')
        self.mv_blank(abv_t, self.UP)
        print('-slide DN')
        self.slide(self.DN)

      dst_coords, t_index, t_coords, blank_coords, delta, abv_t, left_t, right_t = init()
      if t_index == xlcn: return
      #assert(self.blank_ok(blank_coords,t_coords)) # blank now left or above
      if blank_coords[1]>=dst_coords[1]:
        print('blank is to the right of the dst or same column')
        if blank_coords[0]==t_coords[0] and blank_coords[1]==t_coords[1]-1:
          print('-slide RT')
          self.slide(self.RT)
        if blank_coords[0]==t_coords[0]-1 and blank_coords[1]==t_coords[1]:
          print('-slide DN')
          self.slide(self.DN)
 
  def itersolve(self): # solve iteratively
    def insubboard(xcrd, ulcrd):
      return xcrd[0] >= ulcrd[0] and xcrd[1] >= ulcrd[1]
          
    def shifts(st, lcn, c, L):
      for shift in L:
        st = str_swap(st, lcn, shift)
        lcn += shift
        print(pretty(st, c, True))
      return st

    def finallcn(j): # final position of element j
      return j-1
    
    def col_of(st,cols,c): # in state st, column index of chr c
      return st.index(c) % cols

    def targetlist(n): # return target state, as list
      L = []
      for j in range(1,n): L.append(j)
      L.append(0)
      return L

    UP, DN, LF, RT = self.UP, self.DN, self.LF, self.RT
    self.mv_tile(1,0)
    self.mv_tile(2,1)
    self.mv_tile(3,2)

st = Tile()
#st.tst_mv()
st.tst_iter()
