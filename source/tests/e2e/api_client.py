import requests
from Domain import config


def post_to_add_bookmark(title, url, notes):
    url = config.get_api_url()
    r = requests.post(
        f"{url}/add_bookmark", json={"title": title, "url": url, "notes": notes}
    )
    assert r.status_code == 201


def get_bookmark(id):
    url = config.get_api_url()
    return requests.get(f"{url}/bookmarks/{id}")


def list_bookmarks(sort=None, order=None):
    url = config.get_api_url()
    params = {}
    if sort:
        params['sort'] = sort
    if order:
        params['order'] = order
    return requests.get(f"{url}/bookmarks", params=params)


def delete_bookmark(id):
    url = config.get_api_url()
    r = requests.delete(f"{url}/bookmarks/{id}")
    assert r.status_code == 202


def edit_bookmark(id, title=None, url=None, notes=None):
    url = config.get_api_url()
    data = {}
    if title:
        data['title'] = title
    if url:
        data['url'] = url
    if notes:
        data['notes'] = notes
    r = requests.patch(f"{url}/bookmarks/{id}", json=data)
    assert r.status_code == 202
