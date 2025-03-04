from .cog import CogUcsur


def setup(bot):
    bot.add_cog(CogUcsur(bot))
