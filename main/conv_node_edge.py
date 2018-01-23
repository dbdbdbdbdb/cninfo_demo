#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import sys



sys.path.append('source')

from datetime import datetime

from source import translate_dict as td
name_list = ['naturalperson', 'organization', 'securities', 'top10circshareholder', 'top10shareholder']
name1_list = ['naturalperson', 'organization', 'securities']
name2_list = ['top10circshareholder', 'top10shareholder']
event_list = ['assets_frozen', 'assets_restructure', 'company_litigation', 'company_penalty', 'company_arbitration',
              'manager_serve', 'profit_prediction', 'share_capital_change', 'summary_profit_predict']
event_dict = {
    "assets_frozen": "资产冻结",
    "assets_restructure": "资产重组",
    "company_litigation": "公司诉讼",
    "company_penalty": "公司处罚",
    "company_arbitration": "公司仲裁",
    "manager_serve": "管理人员任职",
    "profit_prediction": "盈利预测",
    "share_capital_change": "股本变动",
    "summary_profit_predict": "盈利预测汇总"
}

global json_next
#import re

def to_triples_list(query_result):
    #f = open('sparql_answer.txt', encoding='utf-8')
    #query_result = f.read()
    #如果value中包含\n，eval会出错
    query_result = query_result.replace('\n','')
    # 找到bindings的起始位置
    begin_offset = query_result.find('"bindings":')
    end_offset=query_result.rfind(']')
    #print('offset: ', begin_offset, end_offset)
    try:
        #print(query_result[begin_offset + 14:end_offset+1])
        triples_list = eval(query_result[begin_offset + 14:end_offset+1])
        #print(triples_list)
    except Exception as e:
        print(e)
        return
    # 演示操作.链式操作对应列表-字典-字典-键值对的数据层级.
    # print(triples_list[len(triples_list) - 1]['z']['type'])
    return triples_list

def to_relation_list(query_result):
    #f = open('sparql_answer.txt', encoding='utf-8')
    #query_result = f.read()
    #如果value中包含\n，eval会出错
    query_result = query_result.replace('\n','')
    # 找到bindings的起始位置
    begin_offset = query_result.find('"bindings":')
    end_offset=query_result.rfind(']')
    #print('offset: ', begin_offset, end_offset)
    try:
        #print(query_result[begin_offset + 14:end_offset+1])
        triples_list = eval(query_result[begin_offset + 14:end_offset+1])
        #print(triples_list)
    except Exception as e:
        print(e)
        return
    # 演示操作.链式操作对应列表-字典-字典-键值对的数据层级.
    # print(triples_list[len(triples_list) - 1]['z']['type'])

    nodes_list = []
    # 建立node的set集合,便于用于比较是否存在而去重
    id_set = set()
    # 建立存储边的列表
    edges_list = []
    # 建立汉化词典的键列表
    trans_key_list = list(td.trans_dict.keys())

    for i in triples_list:
        # 对x和y的type进行判断,进而先建立字符串形式的(id,name,category)的节点唯一值set集合
        if i['x1']['type'] == 'uri':
            x_value_splitted_list = i['x1']['value'].split('/')
            if x_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['x1']['value'] + '","name":"' + x_value_splitted_list[5] + '","category":0}')
            elif x_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['x1']['value'] + '","name":"' + x_value_splitted_list[6] + '","category":0}')
            elif x_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['x1']['value'] + '","name":"' + event_dict[x_value_splitted_list[3]] +
                           x_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['x1']['value'] + '","name":"' + i['x1']['value'] + '","category":0}')
        else:
            id_set.add('{"id":"' + i['x1']['value'] + '","name":"' + i['x1']['value'] + '","category":1}')

        if i['z']['type'] == 'uri':
            z_value_splitted_list = i['z']['value'].split('/')
            if z_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[5] + '","category":0}')
            elif z_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[6] + '","category":0}')
            elif z_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + event_dict[z_value_splitted_list[3]] +
                           z_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":0}')
        else:
            id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":1}')

        if i['x2']['type'] == 'uri':
            x_value_splitted_list = i['x2']['value'].split('/')
            if x_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['x2']['value'] + '","name":"' + x_value_splitted_list[5] + '","category":0}')
            elif x_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['x2']['value'] + '","name":"' + x_value_splitted_list[6] + '","category":0}')
            elif x_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['x2']['value'] + '","name":"' + event_dict[x_value_splitted_list[3]] +
                           x_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['x2']['value'] + '","name":"' + i['x2']['value'] + '","category":0}')
        else:
            id_set.add('{"id":"' + i['x2']['value'] + '","name":"' + i['x2']['value'] + '","category":1}')

        # 单条边的属性词典
        edge_dict = {}
        # 边的起点
        edge_dict['source'] = i['x1']['value']
        # if y['z']['type']=='uri':
        #     edge_dict['target']=y['z']['value']
        # 边的终点
        edge_dict['target'] = i['z']['value']
        # 边的描述,直接只取谓词描述
        eng_desc = i['y1']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            edge_dict['value'] = td.trans_dict[eng_desc]
        else:
            edge_dict['value'] = i['y1']['value'].split('/')[4]
        # 将单条边的属性字典加入到边的列表
        edges_list.append(edge_dict)

        # 边的起点
        edge_dict1={}
        edge_dict1['source'] = i['z']['value']
        # if y['z']['type']=='uri':
        #     edge_dict['target']=y['z']['value']
        # 边的终点
        edge_dict1['target'] = i['x2']['value']
        # 边的描述,直接只取谓词描述
        eng_desc = i['y2']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            edge_dict1['value'] = td.trans_dict[eng_desc]
        else:
            edge_dict1['value'] = i['y2']['value'].split('/')[4]
        # 将单条边的属性字典加入到边的列表
        edges_list.append(edge_dict1)

    # 将set元素变为一个个node的dict
    for i in id_set:
        # 每个元素相当于一个词典
        node_dict = eval(i)
        # 将每次循环得到的单个节点加入到节点列表
        nodes_list.append(node_dict)

    return (nodes_list,edges_list)

# 可以加到所有年份的triples(即无时间属性)
def triple_can_add2all(triple_dict, years_list, triples_per_year_dict):
    for i in years_list:
        triples_per_year_dict[i].append(triple_dict)
    return


def triples_sort_by_year(triples_list):
    # 1.根据triples_list建立year的set集合
    years_set = set()
    for i in triples_list:
        # 宾语的type是uri的话,才进入取日期的流程
        if i['z']['type'] == 'uri':
            # 将宾语z的value分割,输出列表
            z_value_splitted_list = i['z']['value'].split('/')
            # 测试:打印分割出来的列表
            # print(z_value_splitted_list)
            # 列表长度大于5,判定在uri中追加了日期
            if z_value_splitted_list[3] not in name1_list and len(z_value_splitted_list) > 5:
                # 将字符串变成时间
                z_date = datetime.strptime(z_value_splitted_list[5], '%Y-%m-%d')
                # 取出date中的year值(int类型),转为字符串,添加到set集合中
                years_set.add(str(z_date.year))

    # 将集合改为列表,并进行排序
    years_list = list(years_set)
    years_list.sort()
    # 2.按照年份分成不同的triple组别
    # 建立(年份:三元组列表)的键值对应词典
    triples_per_year_dict = {}
    for i in years_list:
        triples_per_year_dict[i] = []

    for i in triples_list:
        if i['z']['type'] == 'uri':
            # 将宾语z的value分割,输出列表
            z_value_splitted_list = i['z']['value'].split('/')
            # 测试:打印分割出来的列表
            # print(z_value_splitted_list)
            # 列表长度大于5,判定在uri中追加了日期
            if z_value_splitted_list[3] not in name1_list and len(z_value_splitted_list) > 5:
                # 将字符串变成时间
                z_date = datetime.strptime(z_value_splitted_list[5], '%Y-%m-%d')
                # 取出date中的year值(int类型),转为字符串,对应(年份:三元组列表)的键值对应词典的key值进行添加
                triples_per_year_dict[str(z_date.year)].append(i)
            else:
                triple_can_add2all(i, years_list, triples_per_year_dict)
        else:
            triple_can_add2all(i, years_list, triples_per_year_dict)
    return triples_per_year_dict


def find_edges(triples_list):
    # 建立存储边的列表
    edges_list = []
    # 建立汉化词典的键列表
    trans_key_list = list(td.trans_dict.keys())
    for i in triples_list:
        # 单条边的属性词典
        edge_dict = {}
        # 边的起点
        edge_dict['source'] = i['x']['value']
        # if y['z']['type']=='uri':
        #     edge_dict['target']=y['z']['value']
        # 边的终点
        edge_dict['target'] = i['z']['value']
        # 边的描述,直接只取谓词描述
        eng_desc = i['y']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            edge_dict['value'] = td.trans_dict[eng_desc]
        else:
            edge_dict['value'] = i['y']['value'].split('/')[4]
        # 将单条边的属性字典加入到边的列表
        edges_list.append(edge_dict)
    return edges_list


def find_nodes(triples_list):
    # 建立存储节点的列表
    nodes_list = []
    # 建立node的set集合,便于用于比较是否存在而去重
    id_set = set()
    for i in triples_list:
        # 对x和y的type进行判断,进而先建立字符串形式的(id,name,category)的节点唯一值set集合
        if i['x']['type'] == 'uri':
            x_value_splitted_list = i['x']['value'].split('/')
            if x_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + x_value_splitted_list[5] + '","category":0}')
            elif x_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + x_value_splitted_list[6] + '","category":0}')
            elif x_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + event_dict[x_value_splitted_list[3]] +
                           x_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + i['x']['value'] + '","category":0}')

        if i['z']['type'] == 'uri':
            z_value_splitted_list = i['z']['value'].split('/')
            if z_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[5] + '","category":0}')
            elif z_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[6] + '","category":0}')
            elif z_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + event_dict[z_value_splitted_list[3]] +
                           z_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":0}')
        else:
            id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":1}')
    # 将set元素变为一个个node的dict
    for i in id_set:
        # 每个元素相当于一个词典
        node_dict = eval(i)
        # 将每次循环得到的单个节点加入到节点列表
        nodes_list.append(node_dict)
    return nodes_list

def pfind_nodes_edges(triples_list):
    # 建立存储边的列表
    edges_list = []
    edges_new_list = []
    edge_judge_list=[]
    flagmore={}
    # 建立汉化词典的键列表
    trans_key_list = list(td.trans_dict.keys())
    # 建立存储节点的列表
    nodes_list = []
    nodes_new_list = []
    # 建立node的set集合,便于用于比较是否存在而去重
    id_set = set()
    id_new_set=set()

    for i in triples_list:
        eng_desc = i['y']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            tmp = td.trans_dict[eng_desc]
        else:
            tmp = i['y']['value'].split('/')[4]
        if tmp not in edge_judge_list:
            edge_judge_list.append(tmp)
            flagmore[tmp] = False
        else:
            flagmore[tmp]=True
    for i in triples_list:
        # 单条边的属性词典
        edge_dict = {}
        edge_new_dict={}
        # 对x和y的type进行判断,进而先建立字符串形式的(id,name,category)的节点唯一值set集合
        if i['x']['type'] == 'uri':
            x_value_splitted_list = i['x']['value'].split('/')
            if x_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + x_value_splitted_list[5] + '","category":0}')
            elif x_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + x_value_splitted_list[6] + '","category":0}')
            elif x_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + event_dict[x_value_splitted_list[3]] +
                           x_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['x']['value'] + '","name":"' + i['x']['value'] + '","category":0}')

        # 边的起点
        edge_dict['source'] = i['x']['value']
        # if y['z']['type']=='uri':
        #     edge_dict['target']=y['z']['value']
        # 边的终点
        edge_dict['target'] = i['z']['value']
        # 边的描述,直接只取谓词描述
        eng_desc = i['y']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            edge_dict['value'] = td.trans_dict[eng_desc]
        else:
            edge_dict['value'] = i['y']['value'].split('/')[4]

        if(flagmore[edge_dict['value']])==True:
            edge_dict['target'] = edge_dict['value']
            id_set.add('{"id":"' +  edge_dict['value'] + '","name":"' + edge_dict['value'] + '","category":2}')
            id_new_set.add('{"id":"' + edge_dict['value'] + '","name":"' + edge_dict['value'] + '","category":2}')
            #为了类别具体展开，构造数据
            if i['z']['type'] == 'uri':

                z_value_splitted_list = i['z']['value'].split('/')
                if z_value_splitted_list[3] in name1_list:

                    id_new_set.add(
                        '{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[5] + '","category":0}')
                elif z_value_splitted_list[3] in name2_list:

                    id_new_set.add(
                        '{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[6] + '","category":0}')
                elif z_value_splitted_list[3] in event_list:

                    id_new_set.add('{"id":"' + i['z']['value'] + '","name":"' + event_dict[z_value_splitted_list[3]] +
                               z_value_splitted_list[4] + '","category":0}')
                else:

                    id_new_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":0}')
            else:
                id_new_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":1}')
            edge_new_dict['source'] = edge_dict['value']
            # if y['z']['type']=='uri':
            #     edge_dict['target']=y['z']['value']
            # 边的终点
            edge_new_dict['target'] = i['z']['value']
            edge_new_dict['value']=edge_dict['value']
            edges_new_list.append(edge_new_dict)
        else:
            if i['z']['type'] == 'uri':

                z_value_splitted_list = i['z']['value'].split('/')
                if z_value_splitted_list[3] in name1_list:

                    id_set.add(
                        '{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[5] + '","category":0}')
                elif z_value_splitted_list[3] in name2_list:

                    id_set.add(
                        '{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[6] + '","category":0}')
                elif z_value_splitted_list[3] in event_list:

                    id_set.add('{"id":"' + i['z']['value'] + '","name":"' + event_dict[z_value_splitted_list[3]] +
                               z_value_splitted_list[4] + '","category":0}')
                else:

                    id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":1}')

        edges_list.append(edge_dict)

    for i in id_set:
        # 每个元素相当于一个词典
        node_dict = eval(i)
        # 将每次循环得到的单个节点加入到节点列表
        nodes_list.append(node_dict)
        # 将set元素变为一个个node的dict
    for i in id_new_set:
        # 每个元素相当于一个词典
        node_new_dict = eval(i)
        # 将每次循环得到的单个节点加入到节点列表
        nodes_new_list.append(node_new_dict)
    extend_dict = {}
    extend_dict['data'] = nodes_new_list
    extend_dict['links'] = edges_new_list
    #json_extend = json.dumps(extend_dict)

    return (nodes_list,edges_list,extend_dict)



def conv2graph_dict(nodes_list, edges_list):
    dl_per_year_dict = {}
    dl_per_year_dict['data'] = nodes_list
    dl_per_year_dict['links'] = edges_list


    return dl_per_year_dict
    # json_str = json.dumps(dl_dict)
    # return json_str


def conv2graph(answer):
    # with open('aaa.txt', 'r', encoding='utf-8') as f:
    #     answer = f.read()
    triples_list = to_triples_list(answer)
    #print(triples_list)
    triples_per_year_dict = triples_sort_by_year(triples_list)
    #print(triples_per_year_dict)
    dls_per_year_dict = {}
    # 分开每年对应的triples中的data和links
    for i in triples_per_year_dict:
        edges_list = find_edges(triples_per_year_dict[i])
        nodes_list = find_nodes(triples_per_year_dict[i])
        dl_per_year_dict = conv2graph_dict(nodes_list, edges_list)
        dls_per_year_dict[i] = dl_per_year_dict
    json_str = json.dumps(dls_per_year_dict)
    return json_str

def conv2pgraph(answer):
    # with open('aaa.txt', 'r', encoding='utf-8') as f:
    #     answer = f.read()
    triples_list = to_triples_list(answer)
    #print(triples_list)
    triples_per_year_dict = triples_sort_by_year(triples_list)
    #print(triples_per_year_dict)
    dls_per_year_dict = {}
    # 分开每年对应的triples中的data和links
    for i in triples_per_year_dict:
        #nodes_list = find_nodes(triples_per_year_dict[i])
        global json_next
        (nodes_list,edges_list,json_next) = pfind_nodes_edges(triples_per_year_dict[i])
        json_next=json.dumps(json_next)
        dl_per_year_dict = conv2graph_dict(nodes_list, edges_list)
        dls_per_year_dict[i] = dl_per_year_dict
    json_str = json.dumps(dls_per_year_dict)
    return json_str
def getJsonNext():
    global json_next
    return json_next

def plus2graph(answer, data_id):
    triples_list = to_triples_list(answer)
    edges_list = []
    trans_key_list = list(td.trans_dict.keys())
    if triples_list is None:
        return
    for i in triples_list:
        # 单条边的属性词典
        edge_dict = {}
        # 边的起点
        # 这里之后是变量
        edge_dict['source'] = data_id
        # if y['z']['type']=='uri':
        #     edge_dict['target']=y['z']['value']
        # 边的终点
        edge_dict['target'] = i['z']['value']
        # 边的描述,直接只取谓词描述
        eng_desc = i['y']['value']
        # 判断英文描述是否在key中.
        if eng_desc in trans_key_list:
            edge_dict['value'] = td.trans_dict[eng_desc]
        else:
            edge_dict['value'] = i['y']['value'].split('/')[4]
        # 将单条边的属性字典加入到边的列表
        edges_list.append(edge_dict)
    nodes_list = []
    # 建立node的set集合,便于用于比较是否存在而去重
    id_set = set()
    # 这里之后是变量
    data_id_splitted_list = data_id.split('/')
    if data_id_splitted_list[3] in name1_list:
        id_set.add('{"id":"' + data_id + '","name":"' + data_id_splitted_list[5] + '","category":0}')
    elif data_id_splitted_list[3] in name2_list:
        id_set.add('{"id":"' + data_id + '","name":"' + data_id_splitted_list[6] + '","category":0}')
    elif data_id_splitted_list[3] in event_list:
        id_set.add('{"id":"' + data_id + '","name":"' + event_dict[data_id_splitted_list[3]] +
                   data_id_splitted_list[4] + '","category":0}')
    else:
        id_set.add('{"id":"' + data_id + '","name":"' + i['x']['value'] + '","category":0}')
    # id_set.add(
    #     '{"id":"' + data_id + '","name":"' + 'http://cn.info/securities/810' + '","category":0}')
    for i in triples_list:
        # 对z的type进行判断,进而先建立字符串形式的(id,name,category)的节点唯一值set集合
        if i['z']['type'] == 'uri':
            z_value_splitted_list = i['z']['value'].split('/')
            if z_value_splitted_list[3] in name1_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[5] + '","category":0}')
            elif z_value_splitted_list[3] in name2_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + z_value_splitted_list[6] + '","category":0}')
            elif z_value_splitted_list[3] in event_list:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + event_dict[z_value_splitted_list[3]] +
                           z_value_splitted_list[4] + '","category":0}')
            else:
                id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":0}')
        else:
            id_set.add('{"id":"' + i['z']['value'] + '","name":"' + i['z']['value'] + '","category":1}')

    # 将set元素变为一个个node的dict
    for i in id_set:
        # 每个元素相当于一个词典
        node_dict = eval(i)
        # 将每次循环得到的单个节点加入到节点列表
        nodes_list.append(node_dict)
    plus_dict = {}
    plus_dict['data'] = nodes_list
    plus_dict['links'] = edges_list
    json_plus = json.dumps(plus_dict)
    return json_plus


