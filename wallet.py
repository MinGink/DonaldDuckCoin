from ecdsa import SigningKey
from hashutils import hash_sha256, hash_object, encoded_hash_object
from transaction import Payment, CoinCreation
from duckcoin import Duckcoin
import pdb

class Wallet():
    """ A user of the duckcoin """
    def __init__(self, Private_Key = None):
        if Private_Key is None:
            self.Private_Key = SigningKey.generate()
        else:
            self.Private_Key = Private_Key
        self.Public_Key = self.Private_Key.get_verifying_key()
        self.id = self.get_wallet_id_from_Public_Key(
            self.Public_Key
        )

    def sign(self, message):
        """ Sign a message using the signing key """
        return self.Private_Key.sign(message)

    def verify_signature(self, Public_Key, signature, message):
        """ Verify a signature of a message using the verifying key """
        return Public_Key.verify(signature, message)

    def get_wallet_id_from_Public_Key(self, Public_Key):
        """ Return the wallet key from the verifying key """
        return hash_object(Public_Key.to_string())

    def create_payment(self, amount,wallet_id, blockchain, duck):
        """ Transfer coins from this wallet to other(s).
            Parameters:
             - payments: List of duples (wallet id, amount)
             - blockchain: The complete blockchain
             - duck: An interface to the Duck functions
        """
        consumed_coins = []
        created_coins = []
        my_coins = self.get_coins(blockchain)
        # TODO: Order coins by their values


        my_coins[:] = [coin for coin in my_coins if coin not in consumed_coins]
        for coin in my_coins:
            if coin.value <= amount:
                consumed_coins.append(coin)
                consumed_amount = coin.value
                amount -= coin.value
            else:
                new_coins = self.devide_coin(coin, amount, duck)
                consumed_ind = self.index_coin_value(new_coins, amount)
                consumed_coins.append(new_coins[consumed_ind])
                consumed_amount = amount
                my_coins.append(new_coins[consumed_ind + 1])
                amount = 0
            created_coins.append(Duckcoin(value=consumed_amount, wallet_id=wallet_id))
            if amount == 0:
                break
        return Payment(created_coins, consumed_coins)

    def index_coin_value(self, coins, value):
        """ Return the index of the first coin with the value
            passed as parameter
        """
        ind = 0
        while ind < len(coins):
            if coins[ind].value == value:
                return ind
            else:
                ind += 1
        return None

    def devide_coin(self, coin, value, duck):
        """ Devide a coin in two new coins. The paramenter
            'value' is the value of one of the new coins
            and the value of the other is the rest.
            The original coin is consumed and cannot be used
            again.
        """
        if value > coin.value:
            return
        created_coins = []
        created_coins.append(Duckcoin(value, self.id))
        created_coins.append(Duckcoin(coin.value - value, self.id))
        payment = Payment(created_coins=created_coins, consumed_coins=[coin])
        signature = self.sign(encoded_hash_object(payment))
        new_block = duck.process_payment(
            payment, [(self.Public_Key, signature)]
        )
        return new_block.transaction.created_coins

    def get_coins(self, blockchain):
        """ Get all active coins of the blockchain associated
            to this wallet
        """
        coins = []
        for block in blockchain.blocks:
            tx = block.transaction
            for coin in tx.created_coins:
                if coin.wallet_id == self.id:
                    coins.append(coin)
            if isinstance(tx, CoinCreation):
                continue
            for coin in tx.consumed_coins:
                if coin.wallet_id == self.id:
                    coins.remove(coin)
        return coins
