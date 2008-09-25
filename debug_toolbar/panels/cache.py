from debug_toolbar.panels import DebugPanel
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core.cache import cache

try: from cStringIO import StringIO
except ImportError: import StringIO
import time
import inspect
import os.path

from debug_toolbar.stats import track, STATS

# Track stats on these function calls
cache.set = track(cache.set, 'cache')
cache.get = track(cache.get, 'cache')
cache.delete = track(cache.delete, 'cache')
cache.add = track(cache.add, 'cache')
cache.get_many = track(cache.get_many, 'cache')

class CacheDebugPanel(DebugPanel):
    """
    Panel that displays the cache statistics.
    """
    name = 'Cache'

    def process_ajax(self, request):
        action = request.GET.get('op')
        if action == 'explain':
            return render_to_response('debug_toolbar/panels/cache_explain.html')

    def title(self):
        return 'Cache: %.2fms' % STATS.get_total_time('cache')

    def url(self):
        return ''

    def content(self):
        context = dict(
            cache_calls = STATS.get_total_calls('cache'),
            cache_time = STATS.get_total_time('cache'),
            cache_hits = STATS.get_total_hits('cache'),
            cache_misses = STATS.get_total_misses('cache'),
            cache_gets = STATS.get_total_calls_for_function('cache', cache.get),
            cache_sets = STATS.get_total_calls_for_function('cache', cache.set),
            cache_get_many = STATS.get_total_calls_for_function('cache', cache.get_many),
            cache_delete = STATS.get_total_calls_for_function('cache', cache.delete),
            cache_calls_list = [(c['time'], c['func'].__name__, c['args'], c['kwargs'], c['time'], simplejson.dumps(c['stack'])) for c in STATS.get_calls('cache')],
        )
        return render_to_string('debug_toolbar/panels/cache.html', context)