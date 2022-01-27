import os,sys,json,requests,re
from tqdm import tqdm

def nft_image_download(url,name):
    nft_image = requests.get(url).content
    name = re.sub(r"[^-_.A-Za-z0-9]","",name)
    image_name = '{}.png'.format(name)
    with open(('{}/{}'.format(nft_collection_name,image_name)), 'wb') as handler:
        handler.write(nft_image)

nft_collection_count = 0
nft_collection_name = input("[*] Collection name: ")
try:
    nft_collection = requests.get('https://api.opensea.io/api/v1/collection/{}'.format(nft_collection_name))
    nft_collection_stats = json.loads(nft_collection.text)
    nft_collection_count = nft_collection_stats['collection']['stats']['count']
except KeyError:
    print("[!] The collection you are searching for is not exist!")
    print(" - Make sure you entered a valid collection name that matches with example cases. Not all collection URLs match with its name!")
    print("     - MY COLLECTION --> my-collection")
    print("     - John Doe's Collection --> john-does-collection")
    sys.exit(1)


if nft_collection_count < 1:
    print("[!] This collection has no assets to nfteal!")
    sys.exit(1)
try:
    os.mkdir(nft_collection_name)
except FileExistsError:
    print("[!] File already existing, overwriting!")

assets_spawning = True
offset = 0
print("[!] Found {} images to nfteal!".format(nft_collection_count))
print("[+] Extracting images under the {} folder\n".format(nft_collection_name))
pbar = tqdm(total=nft_collection_count)

while assets_spawning:
    nft_assets_url = "https://api.opensea.io/api/v1/assets?offset={}&limit=50&collection={}".format(offset,nft_collection_name)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36','referrer':nft_assets_url}
    response = requests.get(nft_assets_url, headers=headers)
    nft_assets = json.loads(response.text)
    
    for asset in nft_assets['assets']:
        nft_image_download(asset['image_url'],asset['name'])
        pbar.update(1)
    if len(nft_assets['assets']) < 50:
        assets_spawning = False
    offset+=50
