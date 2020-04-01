def text_parser(text):
    arr = []
    for row, s in enumerate(text.splitlines()):
        arr.append({
            'comment': s[:],
            'from': (row, 0),
            'to': (row, len(s))
        })
    return arr
