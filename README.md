# NITRAWF BOT
## About
This bot is used in conjuction with an api built by [nitrawf](https://github.com/nitrawf) to track elos of players in a country based on the matches they played within the country in osu.

Here's a documentation of the basic commands of the bot:


## Fetch players:

```
$players {-p i}
```

Fetches players ordered by rank and displays it as a table. Currently incompatible with portrait mode on mobile devices. Shows 5 per page. The argument `-p i` where `i` is a number is for the page you'd like to see is optional (default page 1).

## Fetch a single player's summary:

```
$player "username"
```

Fetches the stats of a player with the username "username" (Note: only need to use double quotes if the username has spaces in it).

## Fetch the elo history of a player:

```
$elohistory "username"
```

Fetches the elo history of a player as a graph (.png format) with the username "username" (Note: only need to use double quotes if the username has spaces in it).

## Fetch the matches that have been played:

```
$matches {-p i}
```

Fetches a list of all matches that have been registered including their start and end times. Shows 5 per page. The argument `-p i` where `i` is a number is for the page you'd like to see. Incompatible with portrait mode on mobile devices.

## Fetch the details of a specific match:

```
$match {matchid}
```

Fetches the summary (players, stats) from the given match id. Needs the match id (not the lobby name) to work. You can get the match id from the link (For example osu.ppy.sh/matches/3264734 -> 3264734). Incompatible with portrait mode on mobile devices.

