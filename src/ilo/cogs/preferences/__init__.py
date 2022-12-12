from .cog import CogPreferences

def setup(bot):
    bot.add_cog(CogPreferences(bot))
