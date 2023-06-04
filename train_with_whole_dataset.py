#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   : 使用全部数据集进行训练
@FileName: train_with_whole_dataset.py
@DateTime: 2023/6/4 15:28
@SoftWare:
"""

import os
from models import model
from dataset import LottoDataSet
import settings

# 初始化数据集
lotto_dataset = LottoDataSet(train_data_rate=1)
# 创建保存权重的文件夹
if not os.path.exists(settings.CHECKPOINTS_PATH):
    os.mkdir(settings.CHECKPOINTS_PATH)
# 开始训练
model.fit(lotto_dataset.train_np_x, lotto_dataset.train_np_y, batch_size=settings.BATCH_SIZE, epochs=settings.EPOCHS)
# 保存模型
model.save_weights('{}/model_checkpoint_x'.format(settings.CHECKPOINTS_PATH))
