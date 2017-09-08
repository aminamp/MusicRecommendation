def load_users(file_name):
    """ This function loads users from users file and returns list of users to the caller"""
    with open(file_name, "r") as f:
        u = [line.strip() for line in list(f.readlines())]
    return u


def get_songs_by_popularity(file):
    """ This function counts the number of users that listens to each song """
    s = dict()
    with open(file, "r") as f:
        for line in f:
            _, song, _ = line.strip().split('\t')
            try:
                s[song] += 1
            except:
                s[song] = 1
    return sort_dictionary(s)

def sort_dictionary(d):
    """ This function returns the given dictionary d sorted by its keys"""
    return sorted(d.keys(),key=lambda s:d[s],reverse=True)

def load_unique_users(trainingFile):
    """Load the users into the set"""
    u = set()
    with open(trainingFile,"r") as f:
        for line in f:
            user, _, _ = line.strip().split('\t')
            if user not in u:
                u.add(user)
    return u


def userid_index_map(users):
    """ THis method is used to load indecies for user names"""
    user_indices = {user:i for i,user in enumerate(users)}
    return user_indices

def song_index(file):
    song_indices = {}
    with open(file,"r") as f:
        song_indices= {line.split(' ')[0].strip(): line.split(' ')[1].strip() for line in list(f.readlines())}
    return song_indices

def song_user_map(file, user_indices):
    """ This function loads user,song,play_count triplets to form the map of song with set of users who listens to that song """
    song_users_map = dict()
    with open(file,"r") as f:
        for line in f:
            user_id,song_id,_ = line.strip().split('\t')
            user_index = user_indices[user_id]
            try:
                song_users_map[song_id].add(user_index)
            except:
                song_users_map[song_id]=set([user_index])
    return  song_users_map


def user_song_map(file):
    """ This finctions loads user,song,play_count triplets and returns the dictionar yof users with the set of songs the user has listened to"""
    user_song_dict = dict()
    with open(file,"r") as f:
        for line in f:
            user_id,song_id,count = line.strip().split('\t')
            try:
                user_song_dict[user_id].add(song_id)
            except:
                user_song_dict[user_id]=set([song_id])
    return user_song_dict

# Kristy required as there was no function which used indices to retun u_s map
def u_s_map(file,u_indices,s_indices):
    user_song_map = {}
    with open(file,"r") as f:
        for line in list(f.readlines()):
            u,s,_ = line.strip().split('\t')
            try:
                user_song_map[u_indices[u]].add(s_indices[s])
            except:
                user_song_map[u_indices[u]]=set([s_indices[s]])
    return user_song_map

# Kristy required as there was no function which used indices to retun s_u map
def s_u_map(file,u_indices,s_indices):
    song_user_map = {}
    with open(file,"r") as f:
        for line in list(f.readlines()):
            u,s,_ = line.strip().split('\t')
            try:
                song_user_map[s_indices[s]].add(u_indices[u])
            except:
                song_user_map[s_indices[s]]=set([u_indices[u]])
    return song_user_map

def save_results(top_recommended_songs, out_put_filename):
    """ This function saves recommendation given in argument ito file """
    print("Saving recommendations")
    f = open(out_put_filename,"w")
    if top_recommended_songs != None:
        for top_song in top_recommended_songs:
            out_line = [str(top_song), '\n']
            f.writelines(out_line)
        f.close()
    else:
        print("No recomendation")
    print("Done Saving recommendations")
