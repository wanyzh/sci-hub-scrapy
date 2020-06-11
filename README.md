# 功能

该软件是采用网络爬虫技术，利用sci-hub神器批量下载英文文献pdf文件，同时获取pdf下载地址及文献的检索信息。

# 使用步骤及说明

## 填入doi号
将需要下载的英文文献的doi号填入doi.txt文件中，每行一个记录，实例如下：

	10.1016/j.petrol.2017.12.013
	10.1007/s10483-016-2075-8
	10.1016/j.petrol.2017.12.013
	
## 运行程序

程序会提示自己手动输入sci-hub的网址还是用内置的sci-hub网址。

如果选择1，则输入sci-hub网址并回车，则直接利用用户输入的sci-hub网址下载文献
如果选择2，则程序会在内置的sci-hub网址中选择一个速度较快的来,这个过程稍慢，请耐心等待

程序将自动从doi.txt中读入doi号开始搜索文献下载

## 保存下载的pdf文件
下载的pdf保存在当前目录的pdfs文件夹中，文件名按照doi.txt文件中的顺序按照1.pdf、2.pdf、3.pdf命名

## 保存索引信息：

除下载pdf文件外，此程序还可以下载doi.txt文献所列的文章索引，按顺序保存在papers_citation.txt文件中，格式为Bibtex实例如下：

	@article{
		Wan, Y.-Z., Liu, Y.-W., Chen, F.-F., Wu, N.-Y., & Hu, G.-W.-2018,
		Author={Wan, Y.-Z., Liu, Y.-W., Chen, F.-F., Wu, N.-Y., & Hu, G.-W.},
		Title={Numerical well test model for caved carbonate reservoirs and its application in Tarim Basin, China},
		Journal={Journal of Petroleum Science and Engineering},
		Year={2018},
		Volume={161},
		Issue={},
		Pages={611–624},
		DOI={10.1016/j.petrol.2017.12.013},
	}

	@article{
		Wan, Y., Liu, Y., Ouyang, W., Han, G., & Liu, W.-2016,
		Author={Wan, Y., Liu, Y., Ouyang, W., Han, G., & Liu, W.},
		Title={Numerical investigation of dual-porosity model with transient transfer function based on discrete-fracture model},
		Journal={Applied Mathematics and Mechanics},
		Year={2016},
		Volume={ 37},
		Issue={5},
		Pages={611–626},
		DOI={10.1007/s10483-016-2075-8},
	}

	@article{
		Wan, Y.-Z., Liu, Y.-W., Chen, F.-F., Wu, N.-Y., & Hu, G.-W.-2018,
		Author={Wan, Y.-Z., Liu, Y.-W., Chen, F.-F., Wu, N.-Y., & Hu, G.-W.},
		Title={Numerical well test model for caved carbonate reservoirs and its application in Tarim Basin, China},
		Journal={Journal of Petroleum Science and Engineering},
		Year={2018},
		Volume={161},
		Issue={},
		Pages={611–624},
		DOI={10.1016/j.petrol.2017.12.013},
	}
	
上述格式可以直接用Noteexpress或者endnote导入条目保存，或者使用Latex引用
	
注意：为了保持数量上的一致性，如果给定的doi号找不到或者访问失败，同样还是会输出一个@article记录，主要是为了和输出文件的编号对应
	
## pdf文件下载链接
程序还保存了文章真正的下载链接，保存在papers_links.txt文件中，
实例如下：

	https://dacemirror.sci-hub.tw/journal-article/9af7761843463b1b3eb7344dda0e7e59/wan2018.pdf#view=FitH
	https://cyber.sci-hub.tw/MTAuMTAwNy9zMTA0ODMtMDE2LTIwNzUtOA==/wan2016.pdf#view=FitH
	https://zero.sci-hub.tw/6599/9af7761843463b1b3eb7344dda0e7e59/wan2018.pdf#view=FitH

当程序下载pdf失败时，可以将上述网址复制到浏览器地址栏中手动下载

注意：为了保持数量上的一致性，如果给定的doi号找不到或者访问失败，也会为该doi输出一个链接记录，提示错误，如下：

	Error: searching failed for paper 1, no response
	Error: Paper : 2, 10.1016@j.petrol.2019.106452 not found or the sci-hub is not aviable

此时可以将这些记录对应的doi单独保存为一个doi.txt文件，重新尝试下载
