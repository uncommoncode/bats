import IPython.display


def _html_table(name, column_names, rows):
    html = ''
    html += f'<h4>{name}</h1>'
    html += '<table>'
    html += '<tr>'
    for name in column_names:
        html += f'<th>{name}</td>'
    html += '</tr>'
    for row in rows:
        html += '<tr>'
        for name in column_names:
            value = ''
            if name in row:
                value = row[name]
            html += f'<td>{value}</td>'
        html += '</tr>'
    html += '</table>'
    return html


def display_table(name, column_names, rows):
    html = IPython.display.HTML(_html_table(name, column_names, rows))
    return IPython.display.display(html)


def display_audio(data, sample_rate, normalize):
    audio = IPython.display.Audio(data.T, rate=sample_rate, normalize=normalize)
    return IPython.display.display(audio)
