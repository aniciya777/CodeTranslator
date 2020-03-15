def python_parser(text):
    arr = []
    is_multi_comment = False
    for row, s in enumerate(text.split('\n')):
        if is_multi_comment:
            pass
        else:
            index = s.find('#') + 1
            if index > 0:
                arr.append({
                    'comment': s[index:],
                    'from': (row, index),
                    'to': (row, len(s))
                })
    return arr
