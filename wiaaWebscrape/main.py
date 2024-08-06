import csv
import sys
from bs4 import BeautifulSoup
import requests

def main():

  if len(sys.argv) > 1:
    teams = sys.argv[1]

    #findCodes(teams)
    if len(sys.argv) > 2:
      addGames(teams, sys.argv[2])      


def findCodes(a):
  # a = first file - starts with 35042 for 2021-22 Season 
  # a = first file - starts with 46803 for 2022-23 Season
  # a = first file - starts with 66617 for 2023-24 Season
  count = 35042
  while True:
    while True:
      linkDict = openWebsite(count)
      count += 1
      print(count)
      if linkDict is not None:
        break
    school = linkDict[0]
    enroll = linkDict[1]
    link = linkDict[2]
    with open(a, 'at', newline='') as i:
      writer = csv.writer(i, delimiter=',')
      row = []
      row.append(school)
      row.append(enroll)
      row.append(link)
      writer.writerow(row)


def missing(a, b):
  # a = first files team names
  # b = second files team names
  missing = []
  for row in a:
    if row not in b:
      missing.append(row)
  print(missing)


def openWebsite(a):
  # a = first file
  linkName = []
  link = 'https://schools.wiaawi.org/Directory/Schedule/Index?TeamID=' + str(a)
  page = requests.get(link)
  soup = BeautifulSoup(page.text, "html.parser")
  text = soup.find_all('h5')
  name = soup.find_all('h3')
  if '’' in name:
    name = name.replace('’', '')
  # Edit to season you want data for if you want to download more data
  check = 'Varsity2022-2023GirlsBasketball'
  linkName.append(link)
  if (text[-3].text == "Yes"):
    filler = text[-12].text + text[-10].text + text[-9].text + text[-8].text
    linkName.append(text[-4].text)
  else:
    filler = text[-11].text + text[-9].text + text[-8].text + text[-7].text
    linkName.append(text[-3].text)
  
  if filler == check:
    linkName.append(name[0].text)
    linkName.reverse()
    return linkName

def addGames(a, b):
  # a = first file
  # b = second file
  with open(a, 'rt', newline='') as f, open(b, 'wt', newline='') as i:
    reader = csv.reader(f, delimiter=',')
    wr = csv.writer(i, delimiter=',')
    for row in reader:
      page = requests.get(row[2])
      soup = BeautifulSoup(page.text, "html.parser")
      elements = []
      games = []
      results = []
      scores = []
      dat = []
      name = soup.find('h3').text
      if '’' in name:
        name = name.replace('’', '')
      table = soup.findChildren('table')[0]
      tr = table.findChildren('tr')
      for trs in tr:
        cells = trs.findChildren('td')
        for rows in cells:
          value = rows.findChildren('span')
          for values in value:
            elements.append(values.text)
          date = rows.findChildren('label')
          for dates in date:
            dat.append(dates.text)
      dat = [i for i in dat if '/' in i and '\xa0' not in i and '@' not in i]
      elements = [i for i in elements if i != '\xa0'] 
      j = 0
      while j < len(elements):
        elements.pop(j)
        j += 3
      for e in elements:
        if e.replace('’', '') == name:
          elements.pop(elements.index(e))
      for e in range(len(elements)):
        if elements[e] == '':
          try:
            if 'W ' in elements[e + 1] or 'L ' in elements[e + 1]:
              elements[e] = "Unknown"
              continue
          except IndexError:
            elements = elements[:e-1]
            break
          elements = elements[:e-1]
          break
      for e in elements:
        if 'L ' in e or 'W ' in e:
          results.append(str(e).strip())
          try:
            scores.append(e[2:].split('-')[0]+'-'+e[2:].split('-')[1].split(' ')[0])
          except IndexError:
            games.append(e.replace('’', ''))
        else:  
            games.append(e.replace('’', ''))
      if row[0].replace('’', '') == name:
        row.append(games)
        row.append(scores)
        row.append(results)
        row.append(dat[:len(games)])
        wr.writerow(row)
    
  i.close()

main()