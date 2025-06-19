# coding=utf-8
from docxtpl import DocxTemplate
import requests
import os
from docx import Document


options1 = [
    {"name": "可疑甄别", "selected": 1},
    {"name": "洗钱风险等级分类", "selected": 0},
    {"name": "风险事件", "selected": 1},
    {"name": "高风险类客户定期审核", "selected": 1},
    {"name": "名单管理", "selected": 0},
    {"name": "账户业务（新开、变更、久悬激活等）", "selected": 1},
    {"name": "涉案账户排查", "selected": 0},
    {"name": "持续识别", "selected": 1},
    {"name": "专项业务排查", "selected": 1},
    {"name": "其他", "selected": 0}
]  # 开展调查原因（1可疑甄别2洗钱风险等级分类3风险事件4高风险类客户定期审核5名单管理6账户业务（新开、变更、久悬激活等）7涉案账户排查8持续识别9专项业务排查10其他）
selected_index2 = 1  # 留存的开户资料（信息）是否齐全
selected_index3 = 1  # 登记的地址（单位地址/常住地址）是否真实存在
selected_index4 = 1  # 有效身份证件是否在有效期内
selected_index5 = 1  # 当前洗钱风险等级（1高风险2次高风险3中风险次4低风险5无结果）
options2 = [
    {"name": "结算业务需要", "selected": 0},
    {"name": "信贷业务需要", "selected": 1},
    {"name": "中间业务需要", "selected": 0},
    {"name": "其他:__________", "selected": 0}
]# 客户陈述建立客户关系目的（1结算业务需要2信贷业务需要3中间业务需要4其他）
options3 = [
    {"name": "账户结算", "selected": 1},
    {"name": "存款", "selected": 0},
    {"name": "贷款", "selected": 1},
    {"name": "贷记卡", "selected": 1},
    {"name": "理财", "selected": 1},
    {"name": "保管箱", "selected": 0},
    {"name": "基金", "selected": 0},
    {"name": "信托", "selected": 0},
    {"name": "保险", "selected": 0},
    {"name": "代缴代扣", "selected": 0},
    {"name": "网银/手机银行", "selected": 1},
    {"name": "其他:________", "selected":0}
]# 账户开立及使用本行服务/产品情况（1账户结算2存款3贷款4贷记卡5理财6保管箱7基金8黄金9信托10保险11代缴代扣12网银/手机银行13其他）
selected_index8 = 1  # 职业或经营情况是否与账户交易相匹配
selected_index9 = 0  # 客户的家庭住址或工作地点与银行所在地距离遥远且无合理解释
selected_index10 = 0  # 客户经常以签署授权书或通过代理方式办理业务，避免和银行直接接触，以便躲避身份识别要求
selected_index11 = 0  # 客户代理多个他人账户交易，且无合理解释
selected_index12 = 0  # 是否拒绝或不愿意提所需要的信息，或明显隐藏了与交易有关的重要信息
selected_index13 = 0  # 是否对银行询问持防范态度，表现为拒绝回答或者过度证明其交易正当
selected_index14 = 0  # 是否对银行的反洗钱制度和措施表现出过分关心
selected_index15 = 0  # 是否对自己声称的职业/经营活动并不了解或对交易和账户活动的解释前后矛盾
selected_index16 = 0 # 短期内，存在身份证源于同一地区的大量个人开户，有理由怀疑受人指使
selected_index17 = 0  # 是否存在媒体负面报道信息或不良结算记录
selected_index18 = 0  # 是否怀疑客户特征、业务关系、交易的目的和意图、资金来源和用途存在较高洗钱或者恐怖融资风险
selected_index19 = 0 # 是否因涉嫌犯罪被国家有关机关、部门、机构查询、冻结、扣划，或者疑似国家司法、执法和监察机关发布的涉嫌洗钱及相关犯罪人员
selected_index20 = 0  # 是否被人民银行反洗钱调查
selected_index21 = 0  # 客户、交易对手等是否来自高风险国家（地区），或涉嫌被制裁的实体/个人
selected_index22 = 0  # 是否为外国政要或其亲属及关系密切人
selected_index23 = 0  # 是否存在涉赌涉诈可疑情形
selected_index25 = 0  # 是否存在《泉州银行电子银行反洗钱工作指引》《泉州银行网银手机银行管理办法》规定不得开立的情形
selected_index26 = 0  # 申请调高的网银限额是否与其资产状况或工作单位相符月内即调高网银限额，资金交易需求明显与其资产状况或工作单位不符
selected_index27 = 0  # 是否存在开户三个月内即调高网银限额，资金交易需求明显与其资产状况或工作单位不符
selected_index28 = 0  # 是否利用网银手机银行频繁交易，资金来源及用途与其资产状况或工作单位不符，具有明显的洗钱交易行为

options4 = [
    {"name": "电话回访", "selected": 1},
    {"name": "口头询问", "selected": 0},
    {"name": "公开渠道信息查询", "selected": 0},
    {"name": "分析历史交易", "selected": 1},
    {"name": "查阅客户资料", "selected": 0},
    {"name": "实地查访", "selected": 1},
    {"name": "补充证明材料", "selected": 0},
    {"name": "其他:________", "selected": 0}
] # 以上采取的尽职调查方式包括（1电话回访2口头询问3公开渠道信息查询4分析历史交易5查阅客户资料6实地查访7补充证明材料8其他）

options5 = [
    {"name": "调高客户风险等级", "selected": 1},
    {"name": "报送可疑交易报告", "selected": 0},
    {"name": "提高客户信息的审查和更新频率", "selected": 0},
    {"name": "获取业务关系和交易目的、资金来源和用途的相关信息、证明材料", "selected": 1},
    {"name": "对客户的交易方式、交易规模、交易频率等实施合理限制", "selected": 1},
    {"name": "与客户建立、维持业务关系，或者为客户办理业务，经高级管理层（有权审批人）批准", "selected": 0},
    {"name": "加强对客户及其交易的监测分析", "selected": 1},
    {"name": "其他：持续关注账户使用情况", "selected": 0}
]  # 拟采取的控制措施（1调高客户风险等级2报送可疑交易报告3获取业务关系和交易目的、资金来源和用途的相关信息、证明材料4对客户的交易方式、交易规模、交易频率等实施合理限制5与客户建立、维持业务关系，或者为客户办理业务，经高级管理层（有权审批人）批准6加强对客户及其交易的监测分析7其他：持续关注账户使用情况）
# 准备数据
context = {
    'customer': {
        'ID': '123456789',  # 客户号
        'name': '张三',  # 客户名称
        'reason': '非柜面交易风险等级为“标准”、非柜面交易日限额5万元、月限额70万元。',  # 调查原因详述
        'results': '情况属实',  # 身份信息调查结果
        'career': '××律所，律师',  # 详细职业信息
        'economic': '经济实力较好，有两套房产',  # 经济状况或资产情况（个人/家庭情况）
        'area': '福建省晋江市',  # 主要经营/活动地区（省内的具体到县/区）
        'situation': '他行存款转入',  # 客户交易情况（存量客户填写，定期审核时填写本周期内交易情况，其他情形根据实际分析周期填写）
        'others': '无',  # 其他尽职调查情况
        'conclusion':'张三为我行价值客户，经调查了解，该客户工作单位为晋江市xxx律所，'
                     '职位：律师，年收入：10万。客户开户主要作为日常结算及购买理财、定期等产品使用，'
                     '客户已在我行办理定期存款5万。经查询联防联控风险平台，无风险无分数，无其他风险事件。'
                     '客户需调高额度的原因是客户在我行办理定期，定期到期后需转出使用，同时日常结算需要。'
                     '客户已提供手机号码实名满一年以上作为辅助证件，资产证明为我行资产截图，暂未发现异常。'
                     '经综合评估，现申请调整非柜面等级为标准，日限额5万元，月限额70万元，'
                     '后续会加强对该客户及其交易的监测分析。'
    },

    'options1': [
            {
                'text': opt1['name'],
                'checked': "☑" if opt1['selected']==1 else "□"
            }
            for opt1 in options1
        ],

    'option1_checked2': "☑" if selected_index2 == 1 else "□",
    'option2_checked2': "☑" if selected_index2 == 2 else "□",  # 留存的开户资料（信息）是否齐全

    'option1_checked3': "☑" if selected_index3 == 1 else "□",
    'option2_checked3': "☑" if selected_index3 == 2 else "□",  # 登记的地址（单位地址/常住地址）是否真实存在

    'option1_checked4': "☑" if selected_index4 == 1 else "□",
    'option2_checked4': "☑" if selected_index4 == 2 else "□",  # 有效身份证件是否在有效期内

    'option1_checked5': "☑" if selected_index5 == 1 else "□",
    'option2_checked5': "☑" if selected_index5 == 2 else "□",
    'option3_checked5': "☑" if selected_index5 == 3 else "□",
    'option4_checked5': "☑" if selected_index5 == 4 else "□",
    'option5_checked5': "☑" if selected_index5 == 5 else "□",
    'option6_checked5': "☑" if selected_index5 == 6 else "□",  # 当前洗钱风险等级

    'options2': [
        {
            'text': opt2['name'],
            'checked': "☑" if opt2['selected']==1 else "□"
        }
        for opt2 in options2
    ],    # 客户陈述建立客户关系目的
    'options3': [
        {
            'text': opt3['name'],
            'checked': "☑" if opt3['selected'] else "□"
        }
        for opt3 in options3
    ],   #账户开立及使用本行服务/产品情况

    'option1_checked8': "☑" if selected_index8 == 1 else "□",
    'option2_checked8': "☑" if selected_index8 == 0 else "□",  # 职业或经营情况是否与账户交易相匹配

    'option1_checked9': "☑" if selected_index9 == 1 else "□",
    'option2_checked9': "☑" if selected_index9 == 0 else "□",

    'option1_checked10': "☑" if selected_index10 == 1 else "□",
    'option2_checked10': "☑" if selected_index10 == 0 else "□",

    'option1_checked11': "☑" if selected_index11 == 1 else "□",
    'option2_checked11': "☑" if selected_index11 == 0 else "□",

    'option1_checked12': "☑" if selected_index12 == 1 else "□",
    'option2_checked12': "☑" if selected_index12 == 0 else "□",

    'option1_checked13': "☑" if selected_index13 == 1 else "□",
    'option2_checked13': "☑" if selected_index13 == 0 else "□",

    'option1_checked14': "☑" if selected_index14 == 1 else "□",
    'option2_checked14': "☑" if selected_index14 == 0 else "□",

    'option1_checked15': "☑" if selected_index15 == 1 else "□",
    'option2_checked15': "☑" if selected_index15 == 0 else "□",

    'option1_checked16': "☑" if selected_index16 == 1 else "□",
    'option2_checked16': "☑" if selected_index16 == 0 else "□",

    'option1_checked17': "☑" if selected_index17 == 1 else "□",
    'option2_checked17': "☑" if selected_index17 == 0 else "□",

    'option1_checked18': "☑" if selected_index18 == 1 else "□",
    'option2_checked18': "☑" if selected_index18 == 0 else "□",

    'option1_checked19': "☑" if selected_index19 == 1 else "□",
    'option2_checked19': "☑" if selected_index19 == 0 else "□",

    'option1_checked20': "☑" if selected_index20 == 1 else "□",
    'option2_checked20': "☑" if selected_index20 == 0 else "□",

    'option1_checked21': "☑" if selected_index21 == 1 else "□",
    'option2_checked21': "☑" if selected_index21 == 0 else "□",

    'option1_checked22': "☑" if selected_index22 == 1 else "□",
    'option2_checked22': "☑" if selected_index22 == 0 else "□",

    'option1_checked23': "☑" if selected_index23 == 1 else "□",
    'option2_checked23': "☑" if selected_index23 == 0 else "□",

    'option1_checked25': "☑" if selected_index25 == 1 else "□",
    'option2_checked25': "☑" if selected_index25 == 0 else "□",

    'option1_checked26': "☑" if selected_index26 == 1 else "□",
    'option2_checked26': "☑" if selected_index26 == 0 else "□",

    'option1_checked27': "☑" if selected_index27 == 1 else "□",
    'option2_checked27': "☑" if selected_index27 == 0 else "□",

    'option1_checked28': "☑" if selected_index28 == 1 else "□",
    'option2_checked28': "☑" if selected_index28 == 0 else "□",

    'options4': [
        {
            'text': opt4['name'],
            'checked': "☑" if opt4['selected']==1 else "□"
        }
        for opt4 in options4
    ],  #以上采取的尽职调查方式包括

    'options5': [
        {
            'text': opt5['name'],
            'checked': "☑" if opt5['selected']==1 else "□"
        }
        for opt5 in options5
    ]# 拟采取的控制措施

}


def download_file(url, save_path):
    """
    下载文件并保存到指定路径

    :param url: 文件URL
    :param save_path: 保存路径（包含文件名）
    :return: 成功返回True，失败返回False
    """
    try:
        # 发送HTTP GET请求
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 写入文件
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 过滤掉保持连接的空白块
                    f.write(chunk)

        print(f"文件已成功保存到: {save_path}")
        return True

    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False


# 使用示例
file_url = "https://raw.githubusercontent.com/ZSY52047/-/main/personal.docx"  # 替换为实际URL
local_path = "C:/Users/小章247/Desktop/pesonal_download.docx"  # 指定完整保存路径和文件名

download_file(file_url, local_path)

# # url = "https://www.baidu.com/"
# # 发送 GET 请求
# response = requests.get(url)
# 生成文档
# url = "https://raw.githubusercontent.com/ZSY52047/-/main/personal.docx"
# response = requests.get(url)
# response.raise_for_status()
# AAA=response.content
# print(AAA)

# doc = Document(local_path)

doc = DocxTemplate(local_path)
doc.render(context)
doc.save("C:/Users/小章247/Desktop/1111.docx")