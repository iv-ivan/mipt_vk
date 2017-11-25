import urllib2
import json
import codecs
import pickle
from collections import defaultdict

def loadMIPT():
    print "Getting MIPT people"
    ids = []
    n = 18
    while n < 90:
        while True:
            try:
                answer = urllib2.urlopen("https://api.vk.com/method/users.search?university=297&count=1000&access_token=&age_from=" + str(n) + "&age_to=" + str(n)).read()
                peopleList = json.loads(answer)["response"][1:]
            except:
                print "Exception"
                continue
            break
        print "Age:", n, " count:", len(peopleList)
        n += 1
        for info in peopleList:
            ids.append(info["uid"])
    return ids

def loadInfo(ids):
    info = {}
    l = 0
    while l < len(ids):
        size = 100
        if l + size > len(ids):
            size = len(ids) - l
        print l
        while True:
            try:
                answer = urllib2.urlopen("https://api.vk.com/method/users.get?user_ids=" + ",".join(map(str, ids[l: l + size])) + "&fields=photo_id,verified,sex,bdate,city,country,home_town,has_photo,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,online,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,occupation,nickname,relatives,relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about,quotes,can_post,can_see_all_posts,can_see_audio,can_write_private_message,can_send_friend_request,is_favorite,is_hidden_from_feed,timezone,screen_name,maiden_name,crop_photo,is_friend,friend_status,career,military,blacklisted,blacklisted_by_me&access_token=").read()
                peopleList = json.loads(answer)["response"]
            except Exception, e:
                print "Exception:", e
                continue
            break
        for person in peopleList:
            info[person["uid"]] = person
        l += size
    return info

def getFollowers(ids):
    followers = defaultdict(list)
    for i, id in enumerate(ids):
        n = 0
        for j in xrange(50):
            try:
                answer = urllib2.urlopen("https://api.vk.com/method/users.getFollowers?user_id=" + str(id) + "&count=1&access_token=").read()
                n = json.loads(answer)["response"]["count"]
            except Exception, e:
                print answer
                print "Exception:", e
                continue
            break
        print "Id(num):", id, i, "n:", n
        processed = 0
        while processed < n:
            for j in xrange(50):
                try:
                    answer = urllib2.urlopen("https://api.vk.com/method/users.getFollowers?user_id=" + str(id) + "&offset=" + str(processed) + "&count=1000&access_token=").read()
                    peopleList = json.loads(answer)["response"]["items"]
                except Exception, e:
                    print answer
                    print "Exception:", e
                    continue
                break
            processed += 1000
            for person in peopleList:
                followers[id].append(person)
    return followers

def getSubscriptions(ids):
    subscription_people = defaultdict(list)
    subscription_groups = defaultdict(list)
    for i, id in enumerate(ids):
        print "Id(num):", id, i
        for j in xrange(50):
            try:
                answer = urllib2.urlopen("https://api.vk.com/method/users.getSubscriptions?user_id=" + str(id) + "&access_token=").read()
                peopleList = json.loads(answer)["response"]["users"]["items"]
                groupList = json.loads(answer)["response"]["groups"]["items"]
            except Exception, e:
                print answer
                print "Exception:", e
                continue
            break
        for person in peopleList:
            subscription_people[id].append(person)
        for group in groupList:
            subscription_groups[id].append(group)
    return subscription_people, subscription_groups

def save_obj(obj, name ):
    with open('./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def main():
    #ids = loadMIPT()
    #print len(ids), ids[:5]
    #save_obj(ids, "ids")
    ids = load_obj("ids")
    #info = loadInfo(ids)
    #save_obj(info, "info")
    #subscr_p, subscr_g = getSubscriptions(ids)
    #save_obj(subscr_p, "subscr_p")
    #save_obj(subscr_g, "subscr_g")
    #followers = getFollowers(ids)
    #save_obj(followers, "followers")

if __name__ == "__main__":
    main()
