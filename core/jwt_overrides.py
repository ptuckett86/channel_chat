def jwt_response_payload_handler(token, user=None, request=None):
    if user.is_authenticated:
        return {
            "token": token,
            "uuid": user.pk,
        }