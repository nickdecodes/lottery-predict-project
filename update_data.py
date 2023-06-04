#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: update_data.py
@DateTime: 2023/6/4 15:28
@SoftWare:
"""

import requests
import settings

print('开始尝试从 {} 获取最新的大乐透数据...'.format(settings.LOTTO_DOWNLOAD_URL))
try:
    resp = requests.get(settings.LOTTO_DOWNLOAD_URL)
    if resp.status_code == 200:
        # 解析数据，查看数据集中最新的数据期数
        lines = resp.content.decode('utf-8').split('\n')
        index = lines[0].replace('"', '').split(',')[0]
        print('获取成功！开始更新文件...')
        with open(settings.DATASET_PATH, 'wb') as f:
            f.write(resp.content)
        print('完成！当前最新期数为{}期，请确认期数是否正确！'.format(index))
    else:
        raise Exception('获取数据失败！')
except Exception as e:
    print(e)
