SIGNUP_EXISTING_USER_ERROR = {
    'status': False,
    'message': 'Username/Phone number/Email is used already',
    'code': 101
}

FAIL_LOGIN = {
    'status': False,
    'message': 'Username/password is wrong',
    'code': 201
}

MISSING_AUTHORIZATION_FIELD = {
    'status': False,
    'message': 'Header is missing the authorization field',
    'code': 301
}

BAD_AUTHORIZATION = {
    'status': False,
    'message': 'Value of the authorization field is not in the correct form',
    'code': 302
}

FORBIDDEN_RESPONSE = {
    'status': False,
    'message': 'Request is forbidden',
    'code': 303
}

EXPIRED_TOKEN = {
    'status': False,
    'message': 'Expired access token',
    'code': 304
}

INVALID_TOKEN = {
    'status': False,
    'message': 'Invalid Access Token',
    'code': 305
}

USER_NOT_FOUND = {
    'status': False,
    'message': 'User not found',
    'code': 401
}

BAD_UPDATING_PROFILE_FORM = {
    'status': False,
    'message': 'Invalid Updating Profile Form',
    'code': 402
}

EMAIL_TAKEN = {
    'status': False,
    'message': 'Email is used already',
    'code': 403
}

PHONE_TAKEN = {
    'status': False,
    'message': 'Phone number is used already',
    'code': 404
}

BAD_CARD_REQUEST = {
    'status': False,
    'message': 'Payload consists an invalid card code / password.',
    'code': 501
}

BAD_BET_REQUEST = {
    'status': False,
    'message': 'Bet type >= 0, Bet amount > 0',
    'code': 601
}

MATCH_NOT_FOUND = {
    'status': False,
    'message': 'Match not found',
    'code': 602
}

MATCH_FINISHED = {
    'status': False,
    'message': 'Match is finished',
    'code': 603
}

MATCH_LIVE = {
    'status': False,
    'message': 'Match is live, you can not bet',
    'code': 604
}

INVALID_BET_AMOUNT = {
    'status': False,
    'message': 'Bet amount must be lower than or equal to the balance of account',
    'code': 605
}

BET_ALREADY = {
    'status': False,
    'message': 'Bet this type already',
    'code': 606
}

BAD_COMMENT = {
    'status': False,
    'message': 'Comment must contain 1-300 character',
    'code': 607
}

