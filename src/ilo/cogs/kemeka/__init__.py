from .cog import CogKemeka


def setup(bot):
    bot.add_cog(CogKemeka(bot))
