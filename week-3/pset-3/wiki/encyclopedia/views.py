from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import random
from . import util
import markdown2
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)  # Fetch the raw Markdown content
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error": "The requested page was not found."
        })
    
    # Convert Markdown to HTML using markdown2
    html_content = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content  # Pass the HTML content to the template
    })
    
def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    if query in entries:
        return redirect('entry', title=query)
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })
        
def edit(request, title):
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect('entry', title=title)
    else:
        content = util.get_entry(title)
        html_content = content
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": html_content
        })
        
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)

def new_page(request):
    if request.method == "POST":
        # Get the form data
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Check if the title already exists
        if title in util.list_entries():
            # If the title exists, show an error
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists. Please choose a different title."
            })
        
        # Save the new entry to disk using `save_entry` function
        util.save_entry(title, content)
        
        # Redirect to the new entry's page
        return redirect('entry', title=title)
    
    # If GET request, show the form
    return render(request, "encyclopedia/new_page.html")
