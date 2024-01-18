from mkdocs.config import config_options as ConfigOptions
from mkdocs.config.base import Config


class McDicBlogPluginPostViewsConfig(Config):
    """
    Subconfig class for McDic's Blog plugin on post views.
    Note that `forced_update` is changed to `True` on `gh-deploy`.
    """

    local_path = ConfigOptions.Optional(ConfigOptions.File(exists=True))
    forced_update = ConfigOptions.Type(bool, default=False)


class McDicBlogPluginConfig(Config):
    """
    Config class for McDic's Blog plugin.
    """

    enabled = ConfigOptions.Type(bool, default=True)
    post_views = ConfigOptions.SubConfig(McDicBlogPluginPostViewsConfig)
