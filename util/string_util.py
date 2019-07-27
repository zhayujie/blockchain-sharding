def is_empty(st):
    return True if (not st) else st.strip() == ''


if __name__ == '__main__':
    r = is_empty('')
    print(r)
