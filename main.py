from web3 import Web3
import requests
import json

from fake_useragent import FakeUserAgent
import time
import random

from config import logger

#КОНТРАКТ НА КЛЕЙМ и АБИ!
contract_abi = '[{"inputs":[{"internalType":"address","name":"_initialOwner","type":"address"},{"internalType":"address","name":"_authorizedSigner","type":"address"},{"internalType":"address","name":"_odosDaoRegistry","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[],"name":"AlreadyAuthorized","type":"error"},{"inputs":[],"name":"ECDSAInvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"length","type":"uint256"}],"name":"ECDSAInvalidSignatureLength","type":"error"},{"inputs":[{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"ECDSAInvalidSignatureS","type":"error"},{"inputs":[],"name":"ExpiredSignature","type":"error"},{"inputs":[],"name":"FailedCall","type":"error"},{"inputs":[{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"needed","type":"uint256"}],"name":"InsufficientBalance","type":"error"},{"inputs":[],"name":"InvalidNonce","type":"error"},{"inputs":[],"name":"InvalidShortString","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"NotAuthorized","type":"error"},{"inputs":[],"name":"NotRegistered","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"SafeERC20FailedOperation","type":"error"},{"inputs":[{"internalType":"string","name":"str","type":"string"}],"name":"StringTooLong","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newOdosDaoRegistry","type":"address"}],"name":"DaoRegistryUpdated","type":"event"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferStarted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":true,"internalType":"address","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"RewardClaimed","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"authorizedSigner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"payoutToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct Claim","name":"_claim","type":"tuple"},{"internalType":"bytes","name":"_signature","type":"bytes"}],"name":"claimReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_token","type":"address"}],"name":"extractERC20","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"extractNative","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"payoutToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct Claim","name":"_claim","type":"tuple"}],"name":"getClaimHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"odosDaoRegistry","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"recipientNonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"address","name":"payoutToken","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"internalType":"struct Claim","name":"_claim","type":"tuple"},{"components":[{"internalType":"address","name":"member","type":"address"},{"internalType":"string","name":"agreement","type":"string"},{"internalType":"uint256","name":"nonce","type":"uint256"}],"internalType":"struct Registration","name":"_registration","type":"tuple"},{"internalType":"bytes","name":"_claimSignature","type":"bytes"},{"internalType":"bytes","name":"_registrationSignature","type":"bytes"}],"name":"registerAndClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_odosDaoRegistry","type":"address"}],"name":"updateOdosDaoRegistry","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_newSigner","type":"address"}],"name":"updateSigner","outputs":[],"stateMutability":"payable","type":"function"}]'
claim_contract_address = '0x4C8f8055D88705f52c9994969DDe61AB574895a3'
#----------------------------------------------------------
#КОНТРАКТ ТОКЕНА и АБИ!
token_abi = '[{"inputs":[{"internalType":"address","name":"_bridge","type":"address"},{"internalType":"address","name":"_remoteToken","type":"address"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint8","name":"_decimals","type":"uint8"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"BRIDGE","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REMOTE_TOKEN","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bridge","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"l1Token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"l2Bridge","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"remoteToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"_interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'
token_address = '0xca73ed1815e5915489570014e024b7EbE65dE679'
#----------------------------------------------------------
#RPC
lst_rpc = 'https://mainnet.base.org'


def load_data(file_path) -> list:
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


def write_error_adres(key: str):
    with open('error.txt', 'a') as f:
        f.write(key + '\n')


def get_amount(wallet_address: str, proxy: str, key: str) -> int:
    logger.info(f'{wallet_address}|Получаю амоунт')
    url = f'https://api.odos.xyz/loyalty/users/{wallet_address}/balances'
    proxies = {'http': f'http://{proxy}',
               'https': f'http://{proxy}'}
    user_agent = FakeUserAgent().random
    headers = {
        'authority': 'api.odos.xyz',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent
    }
    for _ in range(3):
        try:
            response = requests.get(url=url, headers=headers, proxies=proxies)
            response.raise_for_status()
            json_data = response.json()
            amount = json_data['data']['pendingTokenBalance']

            logger.success(f'{wallet_address}| токены: {amount}')
            return int(amount)
        except Exception as e:
            logger.error(f'{wallet_address}|Ошибка получения амоунт:{e}')
            write_error_adres(key=key)


def get_data(wallet_address: str, proxy: str, key: str):
    logger.info(f'{wallet_address}|Получаю дату')
    url = f'https://api.odos.xyz/loyalty/permits/8453/0xca73ed1815e5915489570014e024b7EbE65dE679/{wallet_address}'
    proxies = {'http': f'http://{proxy}',
               'https': f'http://{proxy}'}
    user_agent = FakeUserAgent().random

    headers = {
        'accept': '*/*',
        'accept-language': 'pl',
        'origin': 'https://app.odos.xyz',
        'priority': 'u=1, i',
        'referer': 'https://app.odos.xyz/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user_agent,
    }

    for _ in range(3):
        try:
            response = requests.get(url=url, headers=headers, proxies=proxies)
            response.raise_for_status()
            json_data = response.json()
            logger.success(f'{wallet_address}| дату получил')
            print(json_data)
            return json_data
        except Exception as e:
            logger.error(f'{wallet_address}|Ошибка получения даты:{e}')
            write_error_adres(key=key)


def claim_account(account, wallet_address, key, data, web3, amount):
    logger.info(f'{wallet_address}|Начинаю клеймить')

    for _ in range(3):
        try:
            sender = data['claim']['sender']
            reci = sender
            paytoken = data['calim']['payoutToken']
            amount = amount
            nonce = data['claim']['nonce']
            deadline = data['claim']['deadline']
            hashed_claim = data['hashedClaim']
            messagehash = data['messageHash']
            signa = data['signature']

            contract = web3.eth.contract(
                address=web3.to_checksum_address(claim_contract_address),
                abi=contract_abi)
            transaction = (contract.functions.claim(
                (
                    web3.to_checksum_address(sender),
                    web3.to_checksum_address(reci),
                    web3.to_checksum_address(paytoken),
                    amount,
                    int(nonce),
                    deadline
                ),

                messagehash[:2],
                hashed_claim[:2],
                signa[:2]
            ).build_transaction({
                'from': web3.to_checksum_address(account.address),
                'gasPrice': int(web3.eth.gas_price * 15),
                'nonce': web3.eth.get_transaction_count(account.address),
                'gas': 0
            }))

            transaction['gas'] = int(web3.eth.estimate_gas(transaction))
            signed_txn = web3.eth.account.sign_transaction(transaction, key)
            claim_txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            web3.eth.wait_for_transaction_receipt(claim_txn_hash)
            logger.success(f'{wallet_address}| склеймил')
        except Exception as e:
            logger.error(f'{wallet_address}| ошибка клейма:{e}')
            write_error_adres(key=key)


def transfer_to_birj(account, key, deposit_address, web3):
    logger.info(f'{account.address}| отправляю на {deposit_address}')
    for _ in range(3):
        try:
            token_contract = web3.eth.contract(
                address=web3.to_checksum_address(token_address),
                abi=token_abi
            )
            token_amount = token_contract.functions.balanceOf(account.address).call()
            logger.success(f'{account.address}|{token_amount}')
            transfer_transaction = token_contract.functions.transfer(
                web3.to_checksum_address(deposit_address),
                token_amount
            ).build_transaction(
                {
                    'from': account.address,
                    'gasPrice': int(web3.eth.gas_price * 5),
                    'nonce': web3.eth.get_transaction_count(account.address),
                    'gas': 0
                })
            transfer_transaction['gas'] = int(web3.eth.estimate_gas(transfer_transaction) * 5)
            signed_transfer_txn = web3.eth.account.sign_transaction(transfer_transaction, key)
            transfer_txn_hash = web3.eth.send_raw_transaction(signed_transfer_txn.raw_transaction)
            logger.success(f'{account.address}| отправил на {deposit_address}')
            return
        except Exception as e:
            logger.error(f'{account.address}|ошибка трансфера: {e}')
            write_error_adres(key=key)


def main():
    proxys = load_data('proxy.txt')
    keys = load_data('private_key.txt')
    deposit_address = load_data('deposit_address.txt')
    for key, proxy, deposit_adre in zip(keys, proxys, deposit_address):
        for _ in range(3):
            try:
                web3 = Web3(Web3.HTTPProvider(lst_rpc))
                account = web3.eth.account.from_key(key)
                wallet_address = account.address
                logger.info(f'{wallet_address}| к акаунту подключился')
                amount = get_amount(wallet_address=wallet_address, proxy=proxy, key=key)

                data = get_data(wallet_address=wallet_address, proxy=proxy, key=key)
                claim_account(
                    account=account,
                    wallet_address=wallet_address,
                    key=key,
                    data=data,
                    web3=web3,
                    amount=amount
                )

                transfer_to_birj(
                    account=account,
                    key=key,
                    deposit_address=deposit_adre,
                    web3=web3
                    )
                return
            except Exception as e:
                logger.error(f'{wallet_address}| к акаунту не подключился:{e}')
                write_error_adres(key=key)


main()
