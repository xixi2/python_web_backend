def get_req_url(options):
    ip = options.ip
    port = options.port
    api_name = options.api_name
    params = options.params
    url = "http://%s:%s%s?%s" % (ip, port, api_name, params)
    return url
