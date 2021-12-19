import time, datetime
import requests, os, sys, math


basicApiUrl = "https://api.vc.bilibili.com/link_draw/v1/doc/upload_count?uid="
apiUrl = (
    "https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?page_size=30&biz=all&uid="
)
headers = {
    "Referer": "https://space.bilibili.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
}

# Get the amount of all draws
# If error return 0
def getTotalDraw(bid):
    try:
        req = requests.get(basicApiUrl + bid, headers=headers)
        rspJson = req.json()
    except:
        return 0

    if "data" in rspJson and "all_count" in rspJson["data"]:
        return int(rspJson["data"]["all_count"])

    return 0


# Get the draw list, 30 draws in each page
def downloadDrawList(bid, page, base_dir='~/Photos'):
    # Create drawer's directory
    usr_dir = os.path.join(base_dir, bid)
    try:
        os.makedirs(usr_dir)
    except:
        pass

    url = apiUrl + bid

    # Add page num
    url = url + "&page_num=" + str(page)

    try:
        req = requests.get(url, timeout=5, headers=headers)
        rspJson = req.json()

        # Get all items in a range
        items = rspJson["data"]["items"]

        for i in items:
            urls = {}
            did = str(i["doc_id"])

            # convert date from ctime in response
            date = datetime.datetime.strptime(
                time.ctime(i["ctime"]), "%a %b %d %H:%M:%S %Y"
            ).strftime("%Y_%m_%d")

            desc = i["description"]

            # Single item traversal
            count = 0
            for j in i["pictures"]:
                urls[count] = j["img_src"]
                count += 1

            # Download
            downloadDraw(bid, did, urls, usr_dir, date, desc)
    except Exception as e:
        print(e)
        pass


# Download draws
def downloadDraw(bid, did, urls, usr_dir, date, desc):
    if len(desc.strip()) <= 10:
        subdir = "{}_{}".format(date, desc.strip())
    else:
        subdir = "{}_{}".format(date, desc.strip()[:10])
    subdir_path = os.path.join(usr_dir, subdir)
    print("Image saved in", subdir_path)
    os.makedirs(subdir_path)

    with open(os.path.join(subdir_path, "description.txt"), "w") as dsec_file:
        dsec_file.write(desc)

    count = 0
    for i in range(len(urls)):
        img_url = urls[i]
        try:
            # Get image format from url
            suffix = img_url.split(".")[-1]

            # File naming
            ## bid: Bilibili user id
            ## did: Draw id
            fileName = did + "_b" + str(count) + "." + suffix

            if os.path.exists("./" + bid + "/" + fileName):
                print("Skipped " + did + " " + img_url)
                count += 1
                continue
            print("Downloading " + did + " " + img_url)
            # Download single image
            req = requests.get(img_url, timeout=20, headers=headers)
            # Create image file
            # './'+bid+'/'+fileName
            with open(os.path.join(subdir_path, fileName), "wb") as f:
                f.write(req.content)
        except Exception as e:
            print(e)
            print("Fail to download: " + did + " " + img_url)

        count += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please enter the bilibili user id.")
        sys.exit(0)

    bid = str(sys.argv[1])

    totalDraw = getTotalDraw(bid)
    totalPage = math.ceil(totalDraw / 30)
    for page in range(totalPage):
        downloadDrawList(bid, page, base_dir='~/Photos')
