import requests
from bs4 import BeautifulSoup
import os
#from pyaria2 import Aria2RPC
import time
import sys

def get_file_from_url(links):
    """使用aria2下载文件,经常下载不成功"""

    file_num = 0
    for link in links:
        file_num += 1
        if link[:5]=="Error" or link[:5]=="Warn ":#如果网址为错误提示
            print("Error: The paper {} 's link is not valid, downlaod fail".format(file_num))
        else:
            if link[:2]==r"//":
                link = "https:" + link
            try:      
                file_name =str(file_num) + ".pdf"
                jsonrpc = Aria2RPC()
                set_dir = os.path.join(os.path.dirname(__file__),"pdfs")
                options = {"dir": set_dir, "out": file_name, "allow-overwrite":True,}
                res = jsonrpc.addUri([link], options = options)
                print("Paper {} download success".format(file_num))
            except:
                print("Paper {} download fail, please open the address of papers_links.txt in your browser or run aria2c_download.bat to download manually".format(file_num))    
  


def read_doi(path):
    """从文件中读取doi号并返回列表"""

    dois=[]
    with open(path,'r') as f:
        for line in f:
            if line != '\n':
                dois.append(line.strip('\n').strip())
    f.close()
    return dois


def download_file(urls):
    """下载pdf文件"""

    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    file_num=0
    for url in urls:
        file_num += 1
        if url[:2]==r"//":
            url = "https:" + url

        path = str(file_num)+".pdf"
        try:        
            response = requests.get(url,headers=headers,stream=True,timeout=60)                
            with open(path,"wb") as pdf_file:
                for content in response.iter_content():
                    pdf_file.write(content) 
            pdf_file.close()
            print("Paper {} download success".format(file_num))
            time.sleep(3)
        except:
            print("Paper {} download fail, please open the address of papers_links.txt in your browser or run aria2c_download.bat to download manually".format(file_num))
            continue


def save_file_link(file_path,link):
    """保存文件的下载链接到文件中"""
    
    with open(file_path,'a',encoding='utf-8') as f:
        if link[:2]==r"//":
            link = "https:" + link
        f.write(link+"\n")        
    f.close()

def get_bibtex(citation):
    """将网页返回的索引格式转换为bibtex格式"""

    paper_bibtex={
        'Author':'',
        'Title':'',
        'Journal':'',
        'Year':'',
        'Volume':'',
        'Issue':'',
        'Pages':'',
        'DOI':''
    }
    
    if len(citation)==0:#网页没有返回索引信息       
        return paper_bibtex
    elif citation[:5]=="Error":#网页没有找到文章信息
        return paper_bibtex        
    else:
        #Michael, A. (2019). Orientation of Hydraulic Fracture Initiation from Perforated Horizontal Wellbores. SPE Annual Technical Conference and Exhibition. doi:10.2118/199766-stu
        paper_bibtex['Author']=citation[:citation.find('(')].strip()#文章作者姓名是年份括号左边的字符
        paper_bibtex['Year']=citation[citation.find('(')+1:citation.find('(')+5]#年份信息是括号之后4个字符，目前年份只能看是4位
        sub_temp=citation[citation.find('(')+7:].strip()#先获取从年份往后两个字符开始往后的字符串
        paper_bibtex['Title']=sub_temp[:sub_temp.find(r'.')]#在获取的这个字符串中获取从开始到第一个'.'开始的字符为标题
        
        #期刊、卷和期比较复杂，存在如下情况:
        #1.只有期刊名，没有期号和卷号，也没有页码。此时在两个'.'之间的字符即为期刊名称.这种情况一般是返回值出问题，而不是实际情况
        #2.有期刊名，只有卷号没有期号（某些期刊特征，不是返回值的问题，是实际情况），此时格式为Journal,Volume,pages1-pages2
        #3.有期间名，有期号和卷号（这是最常见的格式），此时字符串的格式为Journal,Volume(Issue),pages1-pages2
        #4.可能存在没有页码的情况
        #需要处理这四种情况
        sub_temp1=sub_temp[sub_temp.find(r'.')+1:].strip()#返回从文章标题后边的'.'开始到结束的字符串
        if sub_temp1.count(',')==2:#如果有两个逗号，则说明期刊，期号，卷号完整
            paper_bibtex['Journal']=sub_temp1[:sub_temp1.find(',')].strip()
            sub_temp2=sub_temp1[sub_temp1.find(',')+1:]#返回期刊名后的第一个逗号（不包括逗号）以后的字符串
            if(sub_temp2[:sub_temp1.find('.')].find('(') != -1):#如果在期刊名后到doi号之前的这段字符串中找的了括号，说明属于第3种情况，即有期号，也有卷号
                paper_bibtex['Volume']=sub_temp2[:sub_temp2.find('(')].strip()#卷号是期刊名后第一个逗号至后边左括号之间的字符
                paper_bibtex['Issue']=sub_temp2[sub_temp2.find('(')+1:sub_temp2.find(',')-1].strip()#期号是从左括号以后至后边逗号之前的字符
                paper_bibtex['Pages']=sub_temp2[sub_temp2.find(',')+1:sub_temp2.find('.')].strip()
            else:#没有发现括号，说明只有卷，而没有期
                paper_bibtex['Volume']=sub_temp2[:sub_temp2.find(',')].strip()#此时卷号为期刊第一个逗号往后的字符（不包括逗号）开始直下一个逗号之前的字符
                paper_bibtex['Pages']= sub_temp2[sub_temp2.find(',')+1:sub_temp2.find('.')].strip()               
        elif sub_temp1.count(',')==1:#如果有1个逗号,则是情况4，比较复杂,不做其他处理，只输出作者、标题和doi号，后期自动更新
            pass
        else:#如果没有逗号，则是情况1，只有期刊名
            paper_bibtex['Journal']=sub_temp1[:sub_temp1.find('.')].strip()
            pass

        paper_bibtex['DOI']=citation[citation.rfind(':')+1:]#doi号是整个字符串从末尾往前直到出现':'
        return paper_bibtex

def save_paper_citation(file_path,citation,type):
    """保存文件的索引信息到文件中，输出格式为BibTex""" 

    paper_bibtex=get_bibtex(citation)  
    with open(file_path,'a',encoding='utf-8') as f:
        f.write("@article{\n")#全部是article类型
        f.write(paper_bibtex['Author']+'-'+paper_bibtex['Year']+",\n")       
        for key,value in paper_bibtex.items():
            f.write("\t"+key+"="+"{"+value+"},\n")
        f.write("}\n\n")        
    f.close()

def get_response(url):
    """返回url的响应"""

    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    NETWORK_STATUS = True # 判断状态变量
    try:
        response = requests.get(url,headers=headers,timeout=60)
        if response.status_code == 200:
            return response
    except requests.exceptions.Timeout:        
        NETWORK_STATUS = False # 请求超时改变状态
        if NETWORK_STATUS == False:
            '''请求超时'''
            for i in range(1, 10):
                print('Time out, request {} time'.format(i))
                response = requests.get(url,timeout=60)
                if response.status_code == 200:
                    return response
    except:#发生其他异常导致读取失败
        for i in range(1, 10):
                print('Exception occured, request {} time'.format(i))
                response = requests.get(url,timeout=60)
                if response.status_code == 200:
                    return response
        print("Exception occured when request!")
        return -1
    return -1  # 当所有请求都失败，返回  -1  ，此时有极大的可能是网络问题或IP被封。

def check_sci_site(urls):
    """检查所有sci-hub网址，返回速度最快的用于下载"""

    r_time=10.0
    t_url=""
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    try:
        #print(urls[0])
        r=requests.get(urls[0],headers=headers,timeout=10.0)
        if r.status_code == 200:
            r_time=r.elapsed.microseconds*1.e-6
            t_url=urls[0]
        else:
            r_time=1000.0       
    except:
        r_time=1000.0#如果响应失败，则返回一个很大的值

    for url in urls:
        try:
            r = requests.get(url,timeout=10.0)
            if r.status_code == 200:
                if r.elapsed.microseconds*1.e-6 < r_time:
                    t_url=url
            else:
                t_url=""
        except:
            pass
    return t_url                
                  

###############################################################################
print("SCI-HUB ... to remove all the barriers in the way of science \n")


mark=input("Do you want to input the sci-hub site (1) or use the internal sites (2) ?\n")
if (mark)=="1":

    sci_hub=input("Input sci-hub site:\n")

else:
    sci_hubs=["https://sci-hub.shop/","https://sci-hub.tw","https://sci-hub.ren/","https://sci-hub.tw/","https://sci-hub.tw/"]
    print("Check the avaible sci-hub site") 
    sci_hub=check_sci_site(sci_hubs)#返回速度最快的网址


if sci_hub=="":
    print("No sci-hub site is avaible, try again later\n")
    os.exit(0)


print("The sci-hub address is "+sci_hub+"\n")

################################################################################
link_file_name="papers_links.txt"
citation_file_name="papers_citation.txt"

if os.path.exists(link_file_name):#检查是否存在文章的下载链接，如果存在，则删除文件
    os.remove(link_file_name)

if os.path.exists(citation_file_name):#检查是否存在文章索引信息，如果存在，则删除文件
    os.remove(citation_file_name)
"""
if os.path.isdir("pdfs"):#检查是否存在保持pdf的文件夹，如果存在，则删除该文件夹
    shutil.rmtree("pdfs")"""

start = time.time()
print("Reading doi.txt")
dois=read_doi("doi.txt")
paper_num=len(dois)

if paper_num==0:
    print("No iterms found in the doi.txt, please add dois in the file\n")
    sys.exit(0)

print("There are {} iterms in doi.txt\n".format(len(dois)))

print("Searching begins...")
#使用sci-hub搜索时有三种情况出现：
#1.doi号搜索成功，且找到了pdf地下载链接，此时地特征是返回地html的title值以Sci-Hub开头
#2.doi号搜索成功，但没有找到pdf下载链接，网页跳转到原始文件列表
#3.doi号搜索不成功,此时返回的html是空的

paper_no=0
paper_links=[]
#paper_citation=[]
for doi in dois:    
    paper_no += 1    
    url=sci_hub+"/"+doi
    time.sleep(3.0)#停止3秒
    response=get_response(url)     
    #with open('response.html','w') as file_obj:
        #file_obj.write(response.content.decode('utf-8'))
    if response==-1:#请求无响应，则直接退出
        print("Link searching fail for paper {}, no response from {} ".format(paper_no,url))
        paper_link="Error: searching fail for paper {}, no response".format(paper_no)
        paper_citation="Error: searching fail for paper {}".format(paper_no)
        paper_links.append(paper_link)
        save_file_link(link_file_name,paper_link)
        save_paper_citation(citation_file_name,paper_citation,1)
        continue

    html=response.content.decode('utf-8')#获取响应的内容  
    if html.replace('\n','')=='':#如果响应的内容为空，则说明找不到该doi
        print("Error: Search paper {}, doi: {} fail, please recheck".format(paper_no,doi))
        paper_link="Error: Paper : {}, {} not found or the sci-hub is not aviable".format(paper_no,doi)#没有找到也输出错误信息
        paper_citation="Error: Paper : {}, {} not found or the sci-hub is not aviable".format(paper_no,doi)#没有找到也输出错误信息
        paper_links.append(paper_link)
        save_file_link(link_file_name,paper_link)
        save_paper_citation(citation_file_name,paper_citation,1)
        continue

    else:             
        soup=BeautifulSoup(html,'lxml')
        if(soup.find('title').text[:7]=="Sci-Hub"):
            print("Link searching success for paper : {}, the doi is {}".format(paper_no,doi))  
            paper_link=soup.find('div',id="article").find('iframe')['src']#将文件的所有链接放在list中
            paper_citation=soup.find('div',id="citation").text.strip('\xa0')#将文章的索引信息放在list中
            paper_links.append(paper_link)
            save_file_link(link_file_name,paper_link)
            save_paper_citation(citation_file_name,paper_citation,1)

        else:
            print("Warning: Paper fouund, but link searching fail for paper : {}, the doi is {}".format(paper_no,doi)) 
            paper_link="Warn : Paper fouund but link for paper : {}, {} not found or the sci-hub is not aviable".format(paper_no,doi)#没有找到也输出错误信息
            paper_citations="Warn : Paper found but link for paper : {}, {} not found or the sci-hub is not aviable".format(paper_no,doi)#没有找到也输出错误信息
            paper_links.append(paper_link)
            save_file_link(link_file_name,paper_link)
            save_paper_citation(citation_file_name,paper_citation,1)  


#print("Save citations to papers_citation.txt \n")
#save_paper_citation("papers_citation.txt",paper_citations,1)#文章的索引保存到文件papers_citation.txt中
#print("Save download links to papers_links.txt\n")
#save_file_link('papers_links.txt',paper_links)#文章的下载链接保存到papers_links.txt中
    
print("\nDownloading papers...")
#get_file_from_url(paper_links)
download_file(paper_links)
end = time.time()
print("")
print (f"Time consuming:{end-start:.2f} secs")






