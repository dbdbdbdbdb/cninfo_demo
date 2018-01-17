#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys

sys.path.append('main')
from main import query

app = Flask(__name__, static_folder='static', static_url_path='/static')


# routes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        str_to_solve = request.form.get('str_to_solve')
        search_type = request.form.get('search_type')
        select_object = request.form.get('select')
        if search_type == 'search1':
            json_str = query.entity_search(str_to_solve)
            return json_str
        if search_type == 'plus':
            json_plus = query.plus_search(str_to_solve)
            return json_plus
        if search_type=='search2':
            print(str_to_solve, select_object)
            json_list=query.template_search(str_to_solve, select_object)
            # print(json_list)
            return json_list
        if search_type=='search3':
            entity_1 = request.form.get('entity1')
            entity_2 = request.form.get('entity2')
            json_list=query.relation_search(entity_1, entity_2)
            return json_list
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


