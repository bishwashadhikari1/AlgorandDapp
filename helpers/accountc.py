from algosdk import account, mnemonic


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    return private_key ,address, mnemonic.from_private_key(private_key)
    

def pk_to_seed(pk):
    return mnemonic.from_private_key(pk) 

def seed_to_keys(seed):
    return mnemonic.to_private_key(seed), mnemonic.to_public_key(seed)



