from .cog import CogPrompt


def setup(bot):
    bot.add_cog(CogPrompt(bot))
