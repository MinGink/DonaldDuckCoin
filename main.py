from wallet import Wallet
from duckcoin import Duckcoin
from duck import Duck
from hashutils import hash_object, encoded_hash_object
from transaction import CoinCreation, Payment
import json
import os


if __name__ == '__main__':


    duck = Duck()

    user_dir = './user'
    tran_dir = './transaction'
    block_dir = './block'
    key_dir = './keypair'

    for file in os.listdir(user_dir) :
        if file.endswith('.json'):
             file_name = user_dir + "/" + file
             with open (file_name,encoding='utf_8_sig') as f:
                 d=json.load(f)
                 user = d['user']
                 value = d['default_value']
                 f.close()

             user_name=user
             user = Wallet()
             coins = [Duckcoin(value=value, wallet_id=user.id)]
             duck.create_coins(coins)

             user_sk=hash_object(user.Private_Key.to_string())
             user_pk=hash_object(user.Public_Key.to_string())
             user_file = {"user":user_name, "user_sk":user_sk,"user_pk":user_pk}

             key_name = key_dir +'/'+ user_name+'_key'+'.json'

             with open (key_name,'w+',encoding='utf_8') as k:
                 json.dump(user_file,k)
                 k.close()

                 
    for file in os.listdir(tran_dir) :
        if file.endswith('.json'):
             file_name = tran_dir + "/" + file
             with open (file_name,encoding='utf_8_sig') as f:

                  d=json.load(f)
                  sender = d['sender']
                  reciver = d['reciver']
                  value = d['tran_value']

                  sender=Wallet()
                  reciver = Wallet()

                  payment = sender.create_payment(value, reciver.id, duck.blockchain, duck)
                  signature = sender.sign(encoded_hash_object(payment))
                  payment_result = duck.process_payment(payment, [(sender.Public_Key, signature)])

                  sender_pk = hash_object(sender.Public_Key.to_string())
                  receiver_pk = hash_object(reciver.Public_Key.to_string())

                  sig_str=''
                  sig_str= duck.blockchain.temp_hash_block

                  Sender_output = {"value":value, "pubkey":sender_pk}
                  Reciver_input = [{"number": 1, "output": Sender_output}]
                  Reciver_output = [{"value": value, "pubkey":receiver_pk}]
                  Tran_file = [{"number":duck.genesis_block_hash, "input": Reciver_input,
                    "output":Reciver_output, "sig":sig_str}]
                  Block_file = {"prev": duck.blockchain.temp_hash_block, "n_tx": 1,"Transaction":Tran_file}

                  block_file_name=block_dir +"/" + file.split('.')[0]+'_block'+'.json'
                  with open(block_file_name,'w+', encoding='utf_8') as s:
                      json.dump(Block_file, s)
                      s.close()

                  f.close()


'''
Transaction可以展示的信息
[Payment.consumed_coins]这是消费的数量
[wallet.verifying_key]这是钱包的公钥
[wallet.signing_key]这是钱包的私钥
[Payment.id]TransID
[Payment.created_coins]产生新币的数量

[Duckcoin.id.coin_num]
[Duckcoin.value]
[Duckcoin.wallet_id]

Block可以展示的信息：
[block.hash_previous_block]
[block.transaction.id]
[block.transaction]

公钥私钥可以展示的信息
[wallet.Private_Key]这是钱包的私钥
[wallet.Public_Key]这是钱包的公钥
'''
