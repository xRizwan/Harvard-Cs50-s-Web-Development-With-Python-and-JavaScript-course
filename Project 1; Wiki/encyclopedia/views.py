from django.shortcuts import render, redirect
import random as r
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):

    content = util.get_entry(entry)
    if (content == None):
        content = "Error: No Results Found."
    else:
        content = util.markdownToHTML(content)

    return render(request, "encyclopedia/entry.html", {
        "title" : entry.capitalize(),
        "content": content
    })

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        query = request.POST.get('q')
        found = []
        target = ''
        for entry in entries:
            if((query.lower() in entry.lower()) or (entry.lower() in query.lower())):
                found.append(entry)
            if (entry.lower() == query.lower()):
                target = entry
                print(target)

        if (target == ''):
            return render(request, "encyclopedia/search.html", {
                'found': found
            })
        else:
            # redirect to the target if target found
            return redirect(f'/wiki/{target}')
    else:
        return render(request, "encyclopedia/search.html", {
            'found': util.list_entries()
        })

def newPage(request):
    if(request.method == "POST"):
        title = request.POST.get('title')
        content = request.POST.get('content')
        entry = util.get_entry(title)
        
        if(entry == None):
            if(title == ''):
                return render(request, "encyclopedia/newpage.html", {
                    'error': True,
                    "message": "Title Can't Be Empty"
                })
            
            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/newpage.html", {
                'error': True,
                "message": "A page with that title already exists"
            })
    
    return render(request, "encyclopedia/newpage.html")

def edit(request, entry):
    if (request.method == 'POST'):
        content = request.POST.get('content')
        util.save_entry(entry, content)
        return redirect(f'/wiki/{entry}')

    content = util.get_entry(entry)
    if(content == None):
        return redirect('/')

    content = util.setNLines(content)
    return render(request, "encyclopedia/editpage.html", {
        "content": content,
        "title": entry
    })

def random(request):
    entries = util.list_entries()
    length = len(entries)
    rand = r.randint(0, length - 1)
    randTarget = entries[rand]

    return redirect(f'/wiki/{randTarget}')