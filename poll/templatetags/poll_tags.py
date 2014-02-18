# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from poll.models import *
from poll import views
register = template.Library()

@register.simple_tag(takes_context=True)
def poll(context, poll_id):
    request = context['request']

    if not poll_id:
        try:
            poll = Poll.published.latest("date")
            poll_id = poll.pk
        except:
            return ''

    else:
        poll_id = int(poll_id)

    cookie_key = 'poll_%s' % poll_id

    if cookie_key not in request.COOKIES:
        return views.poll(context['request'], poll_id).content
    else:
        return views.result(context['request'], poll_id).content
    
@register.simple_tag                                                                                                                         
def percentage(vote_count, item_vote_count):
    vote_count = int(vote_count)
    if vote_count > 0:
        return float(item_vote_count) / float(vote_count) * 100
