from mkdocs.config import config_options as ConfigOptions
from mkdocs.config.base import Config


class McDicBlogPluginPostViewsConfig(Config):
    """
    Subconfig class for McDic's Blog plugin on post views.
    Note that `forced_update` is changed to `True` on `gh-deploy`.
    """

    local_path = ConfigOptions.Optional(ConfigOptions.File(exists=True))
    forced_update = ConfigOptions.Type(bool, default=False)


class McDicBlogPluginGitDateConfig(Config):
    """
    Subconfig class for McDic's Blog plugin on git date metadata.
    """

    format = ConfigOptions.Type(str, default="%Y/%b/%d %H:%M:%S %Z")


class McDicBlogPluginSortedConfig(Config):
    """
    Subconfig class for McDic's Blog plugin on sorted posts.
    """

    recent = ConfigOptions.Type(int)
    most_viewed = ConfigOptions.Type(int)


class McDicBlogPluginConfig(Config):
    """
    Config class for McDic's Blog plugin.
    """

    enabled = ConfigOptions.Type(bool, default=True)
    post_views = ConfigOptions.SubConfig(McDicBlogPluginPostViewsConfig)
    git_dates = ConfigOptions.SubConfig(McDicBlogPluginGitDateConfig)
    historical_batch = ConfigOptions.Type(int, default=10)
    sorted = ConfigOptions.SubConfig(McDicBlogPluginSortedConfig)
