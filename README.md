# NITRAWF BOT TODOS:

The bot needs to be able to fetch the following:
- “$players -p i”, i=number : Fetch the ith page of the player rankings as a table
- “$player username” username=osu username: Fetch the stats of user named username and display
- “$matches username {-p i}” fetch matches that username has played and display (should display in pages of 5)
- *low priority* “$elohistory username” show image of graph of user’s elo history
- “$matches -p i” : Fetch matches of page i (sorted by recent) (show 5 per page)
- *low priority* “$match matchid” : Fetch match details given a match id

API routes necessary:
- Get all players by rank (add other sort methods later) - Done
- Get specific player - Done
- Get matches of specific player
- Get matches by recent (add other sort methods later)
- Get match from match id and display summary
- Get elo history of specific player