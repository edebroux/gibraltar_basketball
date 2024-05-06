from datetime import datetime

class team:

    def __init__(self,name,enroll):
        # name = String
        # enroll = String
        self.name = name
        self.enroll = enroll
        self.opponents = []
        self.scores = []
        if int(enroll) > 1000:
          self.elo = 1800
        elif int(enroll) > 800:
          self.elo = 1600
        elif int(enroll) > 600:
          self.elo = 1400
        elif int(enroll) > 400:
          self.elo = 1200
        else:
          self.elo = 1000
          
    def __str__(self):
      return self.name

    def __repr__(self):
      return self.__str__()

    def getEnroll(self):
      return self.enroll

    def addScore(self, score):
      # score = game
      self.scores.append(score)

    def getScores(self):
      return self.scores

    def addOpponent(self, opponent):
      # opponent = team
      self.opponents.append(opponent)

    def getOpponents(self):
      return self.opponents

    def getTotalPoints(self):
      total = 0
      if len(self.scores) > 1:
        for s in self.scores:
          total += int(s.getScore().split('-')[0])
      return total

    def getTotalPointsAgainst(self):
      total = 0
      if len(self.scores) > 1:
        for s in self.scores:
          total += int(s.getScore().split('-')[1])
      return total

    def getRate(self):
      wins = 0
      games = 0
      if len(self.scores) > 1:
        for s in self.scores:
          if int(s.getScore().split('-')[0]) > int(s.getScore().split('-')[1]):
            wins += 1
          games += 1
      try:
        return round((wins/games), 3)
      except ZeroDivisionError:
        return 0.0

    def getRecord(self):
      wins = 0
      games = 0
      if len(self.scores) > 1:
        for s in self.scores:
          if int(s.getScore().split('-')[0]) > int(s.getScore().split('-')[1]):
            wins += 1
          else:
            games += 1
      return wins, games
        
class game:

    def __init__(self, score, date):
      # score = String
      # date = String
      self.score = score
      date = date.split('/')
      try:
        self.date = datetime(int(date[2]), int(date[0]), int(date[1]))
      except IndexError:
        self.date = date

    def __str__(self):
      return self.score

    def __repr__(self):
      return self.__str__()

    def getScore(self):
      return self.score

    def result(self):
      if int(self.getScore().split('-')[0]) > int(self.getScore().split('-')[1]):
        return True
      return False

    def getDate(self):
      return self.date