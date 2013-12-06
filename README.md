This is mostly the code from [Segmentation as Selective Search for Object Recognition](http://koen.me/research/selectivesearch/), downloaded November 2013.
I simply needed a way to call this stuff from Python: `selective_search.py` and `selective_search.m` are the only new files.

    import selective_search_ijcv_with_python as selective_search
    windows = selective_search.get_windows(image_filenames)

To make sure this works, simply `python selective_search.py`.

Sergey Karayev
25 Nov 2013
