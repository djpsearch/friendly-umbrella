from datetime import datetime
from elasticsearch import Elasticsearch
from json import loads

######
# file:    load_training.py
# date:    20180917 
# status:  draft
# version: 0.2
# authors: djptek
# purpose: index multiple documents to elastic via python api
######
 
# set to your elastic host (default the docker instance)
es = Elasticsearch([
    {'host': '0.0.0.0'}
])

training_index = 'training'
training_type = 'example'
training_datafile = '../data/training_docs.json'

# delete ALL indexes to ensure starting afresh
res = es.indices.delete(
    index="_all", 
    ignore=[400, 404])
 
res = es.indices.create(
    index=training_index, 
    ignore=[400, 404], 
    body="""
{
    "settings" : {
        "index" : {
            "number_of_shards" : 1, 
            "number_of_replicas" : 0 
        }
    }
}
""")

# check delete OK likewise accept if Index did not exist
if ('acknowledged' in res.keys() or 
      ('error' in res.keys() and 
       res['error']['root_cause'][0]['type'] == u'index_not_found_exception')):
   print 'populating index [{}]'.format(training_index)

   # open the example docs datafile
   training_docs = open(training_datafile,'r')

   # iterate through the file creating example documents in the index
   for training_doc in training_docs:
      doc = loads(training_doc)   
      res = es.index(index=training_index, doc_type=training_type, body=doc)
      print 'doc [{}] tag [{}] indexed : id [{}]'.format(
         doc['doc']['name'],doc['doc']['tag'],res['_id'])


   # close file on disk
   training_docs.close()
    
else:
   # flag issue with the index
   print 'issue deleting [{}] result [{}]'.format(training_index,str(res))

