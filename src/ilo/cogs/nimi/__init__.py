from .cog import CogNimi


def setup(bot):
    bot.add_cog(CogNimi(bot))
