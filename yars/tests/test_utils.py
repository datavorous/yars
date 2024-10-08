import os
import json
import unittest
import requests
from unittest.mock import patch, MagicMock

from yars.utils import display_results, download_image, export_to_json, export_to_csv

class TestYARSFunctions(unittest.TestCase):

    @patch('builtins.print')
    @patch('json.dumps')
    @patch('pygments.highlight')
    def test_display_results_list_of_dicts(self, mock_highlight, mock_dumps, mock_print):
        mock_dumps.return_value = '{"key": "value"}'
        mock_highlight.return_value = 'highlighted_output'

        results = [{'key': 'value'}]
        title = "Test Results"
        display_results(results, title)

        mock_print.assert_called_with("\n-------------------- Test Results --------------------")
        mock_print.assert_any_call('highlighted_output')
    
    @patch('builtins.print')
    @patch('json.dumps')
    @patch('pygments.highlight')
    def test_display_results_dict(self, mock_highlight, mock_dumps, mock_print):
        mock_dumps.return_value = '{"key": "value"}'
        mock_highlight.return_value = 'highlighted_output'

        results = {'key': 'value'}
        title = "Test Results"
        display_results(results, title)

        mock_print.assert_called_with("\n-------------------- Test Results --------------------")
        mock_print.assert_called_with('highlighted_output')
    
    @patch('builtins.print')
    @patch('logging.warning')
    def test_display_results_empty(self, mock_warning, mock_print):
        results = None
        title = "Test Results"
        display_results(results, title)

        mock_print.assert_called_once_with("No results to display.")
        mock_warning.assert_called_once()

    @patch('requests.Session.get')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_download_image_success(self, mock_open, mock_makedirs, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'data']
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = download_image('http://example.com/image.jpg')

        mock_makedirs.assert_called_once_with('images', exist_ok=True)
        mock_get.assert_called_once_with('http://example.com/image.jpg', stream=True)
        mock_open.assert_called_once_with('images/image.jpg', 'wb')
        mock_open().write.assert_called_once_with(b'data')
        self.assertEqual(result, 'images/image.jpg')

    @patch('requests.Session.get')
    @patch('logging.error')
    def test_download_image_failure(self, mock_logging_error, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        result = download_image('http://example.com/image.jpg')

        self.assertIsNone(result)
        mock_logging_error.assert_called_once_with('Failed to download %s: %s', 'http://example.com/image.jpg', 'Request failed')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_export_to_json_success(self, mock_dump, mock_open):
        data = {'key': 'value'}
        export_to_json(data, 'test_output.json')

        mock_open.assert_called_once_with('test_output.json', 'w', encoding='utf-8')
        mock_dump.assert_called_once_with(data, mock_open(), indent=4)

    @patch('builtins.print')
    @patch('builtins.open', side_effect=Exception("File error"))
    def test_export_to_json_failure(self, mock_open, mock_print):
        data = {'key': 'value'}
        export_to_json(data, 'test_output.json')

        mock_print.assert_called_once_with('Error exporting to JSON: File error')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('csv.DictWriter')
    def test_export_to_csv_success(self, mock_dict_writer, mock_open):
        data = [{'key': 'value'}, {'key': 'value2'}]
        export_to_csv(data, 'test_output.csv')

        mock_open.assert_called_once_with('test_output.csv', 'w', newline='', encoding='utf-8')
        mock_dict_writer.assert_called_once_with(mock_open(), fieldnames=['key'])
        mock_dict_writer().writeheader.assert_called_once()
        mock_dict_writer().writerows.assert_called_once_with(data)

    @patch('builtins.print')
    @patch('builtins.open', side_effect=Exception("File error"))
    def test_export_to_csv_failure(self, mock_open, mock_print):
        data = [{'key': 'value'}]
        export_to_csv(data, 'test_output.csv')

        mock_print.assert_called_once_with('Error exporting to CSV: File error')


if __name__ == '__main__':
    unittest.main()
