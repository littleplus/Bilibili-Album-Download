#encoding=utf-8
import requests,os,sys

basicApiUrl='https://api.vc.bilibili.com/link_draw/v1/doc/upload_count?uid='
apiUrl='https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?page_size=30&biz=all&uid='

# Get the amount of all draws
# If error return 0
def getTotalDraw(bid):
	try:
		req=requests.get(basicApiUrl+bid)
		rspJson = req.json()
	except:
		return 0
	
	if('data' in rspJson and 'all_count' in rspJson['data']):
		return int(rspJson['data']['all_count'])
		
	return 0

# Get the draw list, 30 draws in each page
def downloadDrawList(bid,page):
	url = apiUrl+bid
	
	# Add page num
	url = url+'&page_num='+str(page)
	
	try:
		req=requests.get(url,timeout=5)
		rspJson = req.json()
		
		# Get all items in a range
		items = rspJson['data']['items']
		
		for i in items:
			urls = {}
			did = str(i['doc_id'])
			
			# Single item traversal
			count = 0
			for j in i['pictures']:
				urls[count]=j['img_src']
				count+=1
			
			# Download
			downloadDraw(bid,did,urls)
	except Exception as e:
		print(e)
		pass

# Download draws
def downloadDraw(bid,did,urls):
	count = 0
	for i in range(len(urls)):
		u = urls[i]
		try:
			# Get image format from url
			suffix = u.split(".")[-1]
			
			# File naming
			## bid: Bilibili user id
			## did: Draw id
			fileName = did+'_b'+str(count)+'.'+suffix
			
			if(os.path.exists('./'+bid+'/'+fileName)):
				print('Skipped '+did+' '+u)
				count+=1
				continue
			print('Downloading '+did+' '+u)
			# Download single image
			req = requests.get(u,timeout=20)			
			# Create image file
			with open('./'+bid+'/'+fileName,'wb') as f:
				f.write(req.content)
		except Exception as e:
			print(e)
			print('Fail to download: '+did+' '+u)
			
		count+=1

if __name__=='__main__':
	if(len(sys.argv)<2):
		print('Please enter the bilibili user id.')
		sys.exit(0)
	
	bid = str(sys.argv[1])
	
	# Create drawer's directory
	try:
		os.makedirs('./'+bid)
	except:
		pass

	totalDraw = getTotalDraw(bid)
	totalPage = int(totalDraw/30)+1 if totalDraw % 30 != 0 else totalDraw/30
	for page in range(totalPage):
		downloadDrawList(bid,page)
	
