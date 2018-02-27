#Basic model for borading B737-800 in a all econ config
#Select random process within main-#Random process

import numpy as np
import random as rnd
import math



##INPUT##
RowMax = 6
RowNum = 29
NoShow = int(round(np.random.normal(RowMax*RowNum*0.1,5,1)[0]))
ts_ave = 10
ts_std = 5
reflashRate = 1000
#########

def main():
    #Forming Queue
    Queue = []
    for row in range(1,RowMax+1):
      for col in range(1,RowNum+1):
        Queue.append(col+row*0.1)
    for i in range(NoShow):
      Queue.pop(np.random.randint(0,len(Queue)))
    Queue.sort()

    #Random process
    Queue = simple_rnd(Queue)
    #Queue = group(Queue,5)
    #Queue = rev(Queue)
    #Queue = pos(Queue)

    #Forming aircraft
    plane = np.zeros((RowMax+1,RowNum+1), dtype = float)

    #Borading process
    borading_idx = 0
    CLK = 0
    while np.count_nonzero(plane == 1) < RowMax*RowNum-NoShow or list(plane[0]).count(0) <= RowNum:
      for row in range(RowNum+1):#update_borading
        isle = float(plane[0][row])
        if(int(isle) == row and int(isle) != 0 and not isle.is_integer()):#is_this_row
          seat = int(round(math.modf(isle)[0]*10))
          plane[seat][row] = 1
          plane[0][row] = int(round(np.random.normal(ts_ave,ts_std,1)[0]))
        elif(isle.is_integer() and isle > 0):#is_waiting
          plane[0][row] = int(plane[0][row]) - 1
        elif(isle.is_integer() and isle < 0):#rounding_error
          plane[0][row] = ts_ave
      for row in reversed(range(RowNum)):#update_arrival
        if(int(plane[0][row+1]) == 0 and not float(plane[0][row]).is_integer()):
          plane[0][row+1] = plane[0][row]
          plane[0][row] = 0
      if(borading_idx < len(Queue) and int(plane[0][0]) == 0):#new_arrival
        plane[0][0] = Queue[borading_idx]
        borading_idx += 1
      CLK += 1
      if(CLK%reflashRate==0):
          PrintPlane(plane)
    return(CLK)

#Random Processes
#1) All random
def simple_rnd(Queue):
    rnd.shuffle(Queue)
    return Queue

#2) Reverse N-Groups
def group(Queue,N):
    n = int(round(len(Queue)/N))
    ls = []
    for i in range(0, len(Queue), n):
        ls.append(Queue[i:i + n])
    for i in ls:
        rnd.shuffle(i)
    ret = []
    for i in ls:
        for j in i:
            ret.append(j)
    return ret[::-1]

#3) Reverse order
def rev(Queue):
    return Queue[::-1]

#4) Postive order
def pos(Queue):
    return Queue

# Print
def PrintPlane(plane):
    print(plane)

# Report
print("Total Time is:" + str(main()))




