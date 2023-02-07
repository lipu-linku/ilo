from .cog import CogRelex


def setup(bot):
    bot.add_cog(CogRelex(bot))
