
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

# import os
sys.path.append('gstore_api')
import conv_node_edge
import conv_table
from gstore_api.GstoreConnector import GstoreConnector
import template_search as ts
import json

def entity_search(str):
    # 长于四个字,认为是机构
    if len(str) > 4:
        sparql = 'select ?x ?y ?z\n{\n\t?x <http://cn.info/vocab/organization_ORGNAME> "' + str + '".\n\t?x ?y ?z.\n}'
    else:
        sparql = 'select ?x ?y ?z\n{\n\t?x <http://cn.info/vocab/naturalperson_PERSONNAME> "' + str + '".\n\t?x ?y ?z.\n}'
    # print(sparql)
    answer = query_result(sparql)
    # with open('search1_result.txt', 'r', encoding='utf-8') as f:
    #     answer = f.read()
    # os.remove(os.path.dirname(os.path.abspath(__file__))+'\\search1_result.txt')
    #print(answer)
    json_str = conv_node_edge.conv2pgraph(answer)
    #print(json_str)
    # with open('search1_result.txt', 'w', encoding='utf-8') as f:
    #     f.write(json_str)
    return json_str


def query_result(sparql):
    gc = GstoreConnector('127.0.0.1', 3305)
    #gc = GstoreConnector('172.31.222.93', 3305)
    # 如果未提前加载数据库,则取消下行代码注释
    gc.load('cninfo')

    # # sparql = '''select ?x ?y ?z
    # # {
    # #     ?x <http://cn.info/vocab/organization_ORGNAME> "南华生物医药股份有限公司".
    # #     ?x ?y ?z.
    # # }'''
    # sparql = '''select ?y ?z{
    #     <http://cn.info/securities/810> ?y ?z.
    # }'''
    # 因为最后一行是NUT字符,所以切片掉
    answer = (gc.query(sparql))
    #print(answer)
    
    # print(answer)
    with open('search1_result.txt', 'w', encoding='utf-8') as f:
        f.write(answer)
    return answer


def plus_search(data_id):
    sparql = 'select ?y ?z\n{\n\t<' + data_id + '> ?y  ?z.\n}'
    answer = query_result(sparql)
    json_plus = conv_node_edge.plus2graph(answer, data_id)
    return json_plus

def extend_search(data_id):
    sparql = 'select ?y ?z\n{\n\t<' + data_id + '> ?y  ?z.\n}'
    answer = query_result(sparql)
    json_plus = conv_node_edge.extend2graph(data_id)
    return json_plus

# answer = entity_search("南华生物医药股份有限公司")
# with open('results_end.txt', 'w', encoding='utf-8') as f:
#     f.write(answer)
def template_search(str_to_solve, select_object):
    sparql=''
    if select_object=='securityID':
        sparql = ts.sparqlquery4(str_to_solve)
    elif select_object=='penalty':
        sparql = ts.sparqlquery2(str_to_solve)
    elif select_object=='lawsuit':
        sparql = ts.sparqlquery3(str_to_solve)
    elif select_object=='manager':
        sparql = ts.sparqlquery5(str_to_solve)
    elif select_object=='capitalchange':
        sparql = ts.sparqlquery1(str_to_solve)
    elif select_object=='presentative':
        sparql = ts.sparqlquery6(str_to_solve)
    answer=query_result(sparql)
    #with open('sparql_answer.txt', 'w', encoding='utf-8') as f:
    #    f.write(answer)
    answer_list=conv_node_edge.to_triples_list(answer)
    #conv_table.group2table(answer_list)
    if answer_list:
        json_list=conv_table.conv2table(answer_list)
        json_list=json.dumps(json_list)
        return json_list
    else:
        return json.dumps([])

# print(template_search('公司的证券号是多少？'))
# template_search('南华生物医药股份有限公司的证券号是多少')
def getJsonNext():
    tmp=conv_node_edge.getJsonNext()
    return tmp

def relation_search(entity1, entity2):
    #entity1和entity2都是公司
    if len(entity1)>4 and len(entity2)>4:
        pred1 = '<http://cn.info/vocab/organization_ORGNAME>'
        pred2 = '<http://cn.info/vocab/organization_ORGNAME>'
    #entity1是公司，entity2是个人
    elif len(entity1)>4 and len(entity2)<=4:
        pred1 = '<http://cn.info/vocab/organization_ORGNAME>'
        pred2 = '<http://cn.info/vocab/naturalperson_PERSONNAME>'
    #entity1是个人，entity2是公司
    elif len(entity1)<=4 and len(entity2)>4:
        pred1 = '<http://cn.info/vocab/naturalperson_PERSONNAME>'
        pred2 = '<http://cn.info/vocab/organization_ORGNAME>'
    #entity1和entity2都是个人
    else:
        pred1 = '<http://cn.info/vocab/naturalperson_PERSONNAME>'
        pred2 = '<http://cn.info/vocab/naturalperson_PERSONNAME>'
    sparql='select ?x1 ?y1 ?z ?y2 ?x2\n' + \
               '{\n' + \
               '\t?x1 ' + pred1 + ' "' + entity1 + '".\n' + \
               '\t?x2 ' + pred2 + ' "' + entity2 + '".\n' + \
               '\t?x1 ?y1 ?z.\n' + \
               '\t?z ?y2 ?x2.\n}'
    answer = query_result(sparql)
    (nodes,links) = conv_node_edge.to_relation_list(answer)
    data_dict = conv_node_edge.conv2graph_dict(nodes, links)
    json_list = json.dumps(data_dict)
    return json_list
