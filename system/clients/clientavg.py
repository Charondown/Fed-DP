#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 11:20
# @File    : clientavg.py
# @Author  : Richard Yang
import copy
import numpy as np
import time

import torch
import torch.nn as nn

from system.clients.clientbase import ClientBase
from system.utils.priv_utils import *
from system.utils.utils import sparsify


class clientAvg(ClientBase):
    def __init__(self, args, id, train_dataset, label_idxs, **kwargs):
        super().__init__(args, id, train_dataset, label_idxs, **kwargs)
        
        if self.rate > 1:
            self.topk = int(self.data_len / self.rate)
            print("Topk selecting {} dimensions".format(self.topk))
    
    def train(self, client_id, global_round, metrics):
        local_trainloader = self.local_trainloader
        self.model.train()
        
        train_time = time.time()
        
        for local_epoch in range(self.local_epoch):
            acc = 0
            total = 0
            for batch_idx, (images, labels) in enumerate(local_trainloader):
                images, labels = images.to(self.device), labels.to(self.device)
                total += len(labels)
                
                # 预测和计算准确度
                output = self.model(images)
                acc += (output.argmax(1) == labels).type(torch.float).sum().item()
                
                # 计算损失
                loss = self.criterion(output, labels)
                
                # 将梯度初始化为 0，以便批次之间不会混合梯度
                self.optimizer.zero_grad()
                
                # 后向传递错误
                loss.backward()
                
                # 优化参数
                self.optimizer.step()
                
                if batch_idx % 4 == 0:
                    print(
                        '| Client: {:>3} | Global Round: {:>2} | Local Epoch: {:>2} | Process: {:>3.0f}% | Acc: {:>3.0f}% | Loss: {:.3f}'.format(
                            client_id, global_round + 1, local_epoch + 1,
                                       100. * (batch_idx + 1) / len(local_trainloader),
                                       100. * acc / total, loss.item()))
        
        weight = copy.deepcopy(self.model.state_dict())
        weight = self.weight_update(weight)
        flattened = self.process_grad(weight)
        weight_noise = self.add_noise(flattened)
        weight_noise = self.recover_model_shape(weight_noise, self.data_shape)
        
        # save train model time cost
        metrics.client_train_time[client_id][global_round] = time.time() - train_time
        
        return weight_noise
    
    def add_noise(self, flattened):
        if self.rate > 1:
            return (sparsify(flattened, self.topk))
        else:
            return flattened
