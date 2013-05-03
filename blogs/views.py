# Create your views here.
from django.shortcuts import render_to_response
from blogs.models import Post
import re
from datetime import datetime

MONTH_NAMES = ('', 'January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December')

def frontpage(request):
    posts, pagedata = init()
    pagedata.update({'subtitle': '',})
    return render_to_response('listpage.html', pagedata)

def singlepost(request, year, month, slug2):
    posts, pagedata = init()
    post = posts.get(date_created__year=year,
                            date_created__month=int(month),
                            slug=slug2,)
    pagedata.update({'post': post, 'poll': post.poll})
    return render_to_response('singlepost.html', pagedata)
    
def yearview(request, year):
    posts, pagedata = init()
    posts = posts.filter(date_created__year=year)
    pagedata.update({'post_list': posts,
                     'subtitle': 'Posts for %s' % year})
    return render_to_response('listpage.html', pagedata)

def monthview(request, year, month):
    posts, pagedata = init()
    posts = posts.filter(date_created__year=year)
    posts = posts.filter(date_created__month=int(month))
    pagedata.update({'post_list': posts,
                     'subtitle': 'Posts for %s %s' % (MONTH_NAMES[int(month)], year),})
    return render_to_response('listpage.html', pagedata)

def tagview(request, tag):
    allposts, pagedata = init()
    posts = []
    for post in allposts:
        tags = re.split(' ', post.tags)
        if tag in tags:
            posts.append(post)
    pagedata.update({'post_list': posts,
                     'subtitle': "Posts tagged '%s'" % tag,})
    return render_to_response('listpage.html', pagedata)

def categoryview(request, title):
    allposts, pagedata = init()
    posts = []
    for post in allposts:
        #post_categories 
        if title in map( lambda category:  category.title, post.categories.all() ):
            posts.append(post)  
    pagedata.update({'post_list': posts,
                    'subtitle': "Posts in Category '%s'" % title,})
    return render_to_response('listpage.html', pagedata)

def init():
    posts = Post.objects.all()
    tag_data = create_tag_data(posts)
    archive_data = create_archive_data(posts)
    cat_data = create_cat_data(posts)
    pagedata = {'version': '0.0.6',
                'post_list': posts,
                'tag_counts': tag_data,
                'archive_counts': archive_data,
                'cat_counts': cat_data,
                }
    return posts, pagedata

def create_archive_data(posts):
    archive_data = []
    count = {}
    mcount = {}
    for post in posts:
        year = post.date_created.year
        month = post.date_created.month
        if year not in count:
            count[year] = 1
            mcount[year] = {}
        else:
            count[year] += 1
        if month not in mcount[year]:
            mcount[year][month] = 1
        else:
            mcount[year][month] += 1
    for year in sorted(count.iterkeys(), reverse=True):
        archive_data.append({'isyear': True,
                             'year': year, 
                             'count': count[year],})
        for month in sorted(mcount[year].iterkeys(), reverse=True):
            archive_data.append({'isyear': False,
                                 'yearmonth': '%d/%02d' % (year, month),
                                 'monthname': MONTH_NAMES[month], 
                                 'count': mcount[year][month],})
    return archive_data

def create_tag_data(posts):
    tag_data = []
    count = {}
    for post in posts:
        tags = re.split(" ", post.tags)
        for tag in tags:
            if tag not in count:
                count[tag] = 1 #make count = 1 if this is the first item in that tag
            else:
                count[tag] += 1 # else, increase the count
    for tag, count in sorted(count.iteritems(), key=lambda(k, v): (v, k), reverse=True):
        tag_data.append({'tag': tag,
                         'count': count,})
    return tag_data

def create_cat_data(posts):
    cat_data = []
    count = {}
    for post in posts:
        categories = post.categories.all()
        for category in categories:
            if category.title not in count:
                count[category.title] = 1 #make count = 1 if this is the first item in that category
            else:
                count[category.title] += 1 # else, increase the count
    for category, count in sorted(count.iteritems(), key=lambda(k, v): (v, k), reverse=True):
        cat_data.append({'category': category,
                         'count': count,})
    return cat_data

