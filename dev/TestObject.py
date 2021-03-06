import bcolors
# This class will be used for creating testObjects,
# which will contain information about a specific url
# and the tests performed on that url.
# Methods: Add test, print test, print test to file
class TestObject:
    def __init__(self, url, type = None, query = None) :
        self.url = url
        self.tests = []
        # If only type is set, nothing happens!
        if (type != None and query != None) :
            self.add_test(type, query)
    
    # Only successful tests are intended to be appended!
    def add_test(self, type, query) :
        self.tests.append((type, query)) #Adds a test to the test-object
    
    def print_test(self) :
        for t in self.tests :
            print("URL:  " + self.url + ", TEST:  " + t[0] + ", QUERY:  " + t[1])
    
    def print_test_file(self, fileName) :
        with open(str(fileName), "a") as file :
            for t in self.tests :
                file.write("URL:  " + self.url + ", TEST:  " + t[0] + ", QUERY:  " + t[1])
