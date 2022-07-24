import requests
import git
import keyring
import pwinput
import time

def repo_link(target_username):
    url = 'https://api.github.com/users/'
    url = url+target_username
    r = requests.get(url)
    parsed = r.json()
    repos_url = parsed["repos_url"]
    url_batch = requests.get(repos_url)
    repo_response = url_batch.json()
    return [i['full_name'] for i in repo_response]

resp = input('Do you want to clear your credentials? (y/n): ')
if resp == 'y':
    username = input('Enter username to delete password: ')
    try:
        keyring.delete_password('github', username)
        print('Credentials cleared')
        time.sleep(5)
        exit()
    except:
        print('No credentials found')
        time.sleep(5)
        exit()
else:
    pass

target_username = input("Enter target github username: ")
repoURLs = repo_link(target_username)

service_id = 'github'
downloader_username = input("Enter your github username: ")
save_path = input("Enter the path to save the repos: ")

password = keyring.get_password(service_id, downloader_username)

if password is None:
    downloader_password = pwinput.pwinput()
    input("Enter your github password: ")
    keyring.set_password(service_id, downloader_username, downloader_password)
else:
    downloader_password = password

call_urls = ['https://'+downloader_username+':'+downloader_password+':@github.com/'+i+'.git' for i in repoURLs]

print(f'a total of {len(call_urls)} repos will be downloaded \n')

answer = input("Do you want to continue? (y/n): ")
if answer == 'y':
    try:
        for i in range(len(call_urls)):
            git.Git(save_path).clone(call_urls[i])
            print(f'{i+1}/{len(call_urls)} repos downloaded')
    except Exception as e:
        print(e)
        keyring.delete_password(service_id, downloader_username)
        print("Download failed! Removed stored password")
    print('\nAll repos downloaded')
else:
    print('\nAborted')
    time.sleep(5)
    exit()