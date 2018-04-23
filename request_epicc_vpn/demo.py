import datetime
import copy

dic1 = {
    "a":1,
    "b":2
}
dic2 = copy.deepcopy(dic1)

dic1["a"] = 2
print dic2
# print str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))