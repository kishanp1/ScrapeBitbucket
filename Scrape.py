import requests
from lxml import html
import git

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

#check urls, as if they may slightly change in the future
LOGIN_URL = "https://bitbucket.org/account/signin/?next=/"
URL = "https://bitbucket.org/dashboard/repositories"

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "username": USERNAME, 
        "password": PASSWORD, 
        "csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//div[@class='repo-list--repo']/a/@href")

    #prints all repositories, if you want
    print(bucket_names)
 
    '''
    Here, the USERNAME is the one you will see in the link when you open your profile
    you can change hw1 to anything, which is the keyword for specific group of repositories
    '''
    
    i = 0
    while i<len(bucket_names):
        if 'hw1' in bucket_names[i]:
            cloning="https://USERNAME@bitbucket.org/"+bucket_names[i]
            git.Git().clone(cloning)
            print(bucket_names[i])
        i+=1

if __name__ == '__main__':
    main()
