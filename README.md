# auction_site
In this project I have included both password based login and token based authentication. But login based authentication was implemented fully and for some tasks token based authentication was implemented.
# Admin:
Admin was given perissions for entire CURD operations on Auctions and delete permission for managing user.
<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/31917a4b-b13b-4a02-98d8-27fb92b068d1">

<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/2960639b-52b7-47e5-bcf2-80b0e90cbc39">

<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/2ebbdaa0-2d77-4987-8c65-941cda1e42cb">

<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/1a66c9bd-9fbc-4f7a-9757-f64ca0fc9b4c">

# User:
Through login based authentication, user can create a account and login and then a token will be provided to them. After logging in user can be able to view all the auctions that are live, completed and upcoming. <br>
User can bid for the live auctions and they were provided with the highest bidder and amount.<br>
User can bid any number of times for the auction until it ends.<br>
As soon as the time ends, winner will be declared and shown in the completed auctions.
<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/725a4821-f73b-4958-92cd-4457f02caa33">

<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/820b1ccc-6da6-4054-8b25-78540584f8dd">

<img width="960" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/2faa2b49-07fa-4f23-bba9-d4b0a64da32e">

# Using Token based authentication:
User can be able to seee all their biddings:<br>
http http://127.0.0.1:8000/my_biddings "Authorization: Token 55a560e616f80ce393212abae3b20ff15b6cd398"

<img width="454" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/42dacf61-7ca9-488d-8c78-da373aeca06d">

User can be able to see all available auctions:<br>
http http://127.0.0.1:8000/all_auctions "Authorization: Token 55a560e616f80ce393212abae3b20ff15b6cd398"

<img width="455" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/95c6a7b0-606d-49c7-9176-678db560ecb2">
<img width="217" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/a338b502-00aa-4079-8001-ef07a474d428">

User can be able to place the bid for an auction that is live:<br>
http http://127.0.0.1:8000/auction_bid/14/2750 "Authorization: Token 55a560e616f80ce393212abae3b20ff15b6cd398"

<img width="481" alt="image" src="https://github.com/Giridhar57/auction_site/assets/80587128/44cce28f-bd9e-4b97-a7d8-3839d506781d">

