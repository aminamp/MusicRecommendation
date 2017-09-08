__author__ = 'Amin'
import Music_Recommender_Utils as util
import Song_Based_Predictor
import Music_Recommender
import sys
import User_Based_Predictor as u_predictor
import time

def song_based_recommender(trainingFile, user_id, alpha, q, N):
    print("loading users to a list")
    users_list = list(util.load_users("Data\kaggle_users.txt"))

    # Order songs by popularity
    print("Fetching songs by popularity")
    popular_songs_by_id = util.get_songs_by_popularity("Data\msd_train.txt")

    #load users Index
    print("Load unique Users idecies")
    unique_users_list = util.load_unique_users(trainingFile)

    #Annotate userNames with index
    print("Enumerate User with indexes")
    unique_users_list_with_indecies = util.userid_index_map(unique_users_list)

    #Get the mapping of song to userId set
    print("Get the training data as song to user indecies")
    song_to_user_index_map = util.song_user_map(trainingFile,
                                                unique_users_list_with_indecies)
    #delete the user_id_to_index_mapping
    del unique_users_list_with_indecies

    #next step is to initialize the predictor
    #callign with similarity measure as  cosine for now
    music_predictor = Song_Based_Predictor.SongBasedPredictor(song_user_map=song_to_user_index_map, alpha=alpha,
                                                              similarity_measure=0)
    #load the test data as dictionary of users with the set of songs the user has listened to as user vector
    print("Loading the test data")
    user_song_map = util.user_song_map('Data\kaggle_visible_evaluation_triplets.txt')

    #initialise the recommender required with top 50 songs as output desired
    music_recommender = Music_Recommender.MusicRecommender(songs_ordered_by_popularity=popular_songs_by_id,
                                                           music_predictor=music_predictor, N=N)
    #if(users_list[user_id]):
    top_recommended_songs = music_recommender.recommend_songs_for_user(users_list[user_id], user_song_map)
    #else:
    #   top_recommended_songs=[]
    #   print("Invalid UserId")
    #exit(0)"""
    out_put_filename = "Data\output"+str(time.time())+".txt"
    #util.save_results(top_recommended_songs, out_put_filename)
    return top_recommended_songs


def user_based_recommender(alpha, q, user_id, N):
    users = util.load_users("Data\kaggle_users.txt")
    # index the users
    u_indices = util.userid_index_map(users)
    # sort users by indices so that users can be accessed by id later on
    sorted_users = sorted(u_indices.keys(), key=lambda s: u_indices[s])
    # index the songs
    s_indices = util.song_index('Data\kaggle_songs.txt')
    #sort songs by indices so that users can be accessed by id later on
    sorted_songs = sorted(s_indices.keys(), key=lambda s: s_indices[s])

    #song to user map. song id is key and the user ids who have listened to the song are the values e.g. {1:[2,3,4],3:[4,5,6]}
    s_u_map = util.s_u_map("Data\Test\kaggle_visible.txt", u_indices, s_indices)
    #user to song map. user id is key and the song ids listened by the user are the values e.g. {1:[2,3,4],3:[4,5,6]}
    u_s_map = util.u_s_map("Data\Test\kaggle_visible.txt", u_indices, s_indices)

    print("Fetching songs by popularity")
    #if no listening history is found for a user, then retun popular songs
    popular_songs_by_id = util.get_songs_by_popularity("Data\Test\kaggle_visible.txt")
    #form the predictor based on training data set
    music_predictor = u_predictor.UserBasedPredictor(song_user_map=s_u_map, user_song_map=u_s_map, alpha=alpha, q=q)
    #recommend songs based on the predictor
    music_recommender = Music_Recommender.MusicRecommender(songs_ordered_by_popularity=popular_songs_by_id,
                                                           music_predictor=music_predictor, N=N)
    #return top recommended song ids
    top_recommended_songs = music_recommender.recommend_songs_for_user(user_id, u_s_map)
    #get the actual songs from the ids
    #top_recommended_songs = [sorted_songs[i] for i in top_recommended_songs_ids]
    #util.save_results(top_recommended_songs, 'kp'+str(time.time())+'.txt')
    return top_recommended_songs

def run_algorithms(alpha,q,N):
    users = util.load_users("Data\kaggle_users.txt")
    total_users = len(users)
    trainingFile = "Data\msd_train.txt"
    testFile = "Data\Test\kaggle_hidden.txt"
    expected_op = util.user_song_map(testFile)
    sb_prec = []
    ub_prec = []
    for i,user in enumerate(users):
        predicted_ub_op = user_based_recommender(alpha,q,i,N)
        predicted_sb_op = song_based_recommender(trainingFile,i,alpha,q,N)
        ub_prec_u = average_precision(predicted_ub_op,expected_op[user])
        sb_prec_u = average_precision(predicted_sb_op,expected_op[user])
        sb_prec.append(sb_prec_u)
        ub_prec.append(ub_prec_u)
    mean_averge_precsion_sb = sum(sb_prec)/total_users
    mean_averge_precsion_ub = sum(ub_prec)/total_users

    print("sb prec",mean_averge_precsion_sb)
    print("ub prec",mean_averge_precsion_ub)
    return mean_averge_precsion_sb,mean_averge_precsion_ub

def average_precision(predicted, expected):
    print("Calculating mean average precision")
    num_corr_pred = []
    heard_not_heard = []
    count = 0
    for i,song in enumerate(predicted):
        if song in expected:
            count = count+1
            heard_not_heard.append(1)
        else:
            heard_not_heard.append(0)
        num_corr_pred.append(count)
    num_positively_predicted = count
    print(num_corr_pred)
    precision_at_k = [num_corr_pred[i]/(i+1) for i in range (0,len(num_corr_pred))]
    print(precision_at_k)
    try:
        avg_precision = sum([precision_at_k[i]*heard_not_heard[i] for i in range(0,len(predicted))])/min(num_positively_predicted,len(predicted))
    except ZeroDivisionError:
        avg_precision= 0
    return avg_precision

def load_data(trainfile, testfile, users, songs):
    print("loading data from files")


if __name__ == '__main__':
    # Get the userId for whom we need to recommend songs
    run_algorithms(0.5,3,500)




