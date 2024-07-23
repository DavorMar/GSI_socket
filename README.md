 # GSI_socket

 A small server module that receives data from Dota or Counter strike Game state integration and transmits further to connected clients. 
 Made for maximum transmittion speed with least delay. Game state integration is part of dota / csgo games, where the game sends post requests
 continously, consisting of detailed in game data at the moment. The server receives these post requests, unpacks and cleans the data and transmits
 to clients connected via socket stream.

 
