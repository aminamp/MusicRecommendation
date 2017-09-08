__author__ = 'Amin'

import Music_Recommender_Utils as util
import Music_Recommender as reco
import math
import sys

#TODO
class UserBasedPredictor:
    def __init__(self, song_user_map,user_song_map, alpha = 0.5,q=3):
        print("Creation of user based predictor")
        self.song_user_map = song_user_map
        self.user_song_map = user_song_map
        self.alpha = alpha
        self.q = q

    """
    Similarity is calculated as (number of common songs) ^ alpha / (songs heard by u1) ^ alpha * (songs heard by u1) ^ alpha
    """
    def find_similarity(self, u1, u2):
        print("Calling similarity function")
        n_common_songs = len(self.user_song_map[u1] & self.user_song_map[u2])
        n_u1_songs = len(self.user_song_map[u1])
        n_u2_songs = len(self.user_song_map[u2])
        try:
            similarity = n_common_songs/(math.pow(n_u1_songs,self.alpha) * math.pow(n_u2_songs,(1-self.alpha)))
        except ZeroDivisionError:
            similarity=0
        return similarity

    """
    scores are calculates as sum((similiratity between target user and all users who heard the current song) ^ q)
    """
    def find_score(self,user,songs):
        print("Calculating the score")
        scores = {}
        #calculate the score for each song
        for song in songs:
            users = set()
            if song in self.song_user_map:
                users = self.song_user_map[song]
            if user in users:
                users.remove(user)
            #if len(users) != 0:
            similarities = [math.pow(self.find_similarity(user,u),self.q) for u in users]
            #else:
             #   similarities=[]
            scores[song] = sum(similarities)
        #sorted_scores = sorted(scores.keys(),key=lambda s:scores[s],reverse=True)
        return scores




# if __name__ == '__main__':
#     users = util.load_users("Data\kaggle_users.txt")
#     u_indices = util.userid_index_map(users)
#     s_indices = util.song_index('Data\kaggle_songs.txt')
#     s_u_map = util.s_u_map("Data\Test\kaggle_visible.txt",u_indices,s_indices)
#     u_s_map = util.u_s_map("Data\Test\kaggle_visible.txt",u_indices,s_indices)
#     print(len(u_s_map))
#     user_predictor = UserBasedPredictor(song_user_map=s_u_map,user_song_map=u_s_map)
#     songs = [s_indices[key].strip() for key in s_indices.keys()]
#     #print(songs)
#     print(len(songs))
#     print user_predictor.find_scores(0,songs)

