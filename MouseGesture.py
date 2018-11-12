import mouse
import time
import concurrent.futures

CONFIG_TXT = "./config.txt"
SJIS = "sjis"
EMPTY = ""
CONFIG_KEY_INTERVAL_LEFT_CLICK = "INTERVAL_SECONDS_LEFT_CLICK"
CONFIG_KEY_DEFAULT_MOVE_CLICK = "DEFAULT_MOVE_AND_LEFT_CLICK"
CONFIG_DICT = {}


def move_and_click():
    global is_after_pos_update
    if is_after_pos_update:
        is_after_pos_update = False
    else:
        org_pos = mouse.get_position()
        mouse.move(jump_pos[0], jump_pos[1])
        mouse.click('left')
        mouse.move(org_pos[0], org_pos[1])
        print("\r{:40}".format("Move and left click {}".format(jump_pos)))


def update_pos():
    global jump_pos
    global is_after_pos_update
    is_pressed_last_time = False
    last_pressed_time = None
    while True:
        if mouse.is_pressed('right'):
            if is_pressed_last_time:
                if time.time() - last_pressed_time > 1:
                    jump_pos = mouse.get_position()
                    is_pressed_last_time = False
                    is_after_pos_update = True
                    print("\r{:40}".format("Update click position to {}".format(jump_pos)))
            else:
                is_pressed_last_time = True
                last_pressed_time = time.time()
        else:
            is_pressed_last_time = False

        time.sleep(0.1)


def continue_left_click():
    while True:
        if mouse.is_pressed('left'):
            pos = mouse.get_position()
            print("\r{:40}".format("Left click {}".format(pos)))
            mouse.press('left')
            mouse.release('left')
            mouse.press('left')
        time.sleep(float(CONFIG_DICT[CONFIG_KEY_INTERVAL_LEFT_CLICK]))


def load_config():
    for line in open(CONFIG_TXT, "r", encoding=SJIS):
        items = line.replace("\n", "").split("=")

        if len(items) != 2:
            continue

        CONFIG_DICT[items[0]] = items[1]

    check_config_key(CONFIG_KEY_INTERVAL_LEFT_CLICK)
    check_config_key(CONFIG_KEY_DEFAULT_MOVE_CLICK)


def check_config_key(key_name):
    if CONFIG_DICT.get(key_name) is None \
            or CONFIG_DICT[key_name] == EMPTY:
        print("config.txtの{}の値が未設定です。".format(key_name))
        raise KeyError


def print_pos():
    while True:
        print("\r{:40}".format("Mouse position {}".format(mouse.get_position())), end="")
        time.sleep(0.1)


if __name__ == "__main__":
    is_after_pos_update = False
    load_config()
    jump_pos = (
        int(CONFIG_DICT[CONFIG_KEY_DEFAULT_MOVE_CLICK].split(",")[0]),
        int(CONFIG_DICT[CONFIG_KEY_DEFAULT_MOVE_CLICK].split(",")[1]))
    mouse.on_right_click(move_and_click)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    executor.submit(continue_left_click)
    executor.submit(update_pos)
    print("起動完了...")
    executor.submit(print_pos)
    while True:
        time.sleep(10)
