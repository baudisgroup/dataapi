import click
import json

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
	2. Does not provide page buffering, it's webserver's job.

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
	variant_sets = {'variant_set_id':'HG18'}
	return print( json.dumps(variant_sets) )




########################################################
# Retrieve one variant set
########################################################
@cli.command()
@click.argument('variant_set_id', required=True)
def GetVariantSet(variant_set_id):
	'''Gets one by ID'''
	a_variant_set = {'retrive':variant_set_id}
	return print( json.dumps(a_variant_set) )





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
@click.argument('start', required=True)
@click.argument('end', required=True)
@click.argument('call_set_ids', nargs=-1)
def SearchVariants(variant_set_id, reference_name, start, end, call_set_ids):
	'''Gets many by criteria '''
	variants = {
		'variant_set_id':variant_set_id,
		'reference_name':reference_name,
		'start':start,
		'end':end,
		'call_set_ids':call_set_ids
	}
	return print( json.dumps(variants) )



########################################################
# Retrieve one variant
########################################################
@cli.command()
@click.argument('variant_id', required=True)
def GetVariant(variant_id):
	'''Gets one by ID'''
	a_variant = {'variant_id':variant_id}
	return print( json.dumps(a_variant) )



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
	call_sets ={
		'variant_set_id':variant_set_id,
		'name': name,
		'bio_sample_id': bio_sample_id
	}
	return print( json.dumps(call_sets) )



########################################################
# Retrieve one call set
########################################################
@cli.command()
@click.argument('call_set_id', required=True)
def GetCallSet(call_set_id):
	'''Gets one by ID'''
	a_call_set = {'call_set_id': call_set_id}
	return print( json.dumps((a_call_set)) )




########################################################
# Retrieve a list of bio samples
########################################################
# Difference from GA4GH API:
# Does not provide page buffering, it's webserver's job.
@cli.command()
@click.argument('name', required=True)
def SearchBioSamples(name):
	'''Gets many by name'''
	biosamples = {'name':name}
	return print( json.dumps(biosamples) )




########################################################
# Retrieve one bio sample
########################################################
@cli.command()
@click.argument('bio_sample_id', required=True)
def GetBioSample(bio_sample_id):
	'''Gets one by ID'''
	a_bio_sample = {'bio_sample_id': bio_sample_id}
	return print( json.dumps(a_bio_sample) )





# main
if __name__ == '__main__':
    cli()