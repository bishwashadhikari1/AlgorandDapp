

import random
from django.shortcuts import render, redirect
from localStoragePy import localStoragePy
from helpers.accountc import generate_algorand_keypair, seed_to_keys
from helpers.connectclient import client
def home_index(request):
    return render(request, 'homepage.html')

def create_wallet(request):
    privatekey, publickey, seedcode = generate_algorand_keypair()
    seed = (str(seedcode)).split()
    localStorage = localStoragePy('me.algowallet')
    localStorage.setItem('privatekey', privatekey)
    localStorage.setItem('publickey', publickey)
    return render(request, 'createwallet.html', context= {'seedcode': seed, 'privatekey':privatekey})

from helpers.accountc import pk_to_seed
def confirm_creation(request):
    localStorage = localStoragePy('me.algowallet')
    private_key = localStorage.getItem('privatekey')
    shuffle_seed = str(pk_to_seed(private_key)).split()
    random.shuffle(shuffle_seed)
    error_found = 0
    if request.method == "POST":
        error_found = 1
        entry = request.POST['enteredseed']

        if str(entry) == str(pk_to_seed(private_key)):
            error_found = 0
            return redirect('/wallethome')

    return render(request, 'confirmcreation.html', context={'shuffle_seed':shuffle_seed, 'error_found': error_found})



def wallet_home(request):
    localStorage = localStoragePy('me.algowallet')
    private_key = localStorage.getItem('privatekey')
    public_key = localStorage.getItem('publickey')
    acc_info = client().account_info(public_key)
    print(acc_info)
    return render(request, 'wallethome.html')



def import_wallet(request):
    localStorage = localStoragePy('me.algowallet')
    error_found = 0
    if request.method == "POST":
        error_found = 1
        entry = request.POST['enteredseed']
        try:
            privatekey, publickey = seed_to_keys(entry)
            localStorage.setItem('privatekey', privatekey)
            localStorage.setItem('publickey', publickey)
            error_found = 0
            return redirect('/wallethome')
        except:
            error_found = 1
    return render(request, 'importwallet.html', context={'error_found': error_found})
    

