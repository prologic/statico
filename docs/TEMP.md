# ----------------------- #
#      Main Configs       #
# ----------------------- #

title: Ossama Edbali
subtitle: Learn. Produce. Contribute.
author: Ossama Edbali
description: Ossama Edbali Blog on JavaScript, Python, theoretical Computer Science and much more

# ----------------------- #
#    Jekyll & Plugins     #
# ----------------------- #

# If publishing to a subdirectory as in http://site.com/project set 'root: /project'
root: /
permalink: /blog/:year/:month/:day/:title/
source: source
destination: public
plugins: plugins
code_dir: downloads/code
category_dir: blog/categories
markdown: rdiscount
rdiscount:
  extensions:
    - autolink
    - footnotes
    - smart
highlighter: pygments # default python pygments have been replaced by pygments.rb

paginate: 10          # Posts per page on the blog index
paginate_path: "posts/:num"  # Directory base for pagination URLs eg. /posts/2/
recent_posts: 5       # Posts in the sidebar Recent Posts section
excerpt_link: "Read on &rarr;"  # "Continue reading" link text at the bottom of excerpted articles
excerpt_separator: "<!--more-->"

titlecase: true       # Converts page and post titles to titlecase

# list each of the sidebar modules you want to include, in the order you want them to appear.
# To add custom asides, create files in /source/_includes/custom/asides/ and add them to the list like 'custom/asides/custom_aside_name.html'
default_asides: [custom/asides/about.html, asides/recent_posts.html, asides/github.html, asides/googleplus.html]

# Each layout uses the default asides, but they can have their own asides instead. Simply uncomment the lines below
# and add an array with the asides you want to use.
# blog_index_asides:
# post_asides:
# page_asides:

# ----------------------- #
#   3rd Party Settings    #
# ----------------------- #

# Github repositories
github_user: oss6
github_repo_count: 5
github_show_profile_link: true
github_skip_forks: true

# Twitter
twitter_user: ossedb
twitter_tweet_button: true

# Google +1
google_plus_one: false
google_plus_one_size: medium

# Google Plus Profile
# Hidden: No visible button, just add author information to search results
googleplus_user:
googleplus_hidden: false

# Pinboard
pinboard_user:
pinboard_count: 3

# Delicious
# delicious_user:
# delicious_count: 3

# Disqus Comments
# disqus_short_name:
# disqus_show_comment_count: false

# Google Analytics
google_analytics_tracking_id: UA-54085200-2

# Facebook Like
facebook_like: false