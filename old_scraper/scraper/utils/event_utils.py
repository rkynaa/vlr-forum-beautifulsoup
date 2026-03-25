import requests
from bs4 import BeautifulSoup

def detect_completed_events(urlBase, upcomingEvent, completedMatchesRaw):
    
    urlEventsLst = [] # List of URLs for Events
    eventTitlesLst = [] # List of events' titles

    for resultCompletedMatch in completedMatchesRaw: # For each query result
        url_event = urlBase + resultCompletedMatch.get('href') # Link to each event
        soupEvent = BeautifulSoup(requests.get(url_event).content, 'html.parser') # Soup for specific event
        titleEvent = soupEvent.find_all("title") # Web Title of the Event's VLR webpage
        webTitleLst = " ".join(titleEvent[0].text.split()).split("|")[0].split(":") # Event Web Title Broken down into a list
        
        # Getting the event's title
        eventTitle = "" # Initialize Event Title's name
        if len(webTitleLst) == 2: # If the event web title has only one ":" symbol,
            eventTitle += webTitleLst[0] # The first element is the event's title
            
        else: # If the event web title has two ":" symbols (i.e., 'VCT 2025: China Stage 2: Brackets, Groups, and Standings '),
            eventTitle += webTitleLst[0] + ":" + webTitleLst[1] # the first two elements are the event's title
        
        # Web Scraping for completed events only
        if eventTitle in upcomingEvent: # If the event is not completed,
            continue # It will be skipped
        
        else: # If the event is already completed,
            eventLinks = soupEvent.find_all("a", class_="wf-nav-item") # Query results for event link
            eventPartLink = eventLinks[1].get('href') # Getting the partial link of the event
            eventPartLink = eventPartLink.split("?")[0] + "?" + "series_id=all" # Getting the partial link of the event's overall matches
            matchesEventLink = urlBase + eventPartLink # Completing the event's link
            
            eventTitlesLst.append(eventTitle) # Adding the event's title into the events' titles list
            urlEventsLst.append(matchesEventLink) # Adding the event's url into the events' titles list
        
    return urlEventsLst, eventTitlesLst
    
