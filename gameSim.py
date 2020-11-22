import logging
import sys
import datetime
import random
import socket
import time
import threading
from datetime import datetime
import json
import requests

serverIP = "3.137.149.42"
serverPort = 12345
logging.basicConfig(filename='assignment3log.log', level=logging.INFO)

numGames = input("Enter number of games you'd like to simulate: ")

count = 0
while count < numGames:
    logging.info('Game ID: ' + str(count) + ' requested at ' + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
    runGame()
    count += 1


def runGame():

    # Make list of possible player IDs (for testing)
    idList = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011']


    # Send a random id of a player to the matchmaking server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(serverIP, serverPort)
        id = json.dumps(random.choice(idList))
        print('Send', id)
        sock.sendall(id)
        data = sock.recv(1024)


    # Get a list of players in the game
    playersInGame = json.loads(data)

    competingIDs = []

    # If there are enough players in the db within skill tolerance to start, put their ids in a list and start the game
    if len(playersInGame) == 3:
        for player in playersInGame:
            competingIDs.append(player['playerID'])
                
        # Print the IDs of the players competing
        print('The game is on with these players competing!')
        for ID in competingIDs:
            print(ID)

        # Pick winner randomly
        winner = random.choice(competingIDs)
        competingIDs.remove(winner)

        # Print the winner
        print('The winner is ' + winner + '!')
        logging.info('Player ' + winner + ' won.')

        # Update the database with winner data
        requests.get('https://bg5i4i7ta0.execute-api.us-east-2.amazonaws.com/default/updatePlayerScore', params={'playerID': winner, 'won': 'won'})
        
        # Log skill level of winner after the game
        response = requests.get('https://iu546cqfr3.execute-api.us-east-2.amazonaws.com/default/getAllPlayers')
        players = response.json()['Items']
        for player in players:
            if player['playerID'] == winner:
                logging.info('Updated wins and losses' + str(player))


        # Update the database with loser data
        for loser in competingIDs:
            print(loser + ' is a loser')
            requests.get('https://bg5i4i7ta0.execute-api.us-east-2.amazonaws.com/default/updatePlayerScore', params={'playerID': loser, 'lost': 'lost'})
            # Log skill level of losers after the game
            response = requests.get('https://iu546cqfr3.execute-api.us-east-2.amazonaws.com/default/getAllPlayers')
            players = response.json()['Items']
            for player in players:
                if player['playerID'] == loser:
                    logging.info('Updated wins and losses' + str(player))
    else:
        print('There are not enough players at your skill level. Try again later!')
        logging.info('Could not do game, not enough players within skill level tolerance')
