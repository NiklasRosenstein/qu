# Copyright (c) 2016  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pickle
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import (Boolean, SmallInteger, Integer, BigInteger,
  Enum, Text, String, Unicode, Time, DateTime, Date, Float, Numeric, LargeBinary)


def bool(create_constraint=True, name=None, **kwargs):
  return Column(Boolean(create_constraint, name), **kwargs)


def smallint(**kwargs):
  return Column(SmallInt, **kwargs)


def int(**kwargs):
  return Column(Integer, **kwargs)


def bigint(**kwargs):
  return Column(BigInteger, **kwargs)


def enum(*enums, **kwargs):
  return Column(Enum(*enums), **kwargs)


def text(length=None, collation=None, convert_unicode=None,
    unicode_error=None, unicode=False, _warn_on_bytestring=True, **kwargs):
  if convert_unicode is None:
    convert_unicode = bool(unicode)
  class_ = UnicodeText if unicode else Text
  dtype = class_(length, collation, convert_unicode,
    unicode_error, _warn_on_bytestring)
  return Column(dtype, **kwargs)


def string(length=None, collation=None, convert_unicode=False,
    unicode_error=None, unicode=False, _warn_on_bytestring=True, **kwargs):
  if convert_unicode is None:
    convert_unicode = bool(unicode)
  class_ = Unicode if unicode else String
  dtype = class_(length, collation=collation, convert_unicode=convert_unicode,
    unicode_error=unicode_error, _warn_on_bytestring=_warn_on_bytestring)
  return Column(dtype, **kwargs)


def unicode(length=None, collation=None, convert_unicode=False,
    unicode_error=None, unicode=True, _warn_on_bytestring=True, **kwargs):
  return string(length, collation, convert_unicode, unicode_error,
    unicode, _warn_on_bytestring, **kwargs)


def time(timezone=False, **kwargs):
  return Column(Time(timezone), **kwargs)


def datetime(timezone=False, **kwargs):
  return Column(DateTime(timezone), **kwargs)


def date(**kwargs):
  return Column(Date, **kwargs)


def float(precision=None, asdecimal=False, decimal_return_scale=None, **kwargs):
  return Column(Float(precision, asdecimal, decimal_return_scale), **kwargs)


def decimal(precision=None, scale=None,
    decimal_return_scale=None, asdecimal=True, **kwargs):
  return Column(Numeric(precision, scale, decimal_return_scale, asdecimal), **kwargs)


def blob(length=None, **kwargs):
  return Column(LargeBinary(length), **kwargs)


def python(protocol=pickle.HIGHEST_PROTOCOL, pickler=None, comparator=None, **kwargs):
  return Column(PickleType(protocol, pickler, comparator), **kwargs)


def foreign_key(*args, **kwargs):
  return ForeignKey(*args, **kwargs)
