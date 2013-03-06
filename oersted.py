 
import re
from oersted import OEClient

oeclient = OEClient('localhost')                                                   #创建远程客户端对象
oeclient.login('dbname', 'admin', 'admin')                                    #登录
Product = oeclient.create_browse('dbname', 'product.product') #获取product对象
Product_Tmpl = oeclient.create_browse('dbname', 'product.template') #获取product_template对象
prod_objs = Product.search()                                                                  #获取所有product对象实例
pattern = re.compile(r'([^-]+?)\s*-\s*([^-]+)$')       #考虑到客户在定义产品名称时‘-’周围空格的不规范使用
tmpl_prod = {}
unmatched = []
for prod in prod_objs:
    if not prod.variants:                                                                     #防止多次运行该程序对已转换对象的修改
        matches = pattern.match(prod.name)
        if matches and matches.group(1):
            tmpl_prod.setdefault(matches.group(1), []).append(prod) #获得例如： {'产品型号XXX‘: [红色产品对象, 黑色产品对象, 白色产品对象}的字典
        else:
            unmatched.append(prod.name)                  #记录未匹配的产品名称到umatched列表中，并在后面输出，以方便手工处理
for tmpl in tmpl_prod:
    if len(tmpl_prod[tmpl]) > 1:                                   #如果tmpl_prod字典的值，就是那个列表[红色产品对象， 黑色产品对象]有大于1项，表示该记录需要处理
        old_tmpl = tmpl_prod[tmpl][0].product_tmpl_id #记录列表中第一个产品所对应的产品模板
        new_tmpl_id = old_tmpl.copy(old_tmpl.id)          #拷贝获得新的模板对象，这里获得该新建模板的ID
        new_tmpl = Product_Tmpl(new_tmpl_id)            #获得新建模板对象
        new_tmpl.name = tmpl                                      #改变新建模板的名称为tmpl_prod字典的key值
        new_tmpl.active = True                                      #默认的product.template对象并没有active字段，我们做了继承修改，
                                                                                    #目的是安全考虑保留原template, 
        new_tmpl.save()                                                 #保存修改后的template
        for prod in tmpl_prod[tmpl]:
            prod.product_tmpl_id.active = False               #可以直接删除原template，这里处于安全考虑，将其设置为：inactive
            prod.product_tmpl_id.save()
            m = pattern.match(prod.name)
            prod.product_tmpl_id = new_tmpl                  #给product赋予新的template
            prod.variants = m.group(2)                            #给product的variants字段赋值，如：红色，黑色
            prod.save()
print unmatched