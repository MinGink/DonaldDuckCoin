# DonaldDuckCoin 
Wenyue Ma && Ming Yang

## Requirement
- DonaldDuckCoin implementation in Python 3
- dependencies：
[ecdsa](https://github.com/warner/python-ecdsa)


##Introduction
**DonaldDuck**
- DonaldDuck is a trusted entity that creates coins, manages the blockchain and approves payments.

**Coin creation**
- Only Duck can create coins.
- The coins have an id, a value and the wallet id of the owner.
- The coin id is assigned by Duck when the transaction that creates the coin is inserted in the blockchain.
- This id is composed by its transaction id and the correlative number of the coin into the transaction.

**Payment**
- Whoever owns a coin can transfer it on to someone else.
- Payments must be signed by all the owners whose coins are consumed in the transaction.
- Duck verifies signatures and checks double-spending before approving the transaction.
- When a coin is consumed it is deleted and other coin with the new owner is created.
- The amount of created coins in a payment must be equal to the amout of consumed coins.

**Blockchain**
- Transactions are inserted by Duck into the blockchain.
- Duck publishes the blockchain along with the signature of the last block.

**Wallet**
- A wallet is identified by the sha256 hash of its public key.
- A wallet is assigned to Duck when it is created.
- The blockchain is created too, and the genesis block has a transaction that creates a coin assigned to the Duck's wallet.

**Signing and hashing**
- *ecdsa* is used for signing.
- *sha256* is used for hashing.
