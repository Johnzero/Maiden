# encoding: utf-8

"""
Created by Xero 2012-12-08.
"""

from datetime import date, timedelta
from flask import Blueprint, url_for, redirect, g, \
                flash, request, current_app, render_template,\
                send_from_directory, views, session,jsonify,Flask
from flask.ext.login import login_required, current_user
from ..extensions import db
from ..Models import *
from flask.ext.xmlrpc import XMLRPCHandler, Fault
from ..helper import to_timestamp

sale_view = Blueprint('sale_view', __name__, url_prefix='/sale')
sale_view_sale = Blueprint('sale_view_sale', __name__, url_prefix='/sub_sale')
sale_product = Blueprint('sale_product', __name__, url_prefix='/sub_produce')
sale_partner = Blueprint('sale_partner', __name__, url_prefix='/sub_partner')

@sale_view.route('/')
@login_required
def bp_main():
    td = timedelta(days=1)
    #if current_user.system:
    info = AmountDivision.query.filter_by(date=date.today()-td).order_by(AmountDivision.source.desc())
    recaps = DailyRecap.query.all()
        
    all_amount = 0
    for i in info:
        all_amount = all_amount + i.amount
    
    return render_template('biindex.html', all_amount=all_amount, info=info, recaps=recaps)

@sale_view_sale.route("/amount/division")
@login_required
def amount_division():
    """销售总体趋势"""
    return render_template('sale/amount_division.html')

@sale_view_sale.route("/amount/division/data")
@login_required
def amount_division_data():
    result = None
    if current_user.system:
        result = AmountDivision.query.filter_by(system=current_user.system)
    else:
        result = AmountDivision.query.all()
    
    data = dict()
    for item in result:
        if data.has_key(item.source):
            data[item.source]['data'].append([to_timestamp(item.date), item.amount])
        else:
            data[item.source] = {'name': item.source, 'data':[[to_timestamp(item.date), item.amount]]}
    
    json_data = [data[d] for d in data if '事业部' in d]
    
    return jsonify(result=json_data)

def get_month_data():
    result = None
    if current_user.system:
        result = AmountDivision.query.filter_by(system=current_user.system).group_by(
            AmountDivision.month, AmountDivision.source).order_by(AmountDivision.date)
    else:
        result = AmountDivision.query.group_by(
            AmountDivision.month, AmountDivision.source).order_by(AmountDivision.date)
        
    return result


@sale_view_sale.route("/amount/division/month")
@login_required
def amount_month():
    """月度销售趋势"""
    return render_template('sale/amount_division_month.html')


@sale_view_sale.route("/amount/division/month/data")
@login_required
def amount_division_month_data():
    result = get_month_data()
    data = {}

    for item in result:
        if data.has_key(item.source):
            data[item.source]['data'].append([to_timestamp(item.date), item.amount])
        else:
            data[item.source] = {'name': item.source, 'data':[[to_timestamp(item.date), item.amount]]}
    
    json_data = [data[d] for d in data if '事业部' in d]
            
    return jsonify(result=json_data)

@sale_view_sale.route("/amount/year")
@login_required
def amount_year():
    """年度销售对比"""
    return render_template('sale/amount_year.html')


@sale_view_sale.route("/amount/year/data")
@login_required
def amount_year_data():
    result = get_month_data()
    
    data = {}
    
    plastic_data = dict()
    glass_data = dict()
    vacuume_data = dict()
    he_data = dict()
    
    def _append_data(data, item):
        if data.has_key(item.year):
            data[item.year]['data'].append([item.month, item.amount])
        else:
            data[item.year] = {'name': item.year, 'data':[[item.month, item.amount]]}
    
    def _to_array(d):
        return [d[i] for i in d]
    
    for item in result:
        if item.source == '塑胶事业部':
            _append_data(plastic_data, item)
        elif item.source == '玻璃事业部':
            _append_data(glass_data, item)
        elif item.source == '真空事业部':
            _append_data(vacuume_data, item)
        elif item.source == '安全帽事业部':
            _append_data(he_data, item)
    
    
    return jsonify({'plastic_data':_to_array(plastic_data), 'glass_data':_to_array(glass_data),
                    'vacuume_data':_to_array(vacuume_data), 'he_data':_to_array(he_data)})

@sale_product.route("/qty/month")
@login_required
def qty_month():
    """月销售趋势"""
    if current_user.system:
        products = Product.query.filter_by(system=current_user.system).order_by(Product.id.asc())
    else:
        products = Product.query.order_by(Product.id.asc())
    
    
    return render_template('product/qty_month.html', products=products)


@sale_product.route("/qty/month/data")
@login_required
def qty_month_data():
    
    id = request.args.get('id', 0)
    product = Product.query.get(id)
    
    if not product:
        return [] 

    if current_user.system:
        result = ProductMonth.query.filter_by(product_id=id, system=current_user.system)
    else:
        result = ProductMonth.query.filter_by(product_id=id)
    
    
    data = []
    for item in result:
        data.append([to_timestamp(item.date), item.aux_qty])
    
    
    return jsonify(result=[{'name':product.name, 'data':data}])


@sale_product.route("/price/padding")
@login_required
def price_padding():
    """价格区间"""
    return render_template('product/price_padding.html')


@sale_product.route("/price/padding/data")
@login_required
def price_padding_data():
    
    if current_user.system:
        result = PricePadding.query.filter_by(system=current_user.system).order_by(PricePadding.padding.asc())
    else:
        result = PricePadding.query.order_by(PricePadding.padding.asc())
    
    data = dict()
    for item in result:
        if data.has_key(item.source):
            data[item.source]['data'].append(item.qty)
        else:
            data[item.source] = {'name': item.source, 'data':[item.qty]}
    
    json_data = [data[d] for d in data if '事业部' in d]
    return jsonify(result=json_data)


@sale_product.route("/capacity/padding")
@login_required
def capacity_padding():
    """容量区间"""
    return render_template('product/capacity_padding.html')


@sale_product.route("/capacity/padding/data")
@login_required
def capacity_padding_data():
    
    if current_user.system:
        result = CapacityPadding.query.filter_by(system=current_user.system).order_by(CapacityPadding.capacity.asc())
    else:
        result = CapacityPadding.query.order_by(CapacityPadding.capacity.asc())
    
    data = dict()
    for item in result:
        if data.has_key(item.source):
            data[item.source]['data'].append(['%s ML' % item.capacity ,item.qty])
        else:
            data[item.source] = {'name': item.source, 'data':[['%s ML' % item.capacity ,item.qty]]}
    
    json_data = [data[d] for d in data if '事业部' in d]
    return jsonify(result=json_data)


@sale_product.route("/shape/analyze")
@login_required
def shape_analyze():
    """杯型"""
    return render_template('product/shape_analyze.html')


@sale_product.route("/shape/analyze/data")
@login_required
def shape_analyze_data():
    
    if current_user.system:
        result = ShapeAnalyze.query.filter_by(system=current_user.system)
    else:
        result = ShapeAnalyze.query.all()
    
    
    data = [item.qty for item in result]
    columns = [ item.purpose for item in result]
    
    
    return jsonify(result=[{'name':'杯型', 'data':data}], columns=columns)


@sale_partner.route("/partner/month")
@login_required
def partner_month():
    """客户月销售趋势"""
    if current_user.system:
        partners = Partner.query.filter_by(system=current_user.system)
    else:
        partners = Partner.query.order_by(Partner.id.asc())
    
    return render_template('partner/partners_month.html', partners=partners)


@sale_partner.route("/partner/month/data")
@login_required
def partner_month_data():
    id = request.args.get('id', 0)
    partner = Partner.query.get(id)
    
    if not partner:
        return [] 
    
    if current_user.system:
        result = PartnerMonth.query.filter_by(name=partner.name, system=current_user.system)
    else:
        result = PartnerMonth.query.filter_by(name=partner.name)
    
    data = dict()
    
    for item in result:
        if data.has_key(item.source):
            data[item.source]['data'].append([to_timestamp(item.date), item.amount])
    
        else:
            data[item.source] = {'data':[[to_timestamp(item.date), item.amount]], 'name':item.source}
    
    json_data = [data[d] for d in data if '事业部' in d]
    
    return jsonify(result=json_data, name=partner.name)
        