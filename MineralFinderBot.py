# MinDatBot.py
# Author: The-Unraveling

import praw
import re
import os
import codecs
import wikipedia
import datetime
import time
import pytz

# WRITE CERTAIN INFO(BOT STARTING, BOT COMMENTING) TO A TXT FILE..

def main():

    print "Bot Starting..."

    reddit = praw.Reddit('MineralFinderBot') # SET UP NEW CLIENT AND ALL THAT, ALL IN PRAW.INI

    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.datetime.now()
    #local_tz = pytz.timezone('US/Pacific')

    print "Opening/Reading mineral name file..."
    with codecs.open("mineral_names_on_wiki.txt", "r") as f:
        mineral_names_on_wiki = f.read()
        mineral_names_on_wiki = mineral_names_on_wiki.split("\n")
        mineral_names_on_wiki = tuple(filter(None, mineral_names_on_wiki))

    print "Done!"

    subreddit = reddit.subreddit('whatsthisrock')

    # Have we run this code before? If not, create empty list
    if not os.path.isfile("comments_replied_to.txt"):
        print "comments_replied_to.txt not found, making file..."
        comments_replied_to = []

    # If we've run code before, load list of posts we have replied to
    else:
        #read file into a list and remove any empsy values
        with open("comments_replied_to.txt", "r") as f:
            print "comments_replied_to.txt found, reading file:"
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    if not os.path.isfile("comments_bot_made.txt"):
        print "comments_bot_made.txt not found, making file..."
        comments_bot_made = []

    else:
        # read file into a list and remove any empsy values
        with open("comments_bot_made.txt", "r") as f:
            print "comments_bot_made.txt found, reading file:"
            comments_bot_made = f.read()
            comments_bot_made = comments_bot_made.split("\n")
            comments_bot_made = list(filter(None, comments_bot_made))

    print "Begin monitoring comments..."
    print "Time: ", date.strftime(date_format)
    for comment in subreddit.stream.comments():    #this line allows for indefinite running(DANGEROUS ON BIG SUBREDDITS)
                                                    #ADD comment age filter if implementing this style
    #for submission in subreddit.hot(limit=5):       #IN ORDER TO RUN ON SCHEDULER
        #submission.comments.replace_more(limit=0)   #UNCOMMENT THESE 3 LINES
        #for comment in submission.comments.list():  #COMMENT LINE ABOVE, INDENT CODE BELOW

        if comment.id not in comments_replied_to:

        #print(submission title)

            i = 0

            for i in range(0, len(mineral_names_on_wiki)):

                possible_mineral_match = re.search(mineral_names_on_wiki[i], comment.body, re.IGNORECASE)
                # Search comments for mineral keywords

                if possible_mineral_match:

                    break


            if possible_mineral_match:
                possible_mineral_name = re.findall(mineral_names_on_wiki[i], comment.body, re.IGNORECASE)

                for i in range(i+1,len(mineral_names_on_wiki)):
                    possible_mineral_name_next = re.findall('\\b' + mineral_names_on_wiki[i] + '\\b', comment.body, re.IGNORECASE)
                    if all(possible_mineral_name_next):

                        if len(possible_mineral_name_next) > 0:

                            possible_mineral_name.extend(possible_mineral_name_next)

                minerals_in_comment = []

                i = 0
                while i < (len(possible_mineral_name)):
                    minerals_in_comment.append(possible_mineral_name[i])
                    i += 1

                author = comment.author

                if not re.match('MineralFinderBot|throwAwayBotToday',author.name):

                    comment_time = comment.created_utc
                    #comment_time = datetime.datetime.utcfromtimestamp(comment.created)
                    #print comment_time
                    current_time = time.time()
                    #print current_time
                    #print comment_time
                    format = '%H:%M:%S.%f'
                    time_diff = current_time - comment_time
                    print time_diff, " seconds old"

                    if time_diff < 3600: # if comment is less than an hour old, post reply

                        print "\n"
                        print "Bot replying to :", comment.id,
                        print "author:", author.name
                        print "\n", "Comment text: ", comment.body

                        mineral_greeting = "Talking about minerals? Maybe I can help!  " + "&nbsp;  " + "\n" \
                                               "These are the minerals I found within your comment:  "

                        mineral_greeting_part2 = ""
                        i = 0

                        minerals_replying_to = []
                        while i < len(minerals_in_comment):
                            if not re.search(minerals_in_comment[i], mineral_greeting_part2, re.IGNORECASE):
                                mineral_greeting_part2 += (minerals_in_comment[i])
                                minerals_replying_to.append(minerals_in_comment[i])
                                if i < (len(minerals_in_comment) - 1):
                                    mineral_greeting_part2 += ", "
                                else:
                                    mineral_greeting_part2 += ".  " + "\n"
                            i += 1

                        mineral_greeting += mineral_greeting_part2.lower()

                        mineral_greeting += "The links below can(hopefully) be used to help better" \
                                            " determine what " \
                                            "you're looking at.  \n"

                        i = 0
                        mineral_links = ""


                        #NEW VARIABLES
                        # COMMENT_TITLE
                        # COMMENT_WIKI_LINK
                        # COMMENT_GOOGLE_IMAGES
                        # COMMENT_WIKI_IMAGES

                        # FOR LOOP TO ATTACH/APPEND MINERAL STUFF TO FINSHED_MINERAL_REPLY

                        while i < len(minerals_replying_to):

                            this_mineral = minerals_replying_to[i]

                            mineral_links += "### " + minerals_replying_to[i].lower() + "  \n"\
                                             " [Wikiepedia link to " + \
                                             minerals_replying_to[i].lower() + \
                                        "]" + "("

                            wiki_mineral = wikipedia.page(minerals_replying_to[i])

                            mineral_links += wiki_mineral.url
                            mineral_links += ")  "
                            mineral_links += "  "
                            mineral_links += "\n\n"

                            wiki_image_list = wiki_mineral.images

                            image_length = len(wiki_image_list)

                            mineral_links += "Photos: |  " + "\n"\
                                             ":-------|  " + "\n"\
                                "[Google images] (" + "https://www.google.com/search?tbm=isch&q="\
                                + minerals_replying_to[i] + "+mineral): |  " + "\n"

                            j =0; k = 1
                            while j < image_length and k <= 3: # changes number of wiki images added

                                is_photo_mineral = re.search(minerals_replying_to[i],
                                                    wiki_image_list[j], re.IGNORECASE)

                                if is_photo_mineral:
                                    mineral_links += "[ Wikipedia Photo " + str(k) + " of " + \
                                            minerals_replying_to[i].lower() + ".]"
                                    mineral_links += "(" + wiki_image_list[j] + ") |  "\
                                                    + "\n"

                                    k += 1

                                j += 1

                            mineral_links += "  "
                            mineral_links += "&nbsp;"
                            mineral_links += "  \n"

                            i += 1


                        bot_beep_boop = "beep ^boop, I'm a bot! If you have any questions, " \
                                        "or suggestions on how my programmer can make me better, " \
                                        "send me a PM or add a suggestion to [r/MineralFinderBot]" \
                                        "(reddit.com/r/MineralFinderBot) Comment will be deleted " \
                                        "if score drops below -1."

                        finished_mineral_reply = ""
                        finished_mineral_reply += mineral_greeting
                        finished_mineral_reply += mineral_links
                        finished_mineral_reply += bot_beep_boop

                        #print finished_mineral_reply
                        print "Posting comment..."

                        comment.reply(finished_mineral_reply)
                        with open("comments_replied_to.txt","a") as myfile:
                            myfile.write(comment.id + "\n")
                        comments_replied_to.append(comment.id)

                        date = datetime.datetime.now()
                        print "Comment posted at " + date.strftime(date_format)

                        print "Bot has now replied to "
                        print len(comments_replied_to)
                        print "comments!"

                else:
                    with open("comments_bot_made.txt", "a") as myfile:
                        if comment.id not in comments_bot_made:
                            myfile.write(comment.id + "\n")
                    comments_bot_made.append(comment.id)





    print "Bot has replied to "
    print len(comments_replied_to)
    print "comments"

    # Set up comment deletion code??
    # If score of any commented comment goes under -1, comment is deleted

main()