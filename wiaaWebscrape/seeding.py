import csv
from itertools import chain
import sys
from classes import game
from classes import team

def main():
  
  if len(sys.argv) == 2 or len(sys.argv) == 3:
    wiaa = {}
    opponents = []
    missing = []
    file = sys.argv[1]
    with open(file, 'rt', newline = '') as f:
      reader = csv.reader(f, delimiter = ',')
      for t in reader:
        teams = team(t[0], t[1])
        scores = t[4].split()
        ops = list(t[3].split(",\'"))[0]
        date = t[5].split()
        check_result = True
        print(ops)
        opponents.append()
        print(opponents)
        for t in range(len(scores)):
          scores[t] = scores[t].replace('[', '').replace('\'', '')
          date[t] = date[t].replace('[', '').replace('\'', '')
          teams.addScore(game(scores[t][:-1],date[t][:-1]))
        wiaa[teams] = []
       

    counter = 0
    opss = []
    for t in wiaa:
      for op in opponents[counter]:
        if (op not in [str(element).replace('’', '').replace('\'', '') for element in wiaa]):
          missing.append(op)
        else:
          for w in wiaa:
            if op == w.__str__():
              opss.append(w)
      wiaa[t] = opss
      opss = []
      counter += 1
    missing.append("Unknown")
    missing = list(set(missing))
    print(missing)
    if len(sys.argv) == 3:
      csvGames(wiaa, sys.argv[2], missing)
      
  else:
    print('Usage: python seeding.py [teams.csv]')

def check(a):
  return any(',' not in t for t in a)

def winRate(a, m):
  # a = List
  ave = 0
  for t in a:
    if t in m:
      print(t)
      ave += 0.5
    else:
      ave += t.getRate()
  try:
    return round(ave/len(a), 3)
  except ZeroDivisionError:
    return 0.0
    
def getOps(a, b):
  # a = Dictionary of Teams
  # b = Team
  for i in a:
    if b.__str__() == i.__str__():
      return a[i]
  return

def getOpsOps(a, b):
  # a = Dictionary of Teams
  # b = Team
  ops = []
  for i in getOps(a, b):
    ops.append(getOps(a, i))
  ops = list(set(chain.from_iterable(ops)))
  for i in ops:
    if i == b:
      ops.remove(b)
  return ops

def lost(a, b):
  # a = Dictionary of Teams
  # b = Team
  ls = []
  for i in range(len(getOps(a, b))):
    try:
      if b.getScores()[i].result():
        ls.append(getOps(a, b)[i])
    except IndexError:
      return ls
  return ls

def lostOps(a, b):
  # a = Dictionary of Teams
  # b = Team
  ls = []
  for i in lost(a, b):
    ls.append(getOps(a, i))
  ls = list(set(chain.from_iterable(ls)))
  for i in ls:
    if i == b:
      ls.remove(b)
  return ls

def csvGames(a,b,m):
  # a = Dictionary of Teams
  # b = csv file
  with open(b, 'w', newline = '') as f:
    writer = csv.writer(f)
    for i in a:
      row = []
      own = i
      row.append(own.__str__())
      row.append(own.getRate())
      row.append(winRate(getOps(a, own),m))
      row.append(winRate(getOpsOps(a, own),m))
      row.append(winRate(lost(a, own),m))
      row.append(winRate(lostOps(a, own),m))
      writer.writerow(row)
      
main()