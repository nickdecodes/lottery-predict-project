#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : dongqi.zheng@mxplayer.in
@Usage   :
@FileName: lottery.py
@DateTime: 2023/6/11 15:04
@SoftWare: 
"""

# import fire
import time
import math
import random
from itertools import combinations


class Lottery(object):
    # 历史开奖记录文件
    LOTTERY_FILE = 'lottery.csv'
    # 预测号码记录文件
    PREDICT_FILE = 'predict.csv'
    # 前区号码种类数
    FRONT_VOCAB_SIZE = 35
    # 后区号码种类数
    BACK_VOCAB_SIZE = 12
    # 大乐透中奖及奖金规则（没有考虑浮动情况，税前）
    AWARD_RULES = {
        (5, 2): 10000000,
        (5, 1): 800691,
        (5, 0): 10000,
        (4, 2): 3000,
        (4, 1): 300,
        (3, 2): 200,
        (4, 0): 100,
        (3, 1): 15,
        (2, 2): 15,
        (3, 0): 5,
        (2, 1): 5,
        (1, 2): 5,
        (0, 2): 5
    }

    @classmethod
    def read_data_from_file(cls, **kwargs):
        """
        :param kwargs: {
            'file_name': file path
        }
        :return: list
        """
        file_name = kwargs.get('file_name')
        data_list = []
        try:
            with open(file_name, 'r+') as fp:
                print('file name: ', fp.name)
                for line in fp:
                    line = line.strip('\r')
                    line = line.strip('\n')
                    if len(line) > 0:
                        data_list.append(line.split(','))
        except Exception as ex:
            print(ex)
            return None

        print('count: {}'.format(len(data_list)))
        return data_list

    @classmethod
    def write_data_to_file(cls, **kwargs):
        """
        :param kwargs: {
            'file_name': file path
            'data': list
        }
        :return: None
        """
        file_name = kwargs.get('file_name')
        data = kwargs.get('data')
        try:
            with open(file_name, 'a+') as fp:
                fp.write(time.strftime('%Y-%m-%d %H:%M:%S\n'))
                for d in data:
                    fp.write(','.join(str(x) for x in d) + '\n')
        except Exception as ex:
            print("Error occurred while writing data to file: {ex}".format(ex=ex))

    @staticmethod
    def compute_odd_even_ratio(numbers):
        odd_count = sum(1 for num in numbers if num % 2 == 1)  # 统计奇数个数
        even_count = 5 - odd_count  # 计算偶数个数

        ratio = (odd_count, even_count)
        return ratio

    @staticmethod
    def compute_zone_ratio(numbers):
        first_zone_count = 0
        second_zone_count = 0
        third_zone_count = 0

        for num in numbers:
            if 1 <= int(num) <= 12:
                first_zone_count += 1
            elif 12 < int(num) <= 24:
                second_zone_count += 1
            elif 25 <= int(num) <= 35:
                third_zone_count += 1

        # 计算分区个数的最大公约数
        max_common_divisor = math.gcd(first_zone_count, math.gcd(second_zone_count, third_zone_count))

        # 计算分区比值
        first_zone_ratio = first_zone_count // max_common_divisor
        second_zone_ratio = second_zone_count // max_common_divisor
        third_zone_ratio = third_zone_count // max_common_divisor

        zone_ratio = (first_zone_ratio, second_zone_ratio, third_zone_ratio)
        return zone_ratio

    @staticmethod
    def compute_span(numbers):
        min_num = min(numbers)
        max_num = max(numbers)
        span = max_num - min_num
        return span

    @staticmethod
    def compute_numbers_with_remainder(numbers):
        result = []
        for num in numbers:
            result.append(num + 1)
            result.append(num - 1)

        return result

    def get_numbers_with_remainder(self, data=None):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        result = set()
        numbers = [int(x) for x in data[-1][2:7] if (0 < int(x) < 36)]
        for num in numbers:
            result.add(num + 1)
            result.add(num - 1)
        return result

    def get_sum_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        sum_frequency = {}

        for d in data:
            numbers = [int(x) for x in d[2:7]]
            total_sum = sum(numbers)
            sum_frequency[str(total_sum)] = sum_frequency.get(str(total_sum), 0) + 1

        sorted_sums = sorted(sum_frequency.items(), key=lambda x: x[1], reverse=True)
        if output is True:
            # 打印排序结果
            print('结果数量：', len(sorted_sums))
            print("前区总和频率排序（按降序排列）:")
            for total, freq in sorted_sums:
                print("前区总和 {total} 出现次数: {freq}".format(total=total, freq=freq))
        return sorted_sums

    def get_front_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        combination_frequency = {}
        for d in data:
            front_numbers = tuple(int(x) for x in d[2:7])  # 提取前区号码并转换为元组
            if front_numbers in combination_frequency:
                combination_frequency[front_numbers] += 1
            else:
                combination_frequency[front_numbers] = 1

        # 根据频率排序
        sorted_combinations = sorted(combination_frequency.items(), key=lambda x: x[1], reverse=True)

        if output is True:
            # 打印排序结果
            print('结果数量：', len(sorted_combinations))
            print("最后两个数组合频率排序（按降序排列）:")
            for combination, freq in sorted_combinations:
                print("组合 {combination} 出现次数: {freq}".format(combination=combination, freq=freq))
        return sorted_combinations

    def get_back_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        combination_frequency = {}
        for d in data:
            back_numbers = tuple(int(x) for x in d[-2:])  # 提取后区两个数并转换为元组
            if back_numbers in combination_frequency:
                combination_frequency[back_numbers] += 1
            else:
                combination_frequency[back_numbers] = 1

        # 根据频率排序
        sorted_combinations = sorted(combination_frequency.items(), key=lambda x: x[1], reverse=True)

        if output is True:
            # 打印排序结果
            print('结果数量：', len(sorted_combinations))
            print("最后两个数组合频率排序（按降序排列）:")
            for combination, freq in sorted_combinations:
                print("组合 {combination} 出现次数: {freq}".format(combination=combination, freq=freq))
        return sorted_combinations

    def get_odd_even_ratio_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        odd_even_ratio_frequency = {}
        for d in data:
            numbers = [int(x) for x in d[2:7]]  # 获取5个数
            odd_even_ratio = self.compute_odd_even_ratio(numbers)
            if odd_even_ratio in odd_even_ratio_frequency:
                odd_even_ratio_frequency[odd_even_ratio] += 1
            else:
                odd_even_ratio_frequency[odd_even_ratio] = 1

        # 对奇偶比例频率进行排序
        sorted_odd_even_ratios = sorted(odd_even_ratio_frequency.items(), key=lambda x: x[1], reverse=True)

        if output is True:
            # 打印排序结果
            print('结果数量：', len(sorted_odd_even_ratios))
            print("前区的奇偶比例频率（按降序排列）:")
            for odd_even_ratio, count in sorted_odd_even_ratios:
                odd_count, even_count = odd_even_ratio
                print("奇偶比例 {odd_count}:{even_count}: 出现次数 {count}".format(
                    odd_count=odd_count, even_count=even_count, count=count))
        return sorted_odd_even_ratios

    def get_zone_ratio_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        zone_ratio_frequency = {}

        for d in data:
            numbers = [int(x) for x in d[2:7]]  # 获取前区的数字
            zone_ratio = self.compute_zone_ratio(numbers)
            if zone_ratio in zone_ratio_frequency:
                zone_ratio_frequency[zone_ratio] += 1
            else:
                zone_ratio_frequency[zone_ratio] = 1

        # 对分区比值的频率进行排序
        sorted_zone_ratios = sorted(zone_ratio_frequency.items(), key=lambda x: x[1], reverse=True)

        if output is True:
            # 打印排序后的分区比值频率
            print('结果数量：', len(sorted_zone_ratios))
            print("区间比值的频率（按降序排列）:")
            for ratio, frequency in sorted_zone_ratios:
                print("区间比值 {ratio}: 出现次数 {frequency}".format(ratio=ratio, frequency=frequency))
        return sorted_zone_ratios

    def get_span_frequency(self, data=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        span_frequency = {}

        for d in data:
            numbers = [int(x) for x in d[2:7]]  # 获取5个数
            span = self.compute_span(numbers)
            if span in span_frequency:
                span_frequency[span] += 1
            else:
                span_frequency[span] = 1

        # 对差值频率进行排序
        sorted_spans = sorted(span_frequency.items(), key=lambda x: x[1], reverse=True)

        if output is True:
            # 打印排序结果
            print('结果数量：', len(sorted_spans))
            print("前区最大跨度频率（按降序排列）:")
            for span, frequency in sorted_spans:
                print("跨度 {span}: 出现次数 {frequency}".format(span=span, frequency=frequency))
        return sorted_spans

    def predict(self, data=None, backs=None, odd_even_ratios=None, zone_ratios=None, spans=None, output=True):
        if data is None:
            data = self.read_data_from_file(file_name=self.LOTTERY_FILE)
        if backs is None:
            # print(self.get_back_frequency(data=data, output=False))
            backs = [x[0] for x in self.get_back_frequency(data=data, output=False)][:1]
        if odd_even_ratios is None:
            odd_even_ratios = [x[0] for x in self.get_odd_even_ratio_frequency(data=data, output=False)][:1]
        if zone_ratios is None:
            zone_ratios = [x[0] for x in self.get_zone_ratio_frequency(data=data, output=False)][:1]
        if spans is None:
            spans = [x[0] for x in self.get_span_frequency(data=data, output=False)][:1]
        print('后区: {}, 奇偶比: {}, 区间比: {}, 跨度: {}'.format(backs, odd_even_ratios, zone_ratios, spans))

        # 生成前区所有可能的组合
        front_combinations = combinations(range(1, 36), 5)

        # 将历史前区组合存储为集合
        last_front_combinations = set(int(x) for x in data[-1][2:7])
        history_front_combinations = [x[0] for x in self.get_front_frequency(data=data, output=False)]

        # 存储满足条件的组合
        satisfied_combinations = []

        # 遍历所有组合
        for front_comb in front_combinations:
            # 检查奇偶比例是否满足条件
            if self.compute_odd_even_ratio(front_comb) not in odd_even_ratios:
                continue

            # 检查区间比例是否满足条件
            if self.compute_zone_ratio(front_comb) not in zone_ratios:
                continue

            # 检查跨度是否满足条件
            if self.compute_span(front_comb) not in spans:
                continue

            # 检查是否在历史开奖中出现
            if front_comb in history_front_combinations:
                continue

            # 边号:也叫邻号，与上期开出的中奖号码加减余1的号码，不会出现两个以上
            if len(self.get_numbers_with_remainder(data).intersection(set(front_comb))) >= 2:
                continue

            # 本期开奖号码，大概率不会与上一期出现相同号码
            if len(last_front_combinations.intersection(set(front_comb))) >= 1:
                continue

            # 检查其他条件
            if any([
                sum(front_comb) not in range(80, 101),
                26 not in front_comb,
                35 in front_comb
            ]):
                continue

            for back in backs:
                satisfied_combinations.append(front_comb + back)
        if output is True:
            front_multiple = set()
            back_multiple = set()
            for combination in satisfied_combinations:
                print("组合：", combination)
                front_multiple.update(combination[:-2])
                back_multiple.update(combination[-2:])
            print('复式前区: ', front_multiple)
            print('复式后区: ', back_multiple)
        print(len(satisfied_combinations))

        self.write_data_to_file(file_name=self.PREDICT_FILE, data=satisfied_combinations)
        return satisfied_combinations

    def select_random(self):
        random.seed(time.time())
        random_selections = random.sample(self.predict(), 5)
        print(random_selections)
        for combination in random_selections:
            print("随机组合：", combination)


if __name__ == '__main__':
    # fire.Fire(Lottery)
    Lottery().select_random()
