#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 15:45
# @File    : generate_mnist.py
# @Author  : Richard Yang

import torch
from torchvision import datasets, transforms

from utils.dataset_util import balanced_iid, shard_noniid, unbanlanced_shard_noniid


def mnist_100(dataiid, num_clients):
    print('------start mnist format------')
    
    mnist = datasets.MNIST(
        root='local_dataset/', train=True, download=True,
        transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    )
    
    dir_path = 'formatdata/mnist/'
    # num_classes = 10
    # num_shards = 200
    # num_imgs = 300
    
    if dataiid == 1:
        client = balanced_iid(dir_path, mnist, num_clients, num_classes=10)
        print('-----------------finished mnist iid-balanced-----------------')
        print(f'client[0]: \n {client[0]}  \n length: {len(client[0])} \n type: {type(client[0])}')
        print(f'client[1]: \n {client[1]}  \n length: {len(client[1])} \n type: {type(client[1])}')
    elif dataiid == 2:
        print('not exist unbalanced-iid')
    elif dataiid == 3:
        client = shard_noniid(dir_path, mnist, num_clients, num_shards=200, num_imgs=300)
        print('-----------------finished mnist noniid-shard-----------------')
        print(f'client[0]: \n {client[0]}  \n length: {len(client[0])} \n type: {type(client[0])}')
        print(f'client[1]: \n {client[1]}  \n length: {len(client[1])} \n type: {type(client[1])}')
    elif dataiid == 4:
        client = unbanlanced_shard_noniid(dir_path, mnist, num_clients, num_shards=1200, num_imgs=50)
        print('-----------------finished mnist noniid-unbalanced-shard-----------------')
        print(f'client[0]: \n {client[0]}  \n length: {len(client[0])} \n type: {type(client[0])}')
        print(f'client[1]: \n {client[1]}  \n length: {len(client[1])} \n type: {type(client[1])}')
    else:
        print('dataformat iid = [1,2,3], generate dataformat [balanced_iid, shard_noniid, unbanlanced_shard_noniid]')


if __name__ == "__main__":
    # mnist_100(1, 100)
    # mnist_100(3, 100)
    mnist_100(4, 100)
