#run this to make shit not explode:
#py -m pip install -r requirements.txt
import fedex_tracking_number
fedex_tracking_number.set(474349291333)
print(fedex_tracking_number.get_list_of_keys(fedex_tracking_number.get_json_file()))
print(f'package details go bang: {fedex_tracking_number.get_key_value("scanEvents")}')
