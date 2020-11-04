import mm
import requests
import random
import logging
import datetime

def runGame():

    # Make list of possible player IDs (for testing)
    idList = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011']

    # Make a room requested by a random one of the players in our database
    playersInGame = mm.makeRoomOfThree(random.choice(idList))

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
        responseJson = response.json()
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
            responseJson = response.json()
            players = response.json()['Items']
            for player in players:
                if player['playerID'] == loser:
                    logging.info('Updated wins and losses' + str(player))
    else:
        print('There are not enough players at your skill level. Try again later!')
        logging.info('Could not do game, not enough players within skill level tolerance')
