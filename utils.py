def creat_http_response(status, response_body):
    # 9，拼接响应的报文
    # 响应行
    response_line = "HTTP/1.1 %s\r\n" % status
    # 响应头
    response_header = "server:pythonwb/3.4\r\n"
    # response_header += "Content-Type: text/html\r\n"
    # 响应空行
    response_blank = "\r\n"
    # 拼接响应报文
    response_data = (response_line + response_header + response_blank).encode() + response_body

    return response_data
