import populate


def test_populate_convert():
    list_data = [{
        'title': 'my title',
        'page_content': 'mycontent',
        'quote': None,
    }, {
        'title': 'my title',
        'page_content': 'mycontent2',
        'quote': 'some quote',
    }]
    docs = populate.convert_scientsts_to_documents(list_data)
    assert docs[0].page_content == 'mycontent'
