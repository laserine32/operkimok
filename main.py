import os
import hashlib
import json

def scandir(path):
	ret = []
	obj = os.scandir(path)
	for entry in obj :
		if entry.is_dir() or entry.is_file():
			ret.append(entry.name)
	return ret		

def hasilkan(file, gh=False):
	data = []
	mainpath = "data"
	for i,mp in enumerate(scandir(mainpath)):
		mainorder = ("000"+str(i+1))[-3:]
		tmpd = {
			"id": hashlib.md5(mp.encode()).hexdigest(),
			"komik": mp,
			"poster": "",
			"chapter": []
		}
		chapter_path = os.path.join(mainpath, mp)
		for j, chp in enumerate(scandir(chapter_path)):
			order = mainorder+"-"+("000"+str(j+1))[-3:]
			tmpc = {
				"id": hashlib.md5(f"{mp}{chp}".encode()).hexdigest(),
				"title": chp,
				"link": "",
				"order": order,
				"thumb": "",
				"data": []
			}
			page_dir = os.path.join(chapter_path, chp)
			for k, pg in enumerate(scandir(page_dir)):
				fn = os.path.join(page_dir, pg)
				fn = fn.replace("\\", "/")
				if gh:
					fn = "https://raw.githubusercontent.com/laserine32/operkimok/master/"+fn
				if k == 0:
					tmpd["poster"] = fn
					tmpc["thumb"] = fn
				tmpc["data"].append(fn)
			tmpd["chapter"].append(tmpc)
		data.append(tmpd)
		# break
	# print(json.dumps(data, indent=2))
 	
	with open(file, "w") as f:
		json.dump(data, f)

if __name__ == '__main__':
	print("READY")
	hasilkan("data.json")
	hasilkan("data_gh.json", True)
	print("ALL DONE")