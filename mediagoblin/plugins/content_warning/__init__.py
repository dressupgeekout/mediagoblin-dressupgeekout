# Charlotte's content-warning click-through "NSFW" filter thing
#
# Charlotte Koch <dressupgeekout@gmail.com>
#


import logging

from mediagoblin.tools.pluginapi import get_config


_log = logging.getLogger(__name__)


_setup_plugin_called = 0

def setup_plugin():
    global _setup_plugin_called

    _log.info('Sample plugin set up!')
    config = get_config('mediagoblin.plugins.sampleplugin')
    if config:
        _log.info('%r' % config)
    else:
        _log.info('There is no configuration set.')
    _setup_plugin_called += 1


hooks = {
    'setup': setup_plugin
    }
