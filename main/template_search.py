'''
Created on 2017年7月26日

@author: txl
'''






sparql=''
# 股本变动
# 公司的股本变动情况？
# select ?x ?y ?z
# where{
# ?orgID <http://cn.info/vocab/organization_ORGNAME> sparqlquery1.
# ?orgID <http://cn.info/vocab/has_share_capital_change> ?x.
# ?x ?y ?z
# }
def sparqlquery1(value1):
    sparqlquery = []
    sparqlquery.append('select ?x ?y ?z')
    sparqlquery.append('\n where')
    sparqlquery.append('\n{?orgID <http://cn.info/vocab/organization_ORGNAME> "')
    sparqlquery.append(str(value1))
    sparqlquery.append('" .\n?orgID <http://cn.info/vocab/has_share_capital_change> ?x.')
    sparqlquery.append('\n?x ?y ?z')
    sparqlquery.append('\n}')
    return (''.join(sparqlquery))


# 公司的受处罚情况
# 公司的受处罚情况？
# select ?x ?y ?z
# where{
# ?orgID <http://cn.info/vocab/organization_ORGNAME> sparqlquery1.
# ?orgID <http://cn.info/vocab/has_penalty> ?x.
# ?x ?y ?z
# }
def sparqlquery2(value1):
    sparqlquery = []
    sparqlquery.append('select ?x ?y ?z')
    sparqlquery.append('\n where')
    sparqlquery.append('\n{?orgID <http://cn.info/vocab/organization_ORGNAME> "')
    sparqlquery.append(str(value1))
    sparqlquery.append('".\n?orgID <http://cn.info/vocab/has_penalty> ?x.')
    sparqlquery.append('\n?x ?y ?z')
    sparqlquery.append('\n}')
    return (''.join(sparqlquery))


# 公司的法律纠纷（公司诉讼）有哪些？
# 公司的法律纠纷（公司诉讼）有哪些？---company_litigation
# select ?x ?y ?z
# where{
# ?orgID <http://cn.info/vocab/organization_ORGNAME> sparqlquery1.
# ?orgID <http://cn.info/vocab/has_litigation> ?x.
# ?x ?y ?z
# }
def sparqlquery3(value1):
    sparqlquery = []
    sparqlquery.append('select ?x ?y ?z')
    sparqlquery.append('\n where')
    sparqlquery.append('\n{?orgID <http://cn.info/vocab/organization_ORGNAME> "')
    sparqlquery.append(str(value1))
    sparqlquery.append('".\n?orgID <http://cn.info/vocab/has_litigation> ?x.')
    sparqlquery.append('\n?x ?y ?z')
    sparqlquery.append('\n}')
    return (''.join(sparqlquery))


#
# 公司的证券代码是多少？
# select ?z
# where
# {
# ?orgID <http://cn.info/vocab/organization_ORGNAME> sparqlquery1.
# ?orgID <http://cn.info/vocab/has_securities_published> ?securityID .
# ?securityID <http://cn.info/vocab/securities_SECURITIESCODE> ?z.
# }
def sparqlquery4(value1):
    sparqlquery = []
    sparqlquery.append('select ?z')
    sparqlquery.append('\n where')
    sparqlquery.append('\n{?orgID <http://cn.info/vocab/organization_ORGNAME> "')
    sparqlquery.append(str(value1))
    sparqlquery.append('".\n?orgID <http://cn.info/vocab/has_securities_published> ?securityID .')
    sparqlquery.append('\n?securityID <http://cn.info/vocab/securities_SECURITIESCODE> ?z.')
    sparqlquery.append('\n}')
    return (''.join(sparqlquery))


# 公司的管理人员是谁？
# select ?z
#     where
#     {
#         ?orgID <http://cn.info/vocab/organization_ORGNAME> sparqlquery1.
#         ?orgID <http://cn.info/vocab/has_people_served> ?manager_serve_id.
#         ?manager_serve_id <http://cn.info/vocab/manager_serve_PERSONNAME> ?z.
#         ?manager_serve_id <http://cn.info/vocab/manager_serve_WHETHERONJOB> ?isValid.
#         FILTER (?isValid='1')
#     }
def sparqlquery5(value1):
    sparqlquery = []
    sparqlquery.append('select distinct ?z')
    sparqlquery.append('\n where')
    sparqlquery.append('\n{?orgID <http://cn.info/vocab/organization_ORGNAME> "')
    sparqlquery.append(str(value1))
    sparqlquery.append('".\n?orgID  <http://cn.info/vocab/has_people_served> ?manager_serve_id.')
    sparqlquery.append('\n?manager_serve_id <http://cn.info/vocab/manager_serve_PERSONNAME> ?z.')
    sparqlquery.append('\n?manager_serve_id <http://cn.info/vocab/manager_serve_WHETHERONJOB> ?isValid.')
    sparqlquery.append("\nFILTER (?isValid='1') ")
    sparqlquery.append('\n}')
    return (''.join(sparqlquery))


# print(sparqlquery5('公司的管理人员是谁？'))
