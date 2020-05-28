# This is a program to track your Instagram followers
# Author: https://github.com/julres
# Instagram: juliusxsh
# Essentially, this script first gets all of your followers and then will look every 10 seconds if you've gotten any new followers or if somebody unfollowed.
# TODO: Linux support. This script here currently only runs on Windows machines.
# Also this currently is probably very inefficient, but I really don't care because it works for me and I don't have that much time to work on this rn. This is just
# a little side project
from InstagramAPI import InstagramAPI
import json
import time
from colorama import Fore, Style, init
import os
def cls():
    os.system("cls")
cls()

username = str(input("Please enter your username --> "))
password = str(input("Please enter your password --> "))
api = InstagramAPI(username, password)
api.login()
uid = api.username_id

# Get the current followers and write them to followers.txt
def getAndWriteFollowers():
    followers = api.getTotalFollowers(uid)
    print(Fore.CYAN + "Getting your followers, please be patient..." + Style.RESET_ALL)
    for follower in followers:
        # Get username of the follower.
        username = follower["username"]
        print(Fore.GREEN + f"Got user {username}." + Style.RESET_ALL)
        # Add the username to a new line in the file
        followerFile = open('followers.txt', 'a+')
        followerFile.write(username)
        followerFile.write('\n')
        # Close the file, ofc
        followerFile.close()
    print(Fore.CYAN + "Done." + Style.RESET_ALL)
    
def compareFollowers():
    # Get the old followers from 10 seconds ago
    followers_old = []
    with open('followers.txt', 'r') as oldFollowerFile:
        followers_old = [line.rstrip() for line in oldFollowerFile]
    oldFollowerFile.close()
    
    followers_new = api.getTotalFollowers(uid)
    followers_made = 0
    # Make a new list of the followers the user now has
    followers_new_usernames = []
    for new_follower in followers_new:
        follower_username = new_follower["username"]
        followers_new_usernames.append(follower_username)
    
    # Check for lost followers
    for old_follower in followers_old:
        if old_follower in followers_new_usernames:
            pass
        else:
            print(Fore.RED + f"{old_follower} has unfollowed." + Style.RESET_ALL)
            followers_made -= 1
            with open('followers.txt', 'r') as followerFile:
                lines = followerFile.readlines()
            followerFile.close()
            with open('followers.txt', 'w') as followerFile:
                for line in lines:
                    if line.strip("\n") != old_follower:
                        followerFile.write(line)
            followerFile.close()
    
    # Check for new followers
    for follower_username in followers_new_usernames:
        with open('followers.txt', 'r') as followerFile:
            # If user is already a follower, do nothing
            if follower_username in followerFile.read():
                pass
            # Else, add them to the follower file
            else:
                print(Fore.GREEN + f"New follower: {follower_username}" + Style.RESET_ALL)
                followers_made += 1 # Why does python not support incrementing by i++? Damn
                with open('followers.txt', 'a') as addFollowerFile:
                    addFollowerFile.write(follower_username)
                    addFollowerFile.write('\n')
                    addFollowerFile.close()
        followerFile.close()
    if followers_made == 0:
        print(Fore.RED + "No new followers." + Style.RESET_ALL)
    elif followers_made >= 1:
        print(Fore.CYAN + str(followers_made) + Fore.GREEN + " new followers.")
    else:
        print(Fore.RED + f"You lost {abs(followers_made)} followers.")
if __name__ == '__main__':
    # Init colorama, which we need to use Fore.COLOR and Style.RESET_ALL
    init()
    # Get current followers and write them to followers.txt
    getAndWriteFollowers()
    # Check if we lost or made any followers every 10 seconds 
    time.sleep(10)
    while True:
        compareFollowers()
        time.sleep(10)