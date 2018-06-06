# Colts-Cogs
Things will most likely not work.


## Cogs
- autorole:       Automatically give members who join the server a specified role</li>


## More cog information
### Autorole
#### Note:
If you want the users to recieve the role immediately, do NOT set an agreement channel

This cog allows you to automatically assign new members of your server a role.
##### Usage:
- `[p]autorole` displays help for autorole commands and shows whether autorole is on or off.
- `[p]autorole role (the role's name [use quotes if the name has a space])` sets the role to be given to new users.
- `[p]autorole toggle` switches the state of automatic role assignment.
- `[p]autorole agreement (#channel_for_agreements) [agreement message]` Sets a terms of service/agreement before the role is given.
The agreement feature of this cog is a bit complicated. You need to give the bot a message that it sends the user.

This message can have a few different things to customize it:

- `{key}`- this is replaced with the key the user must input to recieve their role. This parameter IS NEEDED!</li>
- `{name}`- this is replaced with the username of the user who has joined.</li>
- `{mention}`- this is replaced with a mention for the user who has joined.</li>
- `{guild}`- this is replaced with the name of the server the user has joined.</li>
- `{member}`- this is a slightly different parameter as it is a discord Member object. You likely won't need it unless you're an advanced user.

Here's an example of a message:

`Welcome to {guild}, {name}! Please read the #rules and enter this key: {key} into #accept`.

