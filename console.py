import cv2, os, sys

_COPYRIGHT = 'Copyright by okeyw.\nAll Rights Reserved.'.encode()
_N = 10; _I = 2; _D = 4

def recode():
    _frame_array = []
    capture = cv2.VideoCapture('C:/Users/okeyw/PycharmProjects/PymediaStego/data/vid/good_job.divx.avi')
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        _frame_array.append(frame)
    out = cv2.VideoWriter('C:/Users/okeyw/PycharmProjects/PymediaStego/data/tmp/recoded.avi',
                          cv2.VideoWriter_fourcc(*"DIVX"),
                          capture.get(cv2.CAP_PROP_FPS),
                          (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                           int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    print(f'Length of original file: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}\tWritable length: {len(_frame_array)}')
    capture.release()
    for i in range(len(_frame_array)):
        out.write(_frame_array[i])
    out.release()
    cv2.destroyAllWindows()


def encode_video():
    def stego():
        output_image = open('tmp_2.bmp', 'wb')
        input_image = open('tmp_1.bmp', 'rb')
        output_image.write(input_image.read(54))
        text_mask, img_mask = get_masks(_D)
        for symbol in _COPYRIGHT:
            for byte_amount in range(0, 8, _D):
                img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
                bits = symbol & text_mask
                bits >>= (8 - _D)
                img_byte |= bits
                output_image.write(img_byte.to_bytes(1, sys.byteorder))
                symbol <<= _D
        output_image.write(input_image.read())
        input_image.close()
        output_image.close()

    _frame_array = []
    capture = cv2.VideoCapture('C:/Users/okeyw/PycharmProjects/PymediaStego/data/tmp/recoded.avi')
    _i = 0
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        _i += 1
        if _i % _N == 0:
            cv2.imwrite('tmp_1.bmp', frame)
            stego()
            _frame_array.append(cv2.imread('tmp_2.bmp'))
            os.remove('tmp_1.bmp')
            os.remove('tmp_2.bmp')
            for _j in range(_I - 1):
                ret, frame = capture.read()
                if not ret:
                    break
                cv2.imwrite('tmp_1.bmp', frame)
                stego()
                _frame_array.append(cv2.imread('tmp_2.bmp'))
                os.remove('tmp_1.bmp')
                os.remove('tmp_2.bmp')
        else:
            _frame_array.append(frame)
    out = cv2.VideoWriter('C:/Users/okeyw/PycharmProjects/PymediaStego/data/stego.avi',
                          cv2.VideoWriter_fourcc(*"DIVX"),
                          capture.get(cv2.CAP_PROP_FPS),
                          (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                           int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    print(f'Length of recoded file: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}\tWritable length: {len(_frame_array)}\tWritable i: {_i}')
    capture.release()
    for i in range(len(_frame_array)):
        out.write(_frame_array[i])
    out.release()
    cv2.destroyAllWindows()


def decode_video():
    def stego():
        text = b''
        encoded_bmp = open('tmp_1.bmp', 'rb')
        encoded_bmp.seek(54)
        _, img_mask = get_masks(_D)
        img_mask = ~img_mask
        read = 0
        while read < len(_COPYRIGHT):
            symbol = 0
            for bits_read in range(0, 8, _D):
                img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
                symbol <<= _D
                symbol |= img_byte
            if chr(symbol) == '\n' and len(os.linesep) == 2:
                read += 1
            read += 1
            text += symbol.to_bytes(1, sys.byteorder)
        encoded_bmp.close()
        os.remove('tmp_1.bmp')
        print(f'\n{text}\n{_COPYRIGHT}')
        return True if text == _COPYRIGHT else False

    _frame_array = []
    capture = cv2.VideoCapture(r'C:\Users\okeyw\PycharmProjects\PymediaStego\data\stego.avi')
    _i = 0
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        _i += 1
        if _i % _N == 0:
            cv2.imwrite('tmp_1.bmp', frame)
            stego()
            _frame_array.append(frame)
            for _j in range(_I - 1):
                ret, frame = capture.read()
                if not ret:
                    break
                cv2.imwrite('tmp_1.bmp', frame)
                stego()
                _frame_array.append(frame)
        else:
            _frame_array.append(frame)
    print(f'Length of stego file: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}\t\tWritable length: {len(_frame_array)}\tWritable i: {_i}')
    capture.release()
    return True


def encode_image():
    output_image = open('data/tmp/frame_stego.bmp', 'wb')
    input_image = open('data/tmp/frame_10.bmp', 'rb')
    output_image.write(input_image.read(54))
    text_mask, img_mask = get_masks(_D)
    for symbol in _COPYRIGHT:
        for byte_amount in range(0, 8, _D):
            img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - _D)
            img_byte |= bits
            output_image.write(img_byte.to_bytes(1, sys.byteorder))
            symbol <<= _D
    output_image.write(input_image.read())
    input_image.close()
    output_image.close()


def decode_image():
    text = b''
    encoded_bmp = open('data/tmp/frame_stego.bmp', 'rb')
    encoded_bmp.seek(54)
    _, img_mask = get_masks(_D)
    img_mask = ~img_mask
    read = 0
    while read <= len(_COPYRIGHT):
        symbol = 0
        for bits_read in range(0, 8, _D):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
            symbol <<= _D
            symbol |= img_byte
        if chr(symbol) == '\n' and len(os.linesep) == 2:
            read += 1
        read += 1
        text += symbol.to_bytes(1, sys.byteorder)
    encoded_bmp.close()
    print(f'\n{text}\n{_COPYRIGHT}')
    return True if text == _COPYRIGHT else False


def get_masks(degree=8):
    text_mask = 0b11111111
    img_mask = 0b11111111
    text_mask <<= (8 - degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree
    return text_mask, img_mask


# def dec_stego(copyright_encrypted, path):
#     s = Stego(degree=4, i=2, n=10, enc_copyright=copyright_encrypted)
#     return f'Копирайт {"" if s.decode_video(path_in=path) else "не "}аутентичен. Целостность видеофайла не пострадала.'


if __name__ == "__main__":
    encode_image()
    status = decode_image()
    print(status)

    #file_name = os.path.basename(r'data\vid\good_job.divx.avi')
    # recode()
    # encode()
    # state = decode()
    # print(state)

    # props = f'4;2;10'.encode()
    # props = props.decode().split(';')
    # print(type(props[0]))

    # capture = cv2.VideoCapture(r'data\vid\good_job.divx.avi')
    # length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # fourcc = int(capture.get(cv2.CAP_PROP_FOURCC))
    # print(f'{fourcc}\n{cv2.VideoWriter_fourcc(*"H264")}\n{cv2.VideoWriter_fourcc(*"AVC1")}\n{cv2.VideoWriter_fourcc(*"DIVX")}')
    # ret, frame = capture.read()
    # open('tmp_1', 'wb').write(frame)
    # cv2.imwrite('tmp_2.bmp', frame)
    # new_frame = cv2.imread('tmp_2.bmp')
    # open('tmp_2', 'wb').write(new_frame)

    # _s = 'D=4;I=1;N=5;L=8;'.encode()
    # _s += (b'\0' * (271 - len(_s)))
    # print(_s)
    # for s in _s:
    #     print(s.to_bytes(1, sys.byteorder))

    # array = b''
    # for symbol in _COPYRIGHT.encode():
    #     array += symbol.to_bytes(1, sys.byteorder)
    # print(array == _COPYRIGHT.encode())

    # certificate = read_license()
    # report = dec_stego(certificate.get('AdditionalInfo').get('Copyright'),
    #                    r'data\tmp\good_job.divx.avi')
    # print(f'Заключение глубокой проверки:\n{report}')
