# coding = utf-8
import json
import yaml

mconf = yaml.load(open('../project.yaml').read())
home_path = mconf['home_path']
ori_data_file = home_path+"/data/harry_baike&news.json"
out_data_file = home_path+"/data/harry_data.jsonl"

fw = open(out_data_file,'w',encoding='utf-8')
n = 0
for k,v in enumerate(json.load(open(ori_data_file,encoding='utf-8'))):
	p_len = 0
	p_begin_id = 0
	for i,j in enumerate(v['content']):
		if p_len > 0 and p_len+len(j) > 512:
			fw.write(json.dumps(
				{'id':n,
				'title':v['title'],
				'text':' '.join(v['content'][p_begin_id:i]),
				'doc_id':k,
				'p_begin_id':p_begin_id,
				'p_num':i-p_begin_id,
				'passages':v['content'][p_begin_id:i]},ensure_ascii=False))
			fw.write('\n')
			p_len =0
			p_begin_id = i
			n += 1
		p_len += len(j)
	if p_len > 0:
		fw.write(json.dumps(
			{'id':n,
			'title':v['title'],
			'text':' '.join(v['content'][p_begin_id:]),
			'doc_id':k,
			'p_begin_id':p_begin_id,
			'p_num':len(v['content'])-p_begin_id,
			'passages':v['content'][p_begin_id:]},ensure_ascii=False))
		fw.write('\n')
		n += 1

fw.close()

