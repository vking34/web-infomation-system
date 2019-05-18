### Report

+ Architecture Design:
	+ Client-Server
	+ Client: Flux
	+ Server: Passive MVC, Domain Driven Design, Onion


+ Brief API docs:

  + Sign up: 
    + POST /signup

  + Login: 
    + POST /login

  + Update profile (USER):
    + PUT /api/users/<user_id>

  + Deposit money into the balance of an account (USER):
    + POST /api/users/<user_id>/balance

  + Comment on a match (USER):
  	+ POST /api/v1/matches/<match_id>/comments

  + Get comments of a match:
  	+ GET /api/v1/matches/<match_id>/comments

  + Bet on a match (USER):
   	+ POST /api/v1/matches/<match_id>/bets
	
  + Get user's bets on a match (USER):
  	+ GET /api/v1/matches/<match_id>/bets
	
	+ Get user's bet history (USER):
  	+ GET /api/v1/users/<user_id>/bets 

  + Get all leagues: x
   	+ GET /api/v1/leagues
  	
  + Add a league (ADMIN): x
   	+ POST /api/v1/leagues

  + Get details of a league: x
   	+ GET /api/v1/leagues/<league_id>

  + Update a league (ADMIN): x
   	+ PUT /api/v1/leagues/<league_id>

  + Delete a league (ADMIN): x
   	+ DELETE /api/v1/leagues/<league_id>

  + Get fixtures of matches filtered by start-date and stop-date | league_id: x
   	+ GET /api/v1/matches?from=2019-03-15&to=2019-03-21&league_id=<league_id>

  + Get fixtures of a match: x
   	+ GET /api/v1/matches/<match_id>
  

+ Details: 
	+ Content-Type: application/json

	+ Sign up for user:
    	+ POST /signup
    	+ Request Payload:
    		```
				{
					"username": "client1234",
					"password": "client",
					"name": "Tư",
					"email": "vking3413@gmail.com",
					"phone": "0326324233"
				}
    		```

    	+ Responses:
    		+ OK:
    			+ Status Code: 200 
    			+ Payload:
    				```
						{
							"status": true,
							"user": {
									"balance": 0,
									"email": "vking3413@gmail.com",
									"name": "Tư",
									"phone": "0326324233",
									"picture": "",
									"role": "ROLE_USER",
									"user_id": 11,
									"username": "client1234"
							}
						}
    				```
    		+ Bad request (Username is used already,...):
    			- Status Code: 400
    			- Payload:
    				```
						{
							"code": 101,
							"message": "Username/Phone number/Email is used already",
							"status": false
						}
    				```

    + Login:
    	- POST /login
    	- Request payload:
    		```
				{
					"username": "client123",
					"password": "vking34"
				}
    		```
    	
    	- Responses:
    		+ OK:
    			- Status Code: 200
    			- Payload:
					```
					{
						"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTc2NjQ2OTMsImlhdCI6MTU1NzY1MDI5Mywic3ViIjoxMCwicm9sZSI6IlJPTEVfVVNFUiIsInVzZXJuYW1lIjoiY2xpZW50MTIzIn0.EfIFiaYknUou_4jr5f5D_TKeDwjxQdJWEKpGuqtngQ0",
						"status": true,
						"user": {
							"balance": 10400,
							"email": "vking3414@gmail.com",
							"name": "Dũng",
							"phone": "0362225678",
							"picture": "",
							"role": "ROLE_USER",
							"user_id": 10,
							"username": "client123"
						}
					}
					```

    		+ Bad request (Username/password is wrong,...):
    			- Status Code: 400
    			- Payload:
    				```
						{
							"code": 201,
							"message": "Username/password is wrong",
							"status": false
						}
    				```
	+ Update profile:
    	+ PUT /api/v1/users/<user_id>
    	+ Header: Authorization: Bearer <user_token>
    	+ Request Payload:
			```
			{
				"name": "Tân",
				"email": "vking3401@gmail.com",
				"phone": "0362225678"
			}
			```
		+ Responses:
    		+ OK:
        		+ Status Code: 200
        		+ Payload:
    				```
						{
							"status": true,
							"user": {
								"balance": 10400,
								"email": "vking3401@gmail.com",
								"name": "Tân",
								"phone": "0362225678",
								"role": "ROLE_USER",
								"user_id": 10,
								"username": "client123"
							}
						}
    				```
			+ Bad request (email is used already,...)
    			+ Status Code: 400
    			+ Payload:
    				```
						{
							"code": 403,
							"message": "Email is used already",
							"status": false
						}
    				```
	+ Deposit money into balance:
    	+ POST /api/v1/users/<user_id>/balance
    	+ Header: Authorization: Bearer <user_token>
    	+ Request Payload:
			```
			{
				"card_code": "string",
				"password": "string"
			}
			```
		+ Responses:
    		+ OK:
        		+ Status Code: 200
        		+ Payload:
					```
					{
						"status": true,
						"bill": 
						{
							"card_amount": int,
							"previous_balance": int,
							"balance": int,
							"deposit_time": "2019-03-22T20:00:00Z"
						}
					}
			+ Bad request (wrong card code):
    			+ Status Code: 400
    			+ Payload:
    				```
    				{
    				"status": false,
    				"message": "string",
    				"code": int
    				}
    				```
	
	+ Comment on a match (USER):
      + POST /api/v1/matches/<match_id>/comments
      + Header: Authorization: Bearer <user_token>
  		+ Request payload:
			```
			{
				"comment": "Goal!!!"
			}
			```
		+ Responses:
			+ OK:
				+ Status Code: 200
				+ Payload:
					```
					{
						"data": {
								"comment": "Goal!!!",
								"match_id": 410600,
								"time": "2019-05-11T16:22:18",
								"user_id": 10
						},
						"status": true
					}
					```
			+ Bad request:
				+ Status Code: 400
				+ Payload:
					```
						{
								"code": 602,
								"message": "Match not found",
								"status": false
						}
    				```
	+ Get comments of a match:
    	+ GET /api/v1/matches/<match_id>/comments
    	+ Params:
        	+ number: int		(get number of comments)
    	+ Response:
      	+ OK:
        	+ Status code: 200
        	+ Payload:
				```
						{
							"data": 
							[
								{
									"comment": "Goal!!!",
									"time": "2019-05-09T17:12:33",
									"user": {
										"name": "Dũng",
										"user_id": 10
									}
								},
								{
									"comment": "Messi hay nhưng không gánh đc team",
									"time": "2019-05-09T17:11:18",
									"user": {
										"name": "Dũng",
										"user_id": 10
									}
								}
							]
						}
				```
  + Get user's bets on a match (USER):
  	+ GET /api/v1/matches/<match_id>/bets
    + Header: Authorization: Bearer <user_token>
    + Response:
      + OK:
        + Status code: 200
        + Payload:

					```
					{
						"bets": [
							{
								"bet_amount": 200,
								"bet_content": "2-1",
								"bet_gain": 0,
								"bet_status": "PROCESSING",
								"bet_time": "2019-05-11T16:50:40",
								"bet_type": 1,
								"user_id": 10
							}
						],
						"status": true
					}
					```
        + Bad Request:
          + Status: 400
          + Payload: 
			```
				{
					"code": 602,
					"message": "Match not found",
					"status": false
				}
			```
					

  + Bet on a match (USER):
    + POST /api/v1/matches/<match_id>/bets
    + Header: Authorization: Bearer <user_token>
    + Request payload:
    	```
    	{
    		"bet_type": 1,
    		"bet_amount": 200,
    		"bet_content": "2-1"
    	}
    	```
    + Response:
    	+ OK:
    		+ Status Code: 200
    		+ Payload:
    		```
    		{
    			"bet": {
    					"bet_amount": 200,
    					"bet_content": "2-1",
    					"bet_status": "PROCESSING",
    					"bet_time": "2019-05-11T16:50:40",
    					"bet_type": 1,
    					"match_id": 413094,
    					"user_id": 10
    			},
    			"status": true
    		}
    		```
    	+ Bad request (Balance not enough,... ):
    		+ Status Code: 400
    		+ Payload:
    			```
      				{
      				"status": false,
      				"message": "string",
      				"code": int
      				}
      				```
    	+ Pusher Response:
    		```
    		{
    			"match": {
    				"match_id":410609,
    				"league_id":128,
    				"match_awayteam_name":"Le Havre",
    				"match_hometeam_name":"Valenciennes",
    				"match_hometeam_halftime_score":0,
    				"match_awayteam_halftime_score":0,
    				"match_hometeam_score":1,
    				"match_awayteam_score":0,
    				"yellow_card":0,
    				"match_status":"FT",
    				"match_date":"2019-05-10",
    				"match_time":"18:45"
    			},
    			"bet_type":2,
    			"bet_amount":200,
    			"bet_content":"1-0",
    			"bet_time":"2019-05-12T11:38:55",
    			"bet_status":"WIN",
    			"bet_gain":600
    		}
    		```

  + Get user's bet history (USER):
  	+ GET /api/v1/users/<user_id>/bets
  	+ Header: Authorization: Bearer <user_token>
  	+ Response:
    	+ OK:
      	+ Code Status: 200
      	+ Payload: 

				```
				{
					"bets": [
						{
							"bet_amount": 200,
							"bet_content": "1-0",
							"bet_gain": 600,
							"bet_status": "WIN",
							"bet_time": "2019-05-12T11:38:55",
							"bet_type": 2,
							"match": {
									"league_id": 128,
									"match_awayteam_halftime_score": 0,
									"match_awayteam_name": "Le Havre",
									"match_awayteam_score": 0,
									"match_date": "2019-05-10",
									"match_hometeam_halftime_score": 0,
									"match_hometeam_name": "Valenciennes",
									"match_hometeam_score": 1,
									"match_id": 410609,
									"match_status": "FT",
									"match_time": "18:45",
									"yellow_card": 0
							},
							"user_id": 10
						}
					],
					"status": true
				}
				```
    	+ Forbidden:
  			+ Code status: 403
  			+ Payload:
				```
				{
					"code": 305,
					"message": "Invalid Access Token",
					"status": false
				}
				```

  + Get leagues:
  	- GET /api/v1/leagues
  	- Responses:
  		+ OK:
      		- Status Code: 200
      		- Payload:
      			```
      			[
      				{
      				"league_id": int,
      				"league_name": "string",
      				"country": "string"
      				}
      			]
      			```

  + Add a league (ADMIN):
    + POST /api/v1/leagues
    + Header: Authorization: Bearer TOKEN
    + Request Payload:

				```
				{
					"league_id": int,
					"league_name": "string",
					"country": "string"
				}
				```

    + Responses:
    	+ OK:
    		+ Status: 200
    		+ Payload: 
    			```
    			{
    				"status": true,
    				"league":
    						{
    						"league_id": int,
    						"league_name": "string",
    						"country": "string"
    						}
    			}
    			```
  			
    	+ Bad request (League exists, ...):
    		+ Status Code: 400
    		+ Payload:
    			```
    			{
    			"status": false,
    			"message": "string",
    			"code": int
    			}
    			```
    	+ Forbidden (User create league,...):
    		+ Status Code: 403
    		+ Payload:
    			```
    			{
    			"status": false,
    			"message": "string",
    			"code": int
    			}
    			```

  + Get a league:
    + GET /api/v1/leagues/<league_id>
    + Response:
    	+ OK: 
    		+ Status Code: 200
    		+ Payload:
    			```
    			{
          				"league_id": int,
          				"league_name": "string",
          				"country": "string"
          			}
    			```
	
  + Update a league (ADMIN):
    + PUT /api/v1/leagues/<league_id>
    + Header: Authorization: Bearer TOKEN
    + Request Payload: 
    	```
    	{
    		"league_name": "string",
    		"country": "string"
    	}
    	```
    + Responses:
    	+ OK:
    		+ Status Code: 200
    		+ Payload:
    			```
    			{
    				"status": true,
    				"league": {
    					"league_id": int,
    					"league_name": "string",
    					"country": "string"
    				}
    			}
    			```

			+ Bad request (name league is used already)
            	+ Status Code: 400
				+ Payload:
					```
					{
					"status": false,
					"message": "string",
					"code": int
					}
					```

  + Delete a league (ADMIN):
    + DELETE /api/v1/leagues/<league_id>
    + Header: Authorization: Bearer TOKEN
    + Responses:
  		+ OK:
        	+ Status: 200
        	+ Payload: 

				```
					{
						"status": true,
						"league":
							{
							"league_id": int,
							"league_name": "string",
							"country": "string"
							}
					}
				```

    	+ Bad request (League doesn't exist, ...):
    		+ Status Code: 400
    		+ Payload:

				```
				{
				"status": false,
				"message": "string",
				"code": int
				}
				```

      + Forbidden (User delete league,...):
      	+ Status Code: 403
      	+ Payload:
      		```
      		{
      		"status": false,
      		"message": "string",
      		"code": int
      		}
      		```

  + Get fixtures of matches filtered by start-date and stop-date | league_id:
    + GET /api/v1/matches?from=2019-03-15&to=2019-03-21&league_id=<league_id>
    + Response:
      + OK:
        + Status Code: 200
        + Payload:
			```
			[
				{
					"match_id": int,
					"league_id": int,
					"match_date": "2019-03-20",
					"match_time": "15:00",
					"match_hometeam_name": "string",
					"match_awayteam_name": "string",
					"match_hometeam_halftime_score": int,
					"match_awayteam_halftime_score": int,
					"match_hometeam_score": int,
					"match_awayteam_score": int,
					"yellow_card": int
				}
			]
			```
	
  + Get fixtures of a match:
    + GET /api/v1/matches/<match_id>
    + Response:
      + OK:
        + Status Code: 200
        + Payload:
			```
			{
				"match_id": int,
				"league_id": int,
				"match_date": "2019-03-20",
				"match_time": "15:00",
				"match_hometeam_name": "string",
				"match_awayteam_name": "string",
				"match_hometeam_halftime_score": int,
				"match_awayteam_halftime_score": int,
				"match_hometeam_score": int,
				"match_awayteam_score": int,
				"yellow_card": int
			}
			```

  + Millionaires ranking 
  	+ GET /api/v1/users/millionaies
		+ Responses:
			+ OK:
				+ Status Code: 200
				+ Payload:
					```
					[
						{
							"username": "string",
							"name": "string",
							"balance": int
						},
						{
							"username": "string",
							"name": "string",
							"balance": int
						}
					]
					```	
