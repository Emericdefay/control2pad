import usb


def get_dict_products() -> dict:
    """
    type:
        {
            (dev.idVendor, dev.idProduct): {
                "product": dev.product,
                "manufacturer": dev.manufacturer,
            }
        }
    """
    dict_cp = dict()
    for dev in usb.core.find(find_all=True):
        data = {
            (dev.idVendor, dev.idProduct): {
                "product": dev.product,
                "manufacturer": dev.manufacturer,
            }
        }
        dict_cp.update(data)
    return dict_cp

if __name__ == '__main__':
    print(get_dict_products())
