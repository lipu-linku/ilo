from .preview import CogPreview
from .sp import CogSp
from .ss import CogSs


def setup(bot):
    bot.add_cog(CogPreview(bot))
    bot.add_cog(CogSp(bot))
    bot.add_cog(CogSs(bot))

