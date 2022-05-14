import requests
from bs4 import BeautifulSoup
import re
import os
import sys
import time
from clint.textui import progress

class BadLinkException(Exception):
    def __init__(self, ok):
        self.ok = ok

def make_directory(course_name):
    # create folder to store anime
    if not os.path.exists(course_name):
        os.mkdir(course_name)


def clear_tmp(directory):
    # clear tmp files
    for i in os.listdir(directory):
        if i[-3:] == "tmp":
            os.remove(os.path.join(directory, i))

def bookname(name):
    new_book = name.replace(' ', '%20')

    return new_book

def book_list(_name):
    url = 'https://ng1lib.org/s/' + _name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.findAll('h3',{'itemprop': 'name'})
    search_result = []
    for i in title:
        search_result.append({
            'link': i.find('a')['href'],
            'title': i.find('a').text
        })


    return search_result

def get_book(book_link):
    url = 'https://ng1lib.org' +  book_link  #'/book/2519956/2c2800'
    #a = book_link

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    d_links = soup.findAll('a',{'class': 'btn btn-primary dlButton addDownloadedBook'})
    search_result = []
    for i in d_links:
        search_result.append({
            'link':i['href'],
            'extention':re.findall('\((.*)\)', i.text).pop().split(',')[0]
        })
        
    return search_result

def download_book(book_name, download_link, extention):
    
    # download book and store in the folder the same name
    # don't download files that exist and clear tmp files after download
    filename = os.path.basename(download_link)
    download_path = os.path.join(book_name, filename)
    download_path = download_path + '.' + extention
    download_path = str(download_path)
    if not os.path.exists(download_path):
        _url = 'https://ng1lib.org' + download_link
        print("\nTrying " + _url + " ...")

        try:
            # send a download request with current url
            r = requests.get(_url, stream=True)

            print('Gotten Verified Download link!')
            print("Downloading", bookname(filename))

            # download if response of download url request is ok
            with open(download_path, 'wb') as out:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                    if chunk:
                        out.write(chunk)
                        out.flush()
                

            clear_tmp(book_name)
        except BadLinkException as e:
            print(e)

def get_user_choice(cap):
    LIST_OF_ALLOWED_DIGITS = [d for d in "0123456789"]
    choice = input("\nWhich one? Enter the number of your choice ::: ")

    # ensure choice is not empty
    if len(choice) == 0:
        return get_user_choice(cap)

    # separate each digit of the choice string
    digits = [c for c in choice]

    # look for any element that isn't a digit
    for digit in digits:
        if digit not in LIST_OF_ALLOWED_DIGITS:
            print("Your input is invalid! pick another number")
            return get_user_choice(cap)
    
    if int(choice) > cap or int(choice) == 0:
        print("Your input is invalid! pick another number")
        return get_user_choice(cap)
    
    return abs(int(
        choice))


if __name__ == "__main__":
    #print(banner())
    print("\nAll Books are gotten from https://ng1lib.org/")
    #print('File password (s) is: www.downloadly.ir')

    book_name = input("\nWhat course do you wanna download today ::: ")

    c_name = bookname(book_name)

    search_result = book_list(c_name)

    if len(search_result) == 0:
        print(
            "We couldn't find the course you searched for, check the spelling and try again")
        exit()

    print("\nSearch results for", book_name)

    for i, j in enumerate(search_result):
        print(i + 1, " - " + j["title"])

    choice = get_user_choice( len(search_result) )

    course = search_result[choice - 1]

    #this would return direct downloafd links to the book file 
    chosen_book = get_book(course["link"])
    #book_extention = get_book(course["link"])

    make_directory(course["title"])
    print("\nPress CTRL + C to cancel your download at any time")

    try:
        print("Aye aye captain, downloading about to begin, hit CTRL + C to cancel anytime")
        start = time.perf_counter()
        for i in chosen_book:
            download_book(course["title"], i['link'], i['extention'])
        end = time.perf_counter()
        print(f'\ncompleted download in {int(end-start)} seconds')
        print("\nFinished downloading desired book", course["title"])
    except Exception as e:
        print(e)






#print(download_book('courage to be disliked', '/dl/2519956/f40a4b', 'epub'))







#a = bookname('python for beginners')

#print(len(book_list(a)))
#b = int(input('please enter the number of books to display::: '))

#for i in book_list(a)[-5:]:
    #print(i['title'])

#print(get_book('hi'))
