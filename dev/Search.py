from lxml import html
from Proxy import Proxy
import urllib.request
import urllib.parse
import urllib.error
import data
import sys
import bcolors

class Search :
    #Initializes variables
    def __init__(self, useproxy, retries = None, verbose = False, sleep = 5):
        self.urls = [] # contains scraped urls
        self.blacklist = [] # contains blacklisted proxies
        self.useproxy = useproxy # dictates use of proxy
        self.retries = retries # sets the number of search retries, if None => unlimited
        self.verbose = verbose # sets verbosity level
        self.sleep = sleep # dictates sleep while searching for urls
        self.proxyhandler = None
        if (self.useproxy) :
            self.proxyhandler = Proxy(self.verbose)
            self.proxyhandler.proxify()
        if (self.verbose) :
            bcolors.printGreen("[+]Search object created!")
    
    def print_state(self) :
        bcolors.printBold("****Printing object state****")
        bcolors.printBold("URLs:\n")
        print(str(self.urls))
        bcolors.printBold("Blacklist:\n")
        print(str(self.blacklist))
        bcolors.printBold("Settings:\n")
        print("Retries: " + str(self.retries) + ", Verbose: " + str(self.verbose) + ", Sleep: " + str(self.sleep)) 
    
    def print_urls(self) :
        bcolors.printBold("****PRINTING URLS****\n")
        for url in self.urls :
            print(str(url))
            
        
    # Returns the HTML page of a website.
    # It incorporates error checking and retries
    # If an unknown error was raised, 
    def get_html(self, url) :
        if (self.useproxy) :
            self.proxyhandler.validate_proxy()
        req = urllib.request.Request(url, None, data.headers)
        tries = 0
        while (self.retries == None or tries < self.retries):
            try :
                res = urllib.request.urlopen(req)
                src = res.read()
                break
            except urllib.error.HTTPError as e:
                if (self.useproxy) :
                    self.update_proxy()
                if (e.code != 503) :
                    bcolors.printFail("[-]HTTP Error " + str(e) + " was raised!")
                    return None
            
                # If we have to retry, append current proxy to blacklist
                if (self.useproxy) :
                    # Blacklists both proxies if error occured!
                    self.proxyhandler.blacklist_current_proxy(True)
            tries += 1
                
        return html.fromstring(str(src))
    
    def update_proxy(self, https=False) :
        self.proxyhandler.proxify(https, True)
        self.proxyhandler.validate_proxy()
    
    def fatal_exception(self,e = None, function_name = None) :
        bcolors.printFail("A fatal exception has occured!")
        if (not e == None) :
            print(str(e))
        elif (not function_name == None) :
            print(str(function_name))
        bcolors.printBold("****PROGRAM STATE****")
        self.print_state()
        sys.exit(0)
