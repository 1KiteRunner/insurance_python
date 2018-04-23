__author__ = 'weikai'
import  requests
from PIL import Image
from io import BytesIO
headers={
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    'Accept-Encoding':'Accept-Encoding',
    'Accept-Language':'zh-CN,zh;q=0.8',
    #'Accept':'image/webp,image/*,*/*;q=0.8',
    #'Referer':'http://www.epicc.com.cn/wap/carProposal/car/carInput1',
}
imageurl = 'http://www.epicc.com.cn/wap/CreateImage?next=0.13816044071471234'

response = requests.get(imageurl,headers=headers)
i = Image.open(BytesIO(response.content))
i.save('web.jpg')