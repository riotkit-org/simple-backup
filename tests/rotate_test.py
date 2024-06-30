from rbackup.rotate.app import App
from rbackup.filesystem import Dummy


def test_rotate():
    fs = Dummy()
    fs.upload("yeah", "yeah-1")
    fs.upload("yeah", "yeah-2")
    fs.upload("yeah", "yeah-3")

    app = App(fs)
    app.rotate(2, "")

    as_text = list(map(lambda x: x.name, fs.local_list))
    assert as_text == ['yeah-2', 'yeah-3']
