# -*- coding: utf-8 -*-

import errno
import unittest.mock as mock

from time import time
from tornado.testing import get_unused_port
from unittest import TestCase

from api.start import start_server, start_endpoint


class ServiceTest(TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('tornado.ioloop.IOLoop')
    def test_server_default(self, mock_ioloop, mock_parse_args):
        mock_ioloop.time = mock.Mock(return_value=time())
        mock_ioloop.current.return_value = mock_ioloop

        args = mock.MagicMock()
        args.name = None
        args.port = get_unused_port()
        args.settings = "{}"
        mock_parse_args.return_value = args

        start_server()

    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('tornado.ioloop.IOLoop')
    def test_server_custom(self, mock_ioloop, mock_parse_args):
        mock_ioloop.time = mock.Mock(return_value=time())
        mock_ioloop.current.return_value = mock_ioloop

        args = mock.MagicMock()
        args.name = "test"
        args.port = get_unused_port()
        args.settings = "{}"
        mock_parse_args.return_value = args

        start_server()

    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('tornado.ioloop.IOLoop')
    def test_endpoint_document(self, mock_ioloop, mock_parse_args):
        mock_ioloop.time = mock.Mock(return_value=time())
        mock_ioloop.current.return_value = mock_ioloop

        args = mock.MagicMock()
        args.name = "document"
        args.port = get_unused_port()
        args.settings = "{}"
        mock_parse_args.return_value = args

        start_endpoint()

    @mock.patch('sys.exit')
    @mock.patch('argparse.ArgumentParser.parse_args')
    @mock.patch('tornado.ioloop.IOLoop')
    def test_endpoint_nonregistered(self, mock_ioloop, mock_parse_args,
                                    mock_exit):
        mock_ioloop.time = mock.Mock(return_value=time())
        mock_ioloop.current.return_value = mock_ioloop

        args = mock.MagicMock()
        args.name = "nonregistered"
        args.port = get_unused_port()
        args.settings = "{}"
        mock_parse_args.return_value = args

        def side_effect(value):
            raise Exception(value)
        mock_exit.side_effect = side_effect

        with self.assertRaisesRegexp(Exception, str(errno.EACCES)):
            start_endpoint()
