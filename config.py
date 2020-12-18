def digest_self_config(object):
    if hasattr(object,'CONFIG'):
        for key in object.CONFIG.keys():
            setattr(object,key,object.CONFIG[key])
