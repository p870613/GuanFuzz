import os
path = "/home/lin/libtiff/tools/tiffcrop_test/out/master/crashes"
filelist = []
for dirPath, dirNames, fileNames in os.walk("./"):
    for f in fileNames:
        if(f == "test.py" or f == "tiffcrop" or f == ".test.py.swp" or f == "exe.sh"):
            continue
        filelist.append(f)

for file in filelist:
    print(file)
    cmd = ""
    with open(file, "r") as f:
        cmd = f.read()
    # print(type(cmd))
    a = cmd.replace("/home/lin/libtiff/tools/tiffcrop_test/out/master/.cur_input", path + "/" + file)
    print(a)
    with open("./exe_dir/" + file, "w") as f:
        f.write(a)
