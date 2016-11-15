import click
import json
from pymongo import MongoClient
from datetime import datetime
import sys

# init database names
dbname = 'arraymap'
collection_name_individuals = 'individuals'
collection_name_biosamples = 'biosamples'
collection_name_variants = 'variants'
collection_name_callsets = 'callsets'
collection_name_variantsets = 'variantsets'

# init database handlers
db = MongoClient()[dbname]
individuals = db[collection_name_individuals]
biosamples = db[collection_name_biosamples]
variants = db[collection_name_variants]
callsets = db[collection_name_callsets]
variantsets = db[collection_name_variantsets]




def searchvs():
	'''search all variant sets'''
	ret = []
	for i in db[collection_name_variantsets].find({},{'_id':0}):
		ret.append(i)
	return ret

#need to refine
def searchv(vs_id, r_name, start, end, cs_ids):
	'''search variants by criteria'''
	if start > end:
		print('Error: start > end.')
		sys.exit()

	ret = []
	if len(cs_ids) < 1:
		token_csids = '}'
	else:
		token_csids = ", 'calls.call_set_id':{'$in':"+ str(list(cs_ids)) + "} }"
	token_const = "{'variant_set_id':vs_id, 'reference_name': r_name,"
	token_cond =[]
	token_cond.append( "'start': {'$lt':%i}, 'end':{'$gt':%i, '$lte':%i}" % (start, start, end) )
	token_cond.append( "'start': {'$gte':%i, '$lt':%i}, 'end':{'$gt':%i}" % (start, end, end) )
	token_cond.append( "'start': {'$gt':%i}, 'end':{'$lt':%i}" % (start, end) )
	token_cond.append( "'start': {'$lte':%i}, 'end':{'$gte':%i}" % (start, end) )

	for cond in token_cond:
		query = token_const + cond + token_csids
		for i in db[collection_name_variants].find(eval(query),{'_id':0}):
			ret.append(i)
	return ret

def searchcs(vs_id, name, bs_id):
	'''search call sets by criteria'''
	ret = []
	for i in db[collection_name_callsets].find({'variant_set_id': vs_id, 'name': name, 'bio_sample_id': bs_id},{'_id':0}):
		ret.append(i)
	return ret

def searchbs(name):
	'''search biosamples by name'''
	ret = []
	for i in db[collection_name_biosamples].find({'name': name},{'_id':0}):
		ret.append(i)
	return ret

def getvs(vs_id):
	'''get a variant set by id'''
	return db[collection_name_variantsets].find_one({'id': vs_id },{'_id':0})

def getv(v_id):
	'''get a variant by id'''
	return db[collection_name_variants].find_one({'id': v_id },{'_id':0})

def getcs(cs_id):
	'''get a call set by id'''
	return db[collection_name_callsets].find_one({'id': cs_id },{'_id':0})

def getbs(bs_id):
	'''get a biosample by id'''
	return db[collection_name_biosamples].find_one({'id': bs_id },{'_id':0})



def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")



# NOTE: bio_sample_id will soon morph into biosample_id


@click.group()
def cli():
	'''
	This CLI implements the GA4GH schema service API for a local database:

	\b
	getbiosample       req: bio_sample_id
	getcallset         req: call_set_id
	getvariant         req: variant_id
	getvariantset      req: variant_set_id
	searchbiosamples   req: name
	searchcallsets     req: variant_set_id, name, bio_sample_id
	searchvariants     req:	variant_set_id, reference_name, start, end; opt: call_set_ids
	searchvariantsets  req: none

	\b
	Examples:
	>python3 dataAPI.py searchvariantsets
	>python3 dataAPI.py getvariant v_id123
	>python3 dataAPI.py searchvariants vs_id123, rn_18, 1000, 2400, cs_id_01, cs_id_02, cs_id_03

	\b
	Difference from GA4GH API:
	1. Does not support dataset_id argument.
	2. Does not provide page buffering, it's the webserver's job.

	'''
	pass




########################################################
# Retrieve all variant sets in the current database
########################################################
# Difference from GA4GH API:
# 1. Does not support dataset argument.
# 2. Does not provide page buffering, it's webserver's job.
@cli.command()
def SearchVariantSets():
	'''Gets all'''
	return print( json.dumps( searchvs(), default=json_serial) )




########################################################
# Retrieve one variant set
########################################################
@cli.command()
@click.argument('variant_set_id', required=True)
def GetVariantSet(variant_set_id):
	'''Gets one by ID'''
	return print( json.dumps( getvs(variant_set_id), default=json_serial) )





########################################################
# Retrieve a list of variants
########################################################
# Difference from GA4GH API:
# Does not provide page buffering, it's webserver's job.
#
# NOTE:
# call_set_ids can have none or many args.
@cli.command()
@click.argument('variant_set_id', required=True)
@click.argument('reference_name', required=True)
@click.argument('start', type=int, required=True)
@click.argument('end', type=int, required=True)
@click.argument('call_set_ids', nargs=-1)
def SearchVariants(variant_set_id, reference_name, start, end, call_set_ids):
	'''Gets many by criteria '''
	return print( json.dumps(searchv(variant_set_id, reference_name, start, end, call_set_ids), default=json_serial) )



########################################################
# Retrieve one variant
########################################################
@cli.command()
@click.argument('variant_id', required=True)
def GetVariant(variant_id):
	'''Gets one by ID'''
	return print( json.dumps( getv(variant_id), default=json_serial) )



########################################################
# Retrieve a list of call sets
########################################################
# Difference from GA4GH API:
# Does not provide page buffering, it's webserver's job.
@cli.command()
@click.argument('variant_set_id', required=True)
@click.argument('name', required=True)
@click.argument('bio_sample_id', required=True)
def SearchCallSets(variant_set_id, name, bio_sample_id):
	'''Gets many by criteria'''
	return print( json.dumps( searchcs(variant_set_id, name, bio_sample_id) ) )



########################################################
# Retrieve one call set
########################################################
@cli.command()
@click.argument('call_set_id', required=True)
def GetCallSet(call_set_id):
	'''Gets one by ID'''
	return print( json.dumps( getcs(call_set_id), default=json_serial) )




########################################################
# Retrieve a list of bio samples
########################################################
# Difference from GA4GH API:
# Does not provide page buffering, it's webserver's job.
@cli.command()
@click.argument('name', required=True)
def SearchBioSamples(name):
	'''Gets many by name'''
	return print( json.dumps( searchbs(name) ) )




########################################################
# Retrieve one bio sample
########################################################
@cli.command()
@click.argument('bio_sample_id', required=True)
def GetBioSample(bio_sample_id):
	'''Gets one by ID'''
	return print( json.dumps( getbs(bio_sample_id), default=json_serial) )





# main
if __name__ == '__main__':
    cli()
