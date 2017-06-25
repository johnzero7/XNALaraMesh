# -*- coding: utf-8 -*-
# <pep8 compliant>

import struct

from XNALaraMesh import xps_const


# Format
class TypeFormat:
    SByte = '<b'
    Byte = '<B'
    Int16 = '<h'
    UInt16 = '<H'
    Int32 = '<i'
    UInt32 = '<I'
    Int64 = '<l'
    UInt64 = '<L'
    Single = '<f'
    Double = '<d'


def roundToMultiple(numToRound, multiple):
    remainder = numToRound % multiple
    if (remainder == 0):
        return numToRound
    return numToRound + multiple - remainder


def readByte(file):
    numberBin = file.read(1)
    number = struct.unpack(TypeFormat.Byte, numberBin)[0]
    return number


def writeByte(number):
    bytesBin = struct.pack(TypeFormat.Byte, number)
    return bytesBin


def readUInt16(file):
    numberBin = file.read(2)
    number = struct.unpack(TypeFormat.UInt16, numberBin)[0]
    return number


def writeUInt16(number):
    uInt16 = struct.pack(TypeFormat.UInt16, number)
    return uInt16


def readInt16(file):
    numberBin = file.read(2)
    number = struct.unpack(TypeFormat.Int16, numberBin)[0]
    return number


def writeInt16(number):
    int16 = struct.pack(TypeFormat.Int16, number)
    return int16


def readUInt32(file):
    numberBin = file.read(4)
    number = struct.unpack(TypeFormat.UInt32, numberBin)[0]
    return number


def writeUInt32(number):
    uInt32 = struct.pack(TypeFormat.UInt32, number)
    return uInt32


def readSingle(file):
    numberBin = file.read(4)
    single = struct.unpack(TypeFormat.Single, numberBin)[0]
    return single


def writeSingle(number):
    single = struct.pack(TypeFormat.Single, number)
    return single


def readString(file, length):
    try:
        pos1 = file.tell()
        byteString = file.read(length)
        pos2 = file.tell()
        string = ''
        string = decodeBytes(byteString)
    except Exception:
        print('*' * 40)
        print('pos len', pos1)
        print('pos str', pos2)
        print('pos', file.tell())
        print('len', length)
        print('str', byteString)
        string = decodeBytes(byteString)
    return string


def writeString(string):
    # String Lenght
    byteString = encodeString(string)
    return byteString


def decodeBytes(bytes):
    # print(bytes)
    return bytes.decode(xps_const.ENCODING_READ)


def encodeString(string):
    # print(string)
    return string.encode(xps_const.ENCODING_WRITE)
