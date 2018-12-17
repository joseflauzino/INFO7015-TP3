#!/bin/bash
# setting IP addresses
curl -X POST -d '{"address":"192.168.1.254/24"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"address":"192.168.2.254/24"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"address":"192.168.3.254/24"}' http://localhost:8080/router/0000000000000001
