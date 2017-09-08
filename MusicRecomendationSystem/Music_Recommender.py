__author__ = 'Amin'
import Music_Recommender_Utils
class MusicRecommender:
    def __init__(self,songs_ordered_by_popularity, music_predictor,N):
        """:arg
                songs_ordered_by_popularity       - Represents the songs ordered by popularity
                music_predictor                   - Predictor that is used to score the songs for a particular item/user
        """
        print("Creation of Music Recommendor")
        self.songs_ordered_by_popularity = songs_ordered_by_popularity
        self.music_predictor = music_predictor
        self.N = N

    def recommend_songs_for_user(self, user_id, user_to_songs_map):
        """ This method recommends top N songs for a given user based on the score calculated using predictor"""
        print("Calling recommend songs for a user " , str(user_id))
        scores_for_songs = set()
        user_listening_history = user_to_songs_map[user_id]
        if user_id in user_to_songs_map:
            #get scores for all songs for this user
            scores_for_songs = self.music_predictor.find_score(user_listening_history,
                                                               self.songs_ordered_by_popularity)
            sorted_scores_by_song_id = Music_Recommender_Utils.sort_dictionary(scores_for_songs)
        else:
            # if user not in the matrix we recommend the best songs
            sorted_scores_by_song_id = self.songs_ordered_by_popularity

        processed_song_list_for_user = list()
        for song in sorted_scores_by_song_id:
            if len(processed_song_list_for_user)>=self.N:
                break
            if song not in user_to_songs_map[user_id]:
                processed_song_list_for_user.append(song)

        return processed_song_list_for_user