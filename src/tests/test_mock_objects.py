from ..data_collector import collector
from ..data_analyzer import analyzer

def test_collector_get_top_posts(mocker):
    mocker.patch('src.data_collector.collector.get_top_posts')
    collector.get_top_posts('python')
    collector.get_top_posts.assert_called_once_with('python')

def test_analyzer_generate_visualizations_data(mocker):
    mocker.patch('src.data_analyzer.analyzer.generate_visualizations_data')
    analyzer.generate_visualizations_data('python')
    analyzer.generate_visualizations_data.assert_called_once_with('python')
