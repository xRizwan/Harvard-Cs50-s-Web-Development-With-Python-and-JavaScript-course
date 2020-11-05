import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

# converting headings from Markdown to HTML
def replaceHeadings(text):
    for n in range(1,6):
        hRegex = rf"(?<!#)#{{{re.escape(str(n))}}}.+\n"
        
        while True:
            match = re.search(hRegex, text)
            if(match != None):
                span = match.span()
                startI = span[0]
                endI = span[1]
                text = text[:startI] + f"<h{n}>" + text[startI+n+1 : endI] + f"</h{n}>" + text[endI:]
            else:
                break
    return text

# converting bold texts from Markdown to HTML
def replaceBold(text):
    regex = r"(?<!\*)\*\*[\w\s-]+\*\*"

    while True:

        match = re.search(regex, text)
        if(match == None):
            break

        span = match.span()
        startI = span[0]
        endI = span[1]
        text = text[:startI] + "<strong>" + text[startI+2 : endI-2] + f"</strong>" + text[endI:]

    return text

# converting italic texts from Markdown to HTML
def replaceEm(text):
    regex = r"(?<!\*)\*\S[\w\s-]+\*"

    while True:

        match = re.search(regex, text)
        if(match == None):
            break

        span = match.span()
        startI = span[0]
        endI = span[1]
        text = text[:startI] + "<em>" + text[startI+1 : endI-1] + f"</em>" + text[endI:]
        
    return text

# converting links from Markdown to HTML
def replaceLinks(text):
    regex = r"\[(.*?)\]\((.*?)\)"


    while True:

        match = re.search(regex, text)

        if(match == None):
            break

        span = match.span()
        startI = span[0]
        endI = span[1]
        text = text[:startI] + f"<a href='{match.group(2)}'>{match.group(1)}" + "</a>" + text[endI:]
    
    return text

# converting lists from Markdown to HTML
def replaceLists(text):

    regex = r"(?<![a-zA-Z0-9])[\*|-](.+\n)"

    while True:
        match = re.search(regex, text)

        if(match == None):
            break
    
        span = match.span()
        startI = span[0]
        endI = span[1]
        innerText = match.group(1)

        text = text[:startI] + f"<ul><li>{innerText}</li></ul>" + text[endI:]

    return text

# standerdize new lines to be only \n instead of \r\n
def setNLines(text):
    regex = r"\r\n"
    text = re.sub(regex, "\n", text)
    text = re.sub(r"\r", "", text)

    return text

def newLineToParagraph(text):
    regex = r"\n(.+)"
    match = re.finditer(regex, text)

    # variable to hold value everytime a paragraph tag is added
    # because i'm using finditer() only once it will give the location of each
    # match when there was no change made to it
    # after adding a p tag will mean that every other match has move 6 indexes
    # from the initial location
    n = 0

    if (match != None):
    
        for m in match:
            regex2 = r"^<.+>"
            
            match2 = re.search(regex2, m.group(1))

            if(match2 == None):
                location = m.span()
                start = location[0]
                end = location[1]
                text = text[:start+n] + f"<p>{m.group(1)}</p>" + text[end + n:]
                n = n + 6

    return text

def markdownToHTML(text):
    text = setNLines(text)
    text = replaceHeadings(text)
    text = replaceBold(text)
    text = replaceEm(text)
    text = replaceLinks(text)
    text = replaceLists(text)
    text = newLineToParagraph(text)

    return text