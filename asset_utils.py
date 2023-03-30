import os

def asset_to_hostname(asset_number):
    check = os.popen("snow find -a " + asset_number + " --field=domain | awk '{print $(NF-1),$NF}' | tr -s ' ' '.'").readlines()
    if check[0] == "":
        return None
    else:
        hostname = check[0].replace("\n", "")
        return hostname
