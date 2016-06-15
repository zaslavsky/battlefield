#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  battlefield.py
#  
#  Copyright 2014 Dmitry Zaslavsky <zaslavsky@CELESTIA>
#   _____________________________
#__/                             \_____
#  		mail:zaslavsky@live.ru
#  		Phone: 8-903-257-06-31
#  		www.vk.com/dmitry.zaslavsky
#__								  _____
#  \_____________________________/
#
#
import pygame, random , math , configparser
from pygame import gfxdraw

		
def error(ID): # Printing errors messages
	if ID==1:print("ERROR:\n\tFile (data\config.ini) not found or Broken\n\tPleace check (config.ini) file")
	if ID==2:print(("ERROR:\n\tFile (Image File) not found\n\tor wrong file path in (config.ini) > (imageFile)\n\tCheck Data files"))
	print("\a\a\a\nPress any key...")
	input()		
	

#Read INI File.
config = configparser.ConfigParser()
config.read('data\config.ini')
try:data=config['OPTIONS']
except:error(1)	
IMAGEFILE=data.get('ImageFile')
SECTORCOLOR = (0,0,0)

#Pygame init

mainloop = True

pygame.init()
pygame.display.set_caption("Battlefield")
try:background = image = pygame.image.load(IMAGEFILE)
except:error(2)
WH=W,H=background.get_size()
screen=pygame.display.set_mode(WH)
background = background.convert()
image = image.convert() 

######################################
def rand(a,b): #short randomization
	return random.randint(a,b)

def getdata(): # read INI file
	global dotx,doty,DOT,FAR,FOV,targets,ENEMYES,TARGETS,PURE,ANGLEWEIGHT
	TARGETS=[]
	data=config['OPTIONS']
	RANDOM=int(data.get('Generate'))
	PURE=int(data.get('Make_angle_pure'))
	ANGLEWEIGHT=int(data.get('angles_weight'))
	if RANDOM == 0:
		data=config['VALUES']
		DOT=(data.get('DOTCORD'))
		DOT=DOT.split(',')
		DOT=dotx,doty=int(DOT[0]),int(DOT[1])
		FOV=int(data.get('FOV'))
		FAR=int(data.get('FAR'))
		ENEMYES=((data.get('ENEMYES')))
		TARGETS=parser(ENEMYES)
	else:
		data=config['GENERATE_VALUES']
		
		DOTA=(data.get('DOTCORD_MAX'))
		DOTA=DOTA.split(',')
		DOTA=dotax,dotay=int(DOTA[0]),int(DOTA[1])
		
		FOVA=int(data.get('FOV_MAX'))
		FARA=int(data.get('FAR_MAX'))
		
		DOTB=(data.get('DOTCORD_MIN'))
		DOTB=DOTB.split(',')
		DOTB=dotbx,dotby=int(DOTB[0]),int(DOTB[1])
		
		FOVB=int(data.get('FOV_MIN'))
		FARB=int(data.get('FAR_MIN'))
		
		DOT=dotx,doty=rand(dotbx,dotax),rand(dotby,dotay)
		FOV=rand(FOVB,FOVA)
		FAR=rand(FARB,FARA)
		
		ENEMYESCOUNT=int(data.get('ENEMYESCOUNT'))
		TARGETS=randenemy(ENEMYESCOUNT)


def parser(array):# Parser for INI
	output=[]
	for i in (array.split('\n')):
		part=int(i.split(',')[0]),int(i.split(',')[1])
		output.append(part)
	return output
	
def corect(array): # Cordinate localization
	output=[]
	for i in array:
		data=x,y=(i[0]-dotx,i[1]-doty)
		output.append(data)
	return output
	
	

def enemydraw(array): # draw red dots =D
	for i in array:
		pygame.draw.circle(background, (0,0,0), i, 7)
		pygame.draw.circle(background, (255,0,0), i, 5)
		pygame.draw.circle(background, (0,0,0), i, 2)

def randenemy(count): #  generate enemy positions 
	output=[]
	while count!=0:
		data=x,y=(rand(0,W),rand(0,H))
		output.append(data)
		count-=1
	return output
			
def angle(x,y):				# return angle
	rad=math.atan2(y,x)
	angle=math.degrees(rad)
	if angle<0:angle+=360
	return angle
	
def drawsector(angle,far,tar): #drawing fire range
	agh=tar-(angle/2)
	for i in range(angle-1):
		poo=angletocord(agh+i,far)
		pygame.draw.aaline(background, (255,255,0), (dotx,doty),poo,5)
	cord=x,y=dotx,doty
	a1=math.radians(tar+(angle/2))
	a2=math.radians(tar-(angle/2))
	lx1=(math.cos(a1)*far)+x
	ly1=(math.sin(a1)*far)+y
	lx2=(math.cos(a2)*far)+x
	ly2=(math.sin(a2)*far)+y
	pygame.draw.aaline(background, (SECTORCOLOR), (x,y),(lx1,ly1),5)
	pygame.draw.aaline(background, (SECTORCOLOR), (x,y),(lx2,ly2),5)
	
def angletocord(angle,far):	#angle to coordinat
	x=(math.cos(math.radians(angle))*far)+dotx
	y=(math.sin(math.radians(angle))*far)+doty
	out=x,y
	return out
		
def pureangle(array):# make angle good
	angle=0
	output=[]
	cluster=[]
	for i in range(len(array)):
		if array[i]==(max(array)):
			cluster.append(i)
			try:
				if array[i+1]!=(max(array)):
					output.append(cluster)
					cluster=[]
			except:
				output.append(cluster)
				cluster=[]
	for i in output:cluster.append(len(i))
	for i in output[cluster.index(max(cluster))]:angle+=i
	angle=(angle/len(output[cluster.index(max(cluster))]))
	return angle

def optimize(targets): # seporate enemyes who stay beyond the circle
	output=[]
	for i in range(len(targets)):
		x=targets[i][0]
		y=targets[i][1]
		gipo=math.sqrt((x**2)+(y**2))
		if gipo<FAR:output.append(targets[i])
	return output
				
def findangle(targets): # finding better shooting angle
	Rotate=0
	angles=[]
	targets=optimize(targets)
	while Rotate!=360:
		count=0
		for i in range(len(targets)):
			x=targets[i][0]
			y=targets[i][1]
			a=(Rotate-FOV/2)
			b=(Rotate+FOV/2)
			gipo=math.sqrt((x**2)+(y**2))
			if ANGLEWEIGHT==1:
				if a<angle(x,y)<b and gipo<FAR:count+=1
			else:
				if a<angle(x,y)<b and gipo<FAR:count+=1
		angles.append(count)
		if ANGLEWEIGHT==1:
			poo=angletocord(Rotate,count*10)
			pygame.draw.aaline(background, (0,255,0), (dotx,doty),poo,5)
		Rotate+=1
	if PURE==1:V=(pureangle(angles))
	else:V=angles.index(max(angles))
	print("\n_____________________________________________________")
	print("Gun angle: "+str(360-V))
	print("Targets covered: ")+str(max(angles))
	if (max(angles))==0:print("Sad situation. No Enemyes to shoot")
	return V

def execute(): # execute algoritm and little bit drawing 
	try:getdata()
	except:
		print("fail")
		quit()
	pygame.draw.circle(background, (0,0,0), (dotx,doty), 11, 0)
	pygame.draw.circle(background, (40,130,40), (dotx,doty), 9, 0)
	pygame.draw.circle(background, (100,200,90), (dotx,doty), 7, 0)
	pygame.draw.circle(background, (0,0,0), (dotx,doty), 4, 0)
	pygame.gfxdraw.aacircle(background, dotx,doty, FAR, (160,120,217))
	direction=findangle(corect(TARGETS))
	drawsector(FOV,FAR,direction)
	enemydraw(TARGETS)
	pygame.gfxdraw.arc(background, dotx, doty, FAR, direction-FOV/2, direction+FOV/2,SECTORCOLOR)

#we start here!
execute()# predraw
while mainloop:#main loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
				background.blit(image, (0,0))
				execute()
				screen.blit(image, (0,0))
				#pygame.draw.circle(background, (100,100,100), (random.randint(0,500),random.randint(0,500)), 3, 0)
    screen.blit(background, (0,0))                     
    pygame.display.update()            
    pygame.display.flip()
pygame.quit()