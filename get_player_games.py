import berserk
import os
import sys
import json
import boto3
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)
player = 'chaimlefkowitz'

def get_token():
    with open('./.api_key') as f:
        token = f.read()
    return token

def get_client():
    token = get_token()
    session = berserk.TokenSession(token)
    lichess_client = berserk.Client(session)
    return lichess_client

def process_game(game, player):
    players = game['players']
    side = 'white' if players['white']['user']['name'].lower() == player.lower() else 'black'
    moves = game['moves'].split()
    prefix = f'{player}#{side}'
    offset = 0 if side == 'white' else 1
    print(len(moves))
    first_opp_move = '' if side == 'white' else moves[0]
    first_k_moves = [moves[0]] if side == 'black' else []
    prefix = f'{player}#{side}#'
    entry = f'{prefix}{"_".join(first_k_moves)}#'
    for i in range(offset,len(moves),2):
        first_k_moves.append(moves[i])
        first_k_moves.append(moves[i+1])
        print(f'enter: {entry} -> {moves[i]}!')
        entry = f'{prefix}{"_".join(first_k_moves)}#'
        #print(entry)
        if i > 10:
            break

def get_games(player):
    start = berserk.utils.to_millis(datetime(2020, 1, 8))
    lichess_client = get_client()
    games_generator = lichess_client.games.export_by_player(player,until=start,max=100)
    games = list(games_generator)
    process_game(games[1], player)
    process_game(games[2], player)
    #pp.pprint(games[0])

if __name__ == '__main__':
    get_games(player)
