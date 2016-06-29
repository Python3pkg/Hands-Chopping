#!usr/bin/env python
import webbrowser
from colorama import Fore
from prettytable import PrettyTable
from utils.message import colorful_text, error_message
from goods_threads import thread_pool


# TABLE_TITLE = ('编号', '简介', '价格', '邮费', '购买人数', '所属')
# ITEM_KEY = ('index', 'intro', 'price', 'delivery', 'sales', 'belong')
TABLE_TITLE = ('简介', '价格', '邮费', '购买人数', '所属')
ITEM_KEY = ('intro', 'price', 'delivery', 'sales', 'belong')


def get_goods(goods_keywords):
    """get keywords and search

    :param goods_keywords: input keywords
    :return: None
    """
    assert isinstance(goods_keywords, list)
    key_words = '+'.join(goods_keywords)
    thread_pool.build_thread(key_words)
    print_goods(thread_pool.export_date())


def print_goods(search_result):
    """use validate search result to print a table

    :param search_result: search result in taobao and jd
    :return: None
    """
    goods_table = PrettyTable(TABLE_TITLE)
    for goods in search_result:
        goods_row = [goods[item] for item in ITEM_KEY]
        goods_table.add_row(goods_row)
    print(colorful_text('ready to hands chopping?', Fore.CYAN))
    print(goods_table)


def open_detail_page(filtered_goods):
    """expect a number or a string which joined by ','
    to open the target goods url in a browser window

    :param filtered_goods
    :return: None
    """
    print(colorful_text('which do you prefer? type it\'s index', Fore.MAGENTA))
    print(colorful_text('if many, use \',\' to split them', Fore.MAGENTA))
    try:
        index = input('goods index: ')
        result_goods = filter(get_target_goods(index.split(',')), filtered_goods)
        goods_list = [goods for goods in result_goods]

        if len(goods_list):
            for goods in goods_list:
                goods_url = goods["url"]
                if goods_url[0] == '/':
                    goods_url = 'https:{}'.format(goods_url)
                webbrowser.open_new(goods_url)
        else:
            error_message('no such index')
            open_detail_page(filtered_goods)
    except KeyboardInterrupt:
        error_message('exit')


def get_target_goods(indexs):
    """search in filtered_goods by user's input indexs

    :param indexs: user's input indexs
    :return: if is validate
    """
    def filter_goods(goods):
        return str(goods["index"]) in indexs
    return filter_goods
