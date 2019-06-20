#!/usr/bin/env python
# coding: utf-8

# # Hacker News: An Analysis of Online News Postings
# 
# Hacker News is a site where user-submitted stories (known as "posts") are voted and commented upon, similar to reddit.  It is very popular among technology and startup circles, and as such can lead to hundreds of thousands of visitors to posts.
# 
# We are interested in two types of posts submitted by users: Show HN and Ask HN.  Users submit Ask HN posts to ask the Hacker News community a specific question.  Likewise, users submit Show HN posts to show the Hacker News community a project, product, or just generally something interesting.
# 
# In this project I'll compare the two types of posts to determine the following:
# - Do Show HN or Ask HN receive more comments on average?
# - Do posts created at a certain time receive more comments on average?
# 
# It should be noted that the data set we're working with was reduced from almost 300,000 rows to approximately 20,000 rows by removing all submissions that did not receive any comments, and then randomly sampling from the remaining submissions.

# ## Reading in the data
# 
# Let's start by importing the libraries we need and reading the data set into a list of lists.

# In[1]:


from csv import reader

opened_file = open("hacker_news.csv")
read_file = reader(opened_file)
hn = list(read_file)

print(hn[:5])


# ## Remove Headers

# Assign the first row to the variable `headers`

# In[2]:


headers = hn[0]
print(headers)


# In[3]:


hn = hn[1:]
print(hn[:5])


# ## Extract Show HN & Ask HN Posts
# 
# Now that the headers have been removed from the data set, we are ready to begin filtering our data.  Since we are only interested in Show HN and Ask HN posts, we'll separate these type of posts into two different lists:
# - `ask_posts`
# - `show_posts`
# 
# All other posts will be relegated to the list `other_posts`
# 
# We'll print the first few rows as visual checks for each list.

# In[4]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)


# Below are the first five rows of `ask_posts`

# In[5]:


print(ask_posts[:5])


# Below are the first five rows of `show_posts`

# In[6]:


print(show_posts[:5])


# In[7]:


print("Number of 'ask hn' posts:", len(ask_posts))
print("Number of 'show hn' posts:", len(show_posts))
print("Number of 'other' posts:", len(other_posts))


# ##  Calculate the average number of comments
# 
# We'll find the total number of comments and determine the average number of comments for each type of post.

# In[8]:


# Determine the total number of comments for ask hn posts
total_ask_comments = 0

for ask in ask_posts:
    ask_comments = int(ask[4])
    total_ask_comments += ask_comments

# Determine the average number of comments on ask posts
avg_ask_comments = total_ask_comments/(len(ask_posts))

print("Average Number of Comments for 'ask hn' Posts:", avg_ask_comments)

# Determine the total number of comments for show hn posts
total_show_comments = 0

for show in show_posts:
    show_comments = int(show[4])
    total_show_comments += show_comments

# Determine the average number of comments on show posts
avg_show_comments = total_show_comments/(len(show_posts))

print("Average Number of Comments for 'show hn' Posts:", avg_show_comments)


# In[9]:


print("Total 'ask hn' comments:", total_ask_comments)
print("Number of 'ask hn' posts:", len(ask_posts))
print("Total 'show hn' comments:", total_show_comments)
print("Number of 'show hn' posts:", len(show_posts))


# On average, Ask HN posts receive more comments with an average of ~14 comments per post while Show HN posts receive ~10 comments per post.  Since Ask HN posts are more likely to receive comments, I'll focus the remainder of the analysis on this type of post.
# 

# ## Determining the Number of Ask Posts and Comments by Hour Created
# 
# Next we'll determine if the Ask HN posts created at a certain time are more likely to attract comments.  We'll do this in two steps:
# 1. Calculating the amount of Ask HN posts created in each hour of the day, along with the number of comments received.
# 2. Calculating the average number of comments Ask HN posts receive by hour created.

# In[10]:


import datetime as dt

result_list = []

for ask in ask_posts:
     result_list.append([ask[6], int(ask[4])])

counts_by_hour = {}
comments_by_hour = {}

for row in result_list:
    date = row[0]
    comment = row[1]
    date_parse = dt.datetime.strptime(date, "%m/%d/%Y %H:%M")
    hour = date_parse.strftime("%H")
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = comment
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += comment

comments_by_hour


# ## Calculate the Average Number of Comments the Ask HN Posts Receive by Hour Created
# 
# Now we'll use the dictionaries `counts_by_hour` and `comments_by_hour` to calculate the average number of comments for posts created during each hour of the day.

# In[11]:


avg_by_hr = []

for hr in comments_by_hour:
    avg_by_hr.append([hr, comments_by_hour[hr]/counts_by_hour[hr]])

avg_by_hr


# ## Sorting and Printing the Values
# 
# Now lets sort the average number of comments per post by hour and pring the five highest averages.
# 
# First we'll swap the columns so that the average is located in the first column.

# In[12]:


swap_avg_by_hour = []

for row in avg_by_hr:
    hr = row[0]
    avg = row[1]
    swap_avg_by_hour.append([avg, hr])

swap_avg_by_hour


# Now let's sort the averages in descending order using `sorted()` and print the top five hours for Ask HN post comments.

# In[13]:


sorted_swap = sorted(swap_avg_by_hour, reverse = True)

print("Top 5 Hours for Ask HN Posts Comments")

for avg, hr in sorted_swap[:5]:
    print("{}: {:.2f} average comments per post".format(
        dt.datetime.strptime(hr, "%H").strftime("%H:%M"), avg)
         )


# The hour with the highest average of comments per Ask HN post is 15:00 (or 3:00 PM EST) with an average of 38.59 comments per post.  Followed by 2:00 (or 2:00 AM EST) with an average of 23.81 comments per post.  There is about a 62% increase between the hour with the second highest average and the highest average meaning that if you want your post to receive maximum visibility and response, you should definitely post at 15:00.

# ## Conclusions
# 
# In this project, we analyzed Ask HN and Show HN post data from Hacker News to determine which type of post and time receive the most comments on average.  Based on our analysis of posts that received comments, you can maximize the number of comments a post receives by writing an 'Ask HN' post between the time of 15:00 and 16:00 (3:00 PM EST - 4:00 PM EST).
# 
# (It should be noted that the data we analyzed excluded posts without any comments.)
# 
# 
# 

# In[ ]:




