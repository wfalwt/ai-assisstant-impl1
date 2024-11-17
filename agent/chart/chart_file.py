chart_dir = "workspace/tools/chart_dt/"
chart_url_prefix = "http://localhost:7860/chart/"


def write_js_content(js_file, js_data):
    with open(chart_dir + js_file, mode="w", encoding='utf-8') as chart_file:
        chart_file.write(js_data)
    chart_data_url = chart_url_prefix + js_file
    return chart_data_url
