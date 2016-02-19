from subprocess import CalledProcessError
from mock import patch, call
from django import VERSION
from django.test import TestCase
from django.test.utils import override_settings


from sourcerevision.loader import get_revision

class BaseCase(TestCase):

    def setUp(self):
        # blow the revision cache
        from sourcerevision import loader
        loader._revision_loaded = False


class TestLoader(BaseCase):

    @patch('sourcerevision.loader.check_output')
    @override_settings(SOURCE_REVISION_COMMANDS=['foo bar baz'])
    def test_command_returns_revision_if_available(self, check_output):
        check_output.return_value = b'quux\r\n'

        revision = get_revision()

        check_output.assert_called_once_with(['foo', 'bar', 'baz'])
        self.assertEqual(revision, 'quux')

    @patch('sourcerevision.loader.check_output')
    @override_settings(SOURCE_REVISION_COMMANDS=['foo bar baz'])
    def test_command_returns_none_if_vcs_not_available(self, check_output):
        check_output.side_effect = CalledProcessError(255, 'foo')
        check_output.return_value = b'bogus'

        revision = get_revision()

        check_output.assert_called_once_with(['foo', 'bar', 'baz'])
        self.assertEqual(revision, None)

    @patch('sourcerevision.loader.check_output')
    @override_settings(SOURCE_REVISION_COMMANDS=['foo bar baz'])
    def test_command_returns_none_if_vcs_not_available2(self, check_output):
        check_output.return_value = b'\n'

        revision = get_revision()

        check_output.assert_called_once_with(['foo', 'bar', 'baz'])
        self.assertEqual(revision, None)

    @patch('sourcerevision.loader.check_output')
    @override_settings(SOURCE_REVISION_COMMANDS=['foo bar baz'])
    def test_revision_is_cached(self, check_output):
        check_output.return_value = b'quux'

        r1 = get_revision()
        r2 = get_revision()

        check_output.assert_called_once_with(['foo', 'bar', 'baz'])
        self.assertEqual(r2, 'quux')

    @patch('sourcerevision.loader.check_output')
    @override_settings(SOURCE_REVISION_COMMANDS=['foo', 'bar', 'baz'])
    def test_all_command_variants_are_checked_in_order(self, check_output):
        check_output.side_effect = OSError()

        revision = get_revision()

        self.assertEqual(check_output.mock_calls,
            [call(['foo']), call(['bar']), call(['baz'])])


class TestMiddleware(BaseCase):

    def setUp(self):
        super(TestMiddleware, self).setUp()
        self.revision = get_revision()

    def test_revision_in_request(self):
        resp = self.client.get('/request')
        self.assertEqual(resp.content, self.revision.encode('ascii'))

    def test_default_revision_response_header_present(self):
        resp = self.client.get('/header')
        self.assertEqual(resp['X-Source-Revision'], self.revision)

    @override_settings(SOURCE_REVISION_HEADER='X-TestHeader')
    def test_custom_revision_response_header(self):
        resp = self.client.get('/header')
        self.assertEqual(resp['X-TestHeader'], self.revision)


class TestMiddlewareNop(BaseCase):

    @override_settings(SOURCE_REVISION_COMMANDS=[])
    def test_no_header_if_revision_not_available(self):
        resp = self.client.get('/header')
        self.assertFalse('X-Source-Revision' in resp)


class TestRequestContext(BaseCase):

    def test_revision_in_context(self):
        self.revision = get_revision()
        resp = self.client.get('/context')
        self.assertEqual(resp.context['SOURCE_REVISION'], self.revision)
        self.assertEqual(resp.content, self.revision.encode('ascii'))


class TestTemplateTag(BaseCase):

    def setUp(self):
        super(TestTemplateTag, self).setUp()
        self.revision = get_revision()

    @override_settings(INSTALLED_APPS=['testapp', 'sourcerevision'])
    def test_static_template_tag_adds_revision_qs(self):
        resp = self.client.get('/staticfiles')
        self.assertEqual(resp.content,
            b'/static/foo?rev=' +self.revision.encode('ascii'))
