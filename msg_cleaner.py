##########################################
#
#
#   This code was pulled from:
# http://stackoverflow.com/questions/7166922/
#  extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
#
##########################################

import mailbox
import sys, os
import re
import unicodedata
from subprocess import call

def get_charsets(msg):
  charsets = set({})
  for c in msg.get_charsets():
      if c is not None:
          charsets.update([c])
  return charsets

def get_body(msg):
  while msg.is_multipart():
      msg=msg.get_payload()[0]
  t=msg.get_payload(decode=True)
  for charset in get_charsets(msg):
      t=t.decode(charset)
  return t

def remove_emojis(msg):
  htmlReg = re.findall(u'([\U0001f300-\U0001f64F])',msg)
  if htmlReg:
    for terms in htmlReg:
      msg = msg.replace(terms, "")
  return msg
  
def cleanup_email(email, strip_url=False):
  """
  Go through each element of the list of tweets, cleaning up overly repetitious
   words (veeeeeerrrrrrrryyyyyy -> veerryy), getting rid of html tags (<p> ->
   '') and stripping out white space and things enclosed by stars. (*very* ->
   very)
   @param  tweetList    list   list of tweets to be fully cleaned
   @return cleanTweets  list   list of fully cleaned tweets
  """
  #split on space to get words
  email = email.split("\n")
  cleanedEmail = list()
  for lines in email:
    lines = lines.strip(">")
    line = lines.split(" ")
    cleanedLine = list()
    for word in line:
      cleanWord = word.strip().strip("*")
    
      #clean up the word to get rid of white space and * enclosures
      if(strip_url == True):
        if cleanWord.startswith("http") or cleanWord.startswith("www"):
          cleanWord = ""
        if cleanWord.endswith("@vassar.edu"):
          cleanWord = ""
      #if cleanWord.startswith("http") or cleanWord.startswith("www"):
      #  cleanWord = "URL"
      #elif cleanWord.startswith("@"):
      #  cleanWord = "AT_USER"
      #elif re.match(r"[0-9]",cleanWord):
      #  cleanWord = ''
      #replace words that have 4 or more repetitions with 2 of that letter
      cleanWord = re.sub(r"(.)\1{3,}", deleteRepeatingLetters, cleanWord)
        
      #attach the cleaned word to the initially clean list
      cleanedLine.append(cleanWord)
    #join the word list into a sentence
    fullyCleanedLine = " ".join(cleanedLine)
    #get rid of any html tags that snuck through the intiial cleaning
    htmlReg = re.findall(r"<[^>]+>",fullyCleanedLine)
    #if there was a match, get rid of the matching term
    if htmlReg:
      for terms in htmlReg:
        fullyCleanedLine = fullyCleanedLine.replace(terms, "")
    cleanedEmail.append(fullyCleanedLine)
  fullyCleanedEmail = "\n".join(cleanedEmail) 
  return fullyCleanedEmail

def deleteRepeatingLetters(matchobj):
  """
  Use this to reduce the match object to the first two of the match, which will
   be called from from the re.sub area.
  @param   matchobj     matchobj     the object created when re search matches
  @return  replacement  string       the string to replace when matched
  """
  replacement = matchobj.group(0)[:2]
  return replacement

def main(argv):
  input_file = argv[1]
  output_file = argv[2]
  if len(argv) == 4:
    tagger_flag = argv[3]
  else:
    tagger_flag = "f"

  current_mailbox = mailbox.mbox(input_file)
  if tagger_flag == "t":
    write_file = open("interText.txt", "w")
  else:
    write_file = open(output_file, 'w')
  decoded_emails = list()
  for this_email in current_mailbox:
    body = get_body(this_email)
    body = remove_emojis(body)
    body = cleanup_email(body, strip_url=True)
    decoded_emails.append(body)
  for elements in decoded_emails:
    write_file.write(elements + "\n")
  write_file.close()
  if tagger_flag == "t":
    #open a temporary file to write the tagged tweets to
    temp = open("temp.txt","w")
    #create a subprocess call in order to tag from within python
    #  Note: cwd is set to the ark folder under current
    call(["./runTagger.sh", "--model",
      "model.ritter_ptb_alldata_fixed.20130723.txt",
      "../interText.txt"],cwd="./ark-tweet-nlp-0.3.2/",stdout=temp)
    temp.close()
    #remove the intermediate text for cleanup
    os.remove("interText.txt")
    #read in the tagged text file
    tweets = open("temp.txt","r")
    #create a new list for the taggedtweets
    taggedTweets = list()
    for tweet in tweets:
      #hold each of the sets of pairs
      wordTagPair = list()
      #only want the first two b/c those are all that are needed
      words, tags = tweet.split("\t")[:2]
      #get individual words and tags
      words = words.split(" ")
      tags = tags.split(" ")
      #get the length of words for iteration
      sentenceLength = len(words)
      for i in range(sentenceLength):
        #join the words and tags with an underscore
        pair = words[i] + "_" + tags[i]
        #then add it to the list of pairs
        wordTagPair.append(pair)
      #Afterwards, join the pairs like a sentence
      taggedTweet = " ".join(wordTagPair)
      #then append it to the taggedTweets list
      taggedTweets.append(taggedTweet)
    tweets.close()
    #reattach the sentimnets to the tweets
    #for i in range(len(taggedTweets)):
    #    taggedTweets[i] = tweetSentiment[i] + "\t"+ taggedTweets[i]
    outputFile = open(output_file, "w")
    #finally, write to the final file cleaning up temp files
    for fullyTaggedTweets in taggedTweets:
      tweetWN = fullyTaggedTweets + "\n"
      outputFile.write(tweetWN)
    outputFile.close()
    #clean up the last temporary file
    os.remove("temp.txt")


if __name__ == "__main__":
  main(sys.argv)
