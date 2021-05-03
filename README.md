# Deep_Learning_Classification
In this competition, you are asked to solve the image classification problem for DL20 dataset we have prepared.

To evaluate the performance of your model, you should use the accuracy metric, which is widely used in image classification. However, high accuracy doesn't mean you will get a high score on this project. We will consider the novelty of your project, a poster presentation you will prepare, and many other factors during project period.


## Dataset

* preparations:
  1. Prepare DL20 dataset.
  2. make the folder structure of the dataset as follows:
```
┌── README.md
├── data_loader.py
├── model.py
├── train.py
└── data
    └── DL20
        ├── train
        │   ├── cls0
        │   │   ├── 101.png
        │   │   ├── 134.png
        │   │   └── ...
        │   ├── cls1
        │   └── ...
        ├── valid
        │   ├── cls0
        │   │   ├── 6705.png
        │   │   ├── 6722.png
        │   │   └── ...
        │   ├── cls1
        │   └── ...
        └── test
            ├── 100011.png
            ├── 100196.png
            ├── 100334.png
            └── ...
```

# Quick Start

```bash
CUDA_VISIBLE_DEVICES=0 python3 train.py
```

# About Backbone Network

We provide a simple backbone network, Small-Resnet18. However, you can use any other backbone networks for your problem.
