import gameSim
import logging
import sys
import datetime


logging.basicConfig(filename='assignment3log.log', level=logging.INFO)

# Get number of games user would like to run
numGames = int(sys.argv[1])

count = 0
while count < numGames:
    logging.info('Game ID: ' + str(count) + ' requested at ' + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    gameSim.runGame()
    count += 1
