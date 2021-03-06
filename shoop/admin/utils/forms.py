# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS

from django.forms import HiddenInput, Widget, ModelChoiceField
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import escape
from filer.models import File


class MediaChoiceWidget(Widget):
    BROWSE_MARKUP = "<button class='media-browse btn btn-sm' type='button'><i class='fa fa-folder'></i> Browse</button>"

    def render_text(self, obj):
        if obj:
            text = force_text(obj)
            url = obj.url
        else:
            text = u"\u2014"
            url = "about:blank"

        return mark_safe("<a class=\"media-text\" href=\"%(url)s\" target=\"_blank\">%(text)s</a>&nbsp;" % {
            "text": escape(text),
            "url": escape(url),
        })

    def render(self, name, value, attrs=None):
        if value:
            obj = File.objects.get(pk=value)
        else:
            obj = None
        pk_input = HiddenInput().render(name, value, attrs)
        media_text = self.render_text(obj)
        bits = "".join([pk_input, media_text, self.BROWSE_MARKUP])
        return mark_safe("<div class='media-widget'>%s</div>" % bits)


class MediaChoiceField(ModelChoiceField):
    widget = MediaChoiceWidget


def filter_form_field_choices(field, predicate, invert=False):
    """
    Filter the `choices` of a given form field (and its widget)
    by the given predicate.

    The predicate may be a callable of the signature `(pair) -> bool`
    or an iterable of allowable `value`s.

    :param field: Form field.
    :type field: django.forms.Field
    :param predicate: Predicate
    :type predicate: function|Iterable
    :param invert: Invert the semantics of the predicate, i.e. items matching it will be rejected.
    :type invert: bool
    :return: Nothing. The field is modified in-place.
    """

    if not callable(predicate):
        allowed_values = set(predicate)

        def predicate(pair):
            return (pair[0] in allowed_values)

    if invert:
        choices = [pair for pair in field.choices if not predicate(pair)]
    else:
        choices = [pair for pair in field.choices if predicate(pair)]

    field.choices = field.widget.choices = choices


def add_form_errors_as_messages(request, form):
    """
    Add the form's errors, if any, into the request as messages.

    :param request: Request to messagify
    :type request: django.http.HttpRequest
    :param form: The errorful form.
    :type form: django.forms.Form
    :return: Number of messages added. May be thousands, for a very unlucky form.
    :rtype: int
    """
    n_messages = 0
    for field_name, errors in form.errors.items():
        if field_name != NON_FIELD_ERRORS:
            field_label = form[field_name].label
        else:
            field_label = ""
        for error in errors:
            messages.error(request, "%s %s" % (field_label, error))
            n_messages += 1
    return n_messages
