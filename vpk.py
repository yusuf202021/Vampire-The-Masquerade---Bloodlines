import struct
import os, sys
def int32(reader):
    return struct.unpack("<I", reader.read(4))[0]
def export(infile, outfilepath):
    infile = open(infile, 'rb')
    infile.seek(os.stat(infile.name).st_size - 9)
    files = int32(infile)
    datastartoffset = int32(infile)
    infile.seek(datastartoffset)
    filelist = []
    code = """  offset   filesize   filename
--------------------------------------"""
    print(code)
    for i in range(files):
        filenamesize = int32(infile)
        filename = infile.read(filenamesize)
        filelist.append(filename)
        os.makedirs(bytes(outfilepath, "utf8") + b"/" + b"/".join(filename.split(b"/")[:-1]), exist_ok=True)
        newfile = open(bytes(outfilepath, "utf8") + b"/" + filename, 'wb')
        dataoffset = int32(infile)
        size = int32(infile)
        savepos = infile.tell()
        infile.seek(dataoffset)
        data = infile.read(size)
        print(str(dataoffset) + " " + str(size) + "    " + filename.decode("utf8"))
        newfile.write(data)
        infile.seek(savepos)
    fileliste = open("filelist.txt", 'wb')
    for i in filelist:
        fileliste.write(i + b"\n")
def İmport(newfile, files):
    newfile = open(newfile, 'wb')
    filelist = open("filelist.txt", 'r').readlines()
    offset = 0
    offsets = []
    sizes = []
    for i in filelist:
        i = i[:-1]
        i = files + "/" + i
        i = open(i, 'rb').read()
        offsets.append(struct.pack("<I", offset))
        offset += len(i)
        sizes.append(len(i))
        newfile.write(i)
    datastartof = newfile.tell()
    for ran, i in enumerate(filelist):
        i = bytes(i[:-1], "utf8")
        leni = len(i)
        newfile.write(struct.pack("<I", leni))
        newfile.write(i)
        newfile.write(offsets[ran])
        newfile.write(struct.pack("<I", sizes[ran]))
    newfile.write(struct.pack("<I", len(filelist)))
    newfile.write(struct.pack("<I", datastartof))
    newfile.write(b"\x00")


if len(sys.argv) < 2:
    print("Kullanım:\n\t-e\tDosyayı arşivden çıkartır\n\t-i\tDosyayı tekrar arşivler")
else:
    if sys.argv[1] == "-e":
        export(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "-i":
        İmport(sys.argv[2], sys.argv[3])
    else:
        print("Yanlış bir seçenek girdiniz")
        
