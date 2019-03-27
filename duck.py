from blockchain import Blockchain, Block
from ecdsa import SigningKey
from transaction import CoinCreation
from hashutils import hash_sha256, hash_object, encoded_hash_object
from duckcoin import Duckcoin, CoinId
from wallet import Wallet

class Duck():
    """ Trusted entity that creates and manages the blockchain """
    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        self.genesis_block_hash = hash_object(self.add_genesis_block())
        self.last_block_signature = self.wallet.sign(
            self.genesis_block_hash.encode('utf-8')
        )

    def add_genesis_block(self):
        """ Add the genesis block to the blockchain and return
            the hash of the genesis block
        """
        coin = Duckcoin(1, self.wallet.id, CoinId(0,0))
        return self.create_coins([coin])

    def create_coins(self, coins):
        """ Add a CoinCreation transaction to the blockchain
            creating the coins passed as parameters. Return
            the hash of the added block.
        """
        transaction = CoinCreation(created_coins=coins)
        block = Block(transaction)
        return self.blockchain.add_block(block)

    def process_payment(self, payment, signatures):
        """ Process a payment sent by a user.
            The paramenter signatures is a list of duples with
            the users' validation keys as the first component
            and the payment signatures as the second component.
        """
        # Verify users' signatures
        if (not self.verify_signatures(payment, signatures) or
                not payment.verify_balance()):
            return None

        # Check if all the coins that are being transferred
        # exist and were not consumed previously
        if (not self.blockchain.check_coins(payment.consumed_coins)):
            return None

        block = Block(payment)
        return self.blockchain.add_block(block)

    def verify_signatures(self, transaction, signatures):
        """ Verify a list of transaction signatures """
        # Verify all signatures with their corresponding
        # public keys
        for Public_Key, signature in signatures:
            if not self.wallet.verify_signature(
                    Public_Key, signature, encoded_hash_object(transaction)):
                return False

        # Verify if all users whose coins will be consumed signed
        # the payment
        users = []
        for Public_Key, signature  in signatures:
            wallet_id = self.wallet.get_wallet_id_from_Public_Key(Public_Key)
            users.append(wallet_id)
        for coin in transaction.consumed_coins:
            if coin.wallet_id not in users:
                return False

        return True
