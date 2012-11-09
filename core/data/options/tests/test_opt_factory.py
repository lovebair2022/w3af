'''
test_opt_factory.py

Copyright 2011 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import os
import unittest

from core.controllers.exceptions import w3afException
from core.data.parsers.url import URL as URL_KLASS
from core.data.options.opt_factory import opt_factory
from core.data.options.option_types import (BOOL,INT,FLOAT,STRING,URL,IPPORT,LIST,
                                            REGEX,COMBO,INPUT_FILE,OUTPUT_FILE,
                                            PORT)

class TestOptionFactory(unittest.TestCase):
    
    def test_factory_ok(self):
        input_file = os.path.join('core', 'data', 'options', 'tests', 'test.txt') 
        output_file = input_file
        
        data = { BOOL: ('true', True),
                 INT: ('1', 1),
                 FLOAT: ('1.0', 1.0),
                 STRING: ('hello world', 'hello world'),
                 URL: ('http://moth/', URL_KLASS('http://moth/')),
                 IPPORT: ('127.0.0.1:8080', '127.0.0.1:8080'),
                 LIST: ('a,b,c', ['a','b','c']),
                 REGEX: ('.*', '.*'),
                 COMBO: (['a', 'b', 'c'], 'a'),
                 INPUT_FILE: (input_file, input_file),
                 OUTPUT_FILE: (output_file, output_file),
                 PORT: ('12345', 12345)
                 }

        for _type, (user_value, parsed_value) in data.iteritems():
            opt = opt_factory('name', user_value, 'desc', _type)
            
            self.assertEqual(opt.get_name(), 'name')
            self.assertEqual(opt.get_desc(), 'desc')
            self.assertEqual(opt.get_type(), _type)
            self.assertEqual(opt.get_default_value(), parsed_value)
            self.assertEqual(opt.get_value(), parsed_value)

    def test_factory_unknown_type(self):
        self.assertRaises(KeyError, opt_factory, 'name', 'value', 'desc',
                          'unknown_type')
    
    def test_invalid_data(self):
        input_file = os.path.join('core', 'data', 'foobar', 'does-not-exist.txt') 
        output_file = input_file
        
        data = { BOOL: 'rucula',
                 INT: '0x32',
                 FLOAT: '1x2',
                 URL: 'http://',
                 IPPORT: '127.0.0.1',
                 REGEX: '.*(',
                 INPUT_FILE: input_file,
                 OUTPUT_FILE: output_file,
                 PORT: '65536'
                 }

        for _type, fake_value in data.iteritems():
            self.assertRaises(w3afException, opt_factory, 'name', fake_value,
                              'desc', _type)
            
    