#!/usr/bin/env python3

import couchdb2
import datetime
import json
import os

server = couchdb2.Server(href='https://localhost:6984/', username='admin', password='sekret', use_session=True)
quiver = '/Users/YOU/Documents/Quiver.qvlibrary'

# make things for which we don't have a timestamp "created" 3y ago and updated today
now_ts     = datetime.datetime.now().timestamp()
default_ts = now_ts - 94608000

db = couchdb2.Database(server, 'inkdrop', check=True)

def get_couch_tags(db):
    tags = []
    for doc in db:
        if 'tag:' in doc['_id']:
            tags.append(doc['name'])

    return tags

def get_couch_books(db):
    cbooks = []
    for doc in db:
        if 'book:' in doc['_id']:
            cbooks.append({'id': doc['_id'], 'name': doc['name']})

    return cbooks


def tag_update(db, ctags, tag_list):
    """
    Make sure we have these tags in couchdb, add if we don't have them
    """
    these_tags = []
    for t1 in tag_list:
        t = t1.lower()
        if t == 'tutorial':
            continue

        these_tags.append('tag:' + t)

        if t not in ctags:
            print('tag: %s is missing' % t)
            ctags.append(t)
            tag_meta = {'_id'      : 'tag:' + t,
                        'name'     : t,
                        'color'    : 'default',
                        'count'    : 0,
                        'createdAt': int(default_ts),
                        'updatedAt': int(now_ts)
                        }
            db.put(tag_meta)

    return (ctags, these_tags)


def notebook_update(db, cbooks, d2):
    ctmp = []
    null = None

    nb = d2['uuid'].split('-')[0]

    for cb in cbooks:
        ctmp.append(cb['name'])

    if d2['name'] not in ctmp:
        # print('book: %s (%s) is missing' % (d2['name'], nb))

        book_meta = {'_id'         : 'book:' + nb,
                     'name'        : d2['name'],
                     'count'       : 0,
                     'parentBookId': null,
                     'createdAt'   : int(default_ts),
                     'updatedAt'   : int(now_ts)
                     }
        db.put(book_meta)

    return nb


# read data from Quiver
tags   = []
ctags  = get_couch_tags(db)
cbooks = get_couch_books(db)

with open(quiver + '/meta.json') as quiver_file:
    d1 = json.load(quiver_file)
    print(d1['children'])
    for qv in d1['children']:
        child = '%s/%s.qvnotebook' % (quiver, qv['uuid'])

        if os.path.isdir(child):
            if os.path.isfile(child + '/meta.json'):
                with open(child + '/meta.json') as child_file:
                    d2 = json.load(child_file)
                    nb = notebook_update(db, cbooks, d2)

                    note_dirs = os.listdir(child)
                    for n in note_dirs:
                        if 'qvnote' in n:
                            note = {}
                            ndir = '%s/%s' % (child, n)
                            body = ''

                            with open(ndir + '/meta.json') as note_meta_file:
                                nmf = json.load(note_meta_file)
                            with open(ndir + '/content.json') as note_content_file:
                                ncf = json.load(note_content_file)

                            for x in ncf['cells']:
                                body = '%s%s\n\n' % (body, x['data'])

                            (ctags, these_tags) = tag_update(db, ctags, nmf['tags'])

                            # need to convert python timestamps (Quiver) to javascript timestamps (Inkdrop)
                            u_at = nmf['updated_at'] * 1000
                            c_at = nmf['created_at'] * 1000

                            note_meta = {'_id'              : 'note:' + nmf['uuid'],
                                         'tags'             : these_tags,
                                         'updatedAt'        : u_at,
                                         'createdAt'        : c_at,
                                         'title'            : nmf['title'],
                                         'bookId'           : 'book:' + nb,
                                         'numOfTasks'       : 0,
                                         'numOfCheckedTasks': 0,
                                         'status'           : 'none',
                                         'share'            : 'private',
                                         'doctype'          : 'markdown',
                                         'body'             : body
                                         }
                            db.put(note_meta)
