# coding = utf-8

import pickle
import faiss
import json
import main_conf

import contriever.src.contriever as csc
import contriever.src.normalize_text as csn

class ESearch:

	def __init__(self,efname,dfname,mname):
		self.fea_dict = []
		# 反序列化对象，将文件中的数据解析为一个Python对象
		f_load = open(main_conf.home_path+'/embeddings/'+efname, 'rb')
		ids,embeddings = pickle.load(f_load)
		f_load.close()
		
		for line in open(main_conf.home_path+'/data/'+dfname):
			line = line.strip()
			self.fea_dict.append(json.loads(line))
		
		self.index = faiss.IndexFlatL2(embeddings.shape[1])             
		self.index.add(embeddings)                   # 将向量库中的向量加入到index中
		
		self.model, self.tokenizer, _ = csc.load_retriever(mname)
		self.model.eval()
	
	
	def embed_query(self,q):
		q = q.lower()
		q = csn.normalize(q)
	
		inputs = self.tokenizer([q], padding=True, truncation=True, return_tensors="pt")
		output = self.model(**inputs)
	
		return output.detach().numpy()
	
	def get_top_5(self,query):
		query_emb = self.embed_query(query)
	
		D,I = self.index.search(query_emb,5)
		outfeas = []
		for i in range(5):
			outfeas.append({'rank':i, 'score':float(D[0][-1*i-1]), 'msg':self.fea_dict[I[0][i]]})
		return outfeas

	def get_top_n(self,query,n=10):
		query_emb = self.embed_query(query)
	
		D,I = self.index.search(query_emb,n)
		outfeas = []
		for i in range(n):
			outfeas.append({'rank':i, 'score':float(D[0][-1*i-1]), 'msg':self.fea_dict[I[0][i]]})
		return outfeas

#ww = ESearch()
#print(ww.get_top_5('小冰董事长是谁'))

#ww = ESearch()
#print(ww.get_top_5('小冰董事长是谁'))

