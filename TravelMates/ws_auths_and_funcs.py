from rest_framework_simplejwt.tokens import AccessToken

def headers_manage(headers):
    # print('dict headers : ', {key.decode('utf-8'): value.decode('utf-8') for key, value in headers})
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in headers}

def verify_and_get_token_payload_for_ws(scope):
    try:
        query_params = scope['query_string'].decode()
        # print(query_params,'query_params')
        token = query_params.split('=')[1]
        # print(token)
        try:
            access_token = AccessToken(token)
            payload = access_token.payload
            access_token.verify()
            return payload
        except Exception as e:
            return None
            return False, str(e)
    except Exception as e:
        return None
        return False, str(e)




