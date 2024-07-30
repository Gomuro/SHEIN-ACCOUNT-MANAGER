class TwitterBotDriverError(Exception):
    pass


class TwitterBotDriverWarning(Exception):
    pass


class TryAgainPageError(TwitterBotDriverError):
    pass


class TwitterDriverChatParsingError(TwitterBotDriverError):
    pass

