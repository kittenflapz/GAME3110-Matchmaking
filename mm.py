import requests
import json
import sys
import datetime
import random
import time
import socket
from _thread import *
import threading
from operator import itemgetter
import logging
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
logging.basicConfig(filename='matchmakingServer.log', level=logging.INFO)


def makeRoomOfThree(sock):
    while True:
        sock.listen()
        conn, addr = sock.accept()

        with conn:
            IDofPlayerRequestingMatch = conn.recv(1024)
            IDofPlayerRequestingMatch = pickle.loads(IDofPlayerRequestingMatch)
            if IDofPlayerRequestingMatch != "":
                # Get the player database
                response = requests.get(
                    'https://iu546cqfr3.execute-api.us-east-2.amazonaws.com/default/getAllPlayers')

                # Get just the player list from the database (the items)
                players = response.json()['Items']

                tolerance = 20
                playerRequestingMatch = None

                # Print the player's info whose ID was passed in
                # While we are here, set any players who have played less than 3 games' win percentage to 50
                print('Player searching for match: ')
                for player in players:
                    if player['playerID'] == IDofPlayerRequestingMatch:
                        print(player)
                        playerRequestingMatch = player
                    if player['totalGames'] < 3:
                        player['winPercentage'] = 50.0

                # Print everyone else's info
                print('All available players: ')
                for player in players:
                    if player != playerRequestingMatch:
                        print(player)

                potentialPlayers = []
                # Make a list of available players in tolerance
                for player in players:
                    if abs(player['winPercentage']-playerRequestingMatch['winPercentage']) < tolerance and player != playerRequestingMatch:
                        potentialPlayers.append(player)

                # Sort the list by win percentage
                sortedPotentialPlayers = sorted(
                    potentialPlayers, key=itemgetter('winPercentage'))

                # Make a list of tuples of player(dict) and float (distance from player requesting game win% to player available win%)
                doubleSortedPotentialPlayers = [(player, abs(
                    player['winPercentage']-playerRequestingMatch['winPercentage'])) for player in sortedPotentialPlayers]

                # Sort the list of tuples by their dist
                doubleSortedPotentialPlayers.sort(key=itemgetter(1))

                # Turn the list of tuples back into a list of just dicts
                finalSortedPlayers = [seq[0] for seq in doubleSortedPotentialPlayers]

                print('Available players within tolerance of ' + str(tolerance) + ': ')
                for player in finalSortedPlayers:
                    print(player)

                # Remove items from end of list until we have the 2 players closest in win % to the player requesting the game
                while len(finalSortedPlayers) > 2:
                    finalSortedPlayers.pop()

                # Finally, add the player requesting the game back to the list
                finalSortedPlayers.append(playerRequestingMatch)

                for player in finalSortedPlayers:
                    logging.info('Following player connected at ' +
                                datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S"))
                    logging.info(player)

                # Return the final list
                response = pickle.dumps(finalSortedPlayers)
                conn.sendall(response)



ip = ''  
port = 12345        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip, port))
    start_new_thread(makeRoomOfThree, (s,))
    while True:
        time.sleep(1)