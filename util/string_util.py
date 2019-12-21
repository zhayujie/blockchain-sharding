import base64


def is_empty(s):
    return True if (not s) else st.strip() == ''


def base64ToHex(base64_str):
    # base64转base16，先用base64解码, 再用base16编码, 最后解码为string返回
    base16_byte = base64.b16encode(base64.b64decode(base64_str))
    return base16_byte.decode('utf-8')


if __name__ == '__main__':
    st = 'm0JbkN4kcQfXDxozonatLb7UDi6c5ngBrPK6rpuVWGVzBMtOmzx10iJ9SqBfrnlXCZY2IPsc1LfwunvgyzceQA=='
    print(base64ToHex(st))
