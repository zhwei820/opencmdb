#!/usr/bin/env python
# -*- coding: utf-8 -*-

USER_TYPE = {"1":"平台", "2":"商家"}

RESULT_404 = {"status": 0, "message": "页面不存在"}

NO_PERMISSION = {"status": 0, "message": "权限不够"}

PAGE_CAPACITY = 20

PRO_PAGE_CAPACITY = 200


yes_no = {
    '0' : '否',
    '1' : '是'
}

true_false = {
    'False' : '否',
    'True' : '是'
}
true_false_status = {
    'False' : '失效',
    'True' : '<span class="green">有效</span>'
}
public_status = {
    '0' : '失效',
    '1' : '<span class="green">有效</span>'
}

data = 'hbdata/',  # 项目资源文件目录 html/hbdat}

admin_role = {
    '1': '管理员',
    '2': '财务',
    '3': '运营',
    '4': '商务',
}

os_type_option = {
    '0' : 'android/ios',
    '1' : 'android',
    '2' : 'ios',
}

admin_status = {
    '0' : '正常',
    '1' : '停用',
    '2' : '<span class="red">锁定</span>'
}
user_status = {
    '0' : '非正常',
    '1' : '有效',
    '2' : '失效'
}
activity_type_option = {
    '1' : '左边',
    '2'  : '右上',
    '3'  : '右下',
}
pay_status = {
    '-1' : '作弊',
    '0'  : '非法请求',
    '1' : '待审核',
    '2'  : '审核通过',
    '3'  : '处理完成',
    '4'  : '处理出错',
    '5'  : '充值中',
    '6'  : '已退款',
    '7'  : '待退款',
    '8'  : '暂不处理'
}
pay_type = {
    '1' : '充值卡',
    '2'  : 'Q币',
    '3'  : '支付宝提现',
    '4'  : 'wifi上网券',
    '5'  : 'Q币小额兑换',

    '10'  : '兑吧',
},


ad_top = {
    '0' : '否',
    '1' : '<span class="red">是</span>'
}
ad_status = {
    '0' : '无效',
    '1' : '<span class="green">有效</span>'
}
ad_z_status = {
    '0' : '未处理',
    '1' : '已上架',
    '2' : '已下架'
}
hongbao_status = {
    '0' : '未发送',
    '1' : '<span class="red">发送失败</span>',
    '2' : '<span class="green">成功</span>',
    '3' : '<span class="red">失败</span>'
}
channel_set_status = {
    '0' : '失效',
    '1' : '<span class="green">有效</span>'
}
message_os = {
    '0' : 'android/ios',
    '1' : 'android',
    '2' : 'ios',
}
message_status = {
    '0' : '待审核',
    '1' : '已审核',
    '2' : '<span class="green">发送成功</span>',
    '3' : '<span class="red">发送失败</span>',
    '4' : '处理成功'
}

message_notify = {
    '0' : '否',
    '1' : '<span class="green">是</span>'
}

is_public = {
    '0' : '私有',
    '1' : '公开',
}

message_type = {
    '0' : '私有',
    '1' : '公共',
}
message_detail_status = {
    '0' : '未发送',
    '1' : '<span class="green">发送成功</span>',
    '2' : '<span class="red">发送失败</span>'
}
device_modify_status = {
    '0' : '失败',
    '1' : '<span class="green">成功</span>'
}
menu_status = {
    '0' : '失效',
    '1' : '<span class="green">有效</span>'
}

jojo_status_option = {
    '0' : '待上传',
    '1' : '待审核',
    '2' : '待上线',
    '3' : '上线',
    '4' : '被下线',
    '5' : '被切',
}

notification_status = {
    '0' : '待审核',
    '1' : '已审核',
    '2' : '处理成功',
    '3' : '发送成功',
    '4' : '发送失败'
}
exchange_select = {
    '1' : '用户ID',
    '2' : '兑换ID',
    '3' : '手机号',
    '4' : '物品ID',
    '5' : '设备ID',
    '6' : '交易IP',
    '7' : '操作人',
}
is_images = {
    '0' : '否',
    '1' : '是'
}
pk_status = {
    '0' : '待审核',
    '1' : '<span class="green">已审核</span>'
}
pk_scale = {
    '1' : '10%',
    '2' : '20%',
    '3' : '30%',
    '4' : '40%',
    '5' : '50%',
    '6' : '60%',
    '7' : '70%',
    '8' : '80%',
    '9' : '90%',
    '10' : '100%'
}
version_status = {
    '0' : '待审核',
    '1' : '<span class="green">已审核</span>'
}
o_product_status = {
    '0' : '待上架',
    '1' : '<span class="green">已上架</span>',
    '2' : '<span class="red">已下架</span>'
}
o_product_lottery_status = {
    '0' : '未开始',
    '1' : '<span class="green">进行中</span>',
    '2' : '<span class="blue">倒计时</span>',
    '3' : '<span class="brown">已揭晓</span>',
    '4' : '<span class="red">已下线</span>',
}
o_luck_user_status = {
    '0' : '未填写',
    '1' : '<span class="green">待发货</span>',
    '2' : '<span class="brown">已发货</span>',
    '3' : '<span class="blue">已收货</span>',
    '4' : '<span class="yellow">已晒单</span>',
}
o_logistics_option = {
    '1' : '申通快递',
    '10' : '优速快递',
    '11' : '京东',
    '2' : '顺丰快递',
    '3' : '圆通快递',
    '4' : '韵达快递',
    '5' : '汇通快递',
    '6' : '天天快递',
    '7' : 'EMS快递',
    '9' : '虚拟物品',
}

channel_type_option= {
  '0' : '只发送这些渠道',
  '1' : '排除这些渠道',
}

open_type_option= {
  'native' : '应用内打开',
  'webview' : 'webview',
  'browser' : '外部浏览器',
}

os_type = {
    'android' : 'android',
    'ios' : 'ios',
}

all_update = '["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99"]'

all_update_label = {
    '[]' : '全量',
}
