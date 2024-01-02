import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
import app.data_management.database as database

# Configure a mock for the engine and session
mock_engine = MagicMock()
mock_session = MagicMock()


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Patch 'create_engine' and 'sessionmakeer' to return the mock engine and session
        self.engine_patch = patch('database.create_engine', return_value=mock_engine)
        self.session_patch = patch('database.sessionmaker', return_value=mock_session)
        
        self.engine_patch.start()
        self.session_patch.start()
    
    def tearDown(self):
        self.engine_patch.stop()
        self.session_patch.stop()
        mock_session.reset_mock()

    @patch('database.SessionRequests')
    def test_add_request(self, mock_session_class):
        mock_session = mock_session_class.return_value
        
        database.add_request('test_user', 'test@example.com', '2020-01-01 10:00:00', 'classification')
        # Assert the session's add and commit methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @patch('database.SessionRequests')
    def test_update_request_status(self, mock_session_class):
        mock_session = mock_session_class.return_value
        
        mock_request = mock.MagicMock(spec=database.Request)
        mock_session.query.return_value.get.return_value = mock_request
        
        database.update_request_status('test_user', 'COMPLETED')
        
        # Assert the request's status was updated
        self.assertEqual(mock_request.status, 'COMPLETED')
        mock_session.commit.assert_called_once()
    
    @patch('database.SessionRequests')
    def test_get_pending_requests(self, mock_session_class):
        # Create a mock session instance
        mock_session = mock_session_class.return_value

        # Configure the mock session's query to return a list of requests
        mock_request = mock.MagicMock(spec=database.Request)
        mock_session.query.return_value.filter.return_value.all.return_value = [mock_request]

        pending_requests = database.get_pending_requests()

        # Check that the session's query.filter method was called correctly
        filter_call_args = mock_session.query.return_value.filter.call_args
        self.assertIsNotNone(filter_call_args)

        # Extract the first argument passed to filter (which should be the expression)
        filter_expression = filter_call_args[0][0]
        self.assertEqual(str(filter_expression.left), 'requests.status')
        self.assertEqual(str(filter_expression.right.value), 'PENDING')

        self.assertIn(mock_request, pending_requests)
    
    @patch('database.SessionResults')
    def test_add_result(self, mock_session_class):
        mock_session = mock_session_class.return_value
        
        database.add_result('test_user', 'test_summary', 'classification', 'test_metrics')
        # Assert the session's add and commit methods were called
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @patch('database.SessionResults')
    def test_get_result_by_id(self, mock_session_class):
        mock_session = mock_session_class.return_value
        
        mock_result = mock.MagicMock(spec=database.Result)
        mock_session.query.return_value.get.return_value = mock_result
        
        # Configure the mock result's get method to return a mock result
        result = database.get_result_by_id('test_user')
        self.assertEqual(result, mock_result)


if __name__ == '__main__':
    unittest.main()