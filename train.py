import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
from torch.utils.data import DataLoader

from model import *
from data_loader import LoadDataset



data_cfgs = {"name": "DL20", "num_classes": 20, "dir":"./data/DL20"}
train_cfgs = {"batch_size": 32, "lr": 0.0002, "total_epoch":20}

### load small version of ResNet
model = Small_ResNet(BasicBlock, [3, 3, 3], num_classes=data_cfgs['num_classes']).to('cuda')

### load train/valid/test dataset
train_dataset = LoadDataset(data_cfgs["dir"], mode="train", random_flip=True)
valid_dataset = LoadDataset(data_cfgs["dir"], mode="valid", random_flip=False)
test_dataset = LoadDataset(data_cfgs["dir"], mode="test", random_flip=False)

### warp dataset using dataloader
train_dataloader = DataLoader(train_dataset, batch_size=train_cfgs["batch_size"], shuffle=True, pin_memory=True, drop_last=True)
valid_dataloader = DataLoader(valid_dataset, batch_size=train_cfgs["batch_size"], shuffle=False, pin_memory=True, drop_last=False)
test_dataloader = DataLoader(test_dataset, batch_size=train_cfgs["batch_size"], shuffle=False, pin_memory=True, drop_last=False)

### define Adam optimizer: one of the popular optimizers in Deep Learning community
optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), train_cfgs["lr"], eps=1e-6)

### define cross-entropy loss for classification
criterion = nn.CrossEntropyLoss()


####################################################################################################
### Start training ###
print("Start Training")
model.train()
step, epoch, valid_logging = 0, 0, False
train_iter = iter(train_dataloader)
while epoch <= train_cfgs["total_epoch"]:
    model.train()
    optimizer.zero_grad()
    try:
        images, labels = next(train_iter)
        valid_logging = False
        step += 1
    except StopIteration:
        train_iter = iter(train_dataloader)
        images, labels = next(train_iter)
        valid_logging = True
        step += 1
        epoch += 1

    images, labels = images.to('cuda'), labels.to('cuda')
    logits = model(images)
    loss = criterion(logits, labels)

    loss.backward()
    optimizer.step()
    if step % 100 == 0:
        print("Step: {step} \t Loss: {loss}".format(step=step, loss=loss.item()))

    if valid_logging:
        correct, total = 0, 0
        model.eval()
        with torch.no_grad():
            for images, labels in iter(valid_dataloader):
                images, labels = images.to('cuda'), labels.to('cuda')
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print('\nAccuracy of the network on the {num_test} valid images: \
              {acc}'.format(num_test=len(valid_dataset), acc=100*correct/total))
