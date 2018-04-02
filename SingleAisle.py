#Basic model for borading B737-800 in a all econ config
#Select random process within main-#Random process

import numpy as np
import random as rnd
import math
import PIL
from PIL import Image, ImageDraw
import imageio as io
import shutil
import pathlib
import glob


##INPUT##
RowMax = 6
RowNum = 29
NoShow = int(round(np.random.normal(RowMax*RowNum*0.1,5,1)[0]))
ts_ave = 15
ts_std = 10
reflashRate = 10
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
    #Queue = simple_rnd(Queue)
    #Queue = group(Queue,5)
    Queue = altgroup(Queue,29,5)
    #Queue = rev(Queue)
    #Queue = pos(Queue)

    #Forming aircraft
    plane = np.zeros((RowMax+1,RowNum+1), dtype = float)

    #Borading process
    borading_idx = 0
    CLK = 0
    while np.count_nonzero(plane == 1) < RowMax*RowNum-NoShow or list(plane[0]).count(0) <= RowNum:
      CLK += 1
      for row in range(RowNum+1):#update_borading
        isle = float(plane[0][row])
        if(int(isle) == row and int(isle) != 0 and not isle.is_integer()):#is_this_row
          seat = int(round(math.modf(isle)[0]*10))
          plane[seat][row] = 1
          plane[0][row] = max(0,int(round(np.random.normal(ts_ave,ts_std,1)[0])))
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
      if(CLK%reflashRate==0):
          PrintPlane(plane,CLK)
    return(CLK)

###############Random Processes###############
#1) All random
def simple_rnd(Queue):
    rnd.shuffle(Queue)
    return Queue

#2) Reverse N-Groups
def group(Queue,N):
    n = int(round(len(Queue) / N))
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

#5) Alternating Groups
def altgroup(Queue,N,alt):
    n = int(round(len(Queue) / N))
    ls = []
    for i in range(0, len(Queue), n):
        ls.append(Queue[i:i + n])
    ls = ls[::-1]
    templs = []
    i = 0
    while len(templs) < len(ls):
        templs.insert(len(templs),ls[i])
        i = (i+alt)%len(ls)
    for i in templs:
        rnd.shuffle(i)
    ret = []
    for i in templs:
        for j in i:
            ret.append(j)
    return ret
#############################################

# Print
def PrintPlane(plane,CLK):
    array = []
    for i in range(len(plane)):
        if(i == 0):
            array.append(list(plane[int(round(RowMax/2))]))
        elif(i == int(round(RowMax/2))):
            array.append(list(plane[0]))
        else:
            array.append(list(plane[i]))
    ret = [[ "-" for y in range(len(plane[0]))] for x in range(len(plane))]
    for i in range(len(plane)):
        for j in range(len(plane[0])):
            if(array[i][j] == 1):
                ret[i][j] = "O"
            elif(array[i][j] != 0):
                ret[i][j] = "o"
    output = ""
    for i in ret:
        output += (str(i) + '\n')
    div = "-"
    for i in range(RowNum*5):
        div += "-"
        if(i == int(RowNum*5/2)):
            div += "B737-800 Time:"
            div += str(CLK)
    output += (str(div)  + '\n')
    #print(output)
    img = PIL.Image.new("RGBA", ((RowMax+1)*50,(RowNum+1)*50), color=0)
    for i in range((RowMax+1)):
        for j in range((RowNum+1)):
            string = ret[i][j]
            if(string == "-"):
                for x in range(50):
                    for y in range (50):
                        img.putpixel((i*50+x,j*50+y),(255, 255, 255))
            elif(string == "o"):
                for x in range(-25,25):
                    for y in range(-25,25):
                        if ((x)**2+(y)**2 <= 225):
                            img.putpixel((i * 50 + x + 25, j * 50 + y + 25), (51, 102, 255))
                        else:
                            img.putpixel((i * 50 + x + 25, j * 50 + y + 25), (255, 255, 255))
            else:
                for x in range(-25,25):
                    for y in range(-25,25):
                        if ((x ) ** 2 + (y ) ** 2 <= 225):
                            img.putpixel((i*50+x+ 25,j*50+y+ 25),(0, 0, 102))
                        else:
                            img.putpixel((i * 50 + x+ 25, j * 50 + y+ 25), (255, 255, 255))
    img2 = img.rotate(90,expand=1)
    img2 = img2.resize(((RowNum+1)*50-50,(RowMax+1)*50-30))
    imgb = Image.open("BGB738.png")
    imgb = imgb.convert("RGBA")
    tmp = Image.new('RGBA', imgb.size, (0, 0, 0, 0))
    tmp.paste(img2, (435, 285))
    tmp.putalpha(127)
    imgb = Image.alpha_composite(imgb, tmp)
    imgb = imgb.resize((2000,800))
    imgb.save("./png/"+str(CLK)+".png")


# Report
shutil.rmtree('./png/')#delete folder
pathlib.Path('./png/').mkdir(parents=True, exist_ok=True)#make folder

print("Total Time is:" + str(main()))#run

#save .gif
images = []
file_names = glob.glob('./png/*.png')
file_names.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
for filename in file_names:
    images.append(io.imread(filename))
io.mimsave('737.gif', images, fps = 10)

# Data collection
#ave = []
#for i in range(100):
    #print(str(i)+"%")
    #ave.append(main())
#print(sum(ave)/100)



