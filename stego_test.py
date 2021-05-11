import os, sys
import cv2, moviepy.editor as mpe

BMP_HEADER_SIZE = 54

def encode_image(input_img_name, output_img_name, txt_file, degree):
    """
    This function reads text from the txt_file file and encodes it
    by bits from input_img to output_img.
    Because every byte of image can contain maximum 8 bits of information,
    text size should be less than (image_size * degree / 8 - BMP_HEADER_SIZE)
    :param input_img_name: name of 24-bit BMP original image
    :param output_img_name: name of 24-bit BMP encoded image (will create or overwrite)
    :param txt_file: name of file containing text to be encoded in output_img
    :param degree: number of bits from byte (1/2/4/8) that are taken to encode text data in image.
    :return: True if function succeeds else False
    """

    if degree not in [1, 2, 4, 8]:
        print("Degree value can be only 1/2/4/8")
        return False

    text_len = os.stat(txt_file).st_size
    img_len = os.stat(input_img_name).st_size

    if text_len >= img_len * degree / 8 - BMP_HEADER_SIZE:
        print("Too long text")
        return False

    text = open(txt_file, 'r')
    input_image = open(input_img_name, 'rb')
    output_image = open(output_img_name, 'wb')

    bmp_header = input_image.read(BMP_HEADER_SIZE)
    output_image.write(bmp_header)

    text_mask, img_mask = create_masks(degree)

    while True:
        symbol = text.read(1)
        if not symbol:
            break
        symbol = ord(symbol)

        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_byte |= bits

            output_image.write(img_byte.to_bytes(1, sys.byteorder))
            symbol <<= degree

    output_image.write(input_image.read())

    text.close()
    input_image.close()
    output_image.close()

    return True


def decode_image(encoded_img, output_txt, symbols_to_read, degree):
    """
    This function takes symbols_to_read bytes from encoded image and retrieves hidden
    information from them with a given degree.
    Because every byte of image can contain maximum 8 bits of information,
    text size should be less than (image_size * degree / 8 - BMP_HEADER_SIZE)
    :param encoded_img: name of 24-bit BMP encoded image
    :param output_txt: name of txt file where result should be written
    :param symbols_to_read: amount of encoded symbols in image
    :param degree: number of bits from byte (1/2/4/8) that are taken to encode text data in image
    :return: True if function succeeds else False
    """
    if degree not in [1, 2, 4, 8]:
        print("Degree value can be only 1/2/4/8")
        return False

    img_len = os.stat(encoded_img).st_size

    if symbols_to_read >= img_len * degree / 8 - BMP_HEADER_SIZE:
        print("Too much symbols to read")
        return False

    text = open(output_txt, 'w', encoding='utf-8')
    encoded_bmp = open(encoded_img, 'rb')

    encoded_bmp.seek(BMP_HEADER_SIZE)

    _, img_mask = create_masks(degree)
    img_mask = ~img_mask

    read = 0
    while read < symbols_to_read:
        symbol = 0

        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
            symbol <<= degree
            symbol |= img_byte

        if chr(symbol) == '\n' and len(os.linesep) == 2:
            read += 1

        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()
    return True


def create_masks(degree):
    """
    Create masks for taking bits from text bytes and
    putting them to image bytes.
    :param degree: number of bits from byte that are taken to encode text data in image
    :return: a mask for a text and a mask for an image
    """
    text_mask = 0b11111111
    img_mask = 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


def backup():
    path_in = r'data\vid\clip.mp4'
    path_out = r'data\vid\frames\clipframe'

    capture = cv2.VideoCapture(path_in)
    i = 0
    while (capture.isOpened()):
        ret, frame = capture.read()
        if not ret:
            print(f'Кадры закончились.\nВсего кадров считано: {i}')
            break
        i += 1
        if i % 25 == 0:
            print(f'Записываем {i}-й кадр (кратен 25)')
            cv2.imwrite(f'___clipframe-{i}.bmp', frame)
            frame_orig = frame
            frame_chec = cv2.imread(f'___clipframe-{i}.bmp')
            if frame_orig == frame_chec:
                print('Изображения одинаковы')
            else:
                print('Изоюражения различны')
    capture.release()
    cv2.destroyAllWindows()


def video_gen():
    frame_array = []
    capture = cv2.VideoCapture(r'data\vid\clip.mp4')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = capture.get(cv2.CAP_PROP_FPS)
    i = 0
    while (capture.isOpened()):
        ret, frame = capture.read()
        if not ret:
            break
        i += 1
        if i % 50 == 0:
            print(f'Типо стеганография {i}-го кадра')
            cv2.imwrite(f'tmp.bmp', frame)
            loaded_frame = cv2.imread(f'tmp.bmp')
            height, width, layers = loaded_frame.shape
            print(f'Удаляем временный кадр')
            os.remove('tmp.bmp')
        else:
            print(f'Добавляем в массив {i}-й кадр')
            frame_array.append(frame)
    capture.release()

    print(f'Считываение закончено\nНачинаем запись')
    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    print(f'Создан результирующий контейнер')
    for i in range(len(frame_array)):
        out.write(frame_array[i])
        print(f'Записан {i}-й кадр')

    out.release()
    cv2.destroyAllWindows()


def test():
    capture = cv2.VideoCapture(r'data\vid\clip.mp4')
    fps = capture.get(cv2.CAP_PROP_FPS)
    length = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f'fps: {fps}\tframe count: {length}')


def video_compile():
    frame_array = []
    capture = cv2.VideoCapture(r'data\vid\clip.mp4')
    size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = capture.get(cv2.CAP_PROP_FPS)
    while True:
        ret, frame = capture.read()
        if not ret:  break
        frame_array.append(frame)
    capture.release()

    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):  out.write(frame_array[i])
    out.release()
    cv2.destroyAllWindows()


def audio_compile():
    # clip_init = mpe.VideoFileClip(r'data\vid\clip.mp4')
    # clip_res = mpe.VideoFileClip('out.avi')
    # clip_res = clip_res.set_audio(clip_init.audio)
    # clip_res.write_videofile()
    # clip.audio.write_audiofile('out.mp3')
    # audio = mpe.AudioFileClip('out.mp3')
    # clip_res = mpe.VideoFileClip('out.avi').set_audio(clip_init.audio)
    # clip_res.write_videofile('out.avi')
    clip_1 = mpe.VideoFileClip(r'data\vid\clip.mp4')
    clip_2 = mpe.VideoFileClip('out.avi')
    clip_2.write_videofile('out_2.avi', audio=clip_1.audio)



def config_parse_test():
    import configparser
    config = configparser.RawConfigParser()
    config.read('resources/var/config.ini')
    #print(config.getboolean('SETTINGS', 'inquiry'))
    print('Ну типо +') if config.getboolean('SETTINGS', 'inquiry') else print('Ну типо -')


def take_a_bit_ext(path=r'data\vid\clip.mp4'):
    return path[path.rfind('.'):], path[:path.rfind('.')]


def encode_test(_CE):
    from modules.stego import Steganography as Stego
    s = Stego(degree=4,
              i=1,
              n=50,
              enc_copyright=_CE)
    s.encode_video(path_in=r'data\vid\clip.mp4',
                   path_out=r'data\tmp',
                   fname='clip.mp4')


def logging():
    import logging

    # add filemode="w" to overwrite
    # logging.basicConfig(filename="resources/sample.log", level=logging.INFO)
    # logging.debug("This is a debug message")
    # logging.info("Informational message")
    # logging.error("An error has happened!")

    logger = logging.getLogger("resources/sample.log")
    logger.info('Info')
    logger.error('Error')


if __name__ == '__main__':
    logging()