def helpMessage():
    return "```http\n" \
           "Good luck asking me for help - I don't know what's going on either.\n" \
           "[] denotes required parameter. {} denotes optional parameter.\n" \
           "```" \
           "```css\n" \
           "General commands```" \
           "```" \
           "    username [@mention]                 Returns username of mentioned user.\n" \
           "    avatar  [username]                  Returns avatar of user with specified username.\n" \
           "    image [query]                       Searches query in custom google engine for image. Returns first result.\n" \
           "    rimage [query]                      Searches query in custom google engine for image. Returns random result.\n" \
           "```" \
           "```css\n" \
           "Booru commands```" \
           "```" \
           "    tagsearch [tag query]               Searches query in Danbooru tag database. Accepts * and ? wildcards.\n" \
           "    {nsfw|sfw}danbooru [tag] {tag}      Searches tag(s) in Danbooru. Maximum 2 tags.\n" \
           "    {nsfw|sfw}gelbooru [tag] {tags}     Searches tag(s) in Gelbooru.\n" \
           "```" \
           "```css\n" \
           "Memo commands```" \
           "```" \
           "    memo [username] [message]           Adds memo for user to receive when they return.\n" \
           "```" \
           "```css\n" \
           "Quote commands```" \
           "```" \
           "    quote [username]                    Retrieves a quote attributed to specified user.\n" \
           "    addquote [message ID] {message IDs} Add message(s) with specified ID to quote database. Quotes must all be from same user.\n" \
           "    delquote [quote ID]                 Delete quote with specified ID from database.\n" \
           "    idquote [quote ID]                  Retrieves quote with specified ID from database.\n" \
           "```" \
           "```css\n" \
           "Bot commands```" \
           "```" \
           "    refresh                             Refreshes bot username and avatar.\n" \
           "    nickname                            Adds or changes nickname for Bot.\n" \
           "    mute [@mention]                     Mutes mentioned user indefinitely.\n" \
           "    unmute [@mention]                   Unmutes mentioned user.\n" \
           "    timeout [@mention] [seconds]        Mutes mentioned user for specified number of seconds.\n" \
           "    ban [@mention]                      Bans a user.\n" \
           "```"
