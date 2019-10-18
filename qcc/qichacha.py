#-*- coding:utf-8 -*-
import requests
from lxml import etree
from urllib.parse import urljoin


'''
*****查询公司详情*****
'''
def qcc(company):
    url = 'https://www.qichacha.com/search?'

    cookie = 'zg_did=%7B%22did%22%3A%20%2216d1a287b76118-00eae4a92c9c01-e343166-1fa400-16d1a287b7751e%22%7D; UM_distinctid=16d1a287bbd332-0fbf475b68672c-e343166-1fa400-16d1a287bbe7b9; _uab_collina=156810192397653396839387; QCCSESSID=8lqnk378euv7sahq48mi1lue42; hasShow=1; acw_tc=0ed7381e15712798787633611e56025a6764fabaf5463e902997603749; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1571279880,1571295868; CNZZDATA1254842228=421855175-1568101865-https%253A%252F%252Fwww.baidu.com%252F%7C1571296572; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571295322975%2C%22updated%22%3A%201571296609669%2C%22info%22%3A%201571279879249%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%22535d3d8e1e16cde08c27ef8df0b1039d%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1571296610'

    headers = {
        'Host': 'www.qichacha.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': 'https://www.qichacha.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie,
    }
    params = {
        'key': company
    }
    res = requests.get(url, headers=headers, params=params)
    res.encoding = 'utf-8'
    e = etree.HTML(res.text)

    link = e.xpath('//*[@id="search-result"]/tr[1]/td[3]/a/@href')[0]

    detail_link = urljoin(res.url,link)

    response = requests.get(detail_link,headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    #获取公司详情信息
    item={}

    # 公司名
    name =html.xpath('//div[@class="content"]/div[1]/h1/text()')[0]
    item['name'] = name.strip().replace('\n', '') if name else '暂无公司名信息'

    # 电话
    phone = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[1]/span[2]/span/text()')
    item['phone'] = phone[0].strip().replace('\n', '') if phone else '暂无电话信息'

    # 官网
    website = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[1]/span[3]/a/text()')
    item['website'] = website[0].strip().replace('\n', '') if website else '暂无网站信息'

    # 邮箱
    email = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[1]/span[2]/a/text()')
    item['email'] = email[0].strip().replace('\n', '') if email else '暂无邮箱信息'
    # else:
    #     email2 = html.xpath('//div[@class="content"]/div[3]/span[1]/span[2]/text()')[0]
    #     item['email'] = email2.strip().replace('\n', '')

    # 地址
    address = html.xpath('//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]/text()')[0]
    item['address'] = address.strip().replace('\n', '') if address else '暂无地址信息'

    #法定代表人
    legal_representative = html.xpath('//*[@id="Cominfo"]//tr[1]/td[2]/div/div/div[2]/a[1]/h2/text()')[0]
    item['legal_representative'] = legal_representative

    # 注册资本
    registered_capital = html.xpath('//*[@id="Cominfo"]//tr[1]/td[4]/text()')[0]
    item['registered_capital'] = registered_capital.replace('\n', '').strip() if registered_capital else '暂无注册资本'

    # 实缴资本
    contributed_capital = html.xpath('//*[@id="Cominfo"]//tr[2]/td[2]/text()')[0]
    if contributed_capital:
        item['contributed_capital'] = contributed_capital.replace('\n', '').strip()
    else:
        item['contributed_capital'] = '暂无实缴资本'

    # 经营状态
    status = html.xpath('//*[@id="Cominfo"]//tr[3]/td[2]/text()')[0]
    if status:
        item['status'] = status.replace('\n', '').strip()
    else:
        item['status'] = '暂无经营状态信息'

    # 成立日期
    establishment = html.xpath('//*[@id="Cominfo"]//tr[3]/td[4]/text()')[0]
    if establishment:
        item['establishment'] = establishment.replace('\n', '').strip()
    else:
        item['establishment'] = '暂无成立日期信息'

    # 统一社会信用代码
    social_code = html.xpath('//*[@id="Cominfo"]//tr[4]/td[2]/text()')[0]
    if social_code:
        item['social_code'] = social_code.replace('\n', '').strip()
    else:
        item['social_code'] = '暂无统一社会信息代码信息'

    # 纳税人识别号
    taxpayer_num = html.xpath('//*[@id="Cominfo"]//tr[4]/td[4]/text()')[0]
    if taxpayer_num:
        item['taxpayer_num'] = taxpayer_num.replace('\n', '').strip()
    else:
        item['taxpayer_num'] = '暂无纳税人识别号信息'

    # 注册号
    registrate_num = html.xpath('//*[@id="Cominfo"]//tr[5]/td[2]/text()')[0]
    if registrate_num:
        item['registrate_num'] = registrate_num.replace('\n', '').strip()
    else:
        item['registrate_num'] = '暂无注册号信息'

    # 组织机构代码
    organization_code = html.xpath('//*[@id="Cominfo"]//tr[5]/td[4]/text()')[0]
    if organization_code:
        item['organization_code'] = organization_code.replace('\n', '').strip()
    else:
        item['organization_code'] = '暂无组织机构代码信息'

    # 企业类型
    company_type = html.xpath('//*[@id="Cominfo"]//tr[6]/td[2]/text()')[0]
    if company_type:
        item['company_type'] = company_type.replace('\n', '').strip()
    else:
        item['company_type'] = '暂无公司类型信息'

    # 所属行业
    industry_involed = html.xpath('//*[@id="Cominfo"]//tr[6]/td[4]/text()')[0]
    if industry_involed:
        item['industry_involed'] = industry_involed.replace('\n', '').strip()
    else:
        item['industry_involed'] = '暂无所属行业信息'

    # 核准日期
    approval_date = html.xpath('//*[@id="Cominfo"]//tr[7]/td[2]/text()')[0]
    if approval_date:
        item['approval_date'] = approval_date.replace('\n', '').strip()
    else:
        item['approval_date'] = '暂无核准日期信息'

    # 登记机关
    registration_authority = html.xpath('//*[@id="Cominfo"]//tr[7]/td[4]/text()')[0]
    if registration_authority:
        item['registration_authority'] = registration_authority.replace('\n', '').strip()
    else:
        item['registration_authority'] = '暂无登记机关信息'

    # 所属地区
    area = html.xpath('//*[@id="Cominfo"]//tr[8]/td[2]/text()')[0]
    if area:
        item['area'] = area.replace('\n', '').strip()
    else:
        item['area'] = '暂无所属地区信息'

    # 英文名
    english_name = html.xpath('//*[@id="Cominfo"]//tr[8]/td[4]/text()')[0]
    if english_name:
        item['english_name'] = english_name.replace('\n', '').strip()
    else:
        item['english_name'] = '暂无英文名信息'

    # 曾用名
    used_name = html.xpath('//*[@id="Cominfo"]//tr[9]/td[2]//span/text()')
    if used_name:
        item['used_name'] = [i.replace('\n', '').strip().replace('\xa0', '') for i in used_name ]
    else:
        item['used_name'] = '暂无曾用名'

    # 参保人数
    insured_num = html.xpath('//*[@id="Cominfo"]//tr[9]/td[4]/text()')[0]
    if insured_num:
        item['insured_num'] = insured_num.replace('\n', '').strip()
    else:
        item['insured_num'] = '暂无参保人数信息'

    # 人员规模
    staff_size = html.xpath('//*[@id="Cominfo"]//tr[10]/td[2]/text()')[0]
    if staff_size:
        item['staff_size'] = staff_size.replace('\n', '').strip()
    else:
        item['staff_size'] = '暂无人员规模信息'

    # 营业期限
    operate_period = html.xpath('//*[@id="Cominfo"]//tr[10]/td[4]/text()')[0]
    if operate_period:
        item['operate_period'] = operate_period.replace('\n', '').strip()
    else:
        item['operate_period'] = '暂无营业期限信息'

    # 经营范围
    business_scope = html.xpath('//*[@id="Cominfo"]//tr[12]/td[2]/text()')[0]
    if business_scope:
        item['business_scope'] = business_scope.replace('\n', '').strip()
    else:
        item['business_scope'] = '暂无经营范围信息'

    return item


if __name__ == '__main__':
    company = '深圳市乐有家控股集团有限公司'
    #company = '重庆壹证通信息技术有限公司 '
    items = qcc(company)
    print(items)

