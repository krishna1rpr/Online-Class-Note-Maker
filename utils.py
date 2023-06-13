from pynput import mouse


def get_curr_time():
    import time
    return round(time.time() * 1000)


def get_screen_res():
    from screeninfo import get_monitors
    for m in get_monitors():
        if m.is_primary:
            return (m.width, m.height)


mouse_location = {
    "pressed": [],
    "released": []
}


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        if pressed:
            print('{0} at {1}'.format('Pressed', (x, y)))
            # get pressed location
            mouse_location["pressed"] = [x, y]
        else:
            print('{0} at {1}'.format('Released', (x, y)))
            # get released location
            mouse_location["released"] = [x, y]
            # make sure the pressed location was capture
            if mouse_location["pressed"]:
                x0, y0 = mouse_location["pressed"]
                # stop listener when the captured region is bigger than the 5*5 area
                if abs(x - x0) > 5 and abs(y - y0) > 5:
                    return False


def select_region_by_mouse():
    # collect events until released
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    # get selected region
    x1, y1 = mouse_location["pressed"]
    x2, y2 = mouse_location["released"]
    x0, y0 = (min(x1, x2), min(y1, y2))
    w, h = (max(x1, x2) - x0, max(y1, y2) - y0)
    return (x0, y0, w, h)
