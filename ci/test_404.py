import csv

def test_404():
    assert sum([1 for line in open('result.csv')]) == 1, '404 response in HTML - see scraper logs'
