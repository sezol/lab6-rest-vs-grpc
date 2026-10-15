#!/usr/bin/env python3

import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc

# Vectors are generated once so the timing measures the call,
# not the random number generation.
VEC_A = [random.random() for _ in range(100)]
VEC_B = [random.random() for _ in range(100)]


def doAdd(stub, debug=False):
    reply = stub.Add(lab6_pb2.addMsg(a=5, b=10))
    if debug:
        print(reply)


def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    reply = stub.RawImage(lab6_pb2.rawImageMsg(img=img))
    if debug:
        print(reply)


def doDotProduct(stub, debug=False):
    reply = stub.DotProduct(lab6_pb2.dotProductMsg(a=VEC_A, b=VEC_B))
    if debug:
        print(reply)


def doJsonImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    encoded = base64.b64encode(img).decode('utf-8')
    reply = stub.JsonImage(lab6_pb2.jsonImageMsg(img=encoded))
    if debug:
        print(reply)


parser = argparse.ArgumentParser(description='gRPC client for measuring server operations')
parser.add_argument('host', help='IP address or hostname of the gRPC server')
parser.add_argument('cmd', choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
                    help='Operation to perform')
parser.add_argument('reps', type=int, help='Number of repetitions for measurement')
parser.add_argument('-p', '--port', type=int, default=50051,
                    help='Server port (default: 50051)')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Print the response from the server')
args = parser.parse_args()

addr = f"{args.host}:{args.port}"
print(f"Running {args.reps} reps against {addr}")

# One channel, reused for every call
channel = grpc.insecure_channel(addr)
stub = lab6_pb2_grpc.Lab6Stub(channel)

functions = {
    'add': doAdd,
    'rawImage': doRawImage,
    'dotProduct': doDotProduct,
    'jsonImage': doJsonImage,
}
func = functions[args.cmd]

start = time.perf_counter()
for x in range(args.reps):
    func(stub, debug=args.debug)
delta = ((time.perf_counter() - start) / args.reps) * 1000
print("Took", delta, "ms per operation")
