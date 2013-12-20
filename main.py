#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from random import shuffle
import os
import urllib
import webapp2
import cgi
import logging
import random

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.webapp import template

index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
game = []
suffleBoard = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
currentLevel = [{'':game}]
tempStorage = []
is_won = False
winnerPath = ''
completePath=[]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
                'index': index,
                'zero':index[0],
                'one':index[1],
                'two':index[2],
                'three':index[3],
                'four':index[4],
                'five':index[5],
                'six':index[6],
                'seven':index[7],
                'eigth':index[8],
                'nine':index[9],
                'ten':index[10],
                'eleven':index[11],
                'twelve':index[12],
                'thirteen':index[13],
                'fourteen':index[14],
                'fifteen':index[15],
                'path':winnerPath,
                }
    
        print index
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

def up(selected_board,i):
    myData = selected_board
    myData[i]=myData[i-4]
    myData[i-4]=0
    if myData == goal:
        global is_won
        is_won = True
        print 'won=',is_won
    return myData;

def down(selected_board,i):
    myData = selected_board
    myData[i]=myData[i+4]
    myData[i+4]=0
    if myData == goal:
        global is_won
        is_won = True
        print 'won=',is_won
    return myData;

def left(selected_board,i):
    myData = selected_board
    myData[i]=myData[i-1]
    myData[i-1]=0
    if myData == goal:
        global is_won
        is_won = True
        print 'won=',is_won
    return myData;

def right(selected_board,i):
    myData = selected_board
    myData[i]=myData[i+1]
    myData[i+1]=0
    if myData == goal:
        global is_won
        is_won = True
        print 'won=',is_won
    return myData;

def makeNextLevelBoard(currentboard):
    selectedBoard = []
    for m in list(currentboard.viewvalues())[0]:
        selectedBoard.append(int(m))
    selectedPath = list(currentboard.viewkeys())[0]
    global tempStorage
    for i in selectedBoard:
        if i==0:
            if selectedBoard.index(i) in [5,6,9,10]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [1,2]:
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [4,8]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [7,11]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [13,14]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [0]:
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [3]:
                tempStorage.append({''.join([selectedPath,'d']):down(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [12]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'r']):right(selectedBoard[:],selectedBoard.index(i))})
            elif selectedBoard.index(i) in [15]:
                tempStorage.append({''.join([selectedPath,'u']):up(selectedBoard[:],selectedBoard.index(i))})
                tempStorage.append({''.join([selectedPath,'l']):left(selectedBoard[:],selectedBoard.index(i))})
            else:
                print 'hi',i

def visitCurrentLevelBoards():
    while is_won is False:
        global currentLevel
        global tempStorage
        global completePath
        for i in currentLevel:
            makeNextLevelBoard(i)
        completePath.append(tempStorage[:])
        currentLevel = tempStorage[:]
        tempStorage = []
    for j in currentLevel:
        print list(j.viewvalues())[0]
        if list(j.viewvalues())[0]==goal:
            print 'winner path =',list(j.viewkeys())[0]
            global winnerPath
            winnerPath = list(j.viewkeys())[0]
            return 0;
    

class SwitchCell(webapp2.RequestHandler):
    def get(self):
        global index
        index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        global game
        game = []
        global suffleBoard
        suffleBoard = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
        global currentLevel
        currentLevel = [{'':game}]
        global tempStorage
        tempStorage = []
        global is_won
        is_won = False
        global winnerPath
        winnerPath = ''
        global completePath
        completePath = []
        self.redirect("/")
        

class NewGame(webapp2.RequestHandler):
    def get(self):
        global suffleBoard
        j=0
        while j<random.randint(1,10):
            print 'random =', random.randint(1,10)
            for i in suffleBoard:
                if i==0:
                    if suffleBoard.index(i) in [5,6,9,10]:
                        functions = [up,down,left,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [1,2]:
                        functions = [down,left,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [4,8]:
                        functions = [up,down,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [7,11]:
                        functions = [up,down,left]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [13,14]:
                        functions = [up,left,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [0]:
                        functions = [down,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [3]:
                        functions = [down,left]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [12]:
                        functions = [up,right]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                    elif suffleBoard.index(i) in [15]:
                        functions = [up,left]
                        suffleBoard = random.choice(functions)(suffleBoard[:],suffleBoard.index(i))
                j=j+1
        global index
        index = suffleBoard
        self.redirect("/")

class solver(webapp2.RequestHandler):
    def get(self):
        global game
        game.append(self.request.get('t1'))
        game.append(self.request.get('t2'))
        game.append(self.request.get('t3'))
        game.append(self.request.get('t4'))
        game.append(self.request.get('t5'))
        game.append(self.request.get('t6'))
        game.append(self.request.get('t7'))
        game.append(self.request.get('t8'))
        game.append(self.request.get('t9'))
        game.append(self.request.get('t10'))
        game.append(self.request.get('t11'))
        game.append(self.request.get('t12'))
        game.append(self.request.get('t13'))
        game.append(self.request.get('t14'))
        game.append(self.request.get('t15'))
        game.append(self.request.get('t16'))
        print 'game', game
        visitCurrentLevelBoards()

        template_values = {
            'index': game,
            'zero':game[0],
            'one':game[1],
            'two':game[2],
            'three':game[3],
            'four':game[4],
            'five':game[5],
            'six':game[6],
            'seven':game[7],
            'eigth':game[8],
            'nine':game[9],
            'ten':game[10],
            'eleven':game[11],
            'twelve':game[12],
            'thirteen':game[13],
            'fourteen':game[14],
            'fifteen':game[15],
            'path':winnerPath,
            'detailed':completePath,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/switchcell', SwitchCell),
                               ('/newgame', NewGame),
                               ('/solver', solver)],
                              debug=True)
