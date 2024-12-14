from elasticsearch import Elasticsearch

es = Elasticsearch(["http://9.197.242.150:9200"])

# 驗證是否連線成功
if es.ping():
    print("Successfully connected to Elasticsearch!")
else:
    print("Failed to connect to Elasticsearch.")

def list_index_name(es):
    # 列出所有索引名稱
    try:
        indices = es.indices.get_alias(index="*")
        index_names = list(indices.keys())
        print("Indices in Elasticsearch:")
        for index in index_names:
            print(index)
    except Exception as e:
        print(f"Error retrieving indices: {e}")

ES = Elasticsearch("http://9.197.242.150:9200", verify_certs=False)
# list_index_name(ES)
_index = "cpu-2024.12.01"
results = ES.search(index=_index, body={"query": {"match_all": {}}})
print(len(results['hits']['hits']))

if len(results['hits']['hits']) == 0:
    print("No data need to generate category")

else:
    print(f"Start print data for {len(results['hits']['hits'])} datas")
    for i, record in enumerate(results['hits']['hits']):
        print(i)
        print(record['_source'])
# ES.index(index=_index, id=_id, body=document)
# ES.update(index=_index, id=_id, body={"doc": {"column": 'true'}})